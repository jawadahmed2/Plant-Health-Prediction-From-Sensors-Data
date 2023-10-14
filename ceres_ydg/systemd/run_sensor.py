#!/usr/bin/env python3
import subprocess
from time import sleep

while True:
    try:
        # Run ceres_main.py as a subprocess
        subprocess.run(['python', '/home/rmt/ceres_ydg/hw/src/ceres_main.py'])

    except Exception as e:
        # Handle any exception that occurs during the execution of ceres_main.py
        print(f"Error: {e}")
    
    # Wait for a few seconds before restarting
    sleep_duration = 5
    print(f"Restarting ceres_main.py in {sleep_duration} seconds...")
    sleep(sleep_duration)