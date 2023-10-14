#!/usr/bin/env python3
import subprocess
from time import sleep

while True:
    try:
        # Run schduler.py as a subprocess
        subprocess.run(['python', '/home/rmt/ceres_ydg/scheduler.py'])

    except Exception as e:
        # Handle any exception that occurs during the execution of scheduler.py
        print(f"Error: {e}")
    
    # Wait for a few seconds before restarting
    sleep_duration = 5
    print(f"Restarting ceres_main.py in {sleep_duration} seconds...")
    sleep(sleep_duration)