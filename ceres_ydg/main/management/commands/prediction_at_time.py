from datetime import datetime, time
from django.db.models import Avg
from django.core.management.base import BaseCommand
from django.conf import settings  # Import Django settings
import requests  # Import the 'requests' library
from main.models import SensorData, PredictedData, DailyAvg



class Command(BaseCommand):
    help = 'Run predictions and save the results'

    def add_arguments(self, parser):
        # You can add any command line arguments here if needed
        pass

    def handle(self, *args, **kwargs):
        pass


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
        # Access 'api_url' from Django settings
        api_url = settings.API_URL
        response = requests.post(api_url, json=sensor_data)
        if response.status_code == 200:
            return response.json().get('prediction')
        else:
            return None
    except Exception as e:
        print(f"Prediction error: {e}")
        return None


def predict_at_time(date, interval_start, interval_end):
    """
    Predict and save data for a given date and time interval.
    """
    try:
        # Parse the interval start and end times
        start_time = time.fromisoformat(interval_start)
        end_time = time.fromisoformat(interval_end)

        # Combine the date and start time to get the target datetime
        target_datetime = datetime.combine(date, start_time) # 2021-10-09 00:00:00

        # Check if a prediction already exists for this target datetime
        existing_prediction = PredictedData.objects.filter(
            date=date,
            time=start_time
        ).first()

        if existing_prediction:
            print(f"Prediction already exists for {target_datetime}. Skipping.")
            return

        # Fetch sensor data for the selected time interval
        sensor_data = SensorData.objects.filter(
            date=date,
            time__range=(start_time, end_time)
        ).aggregate(
            Avg("light"),
            Avg("nitrogen_data"),
            Avg("phosphorus_data"),
            Avg("potassium_data"),
            Avg("relative_humidity"),
            Avg("temp_c"),
            Avg("temp_f"),
            Avg("soil_moisture"),
        )
        # Create a dictionary of sensor data
        sensor_data_dict = {
            "light": sensor_data["light__avg"],
            "nitrogen": sensor_data["nitrogen_data__avg"],
            "phosphorus": sensor_data["phosphorus_data__avg"],
            "potassium": sensor_data["potassium_data__avg"],
            "humidity": sensor_data["relative_humidity__avg"],
            "temp1": sensor_data["temp_c__avg"],
            "temp2": sensor_data["temp_f__avg"],
            "moisture": sensor_data["soil_moisture__avg"],
        }

        # Make a prediction based on the sensor data
        prediction = make_prediction(sensor_data_dict)
        if prediction:
            # Save the prediction to the PredictedData model
            predicted_data = PredictedData(
                date=date,
                time=start_time,
                light=sensor_data_dict["light"],
                nitrogen_data=sensor_data_dict["nitrogen"],
                phosphorus_data=sensor_data_dict["phosphorus"],
                potassium_data=sensor_data_dict["potassium"],
                relative_humidity=sensor_data_dict["humidity"],
                temp_c=sensor_data_dict["temp1"],
                temp_f=sensor_data_dict["temp2"],
                soil_moisture=sensor_data_dict["moisture"],
                prediction=prediction,
            )
            predicted_data.save()
            print(f"Prediction saved for {target_datetime}: {prediction}")
        else:
            print(f"Prediction failed for {target_datetime}.")

    except Exception as e:
        print(f"Error: {e}")

def predict_daily_average():
    """
    Predict and save data for daily average sensor readings.
    """
    try:
        # Get the current date
        current_date = datetime.now().date()

        # Check if a prediction for the current date already exists
        existing_prediction = PredictedData.objects.filter(date=current_date).first()

        if existing_prediction:
            print(f"Prediction for {current_date} already exists.")
            return

        # Fetch daily average sensor data
        daily_avg_data = DailyAvg.objects.all().latest('date')

        # Create a dictionary of daily average sensor data
        sensor_data_dict = {
            "light": daily_avg_data.light_avg,
            "nitrogen": daily_avg_data.nitrogen_data_avg,
            "phosphorus": daily_avg_data.phosphorus_data_avg,
            "potassium": daily_avg_data.potassium_data_avg,
            "humidity": daily_avg_data.relative_humidity_avg,
            "temp1": daily_avg_data.temp_c_avg,
            "temp2": daily_avg_data.temp_f_avg,
            "moisture": daily_avg_data.soil_moisture_avg,
        }

        # Make a prediction based on the daily average sensor data
        prediction = make_prediction(sensor_data_dict)

        if prediction:
            # Save the prediction to the PredictedData model
            current_time = get_current_time()
            predicted_data = PredictedData(
                date=current_date,
                time=current_time,
                light=sensor_data_dict["light"],
                nitrogen_data=sensor_data_dict["nitrogen"],
                phosphorus_data=sensor_data_dict["phosphorus"],
                potassium_data=sensor_data_dict["potassium"],
                relative_humidity=sensor_data_dict["humidity"],
                temp_c=sensor_data_dict["temp1"],
                temp_f=sensor_data_dict["temp2"],
                soil_moisture=sensor_data_dict["moisture"],
                prediction=prediction,
            )
            predicted_data.save()
            print(f"Daily average prediction saved for {current_date} {current_time}: {prediction}")
        else:
            print(f"Daily average prediction failed for {current_date} {get_current_time()}.")
    except Exception as e:
        print(f"Error: {e}")


def main():
    # Define the time intervals for predictions
    prediction_times = [
        ("00:00:00", "06:00:00"),  # 12:00 AM
        ("06:00:00", "12:00:00"),  # 6:00 AM
        ("12:00:00", "18:00:00"),  # 12:00 PM
        ("18:00:00", "23:59:59"),  # 6:00 PM
    ]

    # Get the current date and time
    current_date = datetime.now().date()
    current_time = datetime.now().time()
    # print(current_date)

    # custom_date = '2023-10-09'
    # current_date = datetime.strptime(custom_date, '%Y-%m-%d')

    # Check if it's the evening (between 18:00 and 23:59)
    evening_start = datetime.strptime("18:00:00", "%H:%M:%S").time()
    evening_end = datetime.strptime("23:59:59", "%H:%M:%S").time()

    if evening_start <= current_time <= evening_end:
        predict_daily_average()
    else:
        for start_time, end_time in prediction_times:
            predict_at_time(current_date, start_time, end_time)

# call the main function
main()

