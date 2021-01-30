from datetime import datetime, time
import datetime
import json
import bum_encryption as bmi
from getpass import getpass

k_time_obj = datetime.datetime.now().time()
data_main = 0


def EnterInfo():
    
    
    print("press 0 twice to skip to reservation if info is already entered")
    first_inp = input()
    inp = int(first_inp)


    if (inp == 0):
        return False


    

    # load credentials
    try:
        with open('credentials.json') as f:
            creds = json.load(f)
    except:
        creds = {}

    print("Enter your NetID:")
    netID = input()
    

    if netID in creds:
        # check if password is correct
        try:
            with open('keys.json') as f:
                keys = json.load(f)
        except:
            print("Looks like we don't have your keys...")
            return False
        
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

        try:
            with open('keys.json') as f:
                keys = json.load(f)
        except:
            keys = {}
        keys[netID] = key

    # open times
    with open('times.json') as f:
        times = json.load(f)

    print("Enter Place (" + ', '.join(times.keys()) + "):")
    place = input()
    if place not in times.keys():
        print("Not an available place")
        return False

    
    print("Enter Time (" + ', '.join(times[place]) + "):")
    time = input()
    if time not in times[place]:
        print("Not an available time. Possible times are:")
        for possible_time in times[place]:
            print(possible_time)
    
    if netID in creds:
        creds[netID]["Places"].append(place)
        creds[netID]["Times"].append(time)
        print("Added a reservation for User (" + netID + ") at " + time + " at " + place)
    else:
        creds[netID] = {"Password": password, "Places": [place], "Times": [time]}
        print("Added User (" + netID + ") with a reservation at " + time + " at " + place)
    
    with open('credentials.json', 'w') as outfile:
        json.dump(creds, outfile)
    with open('keys.json', 'w') as outfile:
        json.dump(keys, outfile)
    return True

##EnterInfo()