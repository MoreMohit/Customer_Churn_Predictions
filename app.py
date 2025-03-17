# import streamlit as st
# import os

# # Force Streamlit to use the correct port and address
# os.environ["STREAMLIT_SERVER_PORT"] = "8080"
# os.environ["STREAMLIT_SERVER_ADDRESS"] = "0.0.0.0"



# # ==================== 🎨 Streamlit UI Config ====================
# st.set_page_config(page_title="Customer Churn Prediction", page_icon="🔑", layout="centered")


# import firebase_admin
# from firebase_admin import credentials, auth, exceptions
# import json
# from streamlit_extras.colored_header import colored_header
# from streamlit_lottie import st_lottie
# import requests
# import base64



# # # 🔥 Load Firebase Credentials from Streamlit Secrets
# # firebase_creds_base64 = st.secrets["firebase"]["credentials_base64"]
# # firebase_creds_json = json.loads(base64.b64decode(firebase_creds_base64).decode())

# # # 🔐 Initialize Firebase
# # if not firebase_admin._apps:
# #     cred = credentials.Certificate(firebase_creds_json)
# #     firebase_admin.initialize_app(cred)

# # 🔥 Load Firebase Credentials from Streamlit Secrets
# if "firebase" in st.secrets:
#     firebase_creds_base64 = st.secrets["firebase"]["credentials_base64"]
#     firebase_creds_json = json.loads(base64.b64decode(firebase_creds_base64).decode())

#     # 🔐 Initialize Firebase
#     if not firebase_admin._apps:
#         cred = credentials.Certificate(firebase_creds_json)
#         firebase_admin.initialize_app(cred)
# else:
#     st.error("🔥 Firebase credentials missing! Add them in Streamlit Cloud secrets.")
        
# # ==================== 🎬 Load Lottie Animations ====================
# def load_lottie_url(url):
#     """Loads Lottie animations from URL."""
#     try:
#         r = requests.get(url)
#         if r.status_code == 200:
#             return r.json()
#         else:
#             return None
#     except requests.exceptions.RequestException as e:
#         print(f"Error loading Lottie animation: {e}")
#         return None

# # Load animations safely
# login_animation = load_lottie_url("https://assets3.lottiefiles.com/packages/lf20_jcikwtux.json")  # Login animation
# success_animation = load_lottie_url("https://assets7.lottiefiles.com/packages/lf20_hy4txm7l.json")  # Success animation

# # ==================== 🔐 Login UI ====================
# st.title("Customer Churn Prediction")

# # UI Header
# colored_header(label="🔐 Secure Login", color_name="blue-70")

# # Show Login Animation
# st_lottie(login_animation, height=200, key="login_animation")

# # Login Form with improved layout
# with st.form("login_form", clear_on_submit=False):
#     email = st.text_input("📧 Email", placeholder="Enter your email")
#     password = st.text_input(
#         "🔑 Password",
#         type="password",
#         placeholder="Enter your password",
#         help="Use your Firebase-registered password",
#         key="password"
#     )
#     login_btn = st.form_submit_button("Login 🚀")

# # ==================== 🔐 Authentication Logic ====================
# if login_btn:
#     try:
#         user = auth.get_user_by_email(email)
#         st.success(f"🎉 Welcome, {user.email}!")

#         # Show Success Animation
#         st_lottie(success_animation, height=150, key="success_animation")

#         # Store session (to persist login)
#         #st.session_state["user"] = user.email

#         # # Placeholder for page switch (Streamlit does not support direct navigation)
#         # st.info("✅ Redirecting to Dashboard... Please select 'Dashboard' from the sidebar.")

#         # Store session (to persist login)
#         st.session_state["user"] = user.email
#         st.switch_page("dashboard.py")
        

#     except auth.UserNotFoundError:
#         st.error("❌ User not found. Please check your email or register first.")
#     except exceptions.FirebaseError as e:
#         st.error(f"🔥 Authentication failed: {str(e)}")

# # # ==================== 🚀 Run Streamlit on Correct Port ====================
# # if __name__ == "__main__":
# #     port = int(os.environ.get("PORT", 8080))  # Default Google Cloud Run port
# #     os.system(f"streamlit run app.py --server.port={port} --server.address=0.0.0.0")



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
