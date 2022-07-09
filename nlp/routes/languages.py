from flask import Blueprint

from nlp.auth import login_required
from nlp.db.models import SupportedLanguage


blueprint = Blueprint("languages", __name__, url_prefix="/languages")

@blueprint.route("/")
@login_required
def languages():
    return SupportedLanguage.objects.to_json()
