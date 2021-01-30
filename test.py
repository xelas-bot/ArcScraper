from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import json
import date as time_manager
from datetime import datetime, time
import datetime

if (time_manager.start_reservation_process(start_time=datetime.time(10,00))):
    # Initiate the browser
    b  = webdriver.Chrome(ChromeDriverManager().install())

    # Open the Website
    b.get('https://hnd-p-ols.spectrumng.net/IllinoisCampusRec/Members/Scheduler/BookSchedule.aspx?siteid=1335&catid=252248be-af49-4103-8ad9-b8a67e3f2997&provid=0&serviceid=63e2a31a-d469-4d90-b2c9-e1da4acb8d4e&d=01/29/2021&du=0')

    

# Scheduler
b.find_element_by_id('menu_SCH').click()

try:
    myElem = WebDriverWait(b, delay).until(EC.presence_of_element_located((By.ID, 'divContainer')))
    print("Loaded Menu!")
except TimeoutException:
    print("Failed to Load Menu")
    exit()

# ARC Workout
b.find_element_by_xpath('//*[@title="ARC Workout Spaces"]').click()

try:
    myElem = WebDriverWait(b, delay).until(EC.presence_of_element_located((By.ID, 'divContainer')))
    print("Loaded Places!")
except TimeoutException:
    print("Failed to Load Places")
    exit()

# Lower Level
b.find_element_by_xpath('//*[@title="ARC Lower Level Reservations"]').click()

# Continue
b.find_element_by_id('btnContinue').click()

try:
    element = WebDriverWait(b, delay).until(EC.element_to_be_clickable((By.ID, "ancSchCalenderView")))
    print("Loaded Calendar!")
except TimeoutException:
    print("Failed to Load Calendar")
    exit()

try:
    WebDriverWait(b, delay).until(EC.invisibility_of_element_located((By.ID, "tblProgess")))
    print("Load done")
except TimeoutException:
    print("???")
    exit()

# Calendar
element = b.find_element_by_id('ancSchCalenderView')
webdriver.ActionChains(b).move_to_element(element).click(element).perform()

# Next button
b.find_element_by_id('ancSchCalendarNextDate').click()
try:
    WebDriverWait(b, delay).until(EC.invisibility_of_element_located((By.ID, "tblProgess")))
    print("Load done")
except TimeoutException:
    print("???")
    exit()
b.find_element_by_id('ancSchCalendarNextDate').click()
try:
    WebDriverWait(b, delay).until(EC.invisibility_of_element_located((By.ID, "tblProgess")))
    print("Load done")
except TimeoutException:
    print("???")
    exit()
b.find_element_by_id('ancSchCalendarNextDate').click()
try:
    WebDriverWait(b, delay).until(EC.invisibility_of_element_located((By.ID, "tblProgess")))
    print("Load done")
except TimeoutException:
    print("???")
    exit()
b.find_element_by_id('ancSchCalendarNextDate').click()

try:
    WebDriverWait(b, delay).until(EC.invisibility_of_element_located((By.ID, "tblProgess")))
    print("Load done")
except TimeoutException:
    print("???")
    exit()
b.find_element_by_id('divbookingbottom').click()