from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import json
import date as time_manager
from datetime import datetime, time
import pandas
import numpy
import bum_encryption as bmi
import time as t

# Delay
delay = 30

def wait_till_reserve():
    while time_manager.check_before_midnight():
        t.sleep(1)

def wait_for_load(b):
    try:
        WebDriverWait(b, delay).until(EC.invisibility_of_element_located((By.ID, "tblProgess")))
        return True, ""
    except TimeoutException:
        print("Loading Wait Failed")
        return False, "ExceedLoadTime"

def check_if_available(b, time, taken):
    # Flip to the Right Time
    times_list = b.find_elements_by_xpath('//*[@class="DgText"]') + b.find_elements_by_xpath('//*[@class="DgTextAlt"]')
    patrons = [t.find_element_by_xpath('.//*[@align="center"]').text + t.find_element_by_xpath('.//*[@class="clstdResurce"]').text for t in times_list]
    start_times = [patron[:8] if patron not in taken else "Taken" for patron in patrons]
    while time not in start_times:
        try:
            b.find_element_by_id('ancSchListNext').click()
            times_list = b.find_elements_by_xpath('//*[@class="DgText"]') + b.find_elements_by_xpath('//*[@class="DgTextAlt"]')
            patrons = [t.find_element_by_xpath('.//*[@align="center"]').text + t.find_element_by_xpath('.//*[@class="clstdResurce"]').text for t in times_list]
            start_times = [patron[:8] if patron not in taken else "Taken" for patron in patrons]
        except:
            print("Failed to find time")
            return False, None, "ExceedLoadTime"
    
    index = start_times.index(time)
    return True, times_list[index], patrons[index]

def preempt_reserve(netID, spot, taken):
    # Get credentials
    with open('credentials.json') as f:
        creds = json.load(f)

    # Check if should reserve
    if not time_manager.reserve_today(creds, netID, spot):
        return False, "NotReserveToday", taken

    # Open the Website
    b = webdriver.Chrome(ChromeDriverManager().install())
    b.get('https://hnd-p-ols.spectrumng.net/IllinoisCampusRec/Login.aspx?ReturnUrl=%2fillinoiscampusrec')

    # Get keys
    with open('keys.json') as f:
        keys = json.load(f)
    
    if netID not in keys:
        print("You don't have your key stored")
        return False, "NoPass", taken
    
    if len(creds[netID]['Places']) == 0:
        print("No reservations for " + netID)
        return False, "NoReservations", taken

    password = creds[netID]['Password']
    place = creds[netID]['Places'][spot]
    time = creds[netID]['Times'][spot]

    # Input Credentials
    b.find_element_by_id('ctl00_pageContentHolder_loginControl_UserName').send_keys(netID)
    b.find_element_by_id('ctl00_pageContentHolder_loginControl_Password').send_keys(bmi.decrypt(password, keys[netID]))
    b.find_element_by_id('ctl00_pageContentHolder_loginControl_Login').click()

    # Wait for login
    try:
        WebDriverWait(b, delay).until(EC.presence_of_element_located((By.ID, 'menu_SCH')))
        print("Successfully Logged In!")
    except TimeoutException:
        print("Invalid Credentials")
        return False, "InvalidCreds", taken
    
    date_url = time_manager.getURL(place)
    b.get(date_url)
    print("Changed to reservation site")


    with open('reservations.json') as f:
        reservations = json.load(f)
    if reservations[place]["List"]:
        # Switch to list
        success, err = wait_for_load(b)
        if not success:
            return False, err, taken
        element = b.find_element_by_id('ancSchListView')
        webdriver.ActionChains(b).move_to_element(element).click(element).perform()

    # Select all
    success, err = wait_for_load(b)
    if not success:
        return False, err
    b.find_element_by_id('ancSchSelectAll').click()
    b.find_element_by_id('ancSchSearch').click()

    success, err = wait_for_load(b)
    if not success:
        return False, err, taken
    
    # Get the time
    print(taken)
    success, row, patron = check_if_available(b, time, taken)

    if not success:
        return False, patron, taken

    # Add to Cart
    row.find_element_by_xpath('.//*[@class="clslistViewAddToCart"]').click()
    taken.append(patron)

    # Continue
    b.find_element_by_id('btnContinue').click()

    return True, b, taken

def reserve(b):
    try:
        b.find_element_by_id('btnAcceptWaiver').click()
    except:
        return False, "FailedAccept"
    return True, b

def finish(b):
    #success, err = wait_for_load(b)
    #if not success:
    #    return False, err

    # Add to Cart
    try:
        el = WebDriverWait(b, delay).until(EC.element_to_be_clickable((By.ID, "ctl00_pageContentHolder_btnContinueCart")))
        el.click()
        #b.find_element_by_id("ctl00_pageContentHolder_btnContinueCart").click()
    except:
        print("Failed to reserve, too early!")
        return False, "FailedReserve"

def reserve_all(safety = 1):
    # Get credentials
    with open('credentials.json') as f:
        creds = json.load(f)
    
    # Preemptively reserve everyone
    print("Start Reservations for date: " + str(time_manager.get_weekdate()) + "!")
    taken = []
    browsers = []
    for i in range(safety):
        for person in creds.keys():
            for i in range(len(creds[person]["Dates"])):
                success, b, taken = preempt_reserve(person, i, taken)
                if success:
                    print("Finished reservation of spot: " + taken[-1])
                    browsers.append(b)
    
    print("Start the Wait!")
    # Wait till 7:30
    wait_till_reserve()
    for b in browsers:
        reserve(b)
    for b in browsers:
        finish(b)
    print("Finished")
    return browsers

def reserve_all_everyday(safety = 1):
    while True:
        while time_manager.check_before_start():
            t.sleep(60)
        print(time_manager.check_before_start())
        reserve_all(safety)
        

reserve_all_everyday(2)
#b = reserve_all(2)
#while True:
#    t.sleep(60)