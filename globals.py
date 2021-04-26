from flask import g, Flask
from model import PricePredictor
from flask import Flask
from flask_cors import CORS
# тут содержатся глобальные переменные для всего приложения

app = Flask(__name__)
CORS(app)
model=PricePredictor()
df=init_df

def set_app(_app):
    global app
    app = _app


def get_app():
    global app
    return app

def get_model():
    global model
    return model