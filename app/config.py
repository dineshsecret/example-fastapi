from dataclasses import fields
from email.mime import base
import this
from pydantic import BaseSettings
import os

class Settings(BaseSettings):
    database_hostname:str
    database_port:str
    database_name:str
    database_password:str
    database_username:str
    secret_key:str
    algorithm:str
    access_token_expire_min:int

    if 'RDS_DB_NAME' in os.environ:
        print('im in RDS')
        
        database_hostname = os.environ['RDS_HOSTNAME']     
        database_port = os.environ['RDS_PORT']
        database_name = os.environ['RDS_DB_NAME']
        database_password = os.environ['RDS_PASSWORD']
        database_username = os.environ['RDS_USERNAME']
        secret_key = os.environ['RDS_SECRETKEY']
        algorithm = os.environ['RDS_ALGO']
        access_token_expire_min = os.environ['ACCESSTOKENEXPIREMIN']
    else:
                     
        class Config:
            env_prefix = ""
            case_sensitive = False
        
            env_file = ".env"
        #print (f"dbhost{os.environ['RDS_HOSTNAME']}")
        
print('settings are as follows')
print(Settings().dict())            
settings = Settings()