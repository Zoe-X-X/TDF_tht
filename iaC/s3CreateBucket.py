# import libraries
import boto3

# connect to s3 client
s3 = boto3.client('s3')

def s3BucketCreate(acl_type,bucket_name,location,key_name,local_file):
    # public bucket does not exist, creat new one 
    if bucket_name not in [n['Name'] for n in s3.list_buckets()['Buckets']]:
        s3.create_bucket(
            ACL=acl_type,
            Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint': location}
        )
        print(f'The new bucket {bucket_name} has been created.')
        # upload the core code of lambda
        s3.upload_file(local_file, bucket_name, key_name)
        print(f'The new object {key_name} has been created.')
    
    #public bucket exist
    else :
        print(f'The bucket {bucket_name} exists.')
        try: # ckeck if the core code of lambda exists
            s3.get_object(Bucket=bucket_name, Key=key_name)
        except :
            # upload the core code of lambda
            s3.upload_file(local_file, bucket_name, key_name)
            print(f'The new object {key_name} has been created.')
        else:
            print(f'The object {key_name} exists.')

if __name__ == '__main__':
    s3BucketCreate('public-read','tdf-tht','ap-southeast-2','Code/tdfThtDeploymentPackage.zip','../tdfThtDeploymentPackage.zip')