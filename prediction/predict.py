from google.cloud import aiplatform
from config import PROJECT_ID, REGION, ENDPOINT_ID
from common.features import build_features


def predict(instance):
    aiplatform.init(project=PROJECT_ID, location=REGION)

    endpoint = aiplatform.Endpoint(
        endpoint_name=f"projects/{PROJECT_ID}/locations/{REGION}/endpoints/{ENDPOINT_ID}"
    )

    response = endpoint.predict(instances=[instance])
    predictions = response.predictions

    parsed_predictions = []
    parsed_confidences = []

    for p in predictions:
        # =========================
        # Case A: dict with scores
        # =========================
        if isinstance(p, dict) and "scores" in p:
            scores = p["scores"]
            pred_class = int(p.get("classes", list(range(len(scores))))[scores.index(max(scores))])
            confidence = float(max(scores))

        # =========================
        # Case B: list of probabilities
        # =========================
        elif isinstance(p, list):
            scores = p
            pred_class = int(scores.index(max(scores)))
            confidence = float(max(scores))

        # =========================
        # Fallback (regression or unknown)
        # =========================
        else:
            pred_class = int(p)
            confidence = None

        parsed_predictions.append(pred_class)
        parsed_confidences.append(confidence)

    return {
        "prediction": parsed_predictions,
        "confidence": parsed_confidences
    }


if __name__ == "__main__":
    raw_input = {
        "age": 65,
        "num_procedures": 2,
        "num_medications": 10,
        "days_in_hospital": 5
    }

    processed_input = build_features(raw_input)

    result = predict(processed_input)

    print("Prediction:", result["prediction"])
    print("Confidence:", result["confidence"])
