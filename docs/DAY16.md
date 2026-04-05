# Day 16 --- Logging Prediction Confidence Scores

## 🎯 Objective

Enhance the inference service to: - Return **prediction confidence
scores** - Log **inputs, predictions, and confidence** - Trigger
**alerts for low-confidence predictions**

------------------------------------------------------------------------

## 🧱 Architecture Context

Current system: - Vertex AI Endpoint (model serving) - FastAPI
(`/api/app.py`) - SHAP explainability - CI/CD via GitHub Actions

👉 Focus today: **Inference Layer Observability**

------------------------------------------------------------------------

## 🔄 Step 1: Update Prediction Service (`/prediction/predict.py`)

### Goal

Standardize Vertex AI output:

``` json
{
  "prediction": [1],
  "confidence": [0.87]
}
```

### Implementation

``` python
from google.cloud import aiplatform
from config import PROJECT_ID, REGION, ENDPOINT_ID

def predict(instance):
    aiplatform.init(project=PROJECT_ID, location=REGION)

    endpoint = aiplatform.Endpoint(
        endpoint_name=f"projects/{PROJECT_ID}/locations/{REGION}/endpoints/{ENDPOINT_ID}"
    )

    response = endpoint.predict(instances=[instance])
    predictions = response.predictions

    parsed_predictions = []
    parsed_confidences = []

    for p in predictions:
        if isinstance(p, dict) and "scores" in p:
            scores = p["scores"]
            pred_class = int(p.get("classes", list(range(len(scores))))[scores.index(max(scores))])
            confidence = float(max(scores))
        elif isinstance(p, list):
            scores = p
            pred_class = int(scores.index(max(scores)))
            confidence = float(max(scores))
        else:
            pred_class = int(p)
            confidence = None

        parsed_predictions.append(pred_class)
        parsed_confidences.append(confidence)

    return {
        "prediction": parsed_predictions,
        "confidence": parsed_confidences
    }
```

------------------------------------------------------------------------

## 🌐 Step 2: Update FastAPI (`/api/app.py`)

### Add Configurable Threshold

``` python
LOW_CONF_THRESHOLD = 0.6
```

### Add Logging Setup

``` python
import logging
import json
from datetime import datetime

logging.basicConfig(level=logging.INFO)
```

------------------------------------------------------------------------

### Update Endpoint Logic

``` python
result = predict(features)

prediction = int(result["prediction"][0])
confidence = float(result["confidence"][0])
```

------------------------------------------------------------------------

### Structured Logging

``` python
log_data = {
    "timestamp": datetime.utcnow().isoformat(),
    "input": features,
    "prediction": prediction,
    "confidence": confidence
}

logging.info(json.dumps(log_data))
```

------------------------------------------------------------------------

### Low-Confidence Alert 🚨

``` python
if confidence < LOW_CONF_THRESHOLD:
    logging.warning(json.dumps({
        "alert": "Low confidence prediction",
        "confidence": confidence,
        "threshold": LOW_CONF_THRESHOLD,
        "input": features
    }))
```

------------------------------------------------------------------------

### Final API Response

``` python
return {
    "prediction": prediction,
    "confidence": confidence,
    "explanation": explanation
}
```

------------------------------------------------------------------------

## 🧪 Step 3: Testing

### Run API

``` bash
uvicorn app:app --reload
```

### Sample Request

``` bash
curl -X POST http://127.0.0.1:8000/predict \
-H "Content-Type: application/json" \
-d '{"age":65,"num_procedures":2,"num_medications":10,"days_in_hospital":5}'
```

------------------------------------------------------------------------

## ✅ Expected Response

``` json
{
  "prediction": 1,
  "confidence": 0.87,
  "explanation": { ... }
}
```

------------------------------------------------------------------------

## 📊 Logging Examples

### Normal Log

``` json
{
  "timestamp": "2026-04-05T20:00:00",
  "input": {...},
  "prediction": 1,
  "confidence": 0.87
}
```

### Alert Log

``` json
{
  "alert": "Low confidence prediction",
  "confidence": 0.52,
  "threshold": 0.6,
  "input": {...}
}
```

------------------------------------------------------------------------

## 🧠 Key Design Decisions

-   Structured JSON logging → enables analytics & monitoring
-   Confidence threshold → exposes model uncertainty
-   Separation of concerns → clean architecture

------------------------------------------------------------------------

## 🎯 Interview Talking Points

> Implemented structured prediction logging with confidence thresholds
> and alerting, enabling real-time monitoring and supporting drift
> detection and observability.

------------------------------------------------------------------------

## ✅ Deliverables

-   Prediction includes confidence
-   API returns confidence
-   Structured logs implemented
-   Low-confidence alert enabled
-   Clean inference abstraction

------------------------------------------------------------------------

## ⏭️ Next Step (Day 17)

**Input Logging + Data Drift Detection**
