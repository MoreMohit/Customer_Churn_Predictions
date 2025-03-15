import streamlit as st
import firebase_admin
from firebase_admin import auth, credentials, exceptions
from streamlit_extras.colored_header import colored_header
from streamlit_lottie import st_lottie
from PIL import Image
import requests

# Initialize Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("customerchurnprediction-f7a4c-firebase-adminsdk-fbsvc-7602b1226a.json")
    firebase_admin.initialize_app(cred)

# Page Config
st.set_page_config(page_title="Login", page_icon="🔑", layout="centered")

# Load Lottie Animation Function
def load_lottie_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Load Animations
login_animation = load_lottie_url("https://assets3.lottiefiles.com/packages/lf20_jcikwtux.json")  # User login animation
success_animation = load_lottie_url("https://assets7.lottiefiles.com/packages/lf20_hy4txm7l.json")  # Success animation

# # App Logo
# image = Image.open("churn.jpg")  # Ensure you have a logo file
# st.image(image, width=150)

# App Title
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

# Authentication Logic
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
