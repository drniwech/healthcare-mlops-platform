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
```ruby
patient_id,age,gender,num_procedures,num_medications,diagnosis,days_in_hospital,readmitted
1,72,M,3,12,Diabetes,7,1
2,58,F,2,8,Hypertension,4,0
3,81,M,4,15,Heart Failure,9,1
4,45,F,1,6,Asthma,2,0
5,67,M,3,11,Pneumonia,6,1
6,39,F,2,7,Arthritis,3,0
7,74,M,5,14,Diabetes,8,0
8,52,F,1,9,Hypertension,5,1
9,88,M,4,13,Heart Failure,10,1
10,61,F,2,8,Kidney Disease,4,0
11,49,M,3,10,COPD,6,0
12,76,F,1,11,Diabetes,7,1
13,55,M,4,12,Hypertension,3,0
14,82,F,2,9,Heart Failure,8,1
15,43,M,3,7,Asthma,2,0
16,69,F,5,14,Pneumonia,9,1
17,37,M,1,6,Arthritis,4,0
18,79,F,4,13,Diabetes,6,1
19,64,M,2,10,Hypertension,5,0
20,51,F,3,8,Heart Failure,7,1
21,85,M,4,15,Kidney Disease,10,0
22,48,F,2,9,COPD,3,0
23,73,M,1,11,Diabetes,8,1
24,59,F,3,12,Hypertension,4,0
25,77,M,5,14,Heart Failure,9,1
26,44,F,2,7,Asthma,2,0
27,68,M,4,13,Pneumonia,6,1
28,56,F,1,8,Arthritis,5,0
29,83,M,3,10,Diabetes,7,1
30,62,F,2,11,Hypertension,4,0
31,50,M,4,9,Heart Failure,8,1
32,80,F,3,12,Kidney Disease,5,0
33,47,M,1,6,COPD,3,0
34,71,F,5,14,Diabetes,9,1
35,54,M,2,10,Hypertension,6,0
36,86,F,4,13,Heart Failure,10,1
37,41,M,3,8,Asthma,2,0
38,75,F,1,11,Pneumonia,7,1
39,66,M,2,9,Arthritis,4,0
40,53,F,4,12,Diabetes,5,1
41,78,M,3,14,Hypertension,8,0
42,60,F,5,10,Heart Failure,9,1
43,46,M,2,7,Kidney Disease,3,0
44,84,F,1,11,COPD,6,1
45,70,M,4,13,Diabetes,7,0
46,57,F,3,9,Hypertension,4,1
47,81,M,2,12,Heart Failure,8,1
48,38,F,1,6,Asthma,2,0
49,65,M,5,15,Pneumonia,10,1
50,63,F,4,11,Arthritis,5,0
51,52,M,3,10,Diabetes,6,1
52,87,F,2,8,Hypertension,4,0
53,44,M,1,9,Heart Failure,3,0
54,79,F,4,13,Kidney Disease,7,1
55,59,M,3,12,COPD,5,0
56,74,F,2,14,Diabetes,9,1
57,48,M,5,10,Hypertension,6,0
58,82,F,1,7,Heart Failure,8,1
59,67,M,4,11,Asthma,4,0
60,55,F,3,9,Pneumonia,5,1
61,40,M,2,8,Arthritis,3,0
62,76,F,1,12,Diabetes,7,1
63,61,M,4,13,Hypertension,4,0
64,50,F,3,10,Heart Failure,6,1
65,85,M,2,11,Kidney Disease,9,0
66,53,F,5,14,COPD,5,0
67,72,M,1,8,Diabetes,8,1
68,58,F,4,12,Hypertension,3,0
69,46,M,3,9,Heart Failure,7,1
70,81,F,2,10,Asthma,2,0
71,64,M,1,13,Pneumonia,6,1
72,49,F,5,11,Arthritis,4,0
73,77,M,4,14,Diabetes,9,1
74,56,F,2,7,Hypertension,5,0
75,83,M,3,12,Heart Failure,8,1
76,42,F,1,6,Kidney Disease,3,0
77,68,M,4,10,COPD,6,0
78,51,F,3,13,Diabetes,7,1
79,86,M,2,9,Hypertension,4,1
80,60,F,5,11,Heart Failure,10,0
81,45,M,1,8,Asthma,2,0
82,73,F,4,14,Pneumonia,9,1
83,54,M,3,12,Arthritis,5,0
84,80,F,2,10,Diabetes,6,1
85,62,M,1,13,Hypertension,4,0
86,39,F,4,9,Heart Failure,7,1
87,75,M,3,11,Kidney Disease,8,0
88,57,F,2,8,COPD,3,0
89,84,M,5,14,Diabetes,9,1
90,66,F,1,7,Hypertension,5,0
91,47,M,4,12,Heart Failure,6,1
92,78,F,3,10,Asthma,4,0
93,69,M,2,13,Pneumonia,7,1
94,55,F,1,9,Arthritis,3,0
95,82,M,4,11,Diabetes,8,1
96,63,F,3,12,Hypertension,5,0
97,50,M,2,10,Heart Failure,4,1
98,87,F,5,14,Kidney Disease,9,0
99,71,M,1,8,COPD,6,0
100,59,F,4,13,Diabetes,7,1
```

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
Format: `CSV`   
Schema: `Auto-detect (for now)`  
Table name: `patient_data`  

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

