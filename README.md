# Weather data hourly ingestion from API

## Description
This project built an one hour scheduling lambada for ingesting data from https://openweathermap.org to AWS S3.

**Boto3** in Python is not only used as the developing tool for core code of Lambda Function, also as **iaC** for building all infrastructures of this project.
There are two mian part:
* The script files in `iaC` can automatically instantiate infrastructure shown in the following diagram, aiming to increase the speed and agility of infrastructure deployments.  
* `tdfThtDeploymentPackage` contains the `request` package to interact with the API and the core function runs by **AWS Lambda**, which implements obtaining the weather data from the API and then update the data file stored in **AWS S3**.

The data file can be check through the public **AWS S3 Bucket**
### Infrastructure Diagram
<img src="https://github.com/Zoe-X-X/TDF_tht/blob/main/Infrastructure.png" width="400" >

## Prerequisties
To run .py files locally or rebuild all infrastructure by other AWS acount, you should have the following:
 
1. Get a free [API Key](https://openweathermap.org/current) for https://openweathermap.org.
2. AWS CLI installed and configures on the the termianl.

## Usage
1. Download all file under `iaC` and folder
2. Run .py files in the following order：
   - `s3CreateBucket.py`
   - `role.py`
   - `lambdaCreate.py`
   - `evenyCreate.py`
