import os
from dotenv import load_dotenv
load_dotenv()
print("ran it")

class Config(object):
    DEBUG = False
    DEVELOPMENT = False
    SECRET_KEY = os.getenv("SECRET_KEY", "dfal;dfkad adf")
    if os.getenv("APP_SETTINGS") == "Config":
        SQLALCHEMY_DATABASE_URI = "postgresql" + os.getenv("DATABASE_URL")[8:]
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", None)
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", None)
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", None)
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", None)
    GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


class StagingConfig(Config):
    if os.getenv("APP_SETTINGS") == "StagingConfig":
        SQLALCHEMY_DATABASE_URI = "postgresql" + os.getenv("DATABASE_URL")[8:]

class DevelopmentConfig(Config):
    DEBUG = True
    #DEVELOPMENT = True
    # using the uri, the url is just a filler
    # SQLALCHEMY_DATABASE_URI = "postgresql://postgres:tamara12@localhost/test"
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:tamara12@localhost/service-hours"
    #SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///database.db")
    print(SQLALCHEMY_DATABASE_URI)
    print('hello')
    FLASK_APP = "main.py"
    # MAIL_SERVER = 'smtp.gmail.com'
    # MAIL_PORT = 465
    # MAIL_USE_TLS = False
    # MAIL_USE_SSL = True
    # MAIL_USERNAME = 'gritzpython@gmail.com'
    # MAIL_PASSWORD = 'vrucxrsmpacwcdsk'