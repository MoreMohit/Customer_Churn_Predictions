import streamlit as st
import os

# Force Streamlit to use the correct port and address
os.environ["STREAMLIT_SERVER_PORT"] = "8501"
os.environ["STREAMLIT_SERVER_ADDRESS"] = "0.0.0.0"



# ==================== 🎨 Streamlit UI Config ====================
st.set_page_config(page_title="Customer Churn Prediction", page_icon="🔑", layout="centered")


import firebase_admin
from firebase_admin import credentials, auth, exceptions
import json
from streamlit_extras.colored_header import colored_header
from streamlit_lottie import st_lottie
import requests
import base64



# ✅ Check if Streamlit Secrets contain Firebase credentials
if "firebase" in st.secrets and "credentials_base64" in st.secrets["firebase"]:
    try:
        # ✅ Load and Decode Base64 credentials
        firebase_creds_base64 = st.secrets["firebase"]["credentials_base64"]
        firebase_creds_json = json.loads(base64.b64decode(firebase_creds_base64).decode("utf-8"))

        # ✅ Initialize Firebase
        if not firebase_admin._apps:
            cred = credentials.Certificate(firebase_creds_json)
            firebase_admin.initialize_app(cred)

        st.success("🔥 Firebase initialized successfully!")

    except Exception as e:
        st.error(f"❌ Failed to initialize Firebase: {str(e)}")

else:
    st.error("❌ Firebase credentials missing! Please add them to `.streamlit/secrets.toml` or set them in Streamlit Cloud App Settings.")
        
# ==================== 🎬 Load Lottie Animations ====================
def load_lottie_url(url):
    """Loads Lottie animations from URL."""
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
    password = st.text_input(
        "🔑 Password",
        type="password",
        placeholder="Enter your password",
        help="Use your Firebase-registered password",
        key="password"
    )
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

        # Placeholder for page switch (Streamlit does not support direct navigation)
        st.info("✅ Redirecting to Dashboard... Please select 'Dashboard' from the sidebar.")

    except auth.UserNotFoundError:
        st.error("❌ User not found. Please check your email or register first.")
    except exceptions.FirebaseError as e:
        st.error(f"🔥 Authentication failed: {str(e)}")

# # ==================== 🚀 Run Streamlit on Correct Port ====================
# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 8080))  # Default Google Cloud Run port
#     os.system(f"streamlit run app.py --server.port={port} --server.address=0.0.0.0")
