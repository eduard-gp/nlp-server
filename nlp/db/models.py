from pydoc import Doc
from mongoengine import (
    Document, StringField, ReferenceField, EmbeddedDocument, EmbeddedDocumentField,
    DictField, ListField, DateTimeField
)

LANGUAGES_SUPPORTED = ("en", "ro")
THEMES_SUPPROTED = ("dark-theme", "white-theme")
DEFAULT_USER_ID = "default"

class UserSettings(EmbeddedDocument):
    ui_theme = StringField(choices=THEMES_SUPPROTED, default="white-theme")
    language = StringField(choices=LANGUAGES_SUPPORTED, default="en")

class User(Document):
    username = StringField(max_length=60, unique=True, required=True)
    password = StringField(max_length=200, required=True)
    settings = EmbeddedDocumentField(UserSettings)

class TextClassification(Document):
    text = StringField()
    label = StringField()
    language = StringField(choices=LANGUAGES_SUPPORTED)
    user_id = ReferenceField(User)

class DialogEntity(EmbeddedDocument):
    label = StringField(required=True)
    questions = ListField(StringField())
    tokenized_questions = ListField(ListField(StringField()))
    ner_questions = ListField(ListField(StringField()))
    answers = ListField(StringField())
    tokenized_answers = ListField(ListField(StringField()))
    ner_answers = ListField(ListField(StringField()))

class Persona(Document):
    description = DictField()
    dialog = ListField(EmbeddedDocumentField(DialogEntity))
    language = StringField(choices=LANGUAGES_SUPPORTED)
    user_id = ReferenceField(User)

class Session(Document):
    user_id = StringField(required=True)
    expiration_date = DateTimeField(required=True)

class SupportedLanguage(Document):
    language = StringField(required=True, unique=True)