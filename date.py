from datetime import datetime, time
import datetime
import calendar
import json

K_START_TIME = datetime.time(7,15)

K_TEST_TIME = datetime.time(7,30)

def reserve_today(creds, netID, spot):
    return creds[netID]["Dates"][spot] == get_weekdate()

def check_before_midnight():
    right_now = datetime.datetime.now().time()
    return right_now <= K_TEST_TIME   

def get_weekdate_name(date):
    return calendar.day_name[date]

def check_before_start():
    right_now = datetime.datetime.now().time()
    return right_now <= K_START_TIME

def start_reservation_process(start_time=None):
    if (start_time is None):
        start_time = K_START_TIME

    right_now = datetime.datetime.now().time()
    return right_now >= start_time

def get_before(weekdate, n):
    return (weekdate - n) % 7

def get_weekdate():
    return int(datetime.datetime.today().weekday())

def is_weekend(weekdate):
    if weekdate >= 5:
        return "Weekend"
    return "Weekday"

def getURL(place):
    today = datetime.date.today()
    next_three_day = today + datetime.timedelta(days=3)
    next_three_day = next_three_day.strftime("%m/%d/%Y")

    with open('reservations.json') as f:
        reservations = json.load(f)
    URL_to_return = reservations[place]['URL'][0] + next_three_day + reservations[place]['URL'][1]
    return URL_to_return
