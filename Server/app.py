# Importing essential libraries
from flask import Flask, render_template, request
import pickle
import numpy as np
import os
from flask_cors import CORS


# Load the Neural Networks Trained model Weights
print('Wait Model Is Loading')
filename = './neural_networks.pickle'
classifier = pickle.load(open(filename, 'rb'))

print('Successfully Loaded')

app = Flask(__name__)
app.secret_key = "planthealthcare"
CORS(app)
basedir = os.path.abspath(os.path.dirname(__file__))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method != 'POST':
        return
    humidity = 50.0
    nitrogen_level = 30.0
    ambient_temperature = 25.0
    presence_of_sunlight = 0

    input_data = np.array([[humidity, nitrogen_level, ambient_temperature, presence_of_sunlight]])

    my_prediction = classifier.predict(input_data)
    predicted_class = np.argmax(my_prediction, axis=1)

    print(predicted_class)
    return render_template('index.html', prediction=predicted_class.upper())

if __name__ == '__main__':
    app.run(debug=True)