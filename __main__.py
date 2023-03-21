from time import sleep
from datetime import datetime
import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

#open a browser window
options = Options()
options.add_argument("--allow-insecure-localhost")
options.add_argument("--no-sandbox") # Bypass OS security model
# possibly linux only
options.add_argument('disable-notifications')
options.add_argument("--disable-gpu")
options.add_argument("--disable-crash-reporter")
options.add_argument("--disable-extensions")
options.add_argument("--disable-infobars")
options.add_argument("--disable-in-process-stack-traces")
options.add_argument("--disable-logging")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--log-level=3")
options.add_argument("--output=/dev/null")
browser  = webdriver.Chrome(options=options)
WAIT = WebDriverWait(browser, 30, poll_frequency=2)

#only urls we care about
MAIN_URL = 'https://www.onlyfans.com/'
SUBS_URL = 'https://onlyfans.com/my/subscribers/expired'

#creds
USERNAME = 'example@example.com'
PASS = 'Passw0rd'

def loginCheck():
    #wait for login
    try:
        print("waiting for login check...")
        sleep(10) #give time for captcha
        WAIT.until(EC.visibility_of_element_located((By.CLASS_NAME, 'b-make-post__main-wrapper')))
        print("OnlyFans login successful!")
        print("login successful")
        return True
    except TimeoutException as te:
        print(str(te))
        print("Login Failure: Timed Out! Please check your credentials.")
        print(": If the problem persists, OnlySnarf may require an update.")
        return False
    except Exception as e:
        print("OnlyFans login failure")
        print(e)
        return False

def login():
    # Open OF
    browser.get(MAIN_URL)

    #login
    username_field = WAIT.until(EC.presence_of_element_located((By.NAME, "email")))
    password_field = WAIT.until(EC.presence_of_element_located((By.NAME, "password")))
    username_field.click()
    username_field.send_keys(USERNAME)
    password_field.click()
    password_field.send_keys(PASS)
    sleep(3)
    browser.find_element(By.CLASS_NAME, 'g-btn.m-rounded.m-block.m-md.mb-0').click()

login()
loginCheck()
#goto subscribers page
browser.get(SUBS_URL)

#do the blocking
num_blocked = 0
while True:
    #daily block limit is 50
    if num_blocked >= 50:
        while (datetime.now().hour != 10):
            sleep(60)
        num_blocked = 0
        browser.get(MAIN_URL)
        if loginCheck() == False:
            login()
    try:
        WAIT.until(EC.presence_of_element_located((By.CLASS_NAME, 'b-users__item.m-fans')))
        fans = browser.find_elements(By.CLASS_NAME, 'b-users__item.m-fans')
        for fan in fans:
            fan_user_name = str(fan.find_element(By.CLASS_NAME, 'b-username').get_attribute('href')).split("/")[-1]
            print("Blocking ", fan_user_name)
            sleep(random.randint(2, 5))
            fan.find_element(By.CLASS_NAME, 'b-dropdown-dots-wrapper.has-tooltip').click()
            block_button = WAIT.until(EC.presence_of_element_located((By.CLASS_NAME, 'dropdown-menu.dropdown-menu-right.show'))).find_elements(By.XPATH, "./child::*")[-2]
            sleep(random.randint(2, 5))
            block_button.click()
            radios = WAIT.until(EC.presence_of_element_located((By.CLASS_NAME, 'modal-body'))).find_elements(By.XPATH, "./child::*")
            block_user = None
            for radio in radios:
                if "Block user from accessing your profile." in radio.find_element(By.CLASS_NAME, 'b-input-radio__text').text:
                    block_user = radio.find_element(By.CLASS_NAME, 'b-input-radio__container')
                    break
            if not block_user:
                assert Exception
            sleep(random.randint(2, 5))
            block_user.click()
            confirm_button = browser.find_element(By.CLASS_NAME, 'modal-footer').find_elements(By.XPATH, "./child::*")[1]
            sleep(random.randint(2, 5))
            confirm_button.click()
            num_blocked = num_blocked + 1
            break
        #can only block 1 user every 60 seconds
        sleep(random.randint(80, 200))
        browser.get(SUBS_URL) #refresh the page
    except KeyboardInterrupt:
        exit()
    except TimeoutException:
        print("No fans left!!")
    except Exception as e:
        print (e)
        browser.get(SUBS_URL) #refresh the page