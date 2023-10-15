import os
import django
import requests
from datetime import datetime, time
from django.db.models import Avg
from main.models import SensorData, PredictedData, DailyAvg  # Import from the 'main' app

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ceres_ydg.settings")

# Initialize Django
django.setup()


# Define the API endpoint
api_url = 'http://127.0.0.1:8000/predict/api/'

def get_current_time():
    """
    Get the current time in the desired format.
    """
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time

def make_prediction(sensor_data):
    """
    Make a prediction based on the given sensor data and return the result.
    """
    try:
        response = requests.post(api_url, json=sensor_data)
        if response.status_code == 200:
            return response.json().get('prediction')
        else:
            return None
    except Exception as e:
        print(f"Prediction error: {e}")
        return None


def predict_at_time(prediction_times):
    """
    Predict and save data for the specified prediction times.
    :param prediction_times: List of time objects for predictions (e.g., [time(0, 0), time(6, 0), ...])
    """
    # Get the current date and time
    now = datetime.now()

    # Iterate over each prediction time
    for prediction_time in prediction_times:
        # Calculate the target datetime for prediction
        target_datetime = datetime.combine(now.date(), prediction_time)

        # Check if a prediction already exists for this target datetime
        existing_prediction = PredictedData.objects.filter(
            date=target_datetime.date(),
            time=target_datetime.time()
        ).first()

        if existing_prediction:
            print(f"Prediction already exists for {target_datetime}. Skipping.")
            continue

        # Query the sensor data for the target datetime
        sensor_data = SensorData.objects.filter(
            date=target_datetime.date(),
            time=target_datetime.time()
        ).first()

        print(sensor_data)
        try:
            if sensor_data:
                # Make a prediction and store it in PredictedData
                prediction = make_prediction({
                    'light': sensor_data.light,
                    'nitrogen': sensor_data.nitrogen_data,
                    'phosphorus': sensor_data.phosphorus_data,
                    'potassium': sensor_data.potassium_data,
                    'humidity': sensor_data.relative_humidity,
                    'temp1': sensor_data.temp_c,
                    'temp2': sensor_data.temp_f,
                    'moisture': sensor_data.soil_moisture
                })
                print(prediction)

                if prediction:
                    # Create a PredictedData record and save it
                    predicted_data = PredictedData(
                        date=target_datetime.date(),
                        time=target_datetime.time(),
                        light=sensor_data.light,
                        nitrogen_data=sensor_data.nitrogen_data,
                        phosphorus_data=sensor_data.phosphorus_data,
                        potassium_data=sensor_data.potassium_data,
                        relative_humidity=sensor_data.relative_humidity,
                        temp_c=sensor_data.temp_c,
                        temp_f=sensor_data.temp_f,
                        soil_moisture=sensor_data.soil_moisture,
                        prediction=prediction
                    )
                    # predicted_data.save()
                    print(f"Prediction saved for {target_datetime}: {prediction}")
                else:
                    print(f"Prediction failed for {target_datetime}.")

        except Exception as e:
            print(f"Error: {e}")


# Define the times for predictions
prediction_times = [
    time(0, 0),   # 12:00 AM
    time(6, 0),   # 6:00 AM
    time(12, 0),  # 12:00 PM
    time(18, 0),  # 6:00 PM
]

predict_at_time(prediction_times)


# def predict_at_time(interval_start, interval_end):
#     """
#     Predict and save data for a given time interval.
#     """
#     try:
#         # Fetch sensor data for the selected time interval
#         sensor_data = SensorData.objects.filter(
#             time__range=(interval_start, interval_end)
#         ).aggregate(
#             Avg("light"),
#             Avg("nitrogen_data"),
#             Avg("phosphorus_data"),
#             Avg("potassium_data"),
#             Avg("relative_humidity"),
#             Avg("temp_c"),
#             Avg("temp_f"),
#             Avg("soil_moisture"),
#         )

#         # Create a dictionary of sensor data
#         sensor_data_dict = {
#             "light": sensor_data["light__avg"],
#             "nitrogen": sensor_data["nitrogen_data__avg"],
#             "phosphorus": sensor_data["phosphorus_data__avg"],
#             "potassium": sensor_data["potassium_data__avg"],
#             "humidity": sensor_data["relative_humidity__avg"],
#             "temp1": sensor_data["temp_c__avg"],
#             "temp2": sensor_data["temp_f__avg"],
#             "moisture": sensor_data["soil_moisture__avg"],
#         }

#         # Make a prediction based on the sensor data
#         prediction = make_prediction(sensor_data_dict)

    #     if prediction:
    #         # Save the prediction to the PredictedData model
    #         current_time = get_current_time()
    #         predicted_data = PredictedData(
    #             date=datetime.now().date(),
    #             time=current_time,
    #             light=sensor_data_dict["light"],
    #             nitrogen_data=sensor_data_dict["nitrogen"],
    #             phosphorus_data=sensor_data_dict["phosphorus"],
    #             potassium_data=sensor_data_dict["potassium"],
    #             relative_humidity=sensor_data_dict["humidity"],
    #             temp_c=sensor_data_dict["temp1"],
    #             temp_f=sensor_data_dict["temp2"],
    #             soil_moisture=sensor_data_dict["moisture"],
    #             prediction=prediction,
    #         )
    #         predicted_data.save()
    #         print(f"Prediction saved for {current_time}: {prediction}")
    #     else:
    #         print(f"Prediction failed for {get_current_time()}.")
    # except Exception as e:
    #     print(f"Error: {e}")

# def predict_daily_average():
#     """
#     Predict and save data for daily average sensor readings.
#     """
#     try:
#         # Fetch daily average sensor data
#         daily_avg_data = DailyAvg.objects.all().latest('date')

#         # Create a dictionary of daily average sensor data
#         sensor_data_dict = {
#             "light": daily_avg_data.light_avg,
#             "nitrogen": daily_avg_data.nitrogen_data_avg,
#             "phosphorus": daily_avg_data.phosphorus_data_avg,
#             "potassium": daily_avg_data.potassium_data_avg,
#             "humidity": daily_avg_data.relative_humidity_avg,
#             "temp1": daily_avg_data.temp_c_avg,
#             "temp2": daily_avg_data.temp_f_avg,
#             "moisture": daily_avg_data.soil_moisture_avg,
#         }

#         # Make a prediction based on the daily average sensor data
#         prediction = make_prediction(sensor_data_dict)

#         if prediction:
#             # Save the prediction to the PredictedData model
#             current_time = get_current_time()
#             predicted_data = PredictedData(
#                 date=datetime.now().date(),
#                 time=current_time,
#                 light=sensor_data_dict["light"],
#                 nitrogen_data=sensor_data_dict["nitrogen"],
#                 phosphorus_data=sensor_data_dict["phosphorus"],
#                 potassium_data=sensor_data_dict["potassium"],
#                 relative_humidity=sensor_data_dict["humidity"],
#                 temp_c=sensor_data_dict["temp1"],
#                 temp_f=sensor_data_dict["temp2"],
#                 soil_moisture=sensor_data_dict["moisture"],
#                 prediction=prediction,
#             )
#             predicted_data.save()
#             print(f"Daily average prediction saved for {current_time}: {prediction}")
#         else:
#             print(f"Daily average prediction failed for {get_current_time()}.")
#     except Exception as e:
#         print(f"Error: {e}")

# def main():
#     # Define the time intervals for predictions
#     prediction_times = [
#         ("00:00:00", "12:00:00"),
#         ("06:00:00", "18:00:00"),
#         ("12:00:00", "00:00:00"),
#         ("18:00:00", "06:00:00"),
#     ]

#     # Get the current time
#     current_time = get_current_time()

#     # Determine the appropriate time interval for prediction
#     prediction_interval = None
#     for start, end in prediction_times:
#         start_time = time.fromisoformat(start)
#         end_time = time.fromisoformat(end)
#         current_time_obj = time.fromisoformat(current_time)
#         if start_time <= current_time_obj <= end_time:
#             prediction_interval = (start, end)
#             break

#     if prediction_interval:
#         # Predict and save data for the selected time interval
#         interval_start, interval_end = prediction_interval
#         predict_at_time(interval_start, interval_end)
#     else:
#         print("No prediction interval found for the current time.")

#     # Predict and save daily average data
#     predict_daily_average()

# if __name__ == "__main__":
#     main()
