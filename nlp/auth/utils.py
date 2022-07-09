from ..db import models

def _init_with_default_personas(user):
    default_personas = models.Persona.objects(__raw__={"user_id": models.DEFAULT_USER_ID})
    user_personas = []
    for doc in default_personas:
        new_doc = models.Persona(
            description=doc.description,
            dialog=doc.dialog,
            language=doc.language,
            user_id=user.id
        )
        user_personas.append(new_doc)
    models.Persona.objects.insert(user_personas)

def _init_with_default_texts(user):
    default_texts = models.TextClassification.objects(__raw__={"user_id": models.DEFAULT_USER_ID})
    user_texts = [] 
    for doc in default_texts:
        new_doc = models.TextClassification(
            text=doc.text,
            language=doc.language,
            label=doc.label,
            user_id=user.id
        )
        user_texts.append(new_doc)
    models.TextClassification.objects.insert(user_texts)

def init_wiht_default_setting(user):
    _init_with_default_personas(user)
    _init_with_default_texts(user)

