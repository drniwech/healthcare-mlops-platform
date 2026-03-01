## Problem Statement
Predict 30-day hospital readmission risk and monitor model trust, drift, and reliability in production.

### Define Target Variable
Binary classification:  
	•	1 = readmitted within 30 days  
	•	0 = not readmitted  

### Define Success Metrics
Model Metrics:  
	•	ROC-AUC ≥ 0.80 (goal)  
	•	Precision / Recall tradeoff documented  

MLOps Metrics:  
	•	Deployment automation  
	•	Drift detection alert  
	•	Versioned model registry  

Trust Metrics:  
	•	Confidence score distribution  
	•	SHAP explanation logging  
	•	Drift report generation  
