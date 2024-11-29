import streamlit as st
import pandas as pd
import pickle
import numpy as np

# Load the saved Random Forest model and label encoders
with open('rf_model.pkl', 'rb') as model_file:
    rf_model = pickle.load(model_file)
#Label Encoder Model
with open('label_encoders.pkl', 'rb') as encoder_file:
    label_encoders = pickle.load(encoder_file)

# Streamlit app title
st.title("Optimization of Bonous Allocation App")

st.markdown("""
This application predicts the optimal bonus for customers based on their spending behavior, demographics, and activity.
""")

# Sidebar for user input
st.sidebar.header("Customer Data Input")

#Function to take the inputs from the user
def user_input_features():
    age = st.sidebar.slider("Age", 18, 70, 40)
    income_level = st.sidebar.selectbox("Income Level", ["Low", "Medium", "High"])
    days_since_last_purchase = st.sidebar.slider("Days Since Last Purchase", 0, 365, 30)
    active_days = st.sidebar.slider("Active Days (last year)", 30, 365, 200)
    total_number_of_purchases = st.sidebar.slider("Total Purchases", 100, 5000, 500)
    total_amount_spent = st.sidebar.slider("Total Amount Spent", 500, 50000, 10000)
    avg_amount_spent = st.sidebar.slider("Average Amount Spent per Purchase", 0, 1000, 200)
    days_since_first_purchase = st.sidebar.slider("Days Since First Purchase", 1, 1000, 500)
    purchase_frequency = st.sidebar.slider("Purchase Frequency", 0.5, 2.0, 1.0)
    last_purchase_amount = st.sidebar.slider("Last Purchase Amount", 50, 5000, 300)
    seasonal_purchase_behavior = st.sidebar.selectbox("Seasonal Purchase Behavior", [0, 1])
    refunds = st.sidebar.slider("Number of Refunds", 0, 5, 1)
    location = st.sidebar.selectbox("Location", ["Urban", "Suburban", "Rural"])

    data = {
        "age": age,
        "income_level": income_level,
        "days_since_last_purchase": days_since_last_purchase,
        "active_days": active_days,
        "total_number_of_purchases": total_number_of_purchases,
        "total_amount_spent": total_amount_spent,
        "avg_amount_spent": avg_amount_spent,
        "days_since_first_purchase": days_since_first_purchase,
        "purchase_frequency": purchase_frequency,
        "last_purchase_amount": last_purchase_amount,
        "seasonal_purchase_behavior": seasonal_purchase_behavior,
        "refunds": refunds,
        "location": location,
    }
    return pd.DataFrame(data, index=[0])

# User input
input_data = user_input_features()

# Display input data
#st.subheader("User Input Data")
#st.write(input_data)

# Encode the  categorical variables
for col in ['income_level', 'location']:
    if col in label_encoders:
        input_data[col] = label_encoders[col].transform(input_data[col])

# Make predictions
prediction = rf_model.predict(input_data)

# Display prediction
st.subheader("Predicted Bonus Amount")
if st.button("Predict"):
    st.write(f"${prediction[0]:,.2f}")
