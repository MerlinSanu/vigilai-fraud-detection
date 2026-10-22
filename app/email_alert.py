import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Your Gmail credentials
SENDER_EMAIL = "merlin.sanu@btech.christuniversity.in"
APP_PASSWORD = "arat ycly hkwo wlux"
RECEIVER_EMAIL = "merlin.sanu@btech.christuniversity.in"

def send_fraud_alert(transaction_amount: float, fraud_probability: float):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "🚨 FRAUD ALERT — VigilAI Detection System"
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL

    html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background-color: #0a0a0a; color: #e0e0e0; padding: 20px;">
        <div style="max-width: 600px; margin: auto; background: #1a1a2e; border: 2px solid #D4AF37; border-radius: 12px; padding: 30px;">
            <h1 style="color: #D4AF37; text-align: center;">🛡️ VigilAI Fraud Detection</h1>
            <div style="background: #3d0000; border: 2px solid #ff4444; border-radius: 8px; padding: 20px; text-align: center; margin: 20px 0;">
                <h2 style="color: #ff4444;">🚨 FRAUDULENT TRANSACTION DETECTED</h2>
            </div>
            <table style="width: 100%; border-collapse: collapse;">
                <tr style="border-bottom: 1px solid #2a2a4a;">
                    <td style="padding: 12px; color: #888;">Transaction Amount</td>
                    <td style="padding: 12px; color: #D4AF37; font-weight: bold;">${transaction_amount:,.2f}</td>
                </tr>
                <tr style="border-bottom: 1px solid #2a2a4a;">
                    <td style="padding: 12px; color: #888;">Fraud Probability</td>
                    <td style="padding: 12px; color: #ff4444; font-weight: bold;">{fraud_probability*100:.1f}%</td>
                </tr>
                <tr>
                    <td style="padding: 12px; color: #888;">Status</td>
                    <td style="padding: 12px; color: #ff4444; font-weight: bold;">🚨 BLOCKED — Under Review</td>
                </tr>
            </table>
            <p style="color: #888; font-size: 0.85rem; text-align: center; margin-top: 20px;">
                This is an automated alert from VigilAI Fraud Detection System.<br>
                Please review this transaction immediately.
            </p>
        </div>
    </body>
    </html>
    """

    msg.attach(MIMEText(html, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        print("Fraud alert email sent successfully!")
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False