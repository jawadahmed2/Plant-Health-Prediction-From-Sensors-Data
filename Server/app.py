# Importing essential libraries
from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
from flask_cors import CORS
from os.path import join, dirname, realpath
import warnings
warnings.filterwarnings('ignore')

# Load the Neural Networks Trained model Weights
print('Wait Model Is Loading')

# Load the saved scaler
scalar_file = join(dirname(realpath(__file__)), 'fitted_scaler.pkl')
with open(scalar_file, 'rb') as file:
    loaded_scaler = pickle.load(file)

# Get the absolute path to the pickle file
filename = join(dirname(realpath(__file__)), 'neural_networks.pickle')

# Load the pickle file
classifier = pickle.load(open(filename, 'rb'))

print('Successfully Loaded')

app = Flask(__name__)
app.secret_key = "planthealthcare"
CORS(app)


@app.route('/')
def home():
    return 'Server is active and ready to give service related to plant health care.'


@app.route('/predict/api', methods=['POST'])
def predict():
    if request.method == 'POST':
        try:
            data = request.json
            humidity = float(data['humidity'])
            nitrogen_level = float(data['nitrogen_level'])
            ambient_temperature = float(data['ambient_temperature'])
            presence_of_sunlight = float(data['presence_of_sunlight'])

            input_data = np.array([[humidity, nitrogen_level, ambient_temperature, presence_of_sunlight]])
            new_data = loaded_scaler.transform(input_data)

            my_prediction = classifier.predict(new_data)
            predicted_class = np.argmax(my_prediction, axis=1)

            # Mapping the predicted class to the respective plant health category
            class_mapping = {0: 'Healthy', 1: 'Moderate', 2: 'Unhealthy'}
            final_result = class_mapping[predicted_class[0]]

            return jsonify(status='success', prediction=final_result.upper())

        except Exception as e:
            return jsonify(status='error', message=str(e))

    return jsonify(status='error', message='Method not allowed')

if __name__ == '__main__':
    app.run(debug=True)
