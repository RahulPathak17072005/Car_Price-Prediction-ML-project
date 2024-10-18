from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pandas as pd
import pickle as pk
from pymongo import MongoClient
from datetime import datetime
app = Flask(__name__)
CORS(app)  # Enables CORS for all routes

# Load the trained model
model = pk.load(open('model.pkl', 'rb'))

# MongoDB client and database connection
client = MongoClient('mongodb://localhost:27017/')
db = client['user']
collection = db['car_data']

# Function to replace categorical values with numeric codes
def preprocess_input(data):
    data['owner'].replace(['First Owner', 'Second Owner', 'Third Owner', 'Fourth & Above Owner', 'Test Drive Car'], [1, 2, 3, 4, 5], inplace=True)
    data['fuel'].replace(['Diesel', 'Petrol', 'LPG', 'CNG'], [1, 2, 3, 4], inplace=True)
    data['seller_type'].replace(['Individual', 'Dealer', 'Trustmark Dealer'], [1, 2, 3], inplace=True)
    data['transmission'].replace(['Manual', 'Automatic'], [1, 2], inplace=True)
    data['name'].replace(
        ['Maruti', 'Skoda', 'Honda', 'Hyundai', 'Toyota', 'Ford', 'Renault', 'Mahindra', 'Tata', 'Chevrolet', 'Datsun', 'Jeep', 'Mercedes-Benz',
         'Mitsubishi', 'Audi', 'Volkswagen', 'BMW', 'Nissan', 'Lexus', 'Jaguar', 'Land', 'MG', 'Volvo', 'Daewoo', 'Kia', 'Fiat', 'Force',
         'Ambassador', 'Ashok', 'Isuzu', 'Opel'],
        list(range(1, 32)), inplace=True)
    return data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get data from the form
        input_data = request.form.to_dict()
        input_df = pd.DataFrame([input_data])
        
        # Preprocess input data for the model
        input_df = preprocess_input(input_df)
        
        # Predict car price
        car_price = model.predict(input_df)[0]
        car_price = round(car_price, 2)
        
        return jsonify({'price': car_price})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/submit_form', methods=['POST'])
def submit_form():
    try:
        # Get data from the request as JSON
        form_data = request.json
        
        # Add the current date and time to the form data
        form_data['submitted_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Insert form data into MongoDB
        collection.insert_one(form_data)
        
        return jsonify({'message': 'Form data saved successfully!'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
