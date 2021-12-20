# import libraries
import os
import boto3
import requests
import pandas as pd
from datetime import datetime

# connect to s3 client
s3 = boto3.client('s3')

def run(event=None, context=None):
    # check if the destination file exist or not
    s3ObjCheck('tdf-tht','Staging/weatherDataHourly.csv')

    # call API to get the current weather of Sydney
    response = weatherApi('Sydney',os.environ['API_KEY'])
    new_row = {'weather':response['weather'][0]['main'], 
                'temp':response['main']['temp'], 
                'temp_min':response['main']['temp_min'], 
                'temp_max':response['main']['temp_max'],
                'pressure':response['main']['pressure'], 
                'humidity':response['main']['humidity'],
                'visibility':response['visibility'],
                'datetime':datetime.fromtimestamp(response['dt']),
                'sunrise':datetime.fromtimestamp(response['sys']['sunrise']), 
                'sunset':datetime.fromtimestamp(response['sys']['sunset'])}
    insertNewRow('tdf-tht','Staging/weatherDataHourly.csv',new_row)


# create CSV in bucket
def s3ObjCheck(bucket_name,key_name):
    try:
        s3.get_object(Bucket=bucket_name, Key=key_name)
    except :
        # create destination file if the bucket was empty
        head = 'weather,temp,temp_min,temp_max,pressure,humidity,visibility,datetime,sunrise,sunset'
        s3.put_object(Body=head, Bucket=bucket_name, Key=key_name)
        print(f'The new object {key_name} has been created.')
    else:
        print(f'The object {key_name} exists.')

# call Api
def weatherApi(city_name,api_key):
    return requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&units=metric&appid={api_key}").json()

def insertNewRow(bucket_name,key_name,new_data):
    # download existing data
    s3.download_file(bucket_name,key_name,'file_name')
    df = pd.read_csv('file_name')
    # append new data from api to the end of existing data
    df = df.append(new_data, ignore_index=True)
    # convert dataframe into csv format and then bytes 
    bytes_to_write = df.to_csv(None, index=False).encode()
    # put data into bucket 
    s3.put_object(Body=bytes_to_write, Bucket=bucket_name, Key=key_name)
    os.remove('file_name')