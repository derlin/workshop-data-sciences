from pyspark.sql import SparkSession
import random

# create context. In Spark 2, a spark session is
# a spark SqlContext. 
spark = SparkSession\
   .builder\
   .appName("Pi estimation")\
   .getOrCreate()

# number of darts thrown
NUM_DARTS = 1000000

# throw a random dart and check if it lands inside the circle
def dart_inside(p):
    x, y = random.random(), random.random()
    return x*x + y*y < 1

# create a list of NUM_DARTS length
darts = xrange(0, NUM_DARTS)

# throw the darts in parallel 
count = spark.sparkContext.parallelize(darts) \
             .filter(dart_inside)\
             .count()

# print the result
print("Pi is roughly %f" % (4.0 * count / NUM_DARTS))

# stop the spark session
spark.stop()

