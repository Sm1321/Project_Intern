import streamlit as st
import pickle
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder

# Load the pre-trained model and encoder from pickle files
with open('random_forest_model.pkl', 'rb') as model_file, open('encoder.pkl', 'rb') as encoder_file:
    model = pickle.load(model_file)
    encoder = pickle.load(encoder_file)

# Streamlit title
st.title('Optimization of Bonous Allocation')

# Input fields for user to enter data
st.header('Input Data')

age = st.number_input('Age', min_value=18, max_value=100, value=30)
income_level = st.selectbox('Income Level', ['Low', 'Medium', 'High'])
days_since_last_purchase = st.number_input('Days Since Last Purchase', min_value=0, value=30)
active_days = st.number_input('Active Days', min_value=0, value=10)
total_number_of_purchases = st.number_input('Total Number of Purchases', min_value=0, value=5)
total_amount_spent = st.number_input('Total Amount Spent', min_value=0.0, value=100.0)
avg_amount_spent = st.number_input('Average Amount Spent', min_value=0.0, value=20.0)
location = st.selectbox('Location', ['Urban', 'Suburban', 'Rural'])

# Convert the input data into a format the model can work with
input_data = {
    'age': age,
    'income_level': income_level,
    'days_since_last_purchase': days_since_last_purchase,
    'active_days': active_days,
    'total_number_of_purchases': total_number_of_purchases,
    'total_amount_spent': total_amount_spent,
    'avg_amount_spent': avg_amount_spent,
    'location': location
}

input_df = pd.DataFrame([input_data])

# OneHotEncode the categorical columns using the same encoder
encoded_categorical = encoder.transform(input_df[['income_level', 'location']])
encoded_categorical_df = pd.DataFrame(encoded_categorical, columns=encoder.get_feature_names_out(['income_level', 'location']))

# Combine the original input with the encoded values
input_df = input_df.drop(columns=['income_level', 'location'])
input_df = pd.concat([input_df, encoded_categorical_df], axis=1)

# Prediction on user input
if st.button('Predict'):
    prediction = model.predict(input_df)
    st.write(f'Predicted Bonus Amount: ${prediction[0]:.2f}')
