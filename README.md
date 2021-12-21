# Weather data hourly ingestion from API

## Description
This project built an one hour scheduling lambada for ingesting data from https://openweathermap.org to AWS S3.

**Boto3** in Python is not only used as the developing tool for core code of Lambda Function, also as **iaC** for building all infrastructures of this project.
There are 3 main parts:
* The script files in `iaC` can automatically instantiate infrastructure shown in the following diagram, aiming to increase the speed and agility of infrastructure deployments.  
* `tdfThtDeploymentPackage.zip` contains the `request` package to interact with the API and the core function runs by **AWS Lambda**, which implements obtaining the weather data from the API and then updating the data file stored in **AWS S3**.
* `Pandas_layer.zip` is used to install `Pandas`packages to enable **AWS Lambda** to run python script files.

The data file can be check through the public **AWS S3 Bucket**  at https://s3.console.aws.amazon.com/s3/buckets/tdf-tht?region=ap-southeast-2&tab=objects
### Infrastructure Diagram
<img src="https://github.com/Zoe-X-X/TDF_tht/blob/main/Infrastructure.png" width="400" >

## Prerequisites
To run .py files locally or rebuild all infrastructure by another AWS account, you should have the following:
 
1. Get a free [API Key](https://openweathermap.org/current) for https://openweathermap.org.
2. AWS CLI installed and configured on the terminal.

## How it work
1. Download  `iaC`  `tdfThtDeploymentPackage.zip` and `Pandas_layer.zip`folder
2. Run .py files under `iaC` in the following order
   - `s3CreateBucket.py`: Create new public Bucket and upload `tdfThtDeploymentPackage.zip` and `Pandas_layer.zip` to S3. Include verification to ensure that there are no buckets with the same name and duplicate content.
   - `roleCreate.py`: Create role for Lambda and attach required policy.
   - `lambdaCreate.py`: Create layer with `Pandas_layer.zip`, create lambda with `tdfThtDeploymentPackage.zip`.
   - `eventCreate.py`: Create scheduled rule in EventBridge for triggering Lambda hourly.
