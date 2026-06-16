from flask import Flask,request,jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

data = pd.read_csv('Crop_recommendation.csv')

X = data.drop('label', axis=1)
y = data['label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier()
model.fit(X_train, y_train)

joblib.dump(model, 'crop_recommendation_model.pkl')

model = joblib.load('crop_recommendation_model.pkl')

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    print("Received data:", data)
    # Extract values from the JSON object and convert to a list
    features = [data['nitrogen'], data['phosphorus'], data['potassium'], data['temperature'], 
                data['humidity'], data['ph'], data['rainfall']]
    # Convert list to numpy array and reshape for prediction
    features = np.array(features).reshape(1, -1)
    # Make prediction
    prediction = model.predict(features)
    # Assuming prediction is a single element array, extract the prediction
    predicted_crop = prediction[0]
    # Return the prediction as JSON response
    return jsonify({'prediction': predicted_crop})


if __name__ == '__main__':
    print("Server started")
    app.run(port=8001,debug=True)