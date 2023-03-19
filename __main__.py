from time import sleep
from datetime import datetime
import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

#open a browser window
browser  = webdriver.Chrome(ChromeDriverManager().install())
WAIT = WebDriverWait(browser, 30, poll_frequency=2)

#only urls we care about
MAIN_URL = 'https://www.onlyfans.com/'
SUBS_URL = 'https://onlyfans.com/my/subscribers'

#creds
USERNAME = 'example@example.com'
PASS = 'Passw0rd'

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

#wait for login
try:
    print("waiting for login check...")
    sleep(10) #give time for captcha
    WAIT.until(EC.visibility_of_element_located((By.CLASS_NAME, 'b-make-post__main-wrapper')))
    print("OnlyFans login successful!")
    print("login successful")
except TimeoutException as te:
    print(str(te))
    print("Login Failure: Timed Out! Please check your credentials.")
    print(": If the problem persists, OnlySnarf may require an update.")
    exit()
except Exception as e:
    print("OnlyFans login failure")
    print(e)
    exit()

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
    try:
        WAIT.until(EC.presence_of_element_located((By.CLASS_NAME, 'b-users__item.m-fans')))
        fans = browser.find_elements(By.CLASS_NAME, 'b-users__item.m-fans')
        for fan in fans:
            fan_user_name = str(fan.find_element(By.CLASS_NAME, 'b-username').get_attribute('href')).split("/")[-1]
            print("Blocking ", fan_user_name)
            sleep(random.randint(1, 10))
            fan.find_element(By.CLASS_NAME, 'b-dropdown-dots-wrapper.has-tooltip').click()
            block_button = WAIT.until(EC.presence_of_element_located((By.CLASS_NAME, 'dropdown-menu.dropdown-menu-right.show'))).find_elements(By.XPATH, "./child::*")[-2]
            sleep(random.randint(1, 10))
            block_button.click()
            radios = WAIT.until(EC.presence_of_element_located((By.CLASS_NAME, 'modal-body'))).find_elements(By.XPATH, "./child::*")
            block_user = None
            for radio in radios:
                if "Block user from accessing your profile." in radio.find_element(By.CLASS_NAME, 'b-input-radio__text').text:
                    block_user = radio
                    break
            if not block_user:
                assert TimeoutException
            sleep(random.randint(1, 10))
            block_user.click()
            confirm_button = browser.find_element(By.CLASS_NAME, 'modal-footer').find_elements(By.XPATH, "./child::*")[1]
            sleep(random.randint(1, 10))
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