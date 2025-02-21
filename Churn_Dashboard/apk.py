import streamlit as st
import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

# 🎨 Apply Custom Theme
st.set_page_config(
    page_title="Customer Churn Prediction",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Model
with open("Customer_Churn_Predictions_models.pkl", "rb") as f:
    model = pickle.load(f)

# Get feature names
model_features = model.feature_names_in_

# Sidebar Navigation
st.sidebar.markdown("## 📌 Navigation")
page = st.sidebar.radio("", ["🏠 Home", "📊 Predict Churn", "📈 Insights"])

# ✨ Custom Styling
st.markdown(
    """
    <style>
    .big-font { font-size:25px !important; font-weight: bold; }
    .sidebar .sidebar-content { background-color: #f7f7f7; }
    .css-1aumxhk { background-color: #F0F2F6; }
    .stButton>button { border-radius:10px; background-color:#4CAF50; color:white; }
    </style>
    """, unsafe_allow_html=True
)

# Home Page
if page == "🏠 Home":
    st.markdown("<h1 class='big-font'>📊 Customer Churn Prediction Dashboard</h1>", unsafe_allow_html=True)
    st.write("Use this AI-powered tool to analyze and predict customer churn.")
    st.image("churn.jpg", use_container_width=True)  # Add a banner image

# Prediction Page
elif page == "📊 Predict Churn":
    st.markdown("<h2 class='big-font'>🔍 Predict Customer Churn</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        tenure = st.slider("📆 Tenure (Months)", 0, 72, 12)
        MonthlyCharges = st.slider("💰 Monthly Charges", 0, 120, 50)
        TotalCharges = st.slider("💳 Total Charges", 0, 9000, 3000)
        SeniorCitizen = st.radio("👴 Senior Citizen?", ["No", "Yes"])
    with col2:
        Contract = st.selectbox("📜 Contract Type", ["Month-to-month", "One year", "Two year"])
        PaymentMethod = st.selectbox("💳 Payment Method", ["Electronic check", "Mailed check", "Bank transfer"])
        PaperlessBilling = st.radio("📑 Paperless Billing?", ["No", "Yes"])

    CLV = MonthlyCharges * tenure  # Customer Lifetime Value

    # Prepare Data for Prediction
    user_data = pd.DataFrame({
        "tenure": [tenure],
        "MonthlyCharges": [MonthlyCharges],
        "TotalCharges": [TotalCharges],
        "SeniorCitizen": [1 if SeniorCitizen == "Yes" else 0],
        "Contract": [Contract],
        "PaymentMethod": [PaymentMethod],
        "PaperlessBilling": [1 if PaperlessBilling == "Yes" else 0],
        "CLV": [CLV]
    })
    user_data = pd.get_dummies(user_data)
    for col in model_features:
        if col not in user_data.columns:
            user_data[col] = 0  # Fill missing features
    user_data = user_data[model_features]

    # Predict Button
    if st.button("🚀 Predict Churn"):
        prediction = model.predict(user_data)[0]
        probability = model.predict_proba(user_data)[0][1] * 100

        if prediction == 1:
            st.error(f"⚠️ High Risk! Churn Probability: {probability:.2f}%")
        else:
            st.success(f"✅ Low Risk! Churn Probability: {probability:.2f}%")

        # Feature Importance (Tree-based)
        feature_importance = model.feature_importances_
        importance_df = pd.DataFrame({"Feature": model_features, "Importance": feature_importance})
        importance_df = importance_df.sort_values(by="Importance", ascending=False)

        # 📊 Display Feature Importance
        st.subheader("🔎 Feature Importance")
        fig = px.bar(importance_df, x="Importance", y="Feature", orientation="h", title="Feature Importance",
                     color="Importance", color_continuous_scale="blues")
        st.plotly_chart(fig, use_container_width=True)

# Insights Page
elif page == "📈 Insights":
    st.markdown("<h2 class='big-font'>📈 Churn Analysis & Feature Importance</h2>", unsafe_allow_html=True)

    # 📌 Feature Importance Plot (Tree-Based)
    feature_importance = model.feature_importances_
    importance_df = pd.DataFrame({"Feature": model_features, "Importance": feature_importance})
    importance_df = importance_df.sort_values(by="Importance", ascending=False)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(importance_df["Feature"], importance_df["Importance"], color="steelblue")
    ax.set_xlabel("Importance Score")
    ax.set_ylabel("Features")
    ax.set_title("Feature Importance")
    st.pyplot(fig)

    # 📝 Key Takeaways
    st.write("### 🔹 Key Insights")
    st.write("- Customers with **higher Monthly Charges** are more likely to churn.")
    st.write("- Shorter **tenure periods** indicate a **higher churn rate**.")
    st.write("- **Electronic check payments** have a higher churn risk compared to other methods.")

