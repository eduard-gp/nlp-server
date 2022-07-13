from flask import Blueprint, jsonify

from nlp.auth import login_required
from nlp.db.models import Persona, SupportedLanguage


blueprint = Blueprint("info", __name__, url_prefix="/info")

@blueprint.route("/languages", methods=["GET"])
@login_required
def languages():
    return SupportedLanguage.objects.to_json()

@blueprint.route("/labels", methods=["GET"])
@login_required
def labels():
    labels = Persona.objects.distinct("dialog.label")
    return jsonify(labels)