import os
class Config:
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY')
    API = os.environ.get('API')
    CURRENCY_API = os.environ.get('CURRENCY_API')
    NEWS_API = os.environ.get('NEWS_API')
    SCHEDULER_API_ENABLED = True