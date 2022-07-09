from flask import Blueprint, session

from nlp.auth import login_required
from nlp.db.models import Persona, Session

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
