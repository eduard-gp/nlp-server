from flask import Blueprint, session, request

from nlp.auth import login_required
from nlp.db.models import Persona

blueprint = Blueprint("personas", __name__, url_prefix="/personas")

@blueprint.route("/", methods=["GET"])
@login_required
def personas():
    user_id = session.get("user_id")
    personas = Persona.objects(user_id=user_id).fields(
        description=1,
        language=1,
        dialog__label=1,
        dialog__questions=1,
        dialog__answers=1
    )
    return personas.to_json()

@blueprint.route("/persona/update", methods=["POST"])
@login_required
def update_persona():
    result = Persona.objects(id= request.json["_id"]["$oid"]).update_one(
        description=request.json["description"],
        dialog=request.json["dialog"],
        language=request.json["language"]
    )
    if result > 0:
        return {"message": "Updated with success!"}
    else:
        return {"message": "Update failed!"}

@blueprint.route("/persona/insert", methods=["POST"])
@login_required
def insert_persona():
    persona = Persona(
        description=request.json["description"],
        dialog=request.json["dialog"],
        language=request.json["language"],
        user_id=session.get("user_id")
    ).save()
    return persona.to_json()