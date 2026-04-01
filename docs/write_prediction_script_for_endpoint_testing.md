## Write prediction script for endpoint testing  

🎯 Objective  

Create a Python prediction script that:  

- Calls our Vertex AI endpoint
- Sends test data
- Receives predictions
- Can be reused in apps / APIs

🧱 Suggested Structure  
```
prediction/
    predict.py
    config.py
```

⚙️ Step 1 — Install Dependency  
```ruby
</> bash

pip install google-cloud-aiplatform
```

🧾 Step 2 — Create prediction/config.py  
```ruby
</> python

PROJECT_ID = "healthcare-mlops-platform"
REGION = "us-central1"

ENDPOINT_ID = "YOUR_ENDPOINT_ID"  # replace this
```

🧑‍💻 Step 3 — Create prediction/predict.py  
```ruby
</> python

from google.cloud import aiplatform
from config import PROJECT_ID, REGION, ENDPOINT_ID


def predict(instance):
    aiplatform.init(project=PROJECT_ID, location=REGION)

    endpoint = aiplatform.Endpoint(
        endpoint_name=f"projects/{PROJECT_ID}/locations/{REGION}/endpoints/{ENDPOINT_ID}"
    )

    response = endpoint.predict(instances=[instance])

    return response.predictions


if __name__ == "__main__":
    # Example test input (must match training features)
    test_instance = {
        "age": 65,
        "num_procedures": 2,
        "num_medications": 10,
        "days_in_hospital": 5,
        "med_per_day": 1.6,
        "procedure_ratio": 0.18,
        "high_risk": 1
    }

    prediction = predict(test_instance)

    print("Prediction:", prediction)
```

▶️ Step 4 — Run Script  
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

👉 You must include them
