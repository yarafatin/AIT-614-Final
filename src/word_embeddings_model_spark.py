import sparknlp
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.linalg import VectorUDT
from pyspark.ml.linalg import Vectors
from pyspark.sql.functions import col, udf
from pyspark.sql.types import ArrayType, DoubleType, IntegerType
from sparknlp.annotator import *
from sparknlp.base import *

from project_properties import WORD_EMBEDDING_MODEL_SAVE_PATH

spark = sparknlp.start()
data = spark.read.format('csv').option('header', True).load('../data/train.csv').limit(100)
data = data.withColumn("target", data["target"].cast(IntegerType()))
data.printSchema()

document_assembler = DocumentAssembler().setInputCol("question_text") \
    .setOutputCol("document")

tokenizer = Tokenizer().setInputCols(["document"]) \
    .setOutputCol("token")

embeddings = WordEmbeddingsModel.pretrained("glove_840B_300", "xx") \
    .setInputCols("document", "token") \
    .setOutputCol("embeddings")

nlpPipeline = Pipeline(stages=[document_assembler,
                               tokenizer,
                               embeddings])

df = nlpPipeline.fit(data).transform(data)


def avg_vectors(word_vectors):
    length = len(word_vectors[0]["embeddings"])
    avg_vec = [0] * length
    for vec in word_vectors:
        for i, x in enumerate(vec["embeddings"]):
            avg_vec[i] += x
        avg_vec[i] = avg_vec[i] / length
    return avg_vec


# create a udf
avg_vectors_udf = udf(avg_vectors, ArrayType(DoubleType()))
df_doc_vec = df.withColumn("doc_vector", avg_vectors_udf(col("embeddings")))


def dense_vector(vec):
    return Vectors.dense(vec)


dense_vector_udf = udf(dense_vector, VectorUDT())
training = df_doc_vec.withColumn("features", dense_vector_udf(col("doc_vector")))

lr = LogisticRegression(labelCol="target", featuresCol="features", maxIter=10, regParam=0.3, elasticNetParam=0.8)
lrParisModel = lr.fit(training)
lrParisModel.save(WORD_EMBEDDING_MODEL_SAVE_PATH)
