from dagster import repository

from .jobs import jobs
from .schedules import schedules
from .sensors import sensors


@repository
def client():
    return jobs + schedules + sensors
