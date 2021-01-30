from datetime import datetime, time
import datetime
import json

K_START_TIME = datetime.time(16,52)


def check_before_midnight():
    midnight = K_START_TIME
    right_now = datetime.datetime.now().time()
    return right_now <= midnight  

def start_reservation_process(start_time=None):
    if (start_time is None):
        start_time = K_START_TIME

    right_now = datetime.datetime.now().time()
    return right_now >= start_time

def getURL(place):
    today = datetime.date.today()
    next_three_day = today + datetime.timedelta(days=4)
    next_three_day = next_three_day.strftime("%m/%d/%Y")

    with open('reservations.json') as f:
        reservations = json.load(f)
    URL_to_return = reservations[place][1] + next_three_day + reservations[place][2]
    return URL_to_return
