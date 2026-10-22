import pickle
import numpy as np
import pandas as pd
import os

# Get the base directory (fraud_detection_project folder)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load the trained model
with open(os.path.join(BASE_DIR, 'best_model_xgboost.pkl'), 'rb') as f:
    model = pickle.load(f)

# Only read the column names, not the full CSV (saves memory!)
df_cols = pd.read_csv(os.path.join(BASE_DIR, 'cleaned_fraud_data.csv'), nrows=1)
feature_cols = [col for col in df_cols.columns if col not in ['isFraud', 'TransactionID']]

def predict_fraud(transaction: dict):
    input_df = pd.DataFrame([transaction])
    
    for col in feature_cols:
        if col not in input_df.columns:
            input_df[col] = -999
    
    input_df = input_df[feature_cols]
    
    pred = model.predict(input_df)[0]
    prob = model.predict_proba(input_df)[0][1]
    
    return {
        "is_fraud": int(pred),
        "fraud_probability": round(float(prob), 4)
    }