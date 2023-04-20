"""
AIT 614 - Big Data Essentials
DL2 Team 3 Final Project
Detecting Abrasive online user content

Team 3
Yasser Parambathkandy
Indranil Pal
Deepak Rajan

University
George Mason University
"""

from pyspark.ml.classification import LogisticRegressionModel
from pyspark.sql.functions import col, explode
from sparknlp.annotator import *
from sparknlp.base import *

from project_properties import MODEL_PATH

"""
The prediction services takes a question and predicts whether it is abrasive or not.
"""


class Predictor:

    def __init__(self, spark_obj):
        self.spark = spark_obj
        self.lmodel = LogisticRegressionModel.load(MODEL_PATH)

        # Pipeline for NLP, same as the one used in the training
        document_assembler = DocumentAssembler() \
            .setInputCol("question_text") \
            .setOutputCol("document")
        embeddings_finisher = EmbeddingsFinisher() \
            .setInputCols(["use_embeddings"]) \
            .setOutputCols(["finished_use_embeddings"]) \
            .setOutputAsVector(True).setCleanAnnotations(False)

        useEmbeddings = UniversalSentenceEncoder.pretrained() \
            .setInputCols("document").setOutputCol("use_embeddings")

        self.nlpPipeline = Pipeline(stages=[
            document_assembler,
            useEmbeddings,
            embeddings_finisher])

    def predict(self, input_data):
        """
        Predict whether the input question is abrasive or not.
        :param input_data: The question to be predicted.
        :return: The prediction.
        """

        print('started')

        data = [(input_data,)]
        df = self.spark.createDataFrame(data, ["question_text"])

        question_df = self.nlpPipeline.fit(df).transform(df)
        question_df = question_df.withColumn("features", explode(question_df.finished_use_embeddings))

        prediction = self.lmodel.transform(question_df)
        return prediction.select(col("prediction").cast("int")).first()[0]
