# import streamlit as st
# import joblib
# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns

# # Set Custom Page Layout
# st.set_page_config(page_title="Customer Churn Prediction", page_icon="🔮", layout="wide")

# # Custom CSS for styling
# st.markdown("""
#     <style>
#         body {
#             background-color: #F5F7F8;
#         }
#         .stButton>button {
#             background-color: #007BFF;
#             color: white;
#             font-size: 18px;
#             border-radius: 10px;
#             padding: 10px 20px;
#         }
#         .stButton>button:hover {
#             background-color: #0056b3;
#         }
#         .stTitle {
#             text-align: center;
#             font-weight: bold;
#         }
#     </style>
# """, unsafe_allow_html=True)

# # Load trained model
# model = joblib.load("churn_prediction_model.pkl")

# # Sidebar for Navigation
# with st.sidebar:
#     st.image("https://upload.wikimedia.org/wikipedia/commons/8/89/Portrait_Placeholder.png", width=100)
#     st.title("🔮 Churn Prediction")
#     st.write("Enter customer details to predict churn.")

# # Main Section
# st.markdown("<h1 class='stTitle'>🔮 Customer Churn Prediction</h1>", unsafe_allow_html=True)

# # User Input Section
# col1, col2 = st.columns(2)

# with col1:
#     tenure = st.slider("Tenure (months)", 0, 72, 12)
#     monthly_charges = st.slider("Monthly Charges ($)", 0.0, 200.0, 50.0)

# with col2:
#     senior_citizen = st.radio("Senior Citizen", [0, 1], horizontal=True)
#     contract_type = st.selectbox("Contract Type", ["Month-to-Month", "One Year", "Two Year"])
#     payment_method = st.selectbox("Payment Method", ["Electronic Check", "Mailed Check", "Bank Transfer", "Credit Card"])

# # Convert categorical inputs into numeric features
# contract_mapping = {"Month-to-Month": 0, "One Year": 1, "Two Year": 2}
# payment_mapping = {"Electronic Check": 0, "Mailed Check": 1, "Bank Transfer": 2, "Credit Card": 3}

# contract_encoded = contract_mapping[contract_type]
# payment_encoded = payment_mapping[payment_method]

# # Create input array
# user_data = np.array([[tenure, monthly_charges, senior_citizen, contract_encoded, payment_encoded]])

# # Predict churn
# if st.button("🔍 Predict Churn"):
#     prediction = model.predict(user_data)
#     probability = model.predict_proba(user_data)[0][1] * 100

#     # Debugging: Print output
#     st.write(f"🔍 **Raw Model Output:** {prediction}")  # Check if it's 0 or 1
#     st.write(f"📊 **Churn Probability:** {probability:.2f}%")  # Check probability

#     st.subheader("📊 Prediction Result")
#     if prediction == 1:
#         st.error(f"🚨 High Risk! Churn Probability: {probability:.2f}%")
#     else:
#         st.success(f"✅ Low Risk! Churn Probability: {probability:.2f}%")

# # Feature Importance
# st.subheader("📊 Feature Importance")
# feature_names = ["Tenure", "Monthly Charges", "Senior Citizen", "Contract Type", "Payment Method"]
# feature_importance = model.feature_importances_

# # Plot feature importance
# fig, ax = plt.subplots()
# sns.barplot(x=feature_importance, y=feature_names, palette="coolwarm", ax=ax)
# ax.set_xlabel("Importance Score")
# ax.set_title("Feature Importance")

# st.pyplot(fig)

# # Run with: streamlit run apps.py



# import streamlit as st

# # Configure page layout
# st.set_page_config(page_title="Churn Dashboard", page_icon="📊", layout="wide")

# # Main Dashboard UI
# st.title("📊 Customer Churn Prediction Dashboard")
# st.write("Welcome to the customer churn prediction dashboard. Use the sidebar to navigate.")

# # Dashboard Overview
# st.markdown(
#     """
#     - 🔍 **Churn Prediction**: Predict if a customer is likely to churn.
#     - 📊 **Data Analysis**: Explore churn trends and key features.
#     """
# )

# # Sidebar Navigation
# st.sidebar.success("Select a page above to continue.")



# Develop a dashboard for churn insights (Streamlit)
# Streamlit code
import streamlit as st
import pickle
import joblib
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the trained model
with open("Customer_Churn_Predictions.pkl", "rb") as f:
    model = pickle.load(f)


    
# Define the Streamlit app
st.title("Customer Churn Prediction")

# Set Custom Page Layout
st.set_page_config(page_title="Customer Churn Prediction", page_icon=":bar_chart:", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
        body {
            background-color: #F5F7F8;
        }
        .stButton>button {
            background-color: #007BFF;
            color: white;
            font-size: 18px;
            border-radius: 10px;
            padding: 10px 20px;
        }
        .stButton>button:hover {
            background-color: #0056b3;
        }
        .stTitle {
            text-align: center;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar for Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Predict Churn"])

if page == "Home":
    st.title("Customer Churn Prediction")
    st.write("Welcome to the Customer Churn Prediction App!")
    st.write("Use the app to predict if a customer will churn or not.")

elif page == "Predict Churn":
    st.title("Predict Churn")


# User input
st.write("Please enter the customer details:")
tenure = st.number_input("Tenure", min_value=0)
MonthlyCharges = st.number_input("Monthly Charges", min_value=0)
TotalCharges = st.number_input("Total Charges", min_value=0)
SeniorCitizen = st.number_input("Senior Citizen", min_value=0, max_value=1)
Contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
PaymentMethod = st.selectbox("Payment Method", ["Electronic check", "Mailed check", "Bank transfer (automatic)"])
PaperlessBilling = st.selectbox("Paperless Billing", ["Yes", "No"])
CLV = MonthlyCharges * tenure

# Make predictions
if st.button("Predict Churn"):
    user_data = pd.DataFrame({
        "tenure": [tenure],
        "MonthlyCharges": [MonthlyCharges],
        "TotalCharges": [TotalCharges],
        "SeniorCitizen": [SeniorCitizen],
        "Contract": [Contract],
        "PaymentMethod": [PaymentMethod],
        "PaperlessBilling": [PaperlessBilling],
        "CLV": [CLV]
    })
    
    prediction = model.predict(user_data)
    probability = model.predict_proba(user_data)[0][1] * 100

    # Display results
    st.subheader("Prediction Result")
    if prediction == 1:
        st.error(f"High Risk! Churn Probability: {probability:.2f}%")
    else:
        st.success(f"Low Risk! Churn Probability: {probability:.2f}%")

# Run the app
if __name__ == "__main__":
    st.run()