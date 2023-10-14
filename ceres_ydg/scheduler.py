import os
import django
import sys

current_folder = os.path.dirname(os.path.abspath(__file__))
parent_folder = os.path.abspath(os.path.join(current_folder, 'ceres_ydg'))
sys.path.append(parent_folder)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ceres_ydg.settings")
django.setup()

from apscheduler.schedulers.blocking import BlockingScheduler
from django.core.management import call_command

scheduler = BlockingScheduler()

@scheduler.scheduled_job('interval', seconds=16)
def load_sensor_data():
    call_command('load_sensor_data')

scheduler.start()