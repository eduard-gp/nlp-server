from flask import Flask
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from mongoengine import connect

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
    return app

app = create_app()

@app.route("/")
# @auth.login_required
def index():
    return "<h1> Hellow world!</h1>"


# @app.route("/personas", methods=["GET"])
# def personas():
#     return {"personas": 1}
