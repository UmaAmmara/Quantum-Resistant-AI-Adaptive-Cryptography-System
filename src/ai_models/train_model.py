"""
Member A — Day 3
Train a Random Forest classifier on dataset.csv to predict the best
algorithm to use, given system conditions (data size, latency, CPU load, etc).

This is the "brain" of the AI Optimization Layer described in the roadmap.
"""

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder
import joblib
import os

DATASET_PATH = os.path.join("data", "dataset.csv")
MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "ai_model.pkl")
ENCODER_PATH = os.path.join(MODEL_DIR, "algorithm_encoder.pkl")


def create_best_choice_labels(df: pd.DataFrame) -> pd.DataFrame:
    """
    The dataset's 'best_choice_label' column is currently empty — we fill it
    in now. For each unique combination of conditions (algorithm_type,
    data_size_bytes, network_condition), we label EVERY row in that group
    with the algorithm name that had the FASTEST time_taken_ms in that group
    (encryption rows compete with encryption rows, signature rows compete
    with signature rows).

    Implemented with transform() instead of groupby().apply() because apply()
    can silently drop the grouping columns in newer pandas versions, which
    caused the previous KeyError.
    """
    df = df.copy()

    # idxmin() of time_taken_ms within each group, broadcast back via transform
    def fastest_algorithm_in_group(sub_df_indices):
        # sub_df_indices is the integer index of rows in this group
        return None  # placeholder, unused — kept for clarity

    group_cols = ["algorithm_type", "data_size_bytes", "network_condition"]

    # For each row, find the algorithm with the minimum time_taken_ms within
    # its own group, and assign that as the label for every row in the group.
    idx_of_min = df.groupby(group_cols)["time_taken_ms"].idxmin()
    # idx_of_min maps each group -> the row index of the fastest algorithm
    group_to_best_algo = df.loc[idx_of_min.values, group_cols + ["algorithm"]]
    group_to_best_algo = group_to_best_algo.rename(columns={"algorithm": "best_choice_label"})

    # Merge that best-choice-per-group back onto every row of the original df
    df = df.drop(columns=["best_choice_label"], errors="ignore")
    df = df.merge(group_to_best_algo, on=group_cols, how="left")

    return df


def prepare_features(df: pd.DataFrame):
    """
    Selects and encodes the features the model will use to predict the
    best algorithm. Returns X (features), y (encoded labels), and the
    label encoder (needed later to decode predictions back to algorithm names).
    """
    # Only keep successful runs — failed runs shouldn't teach the model bad lessons
    df = df[df["success"] == 1].copy()

    feature_cols = ["data_size_bytes", "latency_ms", "cpu_load_percent",
                     "available_memory_mb"]

    # algorithm_type matters too (encryption vs signature have different
    # candidate algorithms), so we encode it as a feature
    type_encoder = LabelEncoder()
    df["algorithm_type_encoded"] = type_encoder.fit_transform(df["algorithm_type"])
    feature_cols.append("algorithm_type_encoded")

    X = df[feature_cols]

    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(df["best_choice_label"])

    return X, y, label_encoder, type_encoder, feature_cols


def train_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=150,
        max_depth=10,
        random_state=42,
        class_weight="balanced",  # helps if some algorithms win more often than others
    )
    model.fit(X_train, y_train)

    return model, X_test, y_test


def evaluate_model(model, X_test, y_test, label_encoder):
    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    print(f"\nAccuracy: {accuracy:.2%}")

    print("\n--- Classification report ---")
    target_names = label_encoder.classes_
    print(classification_report(y_test, y_pred, target_names=target_names, zero_division=0))

    print("\n--- Confusion matrix ---")
    print("Rows = actual, Columns = predicted")
    print("Labels order:", list(target_names))
    print(confusion_matrix(y_test, y_pred))

    return accuracy


def save_model(model, label_encoder, type_encoder, feature_cols):
    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump({
        "model": model,
        "label_encoder": label_encoder,
        "type_encoder": type_encoder,
        "feature_cols": feature_cols,
    }, MODEL_PATH)
    print(f"\nModel saved to {MODEL_PATH}")


def predict_best_algorithm(telemetry: dict, model_bundle_path: str = MODEL_PATH) -> str:
    """
    Example helper showing how Day 4's chat app will use this trained model.
    telemetry must contain: data_size_bytes, latency_ms, cpu_load_percent,
    available_memory_mb, algorithm_type ("encryption" or "signature")
    """
    bundle = joblib.load(model_bundle_path)
    model = bundle["model"]
    label_encoder = bundle["label_encoder"]
    type_encoder = bundle["type_encoder"]
    feature_cols = bundle["feature_cols"]

    type_encoded = type_encoder.transform([telemetry["algorithm_type"]])[0]

    row = pd.DataFrame([{
        "data_size_bytes": telemetry["data_size_bytes"],
        "latency_ms": telemetry["latency_ms"],
        "cpu_load_percent": telemetry["cpu_load_percent"],
        "available_memory_mb": telemetry["available_memory_mb"],
        "algorithm_type_encoded": type_encoded,
    }])[feature_cols]

    prediction_encoded = model.predict(row)[0]
    predicted_algorithm = label_encoder.inverse_transform([prediction_encoded])[0]
    return predicted_algorithm


if __name__ == "__main__":
    print("Loading dataset...")
    df = pd.read_csv(DATASET_PATH)
    print(f"Loaded {len(df)} rows")

    print("\nGenerating best_choice_label for each scenario...")
    df = create_best_choice_labels(df)

    # Save the labeled dataset back so Member B and Day 4 can reuse it
    df.to_csv(DATASET_PATH, index=False)
    print("Labeled dataset saved back to dataset.csv")

    print("\nPreparing features...")
    X, y, label_encoder, type_encoder, feature_cols = prepare_features(df)
    print(f"Features used: {feature_cols}")
    print(f"Possible labels (algorithms): {list(label_encoder.classes_)}")

    print("\nTraining Random Forest...")
    model, X_test, y_test = train_model(X, y)

    print("\nEvaluating model...")
    evaluate_model(model, X_test, y_test, label_encoder)

    save_model(model, label_encoder, type_encoder, feature_cols)

    # Quick sanity-check prediction
    print("\n--- Example prediction ---")
    example = {
        "data_size_bytes": 1024 * 1024,  # 1MB
        "latency_ms": 200,
        "cpu_load_percent": 70,
        "available_memory_mb": 2048,
        "algorithm_type": "encryption",
    }
    result = predict_best_algorithm(example, MODEL_PATH)
    print(f"For {example} -> recommended: {result}")