from smbus2 import SMBus
import time

# function that calcs soil moisture
def calc_soil_moisture(data):
    return (((data / 134) - 1) * 100)

def main():
    # Bus6 is used as the I2C interface
    bus6 = SMBus(6)

    # while true used to get continuous readings
    while True:
        # write to the ADC address and request info from 0x84(CH0/A0)
        bus6.write_byte(0x4b, 0x84)

        # read value from that channel
        data = bus6.read_byte(0x4b)

        # Switch statement to print soil moisture value
        if data <= 134:
            # Code to execute when data is less than or equal to 134
            print(f"Soil Moisture 100 %")
            time.sleep(5)
        elif 134 < data < 255:
            # Code to execute when data is between 134 and 255
            soil_moisture = calc_soil_moisture(data)
            perc_sm = 100 - soil_moisture
            round_sm = round(perc_sm, 2)
            print(f"Soil Moisture {round_sm} %")
            time.sleep(5)
        elif data >= 255:
            # Code to execute when data is greater than or equal to 255
            print(f"Soil Moisture 0 %")
            time.sleep(5)
        else:
            # Code to execute when none of the above conditions are met
            print(f"[Err] No soil data available")
            time.sleep(5)

# Execute main
main()