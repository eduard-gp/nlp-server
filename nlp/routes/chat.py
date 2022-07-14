from flask import Blueprint, request
import numpy as np

from nlp.auth import login_required
from nlp.db.models import Persona
from nlp.ml import models, idx_to_intention


blueprint = Blueprint("chat", __name__, url_prefix="/chat")

@blueprint.route("/utterance", methods=["POST"])
@login_required
def utterance():
    language = request.json["language"]
    utterance = request.json["utterance"]
    persona_id = request.json["persona_id"]

    persona = Persona.objects(id=persona_id).first()

    test_uttenrace = ["hello there"]

    predictions = models["text_classification"]["en"].predict(test_uttenrace)
    intention_idx = np.argmax(predictions)
    intention = idx_to_intention[intention_idx]

    print(predictions)

    return {"ok": "hei"}
