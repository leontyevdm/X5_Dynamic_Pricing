from flask import g, Flask


# тут содержатся глобальные переменные для всего приложения

app = Flask(__name__)

def set_app(_app):
    global app
    app = _app


def get_app():
    global app
    return app

def get_model():
    global model
    return model