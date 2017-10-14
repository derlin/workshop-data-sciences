from pyspark.sql import SparkSession
import sys 

# create context. In Spark 2, a spark session is
# a spark SqlContext. 
spark = SparkSession\
   .builder\
   .appName("PythonWordCount")\
   .getOrCreate()

# read a text file into an RDD of lines
# using the SqlContext instead, we would do:
#    spark.read.text(sys.argv[1]).rdd.map(lambda r: r[0])
lines = spark.sparkContext.textFile(sys.argv[1]) 

# transformations: 
#  - flatMap: RDD of lines -> RDD of words
#  - map: RDD of words -> RDD of (words, frequency)
#  - reduceByKey: gather frequencies
counts = lines.flatMap(lambda x: x.split(' ')) \ 
             .map(lambda x: (x, 1)) \
             .reduceByKey(lambda a, b: a + b)

# actions: get the result into a list of tuple (word, freq)
output = counts.collect()

# print the result
for (word, count) in output: print("%s: %i" % (word, count))

# stop the spark session
spark.stop()

