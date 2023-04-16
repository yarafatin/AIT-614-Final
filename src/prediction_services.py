from pyspark.ml.classification import LogisticRegressionModel
from sparknlp.annotator import *
from sparknlp.base import *
from pyspark.sql.functions import col, udf
from pyspark.ml.linalg import VectorUDT
from pyspark.sql.types import ArrayType, DoubleType
from pyspark.ml.linalg import Vectors

from project_properties import WORD_EMBEDDING_MODEL_SAVE_PATH


class Predictor:

    def __init__(self, spark_obj):
        self.spark = spark_obj
        self.lmodel = LogisticRegressionModel.load(WORD_EMBEDDING_MODEL_SAVE_PATH)
        document_assembler = DocumentAssembler().setInputCol("question_text").setOutputCol("document")
        tokenizer = Tokenizer().setInputCols(["document"]).setOutputCol("token")
        embeddings = WordEmbeddingsModel.pretrained("glove_840B_300", "xx") \
            .setInputCols("document", "token") \
            .setOutputCol("embeddings")

        self.nlpPipeline = Pipeline(stages=[document_assembler,
                                            tokenizer,
                                            embeddings])

    def predict(self, input_data):
        print('started')

        data = [(input_data,)]
        df = self.spark.createDataFrame(data, ["question_text"])
        # df = spark.read.format('csv').option('header', True).load(TRAIN_FILE_PATH).limit(1)

        question_df = self.nlpPipeline.fit(df).transform(df)

        avg_vectors_udf = udf(avg_vectors, ArrayType(DoubleType()))
        df_doc_vec = question_df.withColumn("doc_vector", avg_vectors_udf(col("embeddings")))

        dense_vector_udf = udf(dense_vector, VectorUDT())
        test_df = df_doc_vec.withColumn("features", dense_vector_udf(col("doc_vector")))

        prediction = self.lmodel.transform(test_df)
        return prediction.select(col("prediction").cast("int")).first()[0]


def avg_vectors(word_vectors):
    length = len(word_vectors[0]["embeddings"])
    avg_vec = [0] * length
    for vec in word_vectors:
        for i, x in enumerate(vec["embeddings"]):
            avg_vec[i] += x
        avg_vec[i] = avg_vec[i] / length
    return avg_vec


def dense_vector(vec):
    return Vectors.dense(vec)
