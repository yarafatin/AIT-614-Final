### AIT 614 - Big Data Essentials 
#### DL2 Team 3 Final Project
#### Detecting Abrasive online user content
#### 
#### Team 3
#### Yasser Parambathkandy
#### Indranil Pal
#### Deepak Rajan
#### 
#### University
#### George Mason University

---
### Introduction
This project aims to detect abrasive online content using word and sentence embeddings. The project can be set up in a local machine or in a cloud environment, end-to-end.
The Readme file has been split into local setup and cloud setup.
---

### Local Machine Setup
#### Hardware Requirements  
Hardware: 8 CPUs and 16GB RAM  
OS: WSL2 with Ubuntu 20.04 LTS

#### Installation
Open WSL2 ubuntu window and run below command   
sudo apt update  
- Install anaconda-   
wget https://repo.anaconda.com/archive/Anaconda3-2023.03-1-Linux-x86_64.sh  
chmod 755 Anaconda3-2023.03-1-Linux-x86_64.sh  
./Anaconda3-2023.03-1-Linux-x86_64.sh  
You can accept all defaults
- Install Java  
sudo apt-get install openjdk-11-jdk-headless  
- Install mongodb-  
wget -qO - https://www.mongodb.org/static/pgp/server-5.0.asc | sudo apt-key add -  
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/5.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-5.0.list  
sudo apt-get update  
sudo apt-get install -y mongodb-org  
mkdir -p ~/data/db  
sudo service mongodb start  
verify installation - ps -ef | grep mongo

#### Setup environment
Close and open WSL2 window and run below   
conda create -n ait614 python=3.10  
conda activate ait614  
conda install pip -y  
conda install pyspark=3.2.1 -y  
conda install jupyterlab -y  
conda install matplotlib -y  
conda install scikit-learn -y  
conda install pymongo=3.12.0 -y  
conda install flask -y  
pip install spark-nlp==4.4.0  

#### Start ML training
Run below commands  
sudo mkdir /opt/ait614  
sudo chmod -R 777 ait614  
Copy and extract the submitted project zip AIT614-DL2_Team3_system.zip to /opt/ait614    
The project directory should be like - /opt/ait614/AIT-614-Final    
cd /opt/ait614/AIT-614-Final  
jupyter lab  
This should open jupyter lab in browser, if not copy the url from the startup log and open in browser    
Under src folder open - sentence_embedding_train.ipynb  
This will take a long time to run, approximately 2-4 hours   
If you just want to run for a smaller set, add a line df = df.limit(10000) in the third code cell  
After sentence embedding based model training is complete, repeat the same for word_embedding_train.ipynb      

#### Start Real-time prediction services
- Upload all 1.3 million questions to mongodb by executing below line  
- cd /opt/ait614/AIT-614-Final/src  
- python3 db_client.py  
- The code does the one-time load only if the collection is empty
- Start the flask app
- python3 app.py
- NOTE: Do not run the prediction service while training is running.
- Open browser and navigate to http://localhost:5000/web/user.html
- Enter a question and submit
- On successful submission, you will see the message "Your question has been submitted. A moderator will review it before publishing."
- Open another browser tab and navigate to http://localhost:5000/web/moderator.html
- The most recent questions are displayed here for moderators to review.
- All new questions are saved to mongodb.  
- The "Sincerity prediction" column shows the prediction by the sentence embedding model  

### Troubleshooting
- If you see the error - "Answer from Java side is empty", it means there is not enough resource to run this in the local machine
You can try to reduce the number of records being processed by changing the third code cell in the notebook to limit(10000) records
- If you see Ignore error - Nullpointer, you have missed some key installation steps. Redo the installation

### Cloud Environment Setup
#### Requirements  

Create accounts in the following cloud providers 
- https://aws.amazon.com/
- https://community.cloud.databricks.com/login.html
- https://account.mongodb.com/

#### Training in Databricks
- After training in databricks, model can be saved to AWS S3. AWS access and secret keys are needed. If saving to AWS S3 is not needed, this can be skipped.       
- Login to AWS console first, search for IAM, and create new user. Select "Attach policies directly", and search and set "AmazonS3FullAccess"    
- Upload train.csv from the AIT-614-Final/data directory to databricks    
- This get uploaded to dbfs:/FileStore/tables/train.csv  
- Upload sentence_embedding_train.ipynb and word_embedding_train.ipynb files to workspace
- Create a new databricks Spark cluster - 12.2 LTS (Scala 2.12, Spark 3.3.2), and add the following in the Spark config section  
    ` spark.serializer org.apache.spark.serializer.KryoSerializer  
      spark.kryoserializer.buffer.max 2000M  
      spark.databricks.rocksDB.fileManager.useCommitService false  
      spark.databricks.delta.preview.enabled true `
- Under spark libraries section, install New -> PyPI -> spark-nlp==4.4.0 -> Install
Install New -> Maven -> Coordinates -> com.johnsnowlabs.nlp:spark-nlp_2.12:4.4.0 -> Install


