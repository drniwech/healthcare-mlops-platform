from fastapi import FastAPI
from pydantic import BaseModel
import shap
import numpy as np

from common.features import build_features
from prediction.predict import predict  # Vertex call
from model_loader import model

app = FastAPI()

# Initialize SHAP once (important for performance)
explainer = shap.TreeExplainer(model)


# =========================
# Request Schema
# =========================
class PatientInput(BaseModel):
    age: int
    num_procedures: int
    num_medications: int
    days_in_hospital: int


# =========================
# Endpoint
# =========================
@app.post("/predict")
def predict_with_explain(input: PatientInput):
    raw_input = input.dict()

    # Step 1: Feature engineering
    features = build_features(raw_input)

    # Step 2: Prediction from Vertex AI
    prediction = predict(features)

    # Step 3: SHAP explanation
    feature_array = np.array([list(features.values())])
    shap_values = explainer.shap_values(feature_array)

    explanation = dict(zip(features.keys(), shap_values[0]))

    return {
        "prediction": int(prediction[0]),
        "explanation": explanation
    }
