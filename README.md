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

### Start ML training
Run below commands  
sudo mkdir /opt/ait614  
sudo chmod -R 777 ait614  
Copy the submitted project zip AIT614-DL2_Team3_system.zip to /opt/ait614  
