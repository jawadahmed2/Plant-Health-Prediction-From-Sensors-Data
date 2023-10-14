# myapp/views.py
import pickle
import numpy as np
import os
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import warnings
from django.http import HttpResponse

# Suppressing all warnings
warnings.filterwarnings('ignore')

# Load the KNN Trained model Weights and Scaler
print('Wait Model Is Loading')

# Load the saved scaler
scalar_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fitted_scaler.pkl')
with open(scalar_file, 'rb') as file:
    loaded_scaler = pickle.load(file)  # Loading the scaler object

# Get the absolute path to the pickle file containing the trained model
filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'best_knn_classifier.pickle')

# Load the trained model
with open(filename, 'rb') as file:
    knn_classifier = pickle.load(file)  # Loading the model object

print('Successfully Loaded')


def home(request):
    """
    Home route to check if the server is active.
    :return: An HTTP response with a string indicating that the server is active.
    """
    return HttpResponse('Server is active and ready to give service related to plant health care.')


@csrf_exempt
def predict(request):
    """
    API endpoint to predict the plant health based on the received parameters.
    It receives the parameters as JSON and returns the prediction as JSON.
    :return: A JSON object containing the status and the prediction or an error message.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))  # Getting the data sent in JSON format
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
                [[Light, Nitrogen, Phosphorus, Potassium, Humidity, Temp1, Temp2, Moisture]])

            # Scaling the input data using the loaded scaler
            new_data = loaded_scaler.transform(input_data)

            # Making prediction using the loaded model
            my_prediction = knn_classifier.predict(new_data)

            # Mapping the predicted class to the respective plant health category
            class_mapping = {0: 'Healthy', 1: 'Moderate', 2: 'Unhealthy'}
            # Getting the final result
            final_result = class_mapping[my_prediction[0]]

            # Returning the prediction as JSON
            return JsonResponse({'status': 'success', 'prediction': final_result.upper()})

        except Exception as e:
            # Returning the error message as JSON
            return JsonResponse({'status': 'error', 'message': str(e)})

    # Returning an error message if the method is not allowed
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'})
