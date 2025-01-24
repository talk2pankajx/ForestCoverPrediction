import boto3
import os
from dotenv import load_dotenv
load_dotenv()

class S3client:
    
    s3_client = None
    s3_resource = None
    def __init__(self,region_name= os.environ["AWS_DEFAULT_REGION"]):
        
        if S3client.s3_resource ==None or S3client.s3_client==None:
            __acces_key_id = os.environ["AWS_ACCESS_KEY_ID"]
            __secret_access_key = os.environ["AWS_SECRET_ACCESS_KEY"]
            if __acces_key_id is None:
                raise Exception("Evironment Variable: is not set")
            if __secret_access_key is None:
                raise Exception("Evironment Variable: is not set")
        
            S3client.s3_resource = boto3.resource('s3',
                aws_access_key_id=__acces_key_id,
                aws_secret_access_key=__secret_access_key,
                region_name=region_name
        )

            S3client.s3_client = boto3.client('s3',
                aws_access_key_id=__acces_key_id,
                aws_secret_access_key=__secret_access_key,
                region_name=region_name
            )
        self.s3_resource = S3client.s3_resource
        self.s3_client = S3client.s3_client