## 9. Deploy model to Vertex endpoint  

🎯 Objective  
- Create endpoint
- Deploy your registered model
- Send prediction request

🧠 What We’re Building  
```
Client → Endpoint → Model → Prediction
```  
This is exactly how production ML systems work.  

⚙️ Step 1 — Get Our Model ID  

List models:
```ruby
</> bash


gcloud ai models list --region=us-central1
```  
We’ll see something like:  
```ruby
</> bash

MODEL_ID: 1234567890123456789
DISPLAY_NAME: healthcare-readmission-model
```

👉 Copy the MODEL_ID  

🏗 Step 2 — Create Endpoint  
```ruby
</> bash

gcloud ai endpoints create \
--region=us-central1 \
--display-name=healthcare-endpoint
```

🔍 Get Endpoint ID  
```ruby
</> bash

gcloud ai endpoints list --region=us-central1
```

Copy:
```
ENDPOINT_ID
```

🚀 Step 3 — Deploy Model to Endpoint  
```ruby
</> bash

gcloud ai endpoints deploy-model ENDPOINT_ID \
--region=us-central1 \
--model=MODEL_ID \
--display-name=healthcare-deployed-model \
--machine-type=e2-standard-2 \
--traffic-split=0=100
```

⏳ Wait (Important)  

Deployment takes:

- ~3–5 minutes

👉 This is where cost starts (endpoint = running service)  

🧪 Step 4 — Prepare Test Input  
```ruby
</> JSON

Create request.json

{
  "instances": [
    {
      "age": 65,
      "num_procedures": 2,
      "num_medications": 10,
      "days_in_hospital": 5,
      "med_per_day": 1.6,
      "procedure_ratio": 0.18,
      "high_risk": 1
    }
  ]
}
```  
⚠️ Must match our training features.  

▶️ Step 5 — Send Prediction Request  
```ruby
</> bash

gcloud ai endpoints predict ENDPOINT_ID \
--region=us-central1 \
--json-request=request.json
```

🔍 Expected Response  
```ruby
</> JSON

{
  "predictions": [1]
}
```  
👉 Meaning:  

- 1 = likely readmitted

✅ We Just Built  
```
✔ Live ML API
✔ Cloud-hosted model
✔ Real-time prediction system
```

💰 IMPORTANT (Cost Control)  

Endpoint costs money while running.  

👉 When not using:  
```ruby
</> bash

gcloud ai endpoints undeploy-model ENDPOINT_ID \
--region=us-central1 \
--deployed-model-id=DEPLOYED_MODEL_ID
```

🧠 What We Achieved  
```
Data → Model → Pipeline → Registry → Endpoint → API  
```  
👉 This is end-to-end MLOps.
