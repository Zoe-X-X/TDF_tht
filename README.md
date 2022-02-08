# Weather data hourly ingestion from API

## Description
This project built an one hour scheduling lambada for ingesting data from https://openweathermap.org to AWS S3.

### Solution 1 (CloudFormaion)
* `iac.json` is used for creating stack in AWS CloudFormation.
*  **Boto3** in Python is used for Lambda core function development.

### Solution 2 (Python Boto3)
**Boto3** is used for both launching all infrastructures and Lambda function development.

The `.py` script files in `iaC` can automatically instantiate infrastructure shown in the following diagram, aiming to increase the speed and agility of infrastructure deployments.  


### Lambda Function
* `tdfThtDeploymentPackage.zip` contains the `request` package to interact with the API and the core function runs by **AWS Lambda**, which implements obtaining the weather data from the API and then updating the data file stored in **AWS S3**.
* `Pandas_layer.zip` is used to install `Pandas`packages to enable **AWS Lambda** to run python script files.

The data file can be check through the public **AWS S3 Bucket**  at https://s3.console.aws.amazon.com/s3/buckets/tdf-tht?region=ap-southeast-2&tab=objects (public access avaiable)
### Infrastructure Diagram
<img src="https://github.com/Zoe-X-X/TDF_tht/blob/main/Infrastructure.png" width="400" >

## Prerequisites
To run .py files locally or rebuild all infrastructure by another AWS account, you should have the following:
 
1. Get a free [API Key](https://openweathermap.org/current) for https://openweathermap.org.
2. AWS CLI installed and configured on the terminal.

## How it work
1. Download `iaC.json`or`iaC`, `tdfThtDeploymentPackage.zip`, `Pandas_layer.zip`folder.
2. Upload `tdfThtDeploymentPackage.zip`and `Pandas_layer.zip` to a S3 bucket.
3. For CloudFormation solution ONLY: In CloudFormation Console, use `iaC.json` as the template to create a stack. The resources crested include:
   - An **IAM Role** with AWS manageed policies for Lambda
   - A **Lambda Function**
   - A Layer for Lambda to use **Panda lib** in Python
   - A scheduled event rule in **EventBridge**
   - A Lambda Permission to allow **EventBridge** executing **Lambda Function**
4. For Boto3 solution ONLY: Run .py files under `iaC` in the following order
   - `s3CreateBucket.py`: Create new public Bucket and upload `tdfThtDeploymentPackage.zip` and `Pandas_layer.zip` automatically. Include verification to ensure that there are no buckets with the same name and duplicate content.
   - `roleCreate.py`: Create IAM role for Lambda and attach required policy.
   - `lambdaCreate.py`: Create layer with `Pandas_layer.zip`, create lambda with `tdfThtDeploymentPackage.zip`.
   - `eventCreate.py`: Create scheduled rule in EventBridge for triggering Lambda hourly.
