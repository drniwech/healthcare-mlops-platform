## 2. Load synthetic healthcare dataset into BigQuery  

Using:
```
- Google Cloud Storage (data lake)
- BigQuery (warehouse)
```

🧠 Step 0 — Choose Dataset  

Use a realistic but simple dataset.

Recommended:

Hospital Readmission Dataset (synthetic-like)

Use this structure:
```ruby
patient_id,age,gender,num_procedures,num_medications,diagnosis,days_in_hospital,readmitted
1,65,M,2,10,Diabetes,5,1
2,50,F,1,5,Hypertension,3,0
```

👉 Keep it small (< 1 MB) to stay free.  

👉 Kaggle's Synthetic Healthcare Dataset:
```
https://www.kaggle.com/datasets/divyabhavana/synthetic-healthcare-dataset
```

🚀 Step 1 — Create CSV Locally

Create file:
```ruby
</> bash  
touch healthcare_data.csv
```
Paste ~100–500 rows (you can duplicate rows for now).  

☁️ Step 2 — Upload to Google Cloud Storage
```ruby
</> bash  
gsutil cp healthcare_data.csv gs://healthcare-mlops-data/
```
Verify:
```ruby
</> bash  
gsutil ls gs://healthcare-mlops-data/
```
🏗 Step 3 — Create a Table in BigQuery  
### Option A (UI – fastest)
1. Go to BigQuery Console
2. Select dataset: healthcare_ml
3. Click Create Table

Fill:

Source: **Google Cloud Storage**
File path:
```ruby
</> bash  
gs://healthcare-mlops-data/healthcare_data.csv
```
Format: CSV
Schema: Auto-detect (for now)

Click **Create Table**   

### Option B (CLI – more “engineer-level”)  
```ruby
</> bash  
bq load \
--autodetect \
--source_format=CSV \
healthcare_ml.patient_data \
gs://healthcare-mlops-data/healthcare_data.csv
```

🔍 Step 4 — Validate Data

Run query:
```ruby
</> SQL
SELECT *
FROM healthcare_ml.patient_data
LIMIT 10;
```
Check:

- Columns parsed correctly  
- No NULL issues  
- Data types look reasonable

🧪 Step 5 — Basic Data Profiling (Important)

Run:
```ruby
</> SQL
SELECT
  COUNT(*) AS total_rows,
  AVG(age) AS avg_age,
  AVG(num_medications) AS avg_meds,
  SUM(readmitted)/COUNT(*) AS readmission_rate
FROM healthcare_ml.patient_data;
```
This shows:

We understand data, not just pipelines  

🔧 Step 6 — Create Clean Feature Table

Don’t train directly on raw data.
```ruby
</> SQL
CREATE OR REPLACE TABLE healthcare_ml.features AS
SELECT
  age,
  num_procedures,
  num_medications,
  days_in_hospital,
  readmitted
FROM healthcare_ml.patient_data;
```

### Deliverable

We now have:
```
✔ Dataset in GCS
✔ Table in BigQuery
✔ Query working
✔ Feature table created
```

🧠 What We Just Built (Important)

We implemented:
```
Raw Data → GCS → BigQuery → Feature Table
```
This is exactly how real ML platforms work.

⚠️ Common Mistakes (Avoid These)
- Upload huge dataset → unnecessary cost
- Skip feature table → bad practice
- Wrong schema → breaks pipeline later

