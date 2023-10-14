from django.db import models

# Model for storing sensor data records
class SensorData(models.Model):
    id = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    date = models.DateField(max_length=15)    # Date of the sensor data
    time = models.TimeField(max_length=15)    # Time of the sensor data
    light = models.FloatField(max_length=15)   # Light intensity reading
    nitrogen_data = models.SmallIntegerField() # Nitrogen data reading
    phosphorus_data = models.SmallIntegerField() # Phosphorus data reading
    potassium_data = models.SmallIntegerField() # Potassium data reading
    relative_humidity = models.FloatField(max_length=5)  # Relative humidity reading
    temp_c = models.FloatField(max_length=5)   # Temperature in Celsius
    temp_f = models.FloatField(max_length=5)   # Temperature in Fahrenheit
    soil_moisture = models.FloatField(max_length=5)    # Soil moisture reading

# Model for storing daily average sensor data
class DailyAvg(models.Model):
    date = models.DateField(max_length=15)    # Date of the daily average data
    light_avg = models.FloatField(max_length=15)  # Average light intensity
    nitrogen_data_avg = models.SmallIntegerField() # Average nitrogen data
    phosphorus_data_avg = models.SmallIntegerField() # Average phosphorus data
    potassium_data_avg = models.SmallIntegerField() # Average potassium data
    relative_humidity_avg = models.FloatField(max_length=5)  # Average relative humidity
    temp_c_avg = models.FloatField(max_length=5)   # Average temperature in Celsius
    temp_f_avg = models.FloatField(max_length=5)   # Average temperature in Fahrenheit
    soil_moisture_avg = models.FloatField(max_length=5)  # Average soil moisture

# Model for storing predicted sensor data
class PredictedData(models.Model):
    id = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    date = models.DateField(max_length=15)    # Date of the predicted data
    time = models.TimeField(max_length=15)    # Time of the predicted data
    light = models.FloatField(max_length=15)   # light intensity
    nitrogen_data = models.SmallIntegerField() # nitrogen data
    phosphorus_data = models.SmallIntegerField() #  phosphorus data
    potassium_data = models.SmallIntegerField() #  potassium data
    relative_humidity = models.FloatField(max_length=5)  #  relative humidity
    temp_c = models.FloatField(max_length=5)   #  temperature in Celsius
    temp_f = models.FloatField(max_length=5)   #  temperature in Fahrenheit
    soil_moisture = models.FloatField(max_length=5)    #  soil moisture
    prediction = models.CharField(max_length=25)  # Field for storing prediction information
