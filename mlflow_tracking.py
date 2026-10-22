import mlflow
import mlflow.xgboost
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, f1_score, precision_score, recall_score
import xgboost as xgb
import os
mlflow.set_tracking_uri("sqlite:///mlflow.db")
# Load data
df = pd.read_csv('cleaned_fraud_data.csv')
X = df.drop(columns=['isFraud', 'TransactionID'])
y = df['isFraud']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

scale_pos_weight = (y_train == 0).sum() / (y_train == 1).sum()

# Start MLflow experiment
mlflow.set_experiment("Fraud Detection")

with mlflow.start_run(run_name="XGBoost_Final"):
    # Define parameters
    params = {
        "n_estimators": 200,
        "max_depth": 6,
        "learning_rate": 0.1,
        "scale_pos_weight": scale_pos_weight
    }

    # Train model
    model = xgb.XGBClassifier(**params, random_state=42, eval_metric='auc', n_jobs=-1)
    model.fit(X_train, y_train)

    # Get predictions
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    # Calculate metrics
    metrics = {
        "roc_auc": roc_auc_score(y_test, y_proba),
        "f1_score": f1_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred),
        "recall": recall_score(y_test, y_pred)
    }

    # Log everything to MLflow
    mlflow.log_params(params)
    mlflow.log_metrics(metrics)
    mlflow.xgboost.log_model(model, "model")

    print("=== MLflow Run Complete ===")
    for k, v in metrics.items():
        print(f"{k}: {v:.4f}")
    print("\nAll parameters and metrics logged to MLflow! ✅")