import os
from dotenv import load_dotenv
load_dotenv()
PORT = os.environ.get('PORT')
HOST = os.environ.get('HOST')
USER = os.environ.get('USER')
PASS = os.environ.get('PASS')
DB_Name = os.environ.get('DB_Name')
SECRET = os.environ.get('SECRET')
KEY = os.environ.get('DEV')

