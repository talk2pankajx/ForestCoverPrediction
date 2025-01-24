from logging import exception
import boto3
from aws_connnection import S3client
from io import StringIO
from forest_cover.exception import ForestException
import os, sys
from mypy_boto3_s3.service_resource import Bucket,Object
from typing import Union,List
from forest_cover.logging import logging
import pickle
from botocore.exceptions import ClientError
from pandas import DataFrame,read_csv

class SimpleStorageService:
    def __init__(self):
        s3_client_manager = S3client()
        self.s3_resource= s3_client_manager.s3_resource
        self.s3_client = s3_client_manager.s3_client
        
    def s3_key_path_available(self,bucket_name,s3_key):
        try:
            bucket = self.get_bucket(bucket_name)
            file_objects = [file_object for file_object in bucket.objects.filter(Prefix=s3_key)]
            if len(file_objects)>0:
                return True
            else:
                return False
                
        except Exception as e:
            raise ForestException(e,sys)
    
    @staticmethod
    def read_object(object_name: str,decode:bool=True,make_readable:bool=False)->Union[StringIO,str]:
        
        logging.info("Entered the read_object method of S3operation class")
        try:
            func = (
                lambda: object_name.get()["Body"].read().decode()
                if decode is True
                else object_name.get()["Body"].read()
                
            )
            conv_function = lambda: StringIO(func()) if make_readable is True else func()
            logging.info("Exited the read_object method of S3operation class")
            return conv_function
        except Exception as e:
            raise ForestException(e,sys)
    def get_bucket(self,bucket_name:str)->Bucket:
        logging.info("Entered the get bucket method of S3operation class")
        try:
            bucket = self.s3_resource.Bucket(bucket_name)
            logging.info("Exited the get_bucket method of S3operation class")
            return bucket
        except Exception as e:
            raise ForestException(e,sys)
    
    def get_file_object(self, filename: str,bucket_name:str)->Union[List[object],object]:
        logging.info("Entered the get file object method of S3operation class")
        try:
            bucket = self.get_bucket(bucket_name)
            file_object = [file_object for file_object in bucket.objects.filter(Prefix=filename)]
            func = lambda x: x[0] if len(x)==1 else x
            file_objs = func(file_object)
            logging.info("exited the get_file_object method of S3operation class")
            return file_objs
        except Exception as e:
            raise ForestException(e,sys)
    def load_model(self, model_name: str, bucket_name: str, model_dir: str = None) -> object:
        """
        Load a machine learning model from an S3 bucket.

        This function retrieves a serialized model from an S3 bucket and deserializes it.

        Parameters:
        -----------
        model_name : str
            The name of the model file to be loaded.
        bucket_name : str
            The name of the S3 bucket where the model is stored.
        model_dir : str, optional
            The directory within the bucket where the model is located. If None,
            the model is assumed to be in the root of the bucket.

        Returns:
        --------
        object
            The deserialized machine learning model.

        Raises:
        -------
        ForestException
            If an error occurs during the model loading process.
        """
        logging.info("Entered the load model method of S3operation class")
        try:
            func = (
                lambda: model_name
                if model_dir is None
                else model_dir + "/" + model_name
            )
            model_file = func()
            file_object = self.get_file_object(model_file, bucket_name)
            model_obj = self.read_object(file_object, decode=False)
            model = pickle.loads(model_obj)
            logging.info("exited the load model method of S3operation class")
            return model
        except Exception as e:
            raise ForestException(e, sys)
    def create_folder(self, folder_name: str, bucket_name: str) -> None:
        """
        Creates a folder in the specified S3 bucket.

        This method attempts to create a folder (which is actually a zero-byte object
        with a trailing slash) in the specified S3 bucket. If the folder already exists,
        no action is taken.

        Parameters:
        -----------
        folder_name : str
            The name of the folder to be created in the S3 bucket.
        bucket_name : str
            The name of the S3 bucket where the folder should be created.

        Returns:
        --------
        None

        Raises:
        -------
        ClientError
            If there's an error interacting with the S3 service, except for a 404 error.

        Notes:
        ------
        - The method logs its entry and exit points.
        - If a 404 error is encountered (indicating the folder doesn't exist),
          it creates the folder by putting a zero-byte object with the folder name
          and a trailing slash.
        - Other types of errors are silently ignored.
        """
        logging.info("Entered the create folder method of S3operation class")
        try:
            self.s3_resource.Ob 

        except ClientError as e:
            if e.response["Error"]["Code"] == 404:
                folder_obj = folder_name + "/"
                self.s3_client.put_object(Bucket=bucket_name, Key=folder_obj)
            else:
                pass
        logging.info("Exited the create folder method of S3operation class")

        
    
    def upload_file(self, from_filename: str, to_filename: str, bucket_name: str, remove: bool = True):
        """
        Uploads a file from the local system to an S3 bucket.

        Parameters:
        - from_filename (str): The path to the local file to be uploaded.
        - to_filename (str): The name of the file in the S3 bucket.
        - bucket_name (str): The name of the S3 bucket to upload the file to.
        - remove (bool, optional): If True, the local file will be deleted after uploading. Defaults to True.

        Returns:
        None

        Raises:
        ForestException: If an error occurs during the file upload process.
        """
        logging.info(F"Entered the upload file method of S3operation class")
        try:
            logging.info(f"Uploading {from_filename} file to {to_filename} file in {bucket_name} bucket")

            self.s3_resource.meta.client.upload_file(from_filename, bucket_name, to_filename)

            logging.info(f"Uploading {from_filename} file to {to_filename} file in {bucket_name} bucket ")

            if remove is True:
                os.remove(from_filename)
                logging.info(f"Remove is set to {remove}, deleted the file")
            else:
                logging.info(f"Remove is set to {remove}, file not deleted")

            logging.info("Exited the upload file method of S3operation class")
        except Exception as e:
            raise ForestException(e, sys)
        
    def get_df_from_object(self, object_: object) -> DataFrame:
        """
        Method Name :   get_df_from_object
        Description :   This method gets the dataframe from the object_name object

        Output      :   Folder is created in s3 bucket
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        logging.info("Entered the get_df_from_object method of S3Operations class")

        try:
            content = self.read_object(object_, make_readable=True)
            df = read_csv(content, na_values="na")
            logging.info("Exited the get_df_from_object method of S3Operations class")
            return df
        except Exception as e:
            raise ForestException(e, sys) from e

    def read_csv(self, filename: str, bucket_name: str) -> DataFrame:
        """
        Method Name :   get_df_from_object
        Description :   This method gets the dataframe from the object_name object

        Output      :   Folder is created in s3 bucket
        On Failure  :   Write an exception log and then raise an exception

        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        logging.info("Entered the read_csv method of S3Operations class")

        try:
            csv_obj = self.get_file_object(filename, bucket_name)
            df = self.get_df_from_object(csv_obj)
            logging.info("Exited the read_csv method of S3Operations class")
            return df
        except Exception as e:
            raise ForestException(e, sys) from e
