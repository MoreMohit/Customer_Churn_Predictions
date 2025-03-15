import os
import json
import base64
import google.auth
from google.cloud import secretmanager
import firebase_admin
from firebase_admin import credentials, auth, exceptions
import streamlit as st
from streamlit_extras.colored_header import colored_header
from streamlit_lottie import st_lottie
import requests

# ==================== 🔥 Securely Load Firebase Credentials ====================
def get_firebase_credentials():
    """Retrieves Firebase credentials securely from Google Secret Manager."""
    secret_name = os.getenv("FIREBASE_SECRET_NAME")  # Get secret name from app.yaml
    if not secret_name:
        raise ValueError("🔥 Firebase secret name not set!")

    # Authenticate with Google Cloud
    _, project = google.auth.default()
    client = secretmanager.SecretManagerServiceClient()
    secret_path = f"projects/{project}/secrets/{secret_name}/versions/latest"

    # Access the secret
    response = client.access_secret_version(name=secret_path)
    secret_payload = response.payload.data.decode("utf-8")  # Decode secret

    return json.loads(secret_payload)  # Convert to dictionary

# 🔐 Initialize Firebase Securely
if not firebase_admin._apps:
    firebase_creds = get_firebase_credentials()
    cred = credentials.Certificate(firebase_creds)
    firebase_admin.initialize_app(cred)

# ==================== 🎨 Streamlit UI Config ====================
st.set_page_config(page_title="Customer Churn Prediction", page_icon="🔑", layout="centered")

# ==================== 🎬 Load Lottie Animations ====================
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
login_animation = load_lottie_url("https://assets3.lottiefiles.com/packages/lf20_jcikwtux.json")  # Login animation
success_animation = load_lottie_url("https://assets7.lottiefiles.com/packages/lf20_hy4txm7l.json")  # Success animation

# ==================== 🔐 Login UI ====================
st.title("Customer Churn Prediction")

# UI Header
colored_header(label="🔐 Secure Login", color_name="blue-70")

# Show Login Animation
st_lottie(login_animation, height=200, key="login_animation")

# Login Form with improved layout
with st.form("login_form", clear_on_submit=False):
    email = st.text_input("📧 Email", placeholder="Enter your email")
    password = st.text_input("🔑 Password", type="password", placeholder="Enter your password", help="Use your Firebase-registered password", key="password")
    login_btn = st.form_submit_button("Login 🚀")

# ==================== 🔐 Authentication Logic ====================
if login_btn:
    try:
        user = auth.get_user_by_email(email)
        st.success(f"🎉 Welcome, {user.email}!")

        # Show Success Animation
        st_lottie(success_animation, height=150, key="success_animation")

        # Store session (to persist login)
        st.session_state["user"] = user.email

        # Redirect to Dashboard
        st.switch_page("pages/dashboard.py")  

    except auth.UserNotFoundError:
        st.error("❌ User not found. Please check your email or register first.")
    except exceptions.FirebaseError as e:
        st.error(f"🔥 Authentication failed: {str(e)}")

# Redirect to Dashboard if Logged In
if "user" in st.session_state:
    st.info("✅ Redirecting to Dashboard...")
    st.switch_page("pages/dashboard.py")

# ==================== 🚀 Run Streamlit on Correct Port ====================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Default Google Cloud port
    #st.write(f"Starting Streamlit on port {port}...")
