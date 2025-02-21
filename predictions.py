import streamlit as st
import joblib
import numpy as np

# Load trained model
model = joblib.load("churn_prediction_model.pkl")

st.title("🔮 Customer Churn Prediction")

st.write("Enter customer details below to predict churn probability.")

# User Inputs
tenure = st.slider("Tenure (months)", 0, 72, 12)
monthly_charges = st.slider("Monthly Charges ($)", 0.0, 200.0, 50.0)
senior_citizen = st.radio("Senior Citizen", [0, 1], horizontal=True)
contract_type = st.selectbox("Contract Type", ["Month-to-Month", "One Year", "Two Year"])
payment_method = st.selectbox("Payment Method", ["Electronic Check", "Mailed Check", "Bank Transfer", "Credit Card"])

# Encode categorical data
contract_mapping = {"Month-to-Month": 0, "One Year": 1, "Two Year": 2}
payment_mapping = {"Electronic Check": 0, "Mailed Check": 1, "Bank Transfer": 2, "Credit Card": 3}

contract_encoded = contract_mapping[contract_type]
payment_encoded = payment_mapping[payment_method]

# Create input array
user_data = np.array([[tenure, monthly_charges, senior_citizen, contract_encoded, payment_encoded]])

# Predict Churn
if st.button("🔍 Predict Churn"):
    prediction = model.predict(user_data)
    probability = model.predict_proba(user_data)[0][1] * 100

    st.subheader("📊 Prediction Result")
    if prediction == 1:
        st.error(f"🚨 High Risk! Churn Probability: {probability:.2f}%")
    else:
        st.success(f"✅ Low Risk! Churn Probability: {probability:.2f}%")
