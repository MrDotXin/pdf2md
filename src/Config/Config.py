import os
from dotenv import load_dotenv
load_dotenv(".env", override=True)


class Config :
    def __init__(self,):
        self.textin_app_id = os.environ['X_TI_APP_ID']
        self.textin_secret_key = os.environ['X_TI_SECRET_CODE']
        
        self.zamzar_api_key = os.environ['ZAMZAR_API_KEY']
        
        self.mistral_api_key = os.environ['MISTRAL_API_KEY']
        
        self.doc2x_api_key = os.environ['DOC2X_API_KEY']
        
        self.light_api_key = os.environ['LIGHT_API_KEY']
        
        
config = Config()