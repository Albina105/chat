from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
AUTH_SERVICE_URL= os.getenv('AUTH_SERVICE_URL')
# config