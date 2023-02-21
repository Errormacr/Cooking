import configparser
import os

basedir = os.path.abspath(os.getcwd())
config = configparser.ConfigParser()
config.read(basedir+r'\server\config.ini')
topsecret = config['topsecret']
PORT = topsecret['port']
HOST = topsecret['host']
USER = topsecret['user']
PASS = topsecret['pass']
DB_Name = topsecret['db']
SECRET = topsecret['secret']
