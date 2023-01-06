
import numpy as np
import pickle
import pandas as pd
import streamlit as st
#import xgboost
from xgboost import XGBRegressor
#from PIL import Image


# Loading Regression model
pickle_in = open("Final_model.pkl", "rb")
model = pickle.load(pickle_in)

# Loading scaler
pickle_in = open("Scaling_features.pkl", "rb")
scaler = pickle.load(pickle_in)

# Caching the model for faster loading
@st.cache

# Define the prediction function
def predict(city, purpose, visit, length_stay, travel_type, gender, main_acc, hotel, travel_path, comp_num, month, weight, shop_exp):
    # Predicting the travel expense
    d = {'Weights_QTR': [weight], 'shopping_exp': [shop_exp]}
    df = pd.DataFrame(data=d)
    r = scaler.fit_transform(df)
    weight = r[0][0]
    shop_exp = r[0][1]

    if city == 'Yogyakarta':
        city = 9
    elif city == 'Batam':
        city = 2
    elif city == 'Other cities':
        city = 5
    elif city == 'Tanjung Pinang':
        city = 8
    elif city == 'Jakarta':
        city = 3
    elif city == 'Surabaya':
        city = 6
    elif city == 'Bandung':
        city = 1
    elif city == 'Medan':
        city = 4
    elif city == 'Bali':
        city = 0
    elif city == 'Tanjung Balai':
        city = 7


    if purpose == 'Leisure':
        purpose = 3
    elif purpose == 'Others':
        purpose = 4
    elif purpose == 'Healthcare':
        purpose = 2
    elif purpose == 'Business':
        purpose = 0
    elif purpose == 'Education':
        purpose = 1


    if visit == 'No':
        visit = 0
    elif visit == 'Yes':
        visit = 1


    if travel_type == 'Non-Packaged':
        travel_type = 1
    elif travel_type == 'Packaged':
        travel_type = 2
    elif travel_type == 'Business (Non-Packaged)':
        travel_type = 0


    if gender == 'Male':
        gender = 1
    elif gender == 'Female':
        gender = 0


    if main_acc == 'Hotel':
        main_acc = 2
    elif main_acc == 'Accomodation not required':
        main_acc = 0
    elif main_acc == 'Hostel':
        main_acc = 1
    elif main_acc == 'Stayed with relatives/ friends':
        main_acc = 6
    elif main_acc == 'Others':
        main_acc = 3
    elif main_acc == 'Service Apartment':
        main_acc = 5
    elif main_acc == 'Own Residence':
        main_acc = 4


    if hotel == 'V Hotel Lavender':
        hotel = 8
    elif hotel == 'Ibis Singapore on Bencoolen':
        hotel = 1
    elif hotel == 'Mandarin Orchard Singapore':
        hotel = 2
    elif hotel == 'Concorde Hotel Singapore':
        hotel = 0
    elif hotel == 'York Hotel':
        hotel = 9
    elif hotel == 'Marina Bay Sands Singapore':
        hotel = 3
    elif hotel == 'Royal Plaza':
        hotel = 6
    elif hotel == 'The Elizabeth':
        hotel = 7
    elif hotel == 'Other Hotels':
        hotel = 5
    elif hotel == 'Not Specified':
        hotel = 4

    if travel_path == 'Air':
         travel_path = 0
    elif travel_path == 'Sea':
        travel_path = 3
    elif travel_path == 'Land':
        travel_path = 1
    elif travel_path == 'Not Specified':
        travel_path = 2

    if month == 'January':
        month = 1
    elif month == 'February':
        month = 2
    elif month == 'March':
        month = 3
    elif month == 'April':
        month = 4
    elif month == 'May':
        month = 5
    elif month == 'June':
        month = 6
    elif month == 'July':
        month = 7
    elif month == 'August':
        month = 8
    elif month == 'September':
        month = 9
    elif month == 'October':
        month = 11
    elif month == 'November':
        month = 12

    input_data = pd.DataFrame([[city, purpose, visit, length_stay, travel_type, gender, main_acc, hotel, travel_path, comp_num, month, weight, shop_exp]], columns=[city, purpose, visit, length_stay, travel_type, gender, main_acc, hotel, travel_path, comp_num, month, weight, shop_exp])
    prediction = model.predict(input_data)
    prediction = np.exp(prediction)
    return prediction


def main():
    st.title('Singapore Travel Expense Predictor')
    st.image("""https://static.thehoneycombers.com/wp-content/uploads/sites/2/2022/02/free-things-to-do-in-singapore-family-at-marina-barrage.png""")
    st.header('Enter the details:')
    city = st.selectbox('From which city are you travelling from?', ['Yogyakarta','Batam','Tanjung Pinang','Jakarta','Surabaya','Bandung','Medan','Bali','Tanjung Balai','Other cities'])
    purpose = st.selectbox('What is the purpose of visit?', ['Leisure', 'Others', 'Healthcare','Business', 'Education'])
    visit = st.radio('are you visiting Singapore for the first time', ['Yes', 'No'])
    length_stay = st.number_input('How many days of stay are you planning for', min_value=0.5, value=0.5)
    travel_type = st.selectbox('Select your travel type?', ['Packaged','Non-Packaged','Business (Non-Packaged)'])
    gender = st.radio('Select gender', ['Male', 'Female'])
    main_acc = st.selectbox('Where are you planning to stay', ['Accomodation not required','Hotel','Hostel','Stayed with relatives/ friends','Service Apartment','Own Residence','Others'])
    if main_acc == 'Hotel':
        hotel = st.selectbox('Select your preferred hotel', ['V Hotel Lavender','Ibis Singapore on Bencoolen','Mandarin Orchard Singapore','Concorde Hotel Singapore','York Hotel','Marina Bay Sands Singapore','Royal Plaza','The Elizabeth','Other Hotels','Not Specified'])
    else:
        hotel = 'Not Specified'
    travel_path = st.selectbox('Through which medium you are traveling', ['Air', 'Sea', 'Land', 'Not Specified'])
    comp_num = st.number_input('How many people are accompanying', min_value=0, value=0,)
    month =  st.selectbox('In which month are you planning to travel', ['January','February','March','April','May','June','July','August','September','October','November','December'])
    weight = st.number_input('How much will be your expected baggage weight in pounds?', min_value=0.0, max_value=10000.00, value=0.0)
    #shop_exp = st.number_input('How much dollars you wish to spend on shopping?', min_value=0.0, max_value=100000.00, value=0.0)
    shop_exp = 0

    expense = ""
    if st.button('Predict Expense'):
        expense = predict(city, purpose, visit, length_stay, travel_type, gender, main_acc, hotel, travel_path, comp_num, month, weight, shop_exp)
        st.success(f'The predicted expense of travel is ${expense[0]:.2f}')
        st.snow()

if __name__ == '__main__':
    main()