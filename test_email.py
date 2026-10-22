from app.email_alert import send_fraud_alert

result = send_fraud_alert(2000.00, 0.85)
print("Email sent:", result)