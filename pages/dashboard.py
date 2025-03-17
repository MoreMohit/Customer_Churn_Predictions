import streamlit as st
import pickle
import os
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import requests
from streamlit_lottie import st_lottie
from sklearn.preprocessing import StandardScaler

# 🎨 Streamlit Config
st.set_page_config(page_title="Customer Churn Dashboard", page_icon="📊", layout="wide")

# # 🔄 Load Model, Scaler & Features
# with open("Best_Model_Forest_new.pkl", "rb") as f:
#     model = pickle.load(f)

model_path = "/home/g22113014/Customer_Churn_Predictions/Best_Model_Forest_new.pkl"  # Correct path inside the container

if not os.path.exists(model_path):
    raise FileNotFoundError(f"❌ Model file not found at: {model_path}")

with open(model_path, "rb") as f:
    model = pickle.load(f)

with open("scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

with open("model_features.pkl", "rb") as f:
    model_features = pickle.load(f)

# Load Feature Importance
with open("feature_importance.pkl", "rb") as f:
    importance_df = pickle.load(f)

# 🎬 Load Lottie Animations
# 🎬 Load Lottie Animations
def load_lottie_url(url):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error loading Lottie animation: {e}")
        return None

# Load animations safely
success_animation = load_lottie_url("https://assets7.lottiefiles.com/packages/lf20_hy4txm7l.json")  
error_animation = load_lottie_url("https://assets3.lottiefiles.com/packages/lf20_kll8fwlm.json")  
insight_animation = load_lottie_url("https://assets2.lottiefiles.com/packages/lf20_u4yrau.json")  


# 🎨 Custom Styling
st.markdown(
    """
    <style>
    .stButton>button { border-radius:10px; background-color:#4CAF50; color:white; font-size:18px; padding:10px; }
    .stRadio > div { flex-direction:row; }
    .big-font { font-size:28px !important; font-weight: bold; }
    .stMetric { font-size:22px; font-weight:bold; color:#333; }
    </style>
    """,
    unsafe_allow_html=True
)

# 📌 Sidebar Navigation
st.sidebar.markdown("## 📌 Navigation")
page = st.sidebar.radio("Select a Page:", ["🏠 Home", "📊 Predict Churn", "📈 Insights"], label_visibility="collapsed")

# 🏠 **Home Page**
if page == "🏠 Home":
    st.markdown("<h1 class='big-font'>📊 Customer Churn Prediction Dashboard</h1>", unsafe_allow_html=True)
    
    total_customers = 5000
    churn_rate = 0.27  
    retention_rate = 1 - churn_rate
    
    col1, col2, col3 = st.columns(3)
    col1.metric("👥 Total Customers", total_customers)
    col2.metric("⚠️ Churn Rate", f"{churn_rate * 100:.1f}%")
    col3.metric("✅ Retention Rate", f"{retention_rate * 100:.1f}%")

    churn_data = pd.DataFrame({"Category": ["Churned", "Retained"], "Count": [churn_rate * total_customers, retention_rate * total_customers]})
    fig = px.pie(churn_data, values="Count", names="Category", title="Churn vs. Retention", color_discrete_sequence=["red", "green"])
    st.plotly_chart(fig, use_container_width=True)

# 🔍 **Prediction Page**
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

    CLV = MonthlyCharges * tenure  

    # 🛠️ Prepare Data for Prediction
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

    # 🔄 One-Hot Encoding & Fix Features
    encoded_data = pd.get_dummies(user_data)
    encoded_data = encoded_data.reindex(columns=model_features, fill_value=0)
    user_data = encoded_data.copy()

    # 📏 Scale Numerical Features
    numerical_features = ["tenure", "MonthlyCharges", "TotalCharges", "CLV"]
    user_data[numerical_features] = scaler.transform(user_data[numerical_features])

    # 🚀 Predict Button
    if st.button("🚀 Predict Churn"):
        churn_prob = model.predict_proba(user_data)[0][1] * 100  
        threshold = 50  

        prediction = 1 if churn_prob >= threshold else 0  

        if prediction == 1:
            st.error(f"⚠️ High Risk! Churn Probability: {churn_prob:.2f}%")
            st_lottie(error_animation, height=150, key="error_anim")
        else:
            st.success(f"✅ Low Risk! Churn Probability: {churn_prob:.2f}%")
            st_lottie(success_animation, height=150, key="success_anim")

         # 📊 **Churn Probability Visualization**
        st.subheader("📊 Churn Probability Breakdown")

        # **Gauge Chart for Probability**
        fig_gauge = px.bar(
            x=["Churn Probability"],
            y=[churn_prob],
            text=[f"{churn_prob:.2f}%"],
            color=[churn_prob],
            color_continuous_scale="reds",
            range_y=[0, 100],
            title="Predicted Churn Probability"
        )
        fig_gauge.update_traces(textposition="outside")
        fig_gauge.update_layout(yaxis_title="Probability (%)")
        st.plotly_chart(fig_gauge, use_container_width=True)

# 📈 **Insights Page**
elif page == "📈 Insights":
    st.markdown("<h2 class='big-font'>📈 Churn Analysis & Feature Importance</h2>", unsafe_allow_html=True)

    if hasattr(model, "feature_importances_"):
        feature_importance = model.feature_importances_
        importance_df = pd.DataFrame({"Feature": model_features, "Importance": feature_importance}).sort_values(by="Importance", ascending=False)

        # 📊 Top 5 Most Important Features
        st.subheader("🔎 Top 5 Factors Impacting Churn")
        top5_features = importance_df.head(5)
        fig = px.bar(top5_features, x="Importance", y="Feature", orientation="h", title="Top 5 Churn Risk Factors", color="Importance", color_continuous_scale="reds")
        st.plotly_chart(fig, use_container_width=True)

        # 📝 Key Takeaways
        st.markdown("### 📝 Key Takeaways")
        st.write("- **Higher Monthly Charges** → More likely to churn.")
        st.write("- **Shorter Tenure** → New users are more prone to leave.")
        st.write("- **Electronic Check Payments** → Customers using this method show higher churn rates.")
        st.write("- **No Internet Service** → Customers with fewer services tend to churn.")
