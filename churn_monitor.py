import pandas as pd
import time
import requests
import smtplib
from email.mime.text import MIMEText

# Email configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "mohitrmore14@gmail.com"
EMAIL_PASSWORD = "cqhl fktx mdwc iatp"  # Use App Password

# Function to send an email alert
def send_email(customer_id, churn_probability, features, retention_strategy):
    recipient_email = "khotshubham393@gmail.com"  # Change this
    subject = f"🚨 High Churn Risk Alert: Customer {customer_id}"
    
    message = f"""
    ALERT: High-risk customer detected!
    
    - Customer ID: {customer_id}
    - Churn Probability: {churn_probability:.2f}
    - Factors: {features}
    - Recommended Retention Strategies:
      {retention_strategy}
    """
    
    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = recipient_email

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, recipient_email, msg.as_string())
        server.quit()
        print(f"✅ Email alert sent for Customer {customer_id}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

# Churn Monitoring
CHURN_THRESHOLD = 0.7
POLL_INTERVAL = 60  

def check_new_customers():
    print("Checking for new customer data...")

    df = pd.read_csv("customer_data.csv")
    new_customers = df[df['checked'] == 0]

    for index, row in new_customers.iterrows():
        if row['churn_probability'] > CHURN_THRESHOLD:
            features = []
            if row['low_engagement']: features.append("Low engagement")
            if row['high_complaints']: features.append("High complaint rate")
            if row['delayed_payments']: features.append("Delayed payments")
            
            features_text = ", ".join(features)

            # Call API for retention strategies
            response = requests.post("https://genai-for-customer-churn-explanations.onrender.com/retention_strategy", json={"features": features_text})
            
            if response.status_code == 200:
                retention_strategy = response.json().get("retention_strategy", [])
                print(f"🚨 ALERT: High-risk customer {row['customer_id']}")
                print(f"   - Churn Probability: {row['churn_probability']:.2f}")
                print(f"   - Factors: {features_text}")
                print(f"   - Suggested Retention Strategy: {retention_strategy}\n")

                # Send email alert
                send_email(row['customer_id'], row['churn_probability'], features_text, retention_strategy)
            
            else:
                print(f"❌ Error calling API for customer {row['customer_id']}")

            # Mark customer as checked
            df.at[index, 'checked'] = 1

    df.to_csv("customer_data.csv", index=False)

# Run polling loop
while True:
    check_new_customers()
    time.sleep(POLL_INTERVAL)
