from os import environ
import boto3
import json


if __name__ == '__main__':
    # connect to lambda client
    lambda_client = boto3.client('lambda')
    iam = boto3.client('iam')

    # get arn of role
    roleArn = iam.get_role(RoleName='AWSLambdaGetWeatherDataRole')['Role']['Arn']
    # attachPolicy(roleName, policyList)
     
    layer_response = lambda_client.publish_layer_version(
        LayerName='pandas',
        Content={'S3Bucket': 'tdf-tht','S3Key': 'Code/pandas_layer.zip'},
        CompatibleRuntimes=['python3.7'])

    layerArn = layer_response['LayerVersionArn']
    # create lambda function
    lambda_client.create_function(
        FunctionName='getWeatherData',
        Runtime='python3.7',
        Role=roleArn,
        Handler='tdfThtDeploymentPackage/lambda_function.run',
        Code={'S3Bucket': 'tdf-tht','S3Key': 'Code/tdfThtDeploymentPackage.zip'},
        Environment={
            'Variables': {
                'API_KEY': 'e8fc23c823cba7861ed0fd8355f41174'
            }
        },
        Layers=[layerArn,'arn:aws:lambda:ap-southeast-2:817496625479:layer:AWSLambda-Python37-SciPy1x:113']
    )

