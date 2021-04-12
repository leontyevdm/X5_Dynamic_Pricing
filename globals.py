from flask import g, Flask
from model import PricePredictor

# тут содержатся глобальные переменные для всего приложения

app = Flask(__name__)
model=PricePredictor()

def set_app(_app):
    global app
    app = _app


def get_app():
    global app
    return app

def get_model():
    global model
    return model