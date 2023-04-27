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
    `conda create -n ait614 python=3.10`        
    `conda activate ait614`    
    `conda install pip -y`  
    `conda install pyspark=3.2.1 -y`  
    `conda install jupyterlab -y`  
    `conda install matplotlib -y`  
    `conda install scikit-learn -y`  
    `conda install pymongo=3.12.0 -y`  
    `conda install flask -y`  
    `pip install spark-nlp==4.4.0` 

#### Start ML training
Run below commands  
`sudo mkdir /opt/ait614`  
`sudo chmod -R 777 ait614`  
Copy and extract the submitted project zip AIT614-DL2_Team3_sys.zip to /opt/ait614    
The project directory should be like - /opt/ait614/AIT614-DL2_Team3_sys    
`cd /opt/ait614/AIT614-DL2_Team3_sys`  
`jupyter lab`  
This should open jupyter lab in browser, if not copy the url from the startup log and open in browser    
Under src folder open - sentence_embedding_train.ipynb  
This will take a long time to run, approximately 2-4 hours   
If you just want to run for a smaller set, add a line df = df.limit(10000) in the third code cell  
After sentence embedding based model training is complete, repeat the same for word_embedding_train.ipynb      

#### Start Real-time prediction services
- Upload all 1.3 million questions to mongodb by executing below line  
- `cd /opt/ait614/AIT614-DL2_Team3_sys/src`  
- `python3 db_client.py`  
- The code does the one-time load only if the collection is empty
- Start the flask app
- `python3 app.py`
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
- If you see Nullpointer and the program continues to run fine, then ignore and proceed further

### Cloud Environment Setup
#### Requirements  

Create accounts in the following cloud providers 
- https://aws.amazon.com/
- https://community.cloud.databricks.com/login.html
- https://account.mongodb.com/

#### AWS S3 bucket storage
Save trained models in S3 from databricks and use it from AWS EC2 instance for prediction
- Login to AWS console, look for S3, click Create Bucket
- Name the bucket ait614-models with default configuration
- Unzip the project zip in local machine
- In the S3 bucket, click add Folder and select the project folder "AIT614-DL2_Team3_sys", and upload

#### Training in Databricks Community Cluster
- After training in databricks, model can be saved to AWS S3. AWS access and secret keys are needed. If saving to AWS S3 is not needed, this can be skipped.       
    - Login to AWS console first, search for IAM, and create new user. Select "Attach policies directly", and search and set "AmazonS3FullAccess"
    - Under "Security credentials" tab, click "Create Access Key", select "Application running outside AWS", and generate.  
    - Download the csv file with credentials, rename the file as ait614_databricks_accessKeys.csv, and upload to databricks
    - It should get saved to dbfs:/FileStore/tables/ait614_databricks_accessKeys.csv
    - If access keys are not provided, the program still runs and save model to local file system instead
- Upload train.csv from the AIT614-DL2_Team3_sys/data directory to databricks    
    - This get uploaded to dbfs:/FileStore/tables/train.csv  
- Ensure the file path of the above two files are as give above. If it different update the notebook with new path in code cell #2 
- Upload sentence_embedding_train.ipynb and word_embedding_train.ipynb files to workspace
- Create a new databricks Spark cluster - 12.2 LTS (Scala 2.12, Spark 3.3.2), and add the following in the Spark config section  
    ` spark.serializer org.apache.spark.serializer.KryoSerializer  
      spark.kryoserializer.buffer.max 2000M  
      spark.databricks.rocksDB.fileManager.useCommitService false  
      spark.databricks.delta.preview.enabled true `
- Under spark libraries section, 
    - Install New -> PyPI -> spark-nlp==4.4.0 -> Install
    - Install New -> Maven -> Coordinates -> com.johnsnowlabs.nlp:spark-nlp_2.12:4.4.0 -> Install
- Attach the sentence_embedding_train.ipynb notebook to this new cluster and run
    - Due to memory and time restrictions in databricks, the data size has been limited to 100000 in the code. This can be changed in third code cell
- Run all cells and repeat the same for word_embedding_train.ipynb

#### Setting up MongoDB cloud
- Create a new shared tier cluster called ait614
- Under "Security"/ "Network Access" / "IP Access List", add the address 0.0.0.0/0 to allow AWS EC2 to access MongoDB
- Create a Database user ait614user with password
- Get the cluster connection information from "Cmd Line Tools". It should be something like ait614.adkj20o.mongodb.net.  

#### Run Prediction Services in AWS 
The generated model in S3 will be used to provide real-time prediction
- Create a new EC2 instance
    - Select Ubuntu 22.04 LTS
    - Instance Type - t2.large (2vCPU, 8GB). Smaller instances will not work
        - **This is not a free instance, and you will incur costs** 
    - Configure Storage - 30GB
    - Default the remaining
- Once instance is created, open and navigate to security tab
    - In "Inbound rules", click the link under "Security groups"
    - Click "Inbound rules" in the bottom section, and click "Edit inbound rules"
    - Add new rule with Type - "Custom TCP" and "Port Range" 5000. The IP should be 0.0.0.0/0
    - This will allow us to access the service via internet
- Install software 
    - `sudo apt install python3-pip`
    - `pip install flask`
    - `pip install pymongo`
    - `pip install spark-nlp==4.4.0 pyspark==3.3.1`
    - `pip install numpy`
    - `sudo apt-get update`
    - `sudo apt-get install openjdk-11-jdk-headless`
    - `sudo apt install awscli`
    - `wget https://dlcdn.apache.org/spark/spark-3.3.2/spark-3.3.2-bin-hadoop3.tgz`
    - `tar -xvzf spark-3.3.2-bin-hadoop3.tgz`
    - `export SPARK_HOME=/home/ubuntu/spark-3.3.2-bin-hadoop3`
    - `export PATH=$PATH:$SPARK_HOME/bin`
    - `export FLASK_ENV=cloud`
- Setup S3 access
    - In IAM create new role, Select EC2 and use case, select policy "AmazonS3FullAccess", and submit
    - Open EC2 instance, Choose Actions tab, under security, select "Modify IAM Role", and select the new role created
    - Test the setup by executing this command aws s3 ls s3://ait614-models. This should show the project folder uploader earlier 
- Setup Project and run
    - Download project from s3 -  aws s3 sync s3://ait614-models .
    - `cd AIT614-DL2_Team3_sys/src`
    - edit the project.properties and update values for MONGO_DB_HOST and MONGO_DB_PASSWORD
    - By default, it uses existing models. To use newer models, update MODEL_PATH property and also get that model from S3. 
        - To get new models from S3, create new folder in AIT614-DL2_Team3_sys/src
        - cd to the new folder and to run sync command aws s3 sync s3://ait614-models/<new model folder name>
        - update project properties file with new model path
    - Run below  
      `export FLASK_ENV=cloud`    
      `python3 app.py`
    - This should start the flask app
- Access the application from browser
   - In the EC2 instance dashboard, get the host name under - "Public IPv4 DNS". It will be something like ec2-3-85-234-78.compute-1.amazonaws.com
   - Open browser and call http://<hostname>:5000/web/user.html
   - Enter a valid question (sincere or insincere) and post. You should get a success message
   - Open another tab and invoke http://<hostname>:5000/web/moderator.html. This is the moderator HTML
   - You will see the recently submitted question, predicted using the trained model, fetched from MongoDB

