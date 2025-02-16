import streamlit as st
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load trained model
model = joblib.load("churn_prediction_model.pkl")

# Streamlit App
st.title("🔮 Customer Churn Prediction App")

st.write("Enter customer details below to predict churn probability.")

# Collect user input
tenure = st.number_input("Tenure (months)", min_value=0, max_value=72, value=12)
monthly_charges = st.number_input("Monthly Charges ($)", min_value=0.0, max_value=200.0, value=50.0)
senior_citizen = st.selectbox("Senior Citizen", [0, 1])
contract_type = st.selectbox("Contract Type", ["Month-to-Month", "One Year", "Two Year"])
payment_method = st.selectbox("Payment Method", ["Electronic Check", "Mailed Check", "Bank Transfer", "Credit Card"])

# Convert categorical inputs into numeric features
contract_mapping = {"Month-to-Month": 0, "One Year": 1, "Two Year": 2}
payment_mapping = {"Electronic Check": 0, "Mailed Check": 1, "Bank Transfer": 2, "Credit Card": 3}

contract_encoded = contract_mapping[contract_type]
payment_encoded = payment_mapping[payment_method]

# Create input array
user_data = np.array([[tenure, monthly_charges, senior_citizen, contract_encoded, payment_encoded]])

# Predict churn
if st.button("Predict Churn"):
    prediction = model.predict(user_data)
    probability = model.predict_proba(user_data)[0][1] * 100

    if prediction == 1:
        st.error(f"🚨 High Risk! Churn Probability: {probability:.2f}%")
    else:
        st.success(f"✅ Low Risk! Churn Probability: {probability:.2f}%")

# Feature Importance
st.subheader("🔍 Feature Importance")
feature_names = ["Tenure", "Monthly Charges", "Senior Citizen", "Contract Type", "Payment Method"]
feature_importance = model.feature_importances_

# Plot feature importance
fig, ax = plt.subplots()
sns.barplot(x=feature_importance, y=feature_names, ax=ax)
ax.set_xlabel("Importance Score")
ax.set_title("Feature Importance")

st.pyplot(fig)

# Run with: streamlit run apps.py
