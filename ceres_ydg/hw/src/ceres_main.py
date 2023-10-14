from time import sleep, strftime, time
from sensors.SUN_CD import get_sunlight
from sensors.NPK_CD import get_npk_nit, get_npk_phos, get_npk_pot
from sensors.SHT30_CD import get_rel_hum, get_temp_c, get_temp_f
from sensors.SM_ADC_CD import get_soil_moisture
import csv

# ID is the primary key for the SQLite DB
id = 0
batch_size = 1  # Adjust the batch size according to your needs
data_buffer = []

while True:
    data_buffer.append([
        id,
        strftime("%Y-%m-%d"),
        strftime("%H:%M:%S"),
        get_sunlight(),
        get_npk_nit(),
        get_npk_phos(),
        get_npk_pot(),
        get_rel_hum(),
        get_temp_c(),
        get_temp_f(),
        get_soil_moisture()
    ])

    # Write data to CSV in batches
    if len(data_buffer) >= batch_size:
        with open("/home/rmt/ceres_ydg/hw/src/sensors/ceres_data.csv", "a", newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerows(data_buffer)
        data_buffer = []  # Clear the data buffer after writing to the CSV file

    sleep(1)