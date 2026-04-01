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
