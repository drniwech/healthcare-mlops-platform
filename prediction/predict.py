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

    # Convert to model-ready features
    processed_input = build_features(raw_input)

    # Call endpoint
    prediction = predict(processed_input)

    print("Prediction:", prediction)

