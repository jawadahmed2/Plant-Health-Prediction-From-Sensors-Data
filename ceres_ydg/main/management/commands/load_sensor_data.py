import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from main.models import SensorData

class Command(BaseCommand):
    help = 'Loads sensor data from csv into sqlite db'

    def handle(self, *args, **options):
        # Absolute path for the CSV
        csv_filepath = '/home/rmt/ceres_ydg/hw/src/sensors/ceres_data.csv'

        with open(csv_filepath, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
              _, date, time, light, nitrogen_data, phosphorus_data, potassium_data, relative_humidity, temp_c, temp_f, soil_moisture = row
                
            # Parse date and time strings into datetime objects
            date_obj = datetime.strptime(date, '%Y-%m-%d').date()
            time_obj = datetime.strptime(time, '%H:%M:%S').time()

            SensorData.objects.create(
                date=date_obj,
                time=time_obj,
                light=float(light),
                nitrogen_data=int(nitrogen_data),
                phosphorus_data=int(phosphorus_data),
                potassium_data=int(potassium_data),
                relative_humidity=float(relative_humidity),
                temp_c=float(temp_c),
                temp_f=float(temp_f),
                soil_moisture=float(soil_moisture),
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully loaded sensor data at {datetime.now()}'))

        with open(csv_filepath, 'w', newline='') as csv_file:
            pass
        
        self.stdout.write(self.style.SUCCESS('CSV file cleared.'))  