from flask import Blueprint, make_response, request, session
from flask_bcrypt import generate_password_hash, check_password_hash
from mongoengine import errors
from datetime import datetime, timedelta
import functools

from ..db import models
from . import utils

SESSION_DURATION_HOURS = 8

blueprint = Blueprint("auth", __name__, url_prefix="/auth")

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        session_db = models.Session.objects(user_id=session.get("user_id")).first()
        if session_db is None:
            return {"message": "You are not logged in!"}, 401
        elif session_db.expiration_date < datetime.now():
            session_db.delete()
            return {"message": "You are not logged in!"}, 401
        return view(*args, **kwargs)
    return wrapped_view

def _check_form(username, password):
    error = {
        "username": None,
        "password": None,
        "other": []
    }

    if not username:
        error["username"] = "Username can't be empty!"
    if not password:
        error["password"] = "Password can't be empty!"
    
    return error

@blueprint.route("/signup", methods=["POST"])
def signup():
    username = request.json["username"]
    password = request.json["password"]

    error = _check_form(username, password)
    if error["username"] is not None or error["password"] is not None:
        return make_response(error), 400

    hashed_password = generate_password_hash(password)
    
    try:
        user = models.User(username=username, password=hashed_password).save()
        utils.init_wiht_default_setting(user)
        db_session = models.Session(
            user_id=str(user.id),
            expiration_date=datetime.now() + timedelta(hours=SESSION_DURATION_HOURS)
        ).save()
        session.clear()
        session["user_id"] = db_session.user_id
    except errors.NotUniqueError:
        error["other"].append("Username already exists!")
        return make_response(error), 409

    return {"message": "User created with success."}

@blueprint.route("/login", methods=["POST"])
def login():
    username = request.json["username"]
    password = request.json["password"]
    
    error = _check_form(username, password)
    if error["username"] is not None or error["password"] is not None:
        return make_response(error), 400
    
    user = models.User.objects(username=username).first()
    if not user or not check_password_hash(user.password, password):
        error["other"].append("Username or password are incorrect!")
        return make_response(error), 409

    session_db = models.Session.objects(user_id=str(user.id)).first()
    if session_db is not None and session_db.expiration_date > datetime.now():
        error["other"].append("User already logged in. Please, logout first!")
        return make_response(error), 409

    session_db = models.Session(
        user_id=str(user.id),
        expiration_date=datetime.now() + timedelta(hours=SESSION_DURATION_HOURS)
    ).save()
    session.clear()
    session["user_id"] = session_db.user_id
    return {"message": "You are logged in"}

@blueprint.route("/logout", methods=["POST"])
@login_required
def logout():
    session_db = models.Session.objects(user_id=session.get("user_id")).first()
    session_db.delete()
    return {"message": "Logged out with success."}


@blueprint.route("/islogged", methods=["GET"])
def islogged():
    session_db = models.Session.objects(user_id=session.get("user_id")).first()
    print(session_db)
    if session_db is None or session_db.expiration_date < datetime.now():
        return {"isLogged": False}
    return {"isLogged": True}
