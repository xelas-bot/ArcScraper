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


#taken_patrons = [("04:30 PM" , "ARC Lower Level - Patron 1"), ('04:30 PM', 'ARC Lower Level - Patron 10'),('04:30 PM', 'ARC Lower Level - Patron 8'),('04:30 PM', 'ARC Lower Level - Patron 12'), ('04:30 PM', 'ARC Lower Level - Patron 16'),('04:30 PM', 'ARC Lower Level - Patron 14'),('04:30 PM', 'ARC Lower Level - Patron 2'),('04:30 PM', 'ARC Lower Level - Patron 6'),('04:30 PM', 'ARC Lower Level - Patron 17')]

taken_patrons = [("04:30 PM" , "ARC Lower Level - Patron 1")]
main.EnterInfo()


# Delay
delay = 30

def manage_reserve():
   pass 

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
    print(str(bmi.decrypt(password,keys[netID])))
    b.find_element_by_id('ctl00_pageContentHolder_loginControl_Password').send_keys(str(bmi.decrypt(password,keys[netID])))
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
    
    dg = b.find_elements_by_xpath('//*[@class="DgText"]')
    dgAlt = b.find_elements_by_xpath('//*[@class="DgTextAlt"]')

    altStartTimes = [t.find_element_by_xpath('.//*[@align="center"]').text for t in dgAlt]
    altPatrons = [t.find_element_by_xpath('.//*[@class="clstdResurce"]').text for t in dgAlt]

    StartTimes = [t.find_element_by_xpath('.//*[@align="center"]').text for t in dg]
    Patrons = [t.find_element_by_xpath('.//*[@class="clstdResurce"]').text for t in dg]

    current_slots = []

    for (t,p) in zip(altStartTimes, altPatrons):
        current_slots.append((t,p))

    for (t,p) in zip(StartTimes, Patrons):
        current_slots.append((t,p))

    located_slot =0










    # Flip to the Right Time
    # for now this will work considering a group reserves the same time, if solo then it will always work
    if (len(taken_patrons) ==0):
        while not time in start_times:
            print("BRUH MOMENTO")
            try:
                b.find_element_by_id('ancSchListNext').click()
                times_list = b.find_elements_by_xpath('//*[@class="DgText"]') + b.find_elements_by_xpath('//*[@class="DgTextAlt"]')
                start_times = [t.find_element_by_xpath('.//*[@align="center"]').text for t in times_list]
                patrons_list = [t.find_element_by_xpath('.//*[@class="clstdResurce"]').text for t in times_list]

                located_slot = ()



            
                

                #temp = [t.find_element_by_xpath('.//*[@class="clstdResurce"]').text for t in times_list]
                #patrons_list = filter_pats(order_patrons=temp,timeslots=start_times,time=time)




            except Exception as e:
                print(e)
                print("Failed to find time")
                return False, "ExceedLoadTime"
    else :

        overlap = True
        time_slot_found = False

        print("test")
        
        try:
            slot_flagged = False
            current_slots = []
            

            while not time_slot_found:
                current_slots = []
                dg = b.find_elements_by_xpath('//*[@class="DgText"]')
                dgAlt = b.find_elements_by_xpath('//*[@class="DgTextAlt"]')
                times_list = dg + dgAlt

                altStartTimes = [t.find_element_by_xpath('.//*[@align="center"]').text for t in dgAlt]
                altPatrons = [t.find_element_by_xpath('.//*[@class="clstdResurce"]').text for t in dgAlt]

                StartTimes = [t.find_element_by_xpath('.//*[@align="center"]').text for t in dg]
                Patrons = [t.find_element_by_xpath('.//*[@class="clstdResurce"]').text for t in dg]

                for (t,p) in zip(altStartTimes, altPatrons):
                    current_slots.append((t,p))

                for (t,p) in zip(StartTimes, Patrons):
                    current_slots.append((t,p))


                for (time_, patron_) in current_slots:
                    if time_ == time:
                        time_slot_found = True
                
                if time_slot_found:
                    #overlap = True
                    break
                else:
                    b.find_element_by_id('ancSchListNext').click()

            
            while(overlap):
                ##regen current slots given new browser
                current_slots = []
                dg = b.find_elements_by_xpath('//*[@class="DgText"]')
                dgAlt = b.find_elements_by_xpath('//*[@class="DgTextAlt"]')
                times_list = dg + dgAlt

                altStartTimes = [t.find_element_by_xpath('.//*[@align="center"]').text for t in dgAlt]
                altPatrons = [t.find_element_by_xpath('.//*[@class="clstdResurce"]').text for t in dgAlt]

                StartTimes = [t.find_element_by_xpath('.//*[@align="center"]').text for t in dg]
                Patrons = [t.find_element_by_xpath('.//*[@class="clstdResurce"]').text for t in dg]

                for (t,p) in zip(altStartTimes, altPatrons):
                    current_slots.append((t,p))

                for (t,p) in zip(StartTimes, Patrons):
                    current_slots.append((t,p))


                located_slot = find_valid_slot_in_b(available_slots=current_slots,taken_slots=taken_patrons,time=time_)
                if len(located_slot) == 0:
                    b.find_element_by_id('ancSchListNext').click()
                else:
                    overlap = False

        except:
            print("Failed to find time")
            return False, "ExceedLoadTime"
            




    # Get the index
    index = 0
    print(located_slot)

    for element in times_list:
        time = element.find_element_by_xpath('.//*[@align="center"]').text
        patron = element.find_element_by_xpath('.//*[@class="clstdResurce"]').text
        if time == located_slot[0] and patron == located_slot[1]:
            break

        index = index +1


    

    # Add to Cart
    times_list[index].find_element_by_xpath('.//*[@class="clslistViewAddToCart"]').click()
    ## Fill patrons
    taken_patrons.append((times_list[index].find_element_by_xpath('.//*[@align="center"]').text, times_list[index].find_element_by_xpath('.//*[@class="clstdResurce"]').text))
    
    ##print(taken_patrons)
    ##print(times_list[index].find_element_by_xpath('.//*[@class="clstdResurce"]').text)



    b.find_element_by_id('btnContinue').click()

    return True, b


def find_valid_slot_in_b(available_slots, taken_slots, time):
    slot_to_return = ()
    flag = True
    print(available_slots)

    for (time_, patron_) in available_slots:
        flag = True
        for (t,p) in taken_slots:
            if time_ == time:
                if patron_ == p:
                    flag = False
        if flag and time_ == time:
            slot_to_return = (time_,patron_)
            return slot_to_return

    return slot_to_return

        
    





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

success_a, a_b = preempt_reserve("weedindenver")

success_b, b_b = preempt_reserve("apaarb2")
success_c, c_b = preempt_reserve("dlzhang2")
success_d, d_b = preempt_reserve("sarangmohaniraj")
success_e, e_b = preempt_reserve("404839WTang")

success_f, f_b = preempt_reserve("shreysp3")
success_f, f_b = preempt_reserve("atli3")



while time_manager.check_before_midnight():
    t.sleep(1)


t.sleep(60)
reserve(a_b)
reserve(b_b)
reserve(c_b)

reserve(d_b)
reserve(e_b)
reserve(f_b)
