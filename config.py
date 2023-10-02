import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

class Config:
    SERVER_NAME = os.getenv('SERVER_NAME') or None
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
    SECRET_KEY=os.getenv('SECRET_KEY')
    WTF_CSRF_SECRET_KEY=os.getenv('WTF_CSRF_SECRET_KEY')
    CELERY_CONFIG = {
        'broker_url': os.getenv('REDIS_URL'),
        'result_backend': os.getenv('REDIS_URL'),
    }
    REDIS_URL = os.getenv('REDIS_URL')

class Development(Config):
    ENVIRONMENT = 'development'
    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True
    SEND_FILE_MAX_AGE_DEFAULT = 0