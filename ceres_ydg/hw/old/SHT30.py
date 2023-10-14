from smbus2 import SMBus # for i2c interfacing
import time 

# I2C BUS
# Our bus is 0 because we are using the bus on PINS 27 and 28
bus0 = SMBus(0)

while True:
    # SHT-30 (Sensor) address is 0x44
    # write_i2c_block_data(i2c address, register, list of bytes (repeatability))
    bus0.write_i2c_block_data(0x44, 0x24, [0x0B])
    time.sleep(1)

    # read_i2c_block_data(i2c address, start register, number of bytes to read)
    # return an array of values
    data = bus0.read_i2c_block_data(0x44, 0x00, 6)

    # Convert Data into Temp and Humidity Values
    # Temp is 16 bits split betwen data[0] and data[1] lets make them one value
    raw_temp = ((data[0] << 8) | data[1])

    # Hum is 16 bits split betwen data[3] and data[4] lets make them one value
    raw_hum = ((data[3] << 8) | data[4])

    # Calculate Temp in C and F
    tempc = - 45.0 + 175.0 * (raw_temp/(65535 - 1))
    round_tempc = round(tempc, 1)

    tempf = -49 + 315 * (raw_temp/(65535 - 1))
    round_tempf = round(tempf, 1)

    # Calculate Relative Humidity
    rel_hum = 100 * (raw_hum/(65535 - 1))
    round_hum = round(rel_hum, 1)

    print("------------------------------------")
    print(f"Temperature \t {round_tempc}\u00B0C/{round_tempf}\u00B0F")
    print(f"Relative Humidity \t {round_hum}%")
    print("------------------------------------")
    time.sleep(5)