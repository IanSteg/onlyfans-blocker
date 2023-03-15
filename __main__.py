from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

#open a browser window
browser  = webdriver.Chrome()
WAIT = WebDriverWait(browser, 16, poll_frequency=2)

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
while True:
    try:
        WAIT.until(EC.presence_of_element_located((By.CLASS_NAME, 'b-users__item.m-fans')))
        fans = browser.find_elements(By.CLASS_NAME, 'b-users__item.m-fans')
        if len(fans) == 0:
            print("No fans left!!")
            exit()
        for fan in fans:
            fan_user_name = str(fan.find_element(By.CLASS_NAME, 'b-username').get_attribute('href')).split("/")[-1]
            print("Blocking ", fan_user_name)
            fan.find_element(By.CLASS_NAME, 'b-dropdown-dots-wrapper.has-tooltip').click()
            block_button = WAIT.until(EC.presence_of_element_located((By.CLASS_NAME, 'dropdown-menu.dropdown-menu-right.show'))).find_elements(By.XPATH, "./child::*")[9]
            block_button.click()
            WAIT.until(EC.presence_of_element_located((By.CLASS_NAME, 'modal-body')))
            block_user = browser.find_elements(By.CLASS_NAME, 'b-input-radio__container')[-2]
            block_user.click()
            confirm_button = browser.find_element(By.CLASS_NAME, 'modal-footer').find_elements(By.XPATH, "./child::*")[1]
            confirm_button.click()
            break
        #can only block 1 user every 60 seconds
        sleep(61)
    except KeyboardInterrupt:
        exit()