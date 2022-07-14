import os
import tensorflow as tf

base_dir = os.path.abspath(os.path.dirname(__file__))
dir_path = os.path.join(base_dir, "ml", "models",
                        "text_classification", "en", "model")

demo_path = os.path.join(base_dir, "models", "hei.txt")
print(demo_path)
with open(demo_path) as f:
    print(f.read())

intention_to_idx = {
    "chest_pain": 0,
    "symptoms_changes": 1,
    "fainting_symptoms": 2,
    "cough_symptoms": 3,
    "surgeries": 4,
    "fever_symptoms": 5,
    "palpitations_symptoms": 6,
    "chronic_treatment": 7,
    "diseases_parents": 8,
    "diseases_personal": 9,
    "greetings": 10,
    "symptoms_start": 11,
    "symptoms_circumstances": 12,
    "visit_reason": 13
}

idx_to_intention = {v: k for k, v in intention_to_idx.items()}

models = {
    "text_classification": {
        "en": tf.keras.models.load_model(os.path.join(base_dir, "models", "text_classification", "en", "model"))
    }
}
