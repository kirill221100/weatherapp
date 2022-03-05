from flask import Flask
from app.config import Config
from flask_apscheduler import APScheduler

app = Flask(__name__)
app.config.from_object(Config)
scheduler = APScheduler()
scheduler.init_app(app)

from app.views import *
