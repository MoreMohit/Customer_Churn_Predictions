import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load sample churn dataset (or use your real dataset)
data = pd.read_csv("WA_Fn-UseC_-Telco-Customer-Churn.csv")  # Replace with actual dataset

st.title("📊 Churn Data Analysis")

# Show dataset
if st.checkbox("🔍 Show Raw Data"):
    st.write(data.head())

# Correlation Heatmap
st.subheader("📈 Correlation Matrix")

plt.figure(figsize=(10, 6))
sns.heatmap(data.corr(), annot=True, cmap="coolwarm", fmt=".2f")
st.pyplot(plt)

# Feature Importance (if model trained with feature importance)
if "churn_prediction_model.pkl":
    import joblib
    model = joblib.load("churn_prediction_model.pkl")

    if hasattr(model, "feature_importances_"):
        st.subheader("🔍 Feature Importance")

        feature_names = ["Tenure", "Monthly Charges", "Senior Citizen", "Contract Type", "Payment Method"]
        feature_importance = model.feature_importances_

        fig, ax = plt.subplots()
        sns.barplot(x=feature_importance, y=feature_names, palette="coolwarm", ax=ax)
        ax.set_xlabel("Importance Score")
        ax.set_title("Feature Importance")

        st.pyplot(fig)
