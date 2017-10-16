import numpy as np
from math import sqrt


# normalize a list of doubles
def _normalizeVec(vec):
    """
    Normalize a vector.
    :param vec: a list-like (list, spark vector, numpy array...) of doubles
    :return: the normalized vector as a numpy array
    """
    norm = sqrt(sum([x * x for x in vec]))
    normalizedVec = [x / norm for x in vec]
    return np.array(normalizedVec)


def _normalizeMatrix(M):
    """
    Normalize each row of a matrix.
    :param M: the matrix
    :return: the matrix with each row normalized.
    """
    RowNorm = np.linalg.norm(M, axis=1)  # one norm for each row in M
    return M / RowNorm[:, np.newaxis]  # divide cell by the norm of its row


# print the results as a zeppelin table
def results2table(res):
    """
    Print the result of a query as a Zeppelin table
    :param res: a result, i.e. a list of tuples of the form [(id, title|term, score)]
    """
    print("%table\nid\tdescription\tscore")
    for tup in res:
        print("%d\t%s\t%f" % tup)


# import operator
# class Result(tuple):
#     def __new__(self, id, descr, score):
#         return tuple.__new__(Result, (id, descr, score))

class Result(list):
    """
    Wraps a list of tuples of the form [(id, title|term, score)], so that we can directly print the results
    as a Zeppelin table using the `.toTable` method.

    """

    def __init__(self, *args):
        list.__init__(self, *args)

    def toTable(self):
        """
        Calls `results2table` on this results.
        """
        results2table(self)


class QueryEngine:
    """
    A query engine for an LDA model.
    """

    def __init__(self, model, df, vocabulary, idf_model):
        """
        Create a query engine.
        :param model: the pyspark.ml.clustering.LDAModel model
        :param df: a DataFrame with columns id, title, content, features and topicDistribution
        :param vocabulary: the vocabulary list created with the pyspark.ml.feature.CountVectorizer
        :param idf_model: the model created with the pyspark.ml.feature.IDF
        """
        self.model = model
        self.df = df
        self.vocabulary = vocabulary
        self.idf_model = idf_model

        # create dictionary lookups between documents id and titles
        self.docIds = dict([(r[1], r[0]) for r in df.select("id", "title").collect()])
        self.docTitles = dict([(r[0], r[1]) for r in df.select("id", "title").collect()])

        # create a keypair RDD[(Long, Vector)] with id and normalized topic distribution
        self.topicDist_rdd = df.select("id", "topicDistribution").rdd.map(lambda r: (r[0], _normalizeVec(r[1]))).cache()

        # V is a matrix N x k, with N = num terms and k = num topics
        # So the cell (k2, n1) tells the relative importance of term n1 for topic k2
        topicsMatrix = model.topicsMatrix()  # DenseMatrix
        self.V = np.array(topicsMatrix.toArray()).reshape((topicsMatrix.numRows, topicsMatrix.numCols))

        # U is a matrix M x k, with M = num docs and k = num topics
        # So the cell (m1, k2) tells the relative importance of document m1 for topic k2
        docsMatrix = [r[0].toArray() for r in df.select("topicDistribution").rdd.collect()]
        self.U = np.matrix(docsMatrix)

        # Normalize each row of matrices VS and US to be able to compute the cosine similarity
        # with a simple multiplication
        self.VS = _normalizeMatrix(self.V)
        self.US = _normalizeMatrix(self.U)

    def topDocsForDoc(self, docId, top=10):
        """
        Get the most relevant documents for a given document.
        :param docId: the document
        :param top: the maximum number of results to return
        :return: Result, a list [(id, title, score)] sorted by decreasing relevance
        """
        docRow = np.array(self.topicDist_rdd.lookup(docId))
        top_similarities = self.topicDist_rdd \
            .map(lambda r: ((np.matrix(r[1]) * docRow.T)[0, 0], r[0])) \
            .sortByKey(ascending=False) \
            .take(top)

        return Result([(r[1], self.docTitles[r[1]], r[0]) for r in top_similarities])

    def topDocsForTerm(self, termId, top=10):
        """
        Get the most relevant documents for a given term.
        :param termId: the index of the term in the vocabulary
        :param top: the maximum number of results to return
        :return: Result, a list [(id, title, score)] sorted by decreasing relevance
        """
        termRow = np.asmatrix(self.V[termId, :]).T
        top_similarities = self.topicDist_rdd \
            .map(lambda r: ((np.matrix(r[1]) * termRow)[0, 0], r[0])) \
            .sortByKey(ascending=False) \
            .take(top)

        return Result([(r[1], self.docTitles[r[1]], r[0]) for r in top_similarities])

    # get the more relevant terms for a given term.
    # return: a list of tuple3  [ (termId, term, score) ]
    def topTermsForTerm(self, termId, top=10):
        """
        Get the most relevant terms for a given term.
        :param termId: the index of the term in the vocabulary
        :param top: the maximum number of results to return
        :return: Result, a list [(id, term, score)] sorted by decreasing relevance
        """
        termRow = self.VS[termId, :]
        similarities = (self.VS * np.asmatrix(termRow).T).A1
        sortedIndexes = np.argsort(-similarities)  # use - to sort descending
        return Result([(i, self.vocabulary[i], similarities[i]) for i in sortedIndexes[:top]])

    def topDocsForTermQuery(self, termIds, top=10):
        """
        Get the most relevant document for a given list of terms.
        :param termIds: the indexes of the terms in the vocabulary, as a list
        :param top: the maximum number of results to return
        :return: Result, a list [(id, title, score)] sorted by decreasing relevance
        """

        # create a  query vector using idf:
        # this way, we kaintain the weighting scheme used for the original 
        # term-document matrix
        idfs = [self.idf_model.idf[tid] for tid in termIds]
        query_vector = np.zeros(len(self.vocabulary))
        query_vector[termIds] = idfs

        termRow = self.VS.T * np.asmatrix(query_vector).T  # termRow is of size (10,1)

        top_similarities = self.topicDist_rdd \
            .map(lambda r: ((np.matrix(r[1]) * termRow)[0, 0], r[0])) \
            .sortByKey(ascending=False) \
            .take(top)
        return Result([(r[1], self.docTitles[r[1]], r[0]) for r in top_similarities])

    def showDoc(self, docId):
        """
        Return the title and content of a document as a string.
        :param docId: the document id
        :return: the title and content of the document as a string
        """
        r = self.df.select("title", "content").where(self.df.id == docId).first()
        if r is not None:
            title = "(%d) %s" % (docId, r[0])
            return "%s\n%s\n%s" % (title, '-' * len(title), r[1])
        else:
            return "No document with id %d" % docId