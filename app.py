import streamlit as st
import os
import json
import pickle
import requests
import base64
import pandas as pd
import numpy as np
import plotly.express as px
import firebase_admin
from firebase_admin import credentials, auth, exceptions
from streamlit_lottie import st_lottie
from sklearn.preprocessing import StandardScaler

# ==================== 🎨 Streamlit UI Config ====================
st.set_page_config(page_title="Customer Churn Prediction", page_icon="📊", layout="wide")

# ==================== 🔥 Load Firebase Credentials ====================
if "firebase" in st.secrets:
    firebase_creds_base64 = st.secrets["firebase"]["credentials_base64"]
    firebase_creds_json = json.loads(base64.b64decode(firebase_creds_base64).decode())
    if not firebase_admin._apps:
        cred = credentials.Certificate(firebase_creds_json)
        firebase_admin.initialize_app(cred)
else:
    st.error("🔥 Firebase credentials missing! Add them in Streamlit Cloud secrets.")

# ==================== 🎬 Load Lottie Animations ====================
def load_lottie_url(url):
    try:
        r = requests.get(url)
        return r.json() if r.status_code == 200 else None
    except requests.exceptions.RequestException as e:
        print(f"Error loading Lottie animation: {e}")
        return None

login_animation = load_lottie_url("https://assets3.lottiefiles.com/packages/lf20_jcikwtux.json")
success_animation = load_lottie_url("https://assets7.lottiefiles.com/packages/lf20_hy4txm7l.json")
error_animation = load_lottie_url("https://assets3.lottiefiles.com/packages/lf20_kll8fwlm.json")

# ==================== 🔐 User Authentication ====================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Function to handle login
def login(email, password):
    try:
        user = auth.get_user_by_email(email)
        st.session_state.logged_in = True
        st.session_state.user_email = user.email
        st.success(f"🎉 Welcome, {user.email}!")
    except auth.UserNotFoundError:
        st.error("❌ User not found. Please check your email or register first.")
    except exceptions.FirebaseError as e:
        st.error(f"🔥 Authentication failed: {str(e)}")

# Function to handle logout
def logout():
    st.session_state.logged_in = False
    st.session_state.user_email = None

# ==================== 🔑 Login UI ====================
if not st.session_state.logged_in:
    st.title("Customer Churn Prediction")
    st_lottie(login_animation, height=200, key="login_animation")

    with st.form("login_form"):
        email = st.text_input("📧 Email", placeholder="Enter your email")
        password = st.text_input("🔑 Password", type="password", placeholder="Enter your password")
        login_btn = st.form_submit_button("Login 🚀")

    if login_btn:
        login(email, password)

# ==================== 🚀 Dashboard UI ====================
if st.session_state.logged_in:
    st.sidebar.markdown("## 📌 Navigation")
    page = st.sidebar.radio("Select a Page:", ["🏠 Home", "📊 Predict Churn", "📈 Insights"])

    # Logout Button in the Top-right Corner
    st.markdown(
        """
        <style>
        .logout-button { position: absolute; top: 15px; right: 20px; }
        </style>
        """,
        unsafe_allow_html=True
    )
    col1, col2 = st.columns([8, 1])
    with col2:
        if st.button("Logout 🚪"):
            logout()

    # Load Model & Scaler
    model_path = "Best_Model_Forest_new.pkl"
    scaler_path = "scaler.pkl"
    features_path = "model_features.pkl"

    if os.path.exists(model_path) and os.path.exists(scaler_path) and os.path.exists(features_path):
        with open(model_path, "rb") as f:
            model = pickle.load(f)
        with open(scaler_path, "rb") as f:
            scaler = pickle.load(f)
        with open(features_path, "rb") as f:
            model_features = pickle.load(f)
    else:
        st.error("❌ Model files not found. Please upload the required files.")

    # ==================== 📊 Home Page ====================
    if page == "🏠 Home":
        st.markdown("<h1>📊 Customer Churn Prediction Dashboard</h1>", unsafe_allow_html=True)

        churn_rate = 0.27
        retention_rate = 1 - churn_rate
        col1, col2, col3 = st.columns(3)
        col1.metric("👥 Total Customers", 5000)
        col2.metric("⚠️ Churn Rate", f"{churn_rate * 100:.1f}%")
        col3.metric("✅ Retention Rate", f"{retention_rate * 100:.1f}%")

        churn_data = pd.DataFrame({"Category": ["Churned", "Retained"], "Count": [churn_rate * 5000, retention_rate * 5000]})
        fig = px.pie(churn_data, values="Count", names="Category", title="Churn vs. Retention", color_discrete_sequence=["red", "green"])
        st.plotly_chart(fig, use_container_width=True)

    # ==================== 🔍 Predict Churn ====================
    elif page == "📊 Predict Churn":
        st.markdown("<h2>🔍 Predict Customer Churn</h2>", unsafe_allow_html=True)

        tenure = st.slider("📆 Tenure (Months)", 0, 72, 12)
        MonthlyCharges = st.slider("💰 Monthly Charges", 0, 120, 50)
        TotalCharges = st.slider("💳 Total Charges", 0, 9000, 3000)
        SeniorCitizen = st.radio("👴 Senior Citizen?", ["No", "Yes"])
        Contract = st.selectbox("📜 Contract Type", ["Month-to-month", "One year", "Two year"])
        PaymentMethod = st.selectbox("💳 Payment Method", ["Electronic check", "Mailed check", "Bank transfer"])
        PaperlessBilling = st.radio("📑 Paperless Billing?", ["No", "Yes"])

        CLV = MonthlyCharges * tenure  # Customer Lifetime Value

        # Prepare data for prediction
        user_data = pd.DataFrame({
            "tenure": [tenure], "MonthlyCharges": [MonthlyCharges], "TotalCharges": [TotalCharges],
            "SeniorCitizen": [1 if SeniorCitizen == "Yes" else 0], "Contract": [Contract],
            "PaymentMethod": [PaymentMethod], "PaperlessBilling": [1 if PaperlessBilling == "Yes" else 0], "CLV": [CLV]
        })
        encoded_data = pd.get_dummies(user_data).reindex(columns=model_features, fill_value=0)
        user_data = encoded_data.copy()
        user_data[["tenure", "MonthlyCharges", "TotalCharges", "CLV"]] = scaler.transform(user_data[["tenure", "MonthlyCharges", "TotalCharges", "CLV"]])

        if st.button("🚀 Predict Churn"):
            churn_prob = model.predict_proba(user_data)[0][1] * 100
            prediction = "High Risk!" if churn_prob >= 50 else "Low Risk!"
            st.success(f"{prediction} Churn Probability: {churn_prob:.2f}%")

    # ==================== 📈 Insights Page ====================
    elif page == "📈 Insights":
        st.markdown("<h2>📈 Churn Analysis & Feature Importance</h2>", unsafe_allow_html=True)

        feature_importance = model.feature_importances_
        importance_df = pd.DataFrame({"Feature": model_features, "Importance": feature_importance}).sort_values(by="Importance", ascending=False)

        fig = px.bar(importance_df.head(5), x="Importance", y="Feature", orientation="h", title="Top 5 Churn Risk Factors", color="Importance", color_continuous_scale="reds")
        st.plotly_chart(fig, use_container_width=True)
