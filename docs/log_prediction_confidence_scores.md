## ✅ 14: Log Prediction Confidence Scores

🎯 Objective  

Capture and store model confidence (probabilities) for every prediction so we can:  

- Monitor model certainty
- Detect drift/anomalies
- Build dashboards later

🧠 What does “confidence score” mean  

For most ML models:  

- Classification  
  - Output = probability per class

  - Example:
```ruby
</> JSON

    {
      "prediction": 1,
      "confidence": 0.87
    }
```
- Binary classification (most common)
  - Use predict_proba()[1] (probability of positive class)
 
🏗️ Step 1: Update Prediction Logic (FastAPI)  

Inside our FastAPI app (/api/app.py):  

Before (likely)  
```ruby
</> python

prediction = model.predict(input_data)  
```

After (add confidence)  
```ruby
</> python

proba = model.predict_proba(input_data)[0]
prediction = int(proba.argmax())
confidence = float(max(proba))
```

🧾 Step 2: Return Confidence in API Response  

Update our response model:  
```ruby
</> python

return {
    "prediction": prediction,
    "confidence": confidence
}
```

🧠 Step 3: Log Predictions (CRITICAL for MLOps)  

Now the real value: log every request  

Simple logging (start here)  
```ruby
</> python

import logging

logging.basicConfig(level=logging.INFO)

logging.info({
    "prediction": prediction,
    "confidence": confidence
})
```

🚀 Step 4: Structured Logging  

Instead of plain logs, use structured JSON logs:  
```ruby
</> python

import json
from datetime import datetime

log_data = {
    "timestamp": datetime.utcnow().isoformat(),
    "prediction": prediction,
    "confidence": confidence
}

logging.info(json.dumps(log_data))
```

☁️ Step 5: Send Logs to Vertex AI / Cloud Logging  

Since we're using Vertex AI:  

**Option A (quick win)**
  - Logs automatically go to Cloud Logging if deployed on:
    - Cloud Run
    - Vertex AI Endpoint (custom container)

**Option B (explicit logging client)**  
```ruby
</> python

from google.cloud import logging as cloud_logging

client = cloud_logging.Client()
client.setup_logging()
```
Now logs appear in:  
👉 Google Cloud → Logging → Logs Explorer  

📊 Step 6: (Optional) Save to BigQuery

Instead of just logging:
```ruby
</> python

from google.cloud import bigquery

client = bigquery.Client()

table_id = "your_project.dataset.predictions"

rows_to_insert = [{
    "timestamp": datetime.utcnow().isoformat(),
    "prediction": prediction,
    "confidence": confidence
}]

client.insert_rows_json(table_id, rows_to_insert)
```

🧪 Step 7: Test Our API  

Example request:  
```ruby
</> bash

curl -X POST http://localhost:8000/predict \
-H "Content-Type: application/json" \
-d '{"feature1": 5.1, "feature2": 3.5}'
```

Expected response:  
```ruby
</> JSON

{
  "prediction": 1,
  "confidence": 0.92
}
```

🔥 Pro Tips (High Impact)
  - Flag low-confidence predictions:
```ruby
</> python

if confidence < 0.6:
    logging.warning("Low confidence prediction detected")
```
  - Store input features + prediction + confidence
    - → This enables:
      - Drift detection 
      - Monitoring dashboards 
     
✅ Deliverables  

We should now have:
```
✅ API returns confidence score
✅ Structured logs implemented
✅ Logs visible in Cloud Logging
✅ (Optional) BigQuery table storing predictions
```
