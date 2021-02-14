from datetime import datetime, time
import datetime
import json
import bum_encryption as bmi
from getpass import getpass
import date as time_manager
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

k_time_obj = datetime.datetime.now().time()
data_main = 0

require_pass = False

def EnterInfo():
    # load credentials
    try:
        with open('credentials.json') as f:
            creds = json.load(f)
    except:
        creds = {}
    try:
        with open('keys.json') as f:
            keys = json.load(f)
    except:
        keys = {}

    print("Enter your NetID:")
    netID = input()

    if netID == "--remove":
        print("Enter NetID to remove:")
        remove_netID(input())
        return False
    elif netID == "--list":
        print("Today (" + time_manager.get_weekdate_name(time_manager.get_weekdate()) + ") we will reserve for " + time_manager.get_weekdate_name(time_manager.get_before(time_manager.get_weekdate(), 4)) + ":")
        for netID in creds:
            for spot in range(len(creds[netID]["Times"])):
                if time_manager.reserve_today(creds, netID, spot):
                    print(netID + ": " + creds[netID]["Places"][spot] + " at " + creds[netID]["Times"][spot])
        return False
    elif netID == "--creds":
        print("Users in system:")
        for netID in creds:
            if netID in keys:
                print(netID + " -- affirmed")
            else:
                print(netID + " -- missing")
        return False
    elif netID == "--update_pass":
        print("Enter NetID to update:")
        netID = input()

        if netID not in creds:
            print("Not a user")
            return False
        if netID not in keys:
            print("Key not found!")
            return False

        print("Enter your Password:")
        password, key = bmi.generate_key_encrypt(getpass())

        print("Confirm your Password:")
        password_confirm = bmi.encrypt(getpass(), key)

        if password != password_confirm:
            print("The passwords are not the same")
            return False

        creds[netID]["Password"] = password
        keys[netID] = key
        with open('credentials.json', 'w') as outfile:
            json.dump(creds, outfile)
        with open('keys.json', 'w') as outfile:
            json.dump(keys, outfile)
        
        print("Updated User (" + netID + ")")
        return False
    elif netID == "--update_user":
        print("Enter NetID to update:")
        netID = input()

        if netID not in creds:
            print("Not a user")
            return False
        if netID not in keys:
            print("Key not found!")
            return False
        
        print("Enter NetID to change to:")
        new_netID = input()

        if new_netID in creds:
            print(new_netID + " already exists! Delete it first to change!")
            return False

        creds[new_netID] = creds[netID]
        del creds[netID]
        keys[new_netID] = keys[netID]
        del keys[netID]
        with open('credentials.json', 'w') as outfile:
            json.dump(creds, outfile)
        with open('keys.json', 'w') as outfile:
            json.dump(keys, outfile)
        print("Changed " + netID + " to " + new_netID)
        return False
    elif netID == "--confirm":
        print("Enter NetID to confirm:")
        netID = input()

        if netID not in creds:
            print("Not a user")
            return False
        
        success, err = check_login(netID)
        if success:
            print("Successfully Logged In")
        else:
            print("Error logging in: " + err)
        return False
    elif netID == "--move":
        for netid in creds.keys():
            for i in range(len(creds[netid]["Dates"])):
                creds[netid]["Dates"][i] = time_manager.get_before(creds[netid]["Dates"][i], 6)
        with open('credentials.json', 'w') as outfile:
            json.dump(creds, outfile)
        return False

    
    

    if netID in creds:
        if require_pass:
            print("Enter your Password:")
            password = bmi.encrypt(getpass(), keys[netID])

            if password != creds[netID]["Password"]:
                print("Incorrect Password")
                return False
    else:
        # generate a key for the password
        print("Enter your Password:")
        password, key = bmi.generate_key_encrypt(getpass())

        print("Confirm your Password:")
        password_confirm = bmi.encrypt(getpass(), key)

        if password != password_confirm:
            print("The passwords are not the same")
            return False

        keys[netID] = key

    # open times
    with open('reservations.json') as f:
        reservations = json.load(f)

    print("Enter Place (" + ', '.join(reservations.keys()) + "):")
    place = input()
    if place not in reservations.keys():
        print("Not an available place")
        return False

    print("Enter a Weekday (0 = Monday, 2 = Wednesday, 4 = Friday, 6 = Sunday, etc.). Enter multiple dates delimited with ','. Only do Weekends or Weekdates:")
    try:
        weekdates = input().split(',')
        weekdates = [int(x) for x in weekdates]

        weekend = time_manager.is_weekend(weekdates[0])
        # Check Validity
        for weekdate in weekdates:
            if time_manager.is_weekend(weekdate) != weekend:
                print("Only do Weekends or Weekdays")
                return False
            if weekdate < 0 or weekdate > 6:
                print("Weekday must be between 0 and 6")
                return False
        weekdates = [time_manager.get_before(x, 3) for x in weekdates]
    except:
        print("Weekday must be between 0 and 6")
        return False
    
    print("Enter Time (" + ', '.join(reservations[place]["Times"][weekend]) + "):")
    time = input()
    if time not in reservations[place]["Times"][weekend]:
        print("Not an available time. Possible times are:")
        for possible_time in reservations[place]["Times"][weekend]:
            print(possible_time)
        return False
    
    places = [place] * len(weekdates)
    times = [time] * len(weekdates)
    

    t_combo = [(p, t, d) for p, t, d in zip(places, times, weekdates)]

    if netID in creds:
        for i, combo in enumerate(zip(creds[netID]["Places"], creds[netID]["Times"], creds[netID]["Dates"])):
            if combo in t_combo:
                del creds[netID]["Places"][i]
                del creds[netID]["Times"][i]
                del creds[netID]["Dates"][i]
                t_combo.remove(combo)
                print("Removed a reservation for User (" + netID + ") at place = " + str(combo[0]) + ", time = " + str(combo[1]) + ", date = " + str(combo[2]) + ".")
    else:
        creds[netID] = {"Password": password, "Places": [], "Dates": [], "Times": []}
        print("Added User :" + netID)
        with open('keys.json', 'w') as outfile:
            json.dump(keys, outfile)
    
    for p, t, d in t_combo:
        creds[netID]["Places"].append(p)
        creds[netID]["Times"].append(t)
        creds[netID]["Dates"].append(d)
        print("Added a reservation for User (" + netID + ") at place = " + str(p) + ", time = " + str(t) + ", date = " + str(d) + ".")
    
    with open('credentials.json', 'w') as outfile:
        json.dump(creds, outfile)
    return True

def remove_netID(netID):
    with open('credentials.json') as f:
        creds = json.load(f)
    with open('keys.json') as f:
        keys = json.load(f)
    
    if netID in creds:
        del creds[netID]
    if netID in keys:
        del keys[netID]

    with open('credentials.json', 'w') as outfile:
        json.dump(creds, outfile)
    with open('keys.json', 'w') as outfile:
        json.dump(keys, outfile)

def check_login(netID):
    # Get credentials
    with open('credentials.json') as f:
        creds = json.load(f)
    
    # Get keys
    with open('keys.json') as f:
        keys = json.load(f)
    
    if netID not in keys:
        print("You don't have your key stored")
        return False, "NoPass"

    # Open the Website
    b  = webdriver.Chrome(ChromeDriverManager().install())
    b.get('https://hnd-p-ols.spectrumng.net/IllinoisCampusRec/Login.aspx?ReturnUrl=%2fillinoiscampusrec')
    
    password = creds[netID]['Password']

    # Input Credentials
    b.find_element_by_id('ctl00_pageContentHolder_loginControl_UserName').send_keys(netID)
    b.find_element_by_id('ctl00_pageContentHolder_loginControl_Password').send_keys(bmi.decrypt(password, keys[netID]))
    b.find_element_by_id('ctl00_pageContentHolder_loginControl_Login').click()

    # Wait for login
    try:
        WebDriverWait(b, 20).until(EC.presence_of_element_located((By.ID, 'menu_SCH')))
    except TimeoutException:
        return False, "InvalidCreds"
    return True, "Success"

EnterInfo()