In this workshop, we will create a search engine for BBC articles using pyspark and the Spark ML library. 

* [pyspark documentation](){: target="_blank"}
* [ML guide](https://spark.apache.org/docs/2.1.0/ml-guide.html){: target="_blank"}

## Introduction 

### What we will do

To create the search engine, we will do the following steps:

![steps](resources/spark-lda-steps.png)

### What we will use

LSA, _latent semantic anlysis_ is

> _a technique in natural language processing, in particular distributional semantics, of analyzing relationships between a set of documents and the terms they contain by producing a set of concepts related to the documents and terms_ (source: wikipedia)

In summary, we want to establish underlying relationships between documents in a collection by linking documents and terms through _concepts_. Those concepts are deduced or constructed through a statistical or mathematical algorithm that forms a _model_. Once we have the model, we can begin using it for search queries.

#### Available algorithms 

There are two well-known methods for discovering underlying topics:

1. __SVD__, _Singular Value Decomposition_: is a mathematical method for decomposing a matrix into a product of smaller matrices. It has the advantage of being _mathematically correct_: computing the model, hence  the decomposed matrices, takes only one pass and is deterministic: the same data will always give the same result (as long as the same parameters are used).

2. __LDA__, _Latent Dirichlet Allocation_, is a generative probabilistic model. Based on statistics, many iterations are necessary to get a good-enough model and every run could give a different result. The result is also highly dependant on the parameters we use for the training. 

In this workshop, we will use the LDA technique.

#### LDA Basics

LDA is like a clustering algorithm where :

* the _cluster centers_ are the topics;
* the _training examples_ are documents;
* the _features_ are the word frequencies;
* the distance is ~~euclidean~~ based on a statistical model (Bayesian inference rules / Dirichlet distribution)

As in clustering, we need to give some informations (_parameters_) to the model. The most important one is __the number of topics (k)__ we think there is (exactly as we need to specify the number of clusters to find).

During training, the model will first assign each document to a random topic. Then, on each iteration, it computes how well the actual topic distribution describes/predicts each document, makes adjustments and try again. Most of the time, the programmer will set in advance the __maximum number of iterations__ to do.

In the end, the model outputs a topic distribution over document (how much a document is important to a given topic) and over terms (how much the term describes the topic). Documents with similar topic distributions are likely to be similar, even if they don't use the same words.

## LDA with pyspark

### Getting the dataset

coming soon :wink:


