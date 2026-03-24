## Load synthetic healthcare dataset into BigQuery  

Using:
```
Google Cloud Storage (data lake)
BigQuery (warehouse)
```

🧠 Step 0 — Choose Dataset  

Use a realistic but simple dataset.

Recommended:

Hospital Readmission Dataset (synthetic-like)

Use this structure:
```
patient_id,age,gender,num_procedures,num_medications,diagnosis,days_in_hospital,readmitted
1,65,M,2,10,Diabetes,5,1
2,50,F,1,5,Hypertension,3,0
```

👉 Keep it small (< 1 MB) to stay free.  

🚀 Step 1 — Create CSV Locally

Create file:
```
</> bash  
touch healthcare_data.csv
```
Paste ~100–500 rows (you can duplicate rows for now).  

☁️ Step 2 — Upload to Google Cloud Storage
```
</> bash  
gsutil cp healthcare_data.csv gs://healthcare-mlops-data/
```
Verify:
```
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
```
</> bash  
gs://healthcare-mlops-data/healthcare_data.csv
```
Format: CSV
Schema: Auto-detect (for now)

Click **Create Table**   

### Option B (CLI – more “engineer-level”)  
```
</> bash  
bq load \
--autodetect \
--source_format=CSV \
healthcare_ml.patient_data \
gs://healthcare-mlops-data/healthcare_data.csv
```

🔍 Step 4 — Validate Data

Run query:
```
</> SQL
SELECT *
FROM healthcare_ml.patient_data
LIMIT 10;
```
Check:

- Columns parsed correctly  
- No NULL issues  
- Data types look reasonable

  

