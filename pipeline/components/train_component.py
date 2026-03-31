from kfp.v2.dsl import component, Input, Output, Model, Dataset

@component
def train_op(
    input_data: Input[Dataset],
    model_output: Output[Model],
):
    import pandas as pd
    from sklearn.model_selection import train_test_split
    from xgboost import XGBClassifier
    import joblib

    df = pd.read_csv(input_data.path)

    X = df.drop(columns=["readmitted"])
    y = df["readmitted"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = XGBClassifier()
    model.fit(X_train, y_train)

    joblib.dump(model, model_output.path)
