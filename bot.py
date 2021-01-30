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
import input as main
import time as t

main.EnterInfo()



# Delay
delay = 30

def manage_reserve():
    taken = []

def preempt_reserve(netID, spot = 0):
    b  = webdriver.Chrome(ChromeDriverManager().install())

    # Open the Website
    b.get('https://hnd-p-ols.spectrumng.net/IllinoisCampusRec/Login.aspx?ReturnUrl=%2fillinoiscampusrec')

    # Get credentials
    with open('credentials.json') as f:
        creds = json.load(f)
    
    # Get keys
    with open('keys.json') as f:
        keys = json.load(f)
    
    # Get places
    with open('reservations.json') as f:
        places = json.load(f)
    
    if netID not in keys:
        print("You don't have your key stored")
        return False, "NoPass"

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
        print("Successfully Logged In as", " ", netID)
    except TimeoutException:
        print("Invalid Credentials")
        return False, "InvalidCreds"
    
    date_url = time_manager.getURL(place)
    b.get(date_url)

    try:
        WebDriverWait(b, delay).until(EC.invisibility_of_element_located((By.ID, "tblProgess")))
        print("Load done")
    except TimeoutException:
        print("???")
        return False, "ExceedLoadTime"
    print("Changed to reservation site")

    if place[0]:
        # Switch to list
        element = b.find_element_by_id('ancSchListView')
        webdriver.ActionChains(b).move_to_element(element).click(element).perform()
        pass

    # Select all
    b.find_element_by_id('ancSchSelectAll').click()
    b.find_element_by_id('ancSchSearch').click()

    try:
        WebDriverWait(b, delay).until(EC.invisibility_of_element_located((By.ID, "tblProgess")))
        print("Load done")
    except TimeoutException:
        print("???")
        return False, "ExceedLoadTime"

    # Find Reservation Time
    times_list = b.find_elements_by_xpath('//*[@class="DgText"]') + b.find_elements_by_xpath('//*[@class="DgTextAlt"]')
    start_times = [t.find_element_by_xpath('.//*[@align="center"]').text for t in times_list]

    # Flip to the Right Time
    while not time in start_times:
        try:
            b.find_element_by_id('ancSchListNext').click()
            times_list = b.find_elements_by_xpath('//*[@class="DgText"]') + b.find_elements_by_xpath('//*[@class="DgTextAlt"]')
            start_times = [t.find_element_by_xpath('.//*[@align="center"]').text for t in times_list]
        except:
            print("Failed to find time")
            return False, "ExceedLoadTime"
        
    # Get the index
    index = start_times.index(time)

    # Add to Cart
    times_list[index].find_element_by_xpath('.//*[@class="clslistViewAddToCart"]').click()


    b.find_element_by_id('btnContinue').click()

    return True, b

def reserve(b):
    try:
        b.find_element_by_id('btnAcceptWaiver').click()
    except:
        pass

    try:
        WebDriverWait(b, delay).until(EC.invisibility_of_element_located((By.ID, "tblProgess")))
        print("Load done")
    except TimeoutException:
        print("???")
        return False, "ExceedLoadTime"

    # Add to Cart
    try:
        b.find_element_by_id('ctl00_pageContentHolder_btnContinueCart').click()
    except:
        print("Failed to reserve, too early!")
        return False, "FailedReserve"
    
    return True

print(time_manager.check_before_midnight())


success_dlz, b_dlz = preempt_reserve("dlzhang2")
success_ssp, b_ssp = preempt_reserve("shreysp3")

while time_manager.check_before_midnight():
    t.sleep(1)


if success_dlz:
    reserve(b_dlz)
if success_ssp:
    reserve(b_ssp)
