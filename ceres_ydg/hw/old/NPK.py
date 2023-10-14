import minimalmodbus
import time

mb_address = 1 # modbus address as per manual

npk_sensor = minimalmodbus.Instrument('/dev/ttyUSB0', mb_address)

# As per device specifications
npk_sensor.serial.baudrate = 9600
npk_sensor.serial.bytesize = 8
npk_sensor.serial.parity = minimalmodbus.serial.PARITY_NONE
npk_sensor.serial.stopbits = 1
npk_sensor.serial.timeout = 0.5
npk_sensor.mode = minimalmodbus.MODE_RTU

npk_sensor.clear_buffers_before_each_transaction = True
npk_sensor.close_port_after_each_call = True

print("")
print("Requesting NPK Data from Sensor...")

# One Register
# single_data = npk_sensor.read_register(30, 0, 3)
# print(f"Raw Data is {single_data}")

# We want to constantly be getting data from the sensor
while True: 
	# Multiple Regs
	# read_registers(register address, number of registers to be read, function code)
	data = npk_sensor.read_registers(30, 3, 3)

	nitrogen = data[0]
	phosphorus = data[1]
	potassium = data[2]

	print("------------------------------------")
	print(f"Nitrogren content \t {nitrogen} mg/kg")
	print(f"Phosphorus content \t {phosphorus} mg/kg")
	print(f"Potassium content \t {potassium} mg/kg")
	print("------------------------------------")
	time.sleep(5)


