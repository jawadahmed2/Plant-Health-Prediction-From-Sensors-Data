import os
import django
import sys

current_folder = os.path.dirname(os.path.abspath(__file__))
parent_folder = os.path.abspath(os.path.join(current_folder, 'ceres_ydg'))
sys.path.append(parent_folder)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ceres_ydg.settings")
django.setup()

from django.db import models
from datetime import datetime, timedelta
from main.models import SensorData, DailyAvg

def calc_daily_avg():
    min_date = SensorData.objects.earliest('date').date
    max_date = SensorData.objects.latest('date').date

    current_date = min_date
    while current_date <= max_date:
        sensor_data = SensorData.objects.filter(date=current_date)

        if sensor_data.exists():
            light_avg = sensor_data.aggregate(light_avg=models.Avg('light'))['light_avg']
            nitrogen_data_avg = sensor_data.aggregate(nitrogen_data_avg=models.Avg('nitrogen_data'))['nitrogen_data_avg']
            phosphorus_data_avg = sensor_data.aggregate(phosphorus_data_avg=models.Avg('phosphorus_data'))['phosphorus_data_avg']
            potassium_data_avg = sensor_data.aggregate( potassium_data_avg=models.Avg('potassium_data'))['potassium_data_avg']
            relative_humidity_avg = sensor_data.aggregate(relative_humidity_avg=models.Avg('relative_humidity'))['relative_humidity_avg']
            temp_c_avg = sensor_data.aggregate(temp_c_avg=models.Avg('temp_c'))['temp_c_avg']
            temp_f_avg = sensor_data.aggregate(temp_f_avg=models.Avg('temp_f'))['temp_f_avg']
            soil_moisture_avg = sensor_data.aggregate(soil_moisture_avg=models.Avg('soil_moisture'))['soil_moisture_avg']

            # Store daily averages
            daily_averages = DailyAvg(
                date=current_date,
                light_avg=round(light_avg, 2),
                nitrogen_data_avg=nitrogen_data_avg,
                phosphorus_data_avg=phosphorus_data_avg,
                potassium_data_avg=potassium_data_avg,
                relative_humidity_avg=round(relative_humidity_avg, 2),
                temp_c_avg=round(temp_c_avg, 2),
                temp_f_avg=round(temp_f_avg, 2),
                soil_moisture_avg=round(soil_moisture_avg, 2),
            )
            daily_averages.save()

        current_date += timedelta(days=1)

if __name__ == "__main__":
    calc_daily_avg()
           
           