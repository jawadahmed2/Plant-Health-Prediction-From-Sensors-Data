import time
import board
import busio

import adafruit_tsl2591

def get_sunlight():
	i2c = busio.I2C(board.SCL, board.SDA)

	sensor = adafruit_tsl2591.TSL2591(i2c)

	sensor.gain = adafruit_tsl2591.GAIN_MED

	sensor.integration_time = adafruit_tsl2591.INTEGRATIONTIME_600MS
	
	time.sleep(1)

	return round(sensor.lux, 2)



