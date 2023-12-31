# Importing essential libraries
from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
from flask_cors import CORS
from os.path import join, dirname, realpath
import warnings

# Suppressing all warnings
warnings.filterwarnings('ignore')

# Initializing Flask app
app = Flask(__name__)
app.secret_key = "planthealthcare"
CORS(app)  # Enabling CORS

# Load the KNN Trained model Weights and Scaler
print('Wait Model Is Loading')

# Load the saved scaler
scalar_file = join(dirname(realpath(__file__)), 'fitted_scaler.pkl')
with open(scalar_file, 'rb') as file:
    loaded_scaler = pickle.load(file)  # Loading the scaler object

# Get the absolute path to the pickle file containing the trained model
filename = join(dirname(realpath(__file__)), 'best_knn_classifier.pickle')

# Load the trained model
with open(filename, 'rb') as file:
    knn_classifier = pickle.load(file)  # Loading the model object

print('Successfully Loaded')


@app.route('/')
def home():
    """
    Home route to check if the server is active.
    :return: A string indicating that the server is active.
    """
    return 'Server is active and ready to give service related to plant health care.'


@app.route('/predict/api', methods=['POST'])
def predict():
    """
    API endpoint to predict the plant health based on the received parameters.
    It receives the parameters as JSON and returns the prediction as JSON.
    :return: A JSON object containing the status and the prediction or an error message.
    """
    if request.method == 'POST':
        try:
            data = request.json  # Getting the data sent in JSON format
            # Extracting individual parameters from the received JSON data
            Light = float(data['light'])
            Nitrogen = float(data['nitrogen'])
            Phosphorus = float(data['phosphorus'])
            Potassium = float(data['potassium'])
            Humidity = float(data['humidity'])
            Temp1 = float(data['temp1'])
            Temp2 = float(data['temp2'])
            Moisture = float(data['moisture'])

            # Preparing the input data
            input_data = np.array(
                [[Light, Nitrogen, Phosphorus,	Potassium,	 Humidity,	Temp1,	Temp2,	 Moisture]])

            # Scaling the input data using the loaded scaler
            new_data = loaded_scaler.transform(input_data)

            # Making prediction using the loaded model
            my_prediction = knn_classifier.predict(new_data)

            # Mapping the predicted class to the respective plant health category
            class_mapping = {0: 'Healthy', 1: 'Moderate', 2: 'Unhealthy'}
            # Getting the final result
            final_result = class_mapping[my_prediction[0]]

            # Returning the prediction as JSON
            return jsonify(status='success', prediction=final_result.upper())

        except Exception as e:
            # Returning the error message as JSON
            return jsonify(status='error', message=str(e))

    # Returning an error message if the method is not allowed
    return jsonify(status='error', message='Method not allowed')


if __name__ == '__main__':
    app.run(debug=True)  # Running the app in debug mode
