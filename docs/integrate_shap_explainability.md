## 13. Integrate SHAP explainability  

🎯 Objective (Explainable AI API)  

Build an API that returns:  
```ruby
</> JSON

{
  "prediction": 1,
  "explanation": {
    "num_medications": 0.42,
    "days_in_hospital": 0.31,
    "high_risk": 0.18
  }
}
```

👉 Using SHAP + Google Vertex AI  

🧠 Architecture (Important)  
```
Client
  ↓
FastAPI
  ↓
Feature Engineering (shared module)
  ↓
Vertex Endpoint (prediction)
  ↓
SHAP (local explanation)
  ↓
Response (prediction + explanation)
```

⚠️ Key Design Decision (CRITICAL)  

👉 SHAP will run locally in API, NOT in Vertex endpoint.  

Why?  
```
Option  |  Pros  |  Cons  
SHAP in endpoint  |  simple  |  expensive, slow  
SHAP in API (your choice)  |  fast, flexible  |  requires model locally  
```
👉 So we will:  

- Call Vertex endpoint → prediction
- Load model locally → SHAP explanation

🧱 Step 1 — Update Project Structure  
```
</> bash

api/
├── app.py
├── model_loader.py
└── requirements.txt
```

⚙️ Step 2 — Install Dependencies  
👉 add these to the /api/requirements.txt:  
```
fastapi==0.110.0
uvicorn==0.29.0
shap==0.44.1
joblib==1.3.2
numpy
pydantic
google-cloud-aiplatform
```
```ruby
</> bash  

pip install fastapi uvicorn shap joblib
```

🧾 Step 3 — Load Model Locally  
api/model_loader.py  
```ruby
</> python

import joblib

MODEL_PATH = "model/model.joblib"

model = joblib.load(MODEL_PATH)
```

⚠️ Where does the model come from?  

👉 Download from GCS:  
```
</> bash

gsutil cp gs://healthcare-mlops-data/models/model.joblib api/model/
```

⚙️ Step 4 — Build API with SHAP  
api/app.py  
```ruby
</> python

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
```

▶️ Step 5 — Run API  
```
</> bash

uvicorn api.app:app --reload
```

🌐 Step 6 — Test API  

Go to:  
```
http://127.0.0.1:8000/docs
```
Try:  
```ruby
</> JSON

{
  "age": 70,
  "num_procedures": 3,
  "num_medications": 12,
  "days_in_hospital": 6
}
```

🔍 Example Response  
```ruby
</> JSON  

{
  "prediction": 1,
  "explanation": {
    "age": 0.02,
    "num_procedures": 0.15,
    "num_medications": 0.40,
    "days_in_hospital": 0.30,
    "med_per_day": 0.22,
    "procedure_ratio": 0.12,
    "high_risk": 0.35
  }
}
```

🧠 Why This Is Powerful  

We now provide:  
```
✔ Prediction
✔ Reasoning
✔ Transparency
```
👉 This is critical in healthcare AI.  

🏆 What We Built  
```
Explainable AI API (production-ready)
```
Used in:

- healthcare risk scoring
- fraud detection
- credit scoring

