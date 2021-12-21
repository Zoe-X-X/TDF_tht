from os import environ
import boto3
import json

# # connect to iam client
# iam = boto3.client('iam')


# # create role for lambda (without attached policy)
# def roleCreate(roleName):
#     rolePolicy = json.dumps({
#         "Version": "2012-10-17",
#         "Statement": {
#             "Effect": "Allow",
#             "Principal": {"Service": "lambda.amazonaws.com"},
#             "Action": "sts:AssumeRole"
#         }})
#     role_response = iam.create_role(
#         RoleName=roleName,
#         AssumeRolePolicyDocument=rolePolicy)
#     ## return arn of this role 
#     return role_response['Role']['Arn']

# # attach policy to the role
# def attachPolicy(roleName, policyList):
#     for arn in policyList:
#         iam.attach_role_policy(
#             RoleName=roleName, 
#             PolicyArn=arn)


if __name__ == '__main__':
    # connect to lambda client
    lambda_client = boto3.client('lambda')
    iam = boto3.client('iam')

    # roleName = 'AWSLambdaGetWeatherDataRole'
    # policyList = ['arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole',\
    #             'arn:aws:iam::aws:policy/AmazonS3FullAccess',\
    #             'arn:aws:iam::aws:policy/service-role/AmazonS3ObjectLambdaExecutionRolePolicy']

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

    # lambda_client.create_function(
    #     FunctionName='getWeatherData',
    #     Runtime='python3.7',
    #     Role=roleArn,
    #     Handler='lambda_function.run',
    #     Code={'S3Bucket': 'tdf-tht','S3Key': 'Code/tdfThtDeploymentPackage.zip'}
    # )
    # lambda_client.update_function_configuration(
    #     FunctionName='getWeatherData',
    #     Runtime='python3.7',
    #     Handler='tdfThtDeploymentPackage/lambda_function.run',
    #     Environment={
    #         'Variables': {
    #             'API_KEY': os.environ['API_KEY']
    #         }
    #     }
    # )