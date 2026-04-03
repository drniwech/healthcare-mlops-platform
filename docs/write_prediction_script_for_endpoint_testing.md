## 10. Write prediction script for endpoint testing  

🎯 Objective  

Create a Python prediction script that:  

- Calls our Vertex AI endpoint
- Sends test data
- Receives predictions
- Can be reused in apps / APIs

🧱 Suggested Structure  
```
project-root/
│
├── common/
│   ├── __init__.py
│   └── features.py
│
├──prediction/
    ├── predict.py
    ├── config.py
```

⚙️ Step 1 — Install Dependency  
```ruby
</> bash

pip install google-cloud-aiplatform
```

🧱 Step 2 — Create Shared Module  
🧾 common/features.py  
```ruby
</> python

def build_features(raw_input):
    return {
        "age": raw_input["age"],
        "num_procedures": raw_input["num_procedures"],
        "num_medications": raw_input["num_medications"],
        "days_in_hospital": raw_input["days_in_hospital"],
        "med_per_day": raw_input["num_medications"] / (raw_input["days_in_hospital"] + 1),
        "procedure_ratio": raw_input["num_procedures"] / (raw_input["num_medications"] + 1),
        "high_risk": int(raw_input["age"] > 65 and raw_input["num_medications"] > 10),
    }
```


🧾 Step 3 — Create prediction/config.py  
```ruby
</> python

PROJECT_ID = "healthcare-mlops-platform"
REGION = "us-central1"

ENDPOINT_ID = "YOUR_ENDPOINT_ID"  # replace this
```

🧑‍💻 Step 4 — Create prediction/predict.py  
```ruby
</> python

from google.cloud import aiplatform
from config import PROJECT_ID, REGION, ENDPOINT_ID
from common.features import build_features

def predict(instance):
    aiplatform.init(project=PROJECT_ID, location=REGION)

    endpoint = aiplatform.Endpoint(
        endpoint_name=f"projects/{PROJECT_ID}/locations/{REGION}/endpoints/{ENDPOINT_ID}"
    )

    response = endpoint.predict(instances=[instance])

    return response.predictions


if __name__ == "__main__":
    # Raw input (what real users would send)
    raw_input = {
        "age": 65,
        "num_procedures": 2,
        "num_medications": 10,
        "days_in_hospital": 5
    }

    # 🔥 Convert to model-ready features
    processed_input = build_features(raw_input)

    # Call endpoint
    prediction = predict(processed_input)

    print("Prediction:", prediction)
```

▶️ Step 5 — Run Script  
```ruby
</> bash

python prediction/predict.py
```

🔍 Expected Output  
```
</> bash  

Prediction: [1]
```

⚠️ Critical Detail 

Our input must match:
```
EXACT feature schema used in training
```
If we used:

one-hot encoding
extra features

👉 We must include them.  

🧠 Why This Is Important  

We now separate:
```
User Input → Feature Engineering → Model Input → Prediction
```
👉 This is CRITICAL in real systems.  


