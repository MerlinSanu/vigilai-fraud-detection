from fastapi import FastAPI
from pydantic import BaseModel
from app.model import predict_fraud
from app.email_alert import send_fraud_alert

app = FastAPI(title="VigilAI Fraud Detection API")

class Transaction(BaseModel):
    TransactionAmt: float
    email_risk_score: float = 3.5
    card1_avg_amt: float = 100.0
    card1_txn_count: float = 10.0
    amt_diff_from_avg: float = 0.0
    amt_ratio_to_avg: float = 1.0
    hour: float = 12.0

@app.get("/")
def home():
    return {"message": "VigilAI Fraud Detection API is running!"}

@app.post("/predict")
def predict(transaction: Transaction):
    result = predict_fraud(transaction.dict())
    fraud_prob = result["fraud_probability"]
    is_fraud = 1 if fraud_prob >= 0.65 else 0

    # Send email alert if fraud detected
    if is_fraud == 1:
        send_fraud_alert(
            transaction_amount=transaction.TransactionAmt,
            fraud_probability=fraud_prob
        )

    return {
        "transaction_amount": transaction.TransactionAmt,
        "is_fraud": is_fraud,
        "fraud_probability": fraud_prob,
        "verdict": "🚨 FRAUD DETECTED" if is_fraud == 1 else "✅ LEGITIMATE"
    }