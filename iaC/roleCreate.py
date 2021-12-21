import boto3
import json
# connect to iam client
iam = boto3.client('iam')


# create role for lambda (without attached policy)
def roleCreate(roleName):
    rolePolicy = json.dumps({
        "Version": "2012-10-17",
        "Statement": {
            "Effect": "Allow",
            "Principal": {"Service": "lambda.amazonaws.com"},
            "Action": "sts:AssumeRole"
        }})
    iam.create_role(
        RoleName=roleName,
        AssumeRolePolicyDocument=rolePolicy)

# attach policy to the role
def attachPolicy(roleName, policyList):
    for arn in policyList:
        iam.attach_role_policy(
            RoleName=roleName, 
            PolicyArn=arn)


if __name__ == '__main__':
    # connect to lambda client

    roleName = 'AWSLambdaGetWeatherDataRole'
    policyList = ['arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole',\
                'arn:aws:iam::aws:policy/AmazonS3FullAccess',\
                'arn:aws:iam::aws:policy/service-role/AmazonS3ObjectLambdaExecutionRolePolicy']

    # get arn of role
    roleCreate(roleName)
    attachPolicy(roleName, policyList)
    