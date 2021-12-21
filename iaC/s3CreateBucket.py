# import libraries
import boto3

# connect to s3 client
s3 = boto3.client('s3')

def s3BucketCreate(acl_type,bucket_name,location,code_key,layer_key):
    # public bucket does not exist, creat new one 
    if bucket_name not in [n['Name'] for n in s3.list_buckets()['Buckets']]:
        s3.create_bucket(
            ACL=acl_type,
            Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint': location}
        )
        print(f'The new bucket {bucket_name} has been created.')
        # upload the core code of lambda
        s3.upload_file(code_key[1], bucket_name, code_key[0])
        s3.upload_file(layer_key[1], bucket_name, layer_key[0])
        print(f'The new object {code_key[0]} and {layer_key[0]} have been created.')
    
    #public bucket exist
    else :
        print(f'The bucket {bucket_name} exists.')
        try: # ckeck if the core code of lambda exists
            assert len(s3.list_objects(Bucket=bucket_name, Prefix=code_key[0].split('/')[0]+'/', Delimiter='/')['Contents'])==2
        except :
            # upload the core code of lambda
            s3.upload_file(code_key[1], bucket_name, code_key[0])
            s3.upload_file(layer_key[1], bucket_name, layer_key[0])
            print(f'The new object {code_key[0]} and {layer_key[0]} have been created.')
        else:
            print(f'The new object {code_key[0]} and {layer_key[0]} have been created.')

if __name__ == '__main__':
    s3BucketCreate('public-read','tdf-tht','ap-southeast-2',('Code/tdfThtDeploymentPackage.zip','../tdfThtDeploymentPackage.zip'),('Code/pandas_layer.zip','../pandas_layer.zip'))