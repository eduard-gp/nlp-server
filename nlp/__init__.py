import os
from flask import Flask
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from mongoengine import connect

import tensorflow as tf
import tensorflow_text as text

from . import auth
from . import routes

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config:
        app.config.from_mapping(test_config)
    else:
        app.config.from_pyfile("config.py")

    connect(host=app.config["DATABASE_URI"])
    CORS(app, supports_credentials=True, origins="http://127.0.0.1:3000")
    Bcrypt(app)

    app.register_blueprint(auth.blueprint)
    app.register_blueprint(routes.personas.blueprint)
    app.register_blueprint(routes.info.blueprint)
    app.register_blueprint(routes.chat.blueprint)

    # base_dir = os.path.abspath(os.path.dirname(__file__))
    # dir_path = os.path.join(base_dir, "ml", "models", "text_classification", "en", "model")

    # demo_path = os.path.join(base_dir, "ml", "models", "hei.txt")
    # print(demo_path)
    # with open(demo_path) as f:
    #     print(f.read())

    return app

app = create_app()

from . import ml

print(ml.demo_path)

@app.route("/")
# @auth.login_required
def index():
    return "<h1> Hellow world!</h1>"


# @app.route("/personas", methods=["GET"])
# def personas():
#     return {"personas": 1}
