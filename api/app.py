from fastapi import FastAPI
from pydantic import BaseModel
import shap
import numpy as np
import logging
import json
from datetime import datetime

from common.features import build_features
from prediction.predict import predict  # Vertex call
from model_loader import model

LOW_CONF_THRESHOLD = 0.6

app = FastAPI()

# =========================
# Logging Setup
# =========================
logging.basicConfig(level=logging.INFO)

# =========================
# Initialize SHAP once
# =========================
explainer = shap.TreeExplainer(model)


# =========================
# Request Schema
# =========================
class PatientInput(BaseModel):
    age: int
    num_procedures: int
    num_medications: int
    days_in_hospital: int
    gender: str
    diagnosis: str


# =========================
# Endpoint
# =========================
@app.post("/predict")
def predict_with_explain(input: PatientInput):
    raw_input = input.dict()

    # Step 1: Feature engineering
    features = build_features(raw_input)

    # Step 2: Prediction from Vertex AI
    # Expecting: prediction + confidence
    result = predict(features)

    # Example expected structure:
    # result = {
    #     "prediction": [1],
    #     "confidence": [0.87]
    # }

    prediction = int(result["prediction"][0])
    confidence = float(result["confidence"][0])

    # =========================
    # Step 3: SHAP explanation
    # =========================
    feature_array = np.array([list(features.values())])
    shap_values = explainer.shap_values(feature_array)
    explanation = dict(zip(features.keys(), shap_values[0]))

    # =========================
    # Step 4: Logging
    # =========================
    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "input": features,
        "prediction": prediction,
        "confidence": confidence,
    }

    logging.info(json.dumps(log_data))

    # =========================
    # Step 5: Low Confidence Alert
    # =========================
    if confidence < LOW_CONF_THRESHOLD:
        logging.warning(
            json.dumps(
                {
                    "alert": "Low confidence prediction",
                    "confidence": confidence,
                    "threshold": LOW_CONF_THRESHOLD,
                    "input": features,
                }
            )
        )

    # =========================
    # Response
    # =========================
    return {
        "prediction": prediction,
        "confidence": confidence,
        "explanation": explanation,
    }
