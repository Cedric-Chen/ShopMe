from pyspark.sql import SparkSession, Row
from pyspark.ml.fpm import FPGrowth
import sys

filepath = sys.argv[1]
minsup = int(sys.argv[2])

spark = SparkSession \
    .builder \
    .appName("mine frequent pattern") \
    .getOrCreate()

sc = spark.sparkContext
lines = sc.textFile(filepath)\
        .map(lambda x: Row(items = x.split('\t')))
lines.persist()
N = lines.count()
print('number of lines: ', N)
#print('data')
#for x in lines.collect():
#    print(x)

df = spark.createDataFrame(lines, ['items'])
#df.show()

fpGrowth = FPGrowth(itemsCol="items", minSupport=minsup*1.0/N, minConfidence=0.6)
model = fpGrowth.fit(df)

# Display frequent itemsets.
#model.freqItemsets.show()
out = open('res_spark.txt','w')
for x in model.freqItemsets.rdd.map(lambda i: i.items).collect():
    out.write(str(x)+'\n')

spark.stop()
