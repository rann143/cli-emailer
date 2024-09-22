#! python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os, time

load_dotenv()  # take environment variables from .env.
username = os.environ.get("USERNAME")
password = os.environ.get("PASS")

browser = webdriver.Firefox()
wait = WebDriverWait(browser, 20)
browser.get('https://accounts.google.com')

try:
    email_element = wait.until(EC.presence_of_element_located((By.ID, "identifierId")))
    email_element.send_keys(username)
    next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']")))
    next_button.click()
except Exception as e:
    print(f'Error in email step: {str(e)}')

try:
    password_element = wait.until(EC.presence_of_element_located((By.NAME, "Passwd")))
    password_element.send_keys(password)
    submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']")))
    submit_button.click()
except Exception as e:
    print(f'Error in password step: {str(e)}')

# Wait for Gmail to load
try:
    wait.until(EC.title_contains("Inbox"))
    print("Successfully logged in!")
except Exception as e:
    print(f'Login unsuccessful: {str(e)}')

# Keep the browser open for a while to see the result
time.sleep(10)
browser.quit()


# try: 
#     email_element = browser.find_element_by_id('identifierId')
#     email_element.send_keys(username)

# except:
#     print('email element not found')


# try:
#     next_btn_element = browser.find_element_by_css_selector('button.VfPpkd-LgbsSe:nth-child(2)')
#     next_btn_element.click()
#     time.sleep(3)
# except:
#     print('next button  not found')

# try: 
#     password_element = browser.find_element_by_name('Passwd')
#     password_element.send_keys(password)
# except:
#     print('password input not found')


# try:
#     submit_btn = browser.find_element_by_css_selector('.VfPpkd-LgbsSe-OWXEXe-k8QpJ')
#     submit_btn.click()
# except:
#     print('submit btn not found')



