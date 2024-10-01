#! python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
import os, time, sys

load_dotenv()  # take environment variables from .env.
username = os.environ.get("USERNAME")
password = os.environ.get("PASS")

email_recipient = input("What is the recipient's email address?\n\n")
email_subject = input("what is your email's subject?\n\n")
email_body = input("Please write the body of your email\n\n")


browser = webdriver.Firefox()
wait = WebDriverWait(browser, 20)
browser.get('https://accounts.google.com')

original_window = browser.current_window_handle

try:
    email_element = wait.until(EC.presence_of_element_located((By.ID, "identifierId")))
    email_element.send_keys(username)
    next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']")))
    next_button.click()
except Exception as e:
    print(f'Error in email step: {str(e)}')

try:
    password_element = wait.until(EC.element_to_be_clickable((By.NAME, "Passwd")))
    password_element.send_keys(password)
    submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']")))
    submit_button.click()
except Exception as e:
    print(f'Error in password step: {str(e)}')

# Wait for Google Account Page to load
try:
    wait.until(EC.title_contains("Google Account"))
    print("Successfully logged in!")
except Exception as e:
    print(f'Login unsuccessful: {str(e)}')

try:
    apps_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='gbwa']/div/a")))
    apps_button.click()
    print("opened apps menu")
    iframe = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[name='app']")))
    browser.switch_to.frame(iframe)
    print("switched to iframe")
    gmail_button = wait.until( EC.element_to_be_clickable((By.XPATH, "//*[@id='yDmH0d']/c-wiz/div/div/c-wiz/div/div/div[2]/div[2]/div[1]/ul/li[7]/a")))
    gmail_button.click()

except Exception as e:
    print(f"An unexpected error occurred: {e}")
    browser.quit()  # Close the browser
    sys.exit(1)  # Exit the program with a non-zero status code

wait.until(EC.number_of_windows_to_be(2))
print('opened gmail')

# switch to newly opened gmail tab
for window_handle in browser.window_handles:
    if window_handle != original_window:
        browser.switch_to.window(window_handle)
        break

WebDriverWait(browser, 10).until(EC.title_contains("Inbox"))

# Open email composer using 'c' key shortcut
html = wait.until(EC.presence_of_element_located((By.TAG_NAME, "html")))
body = wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
html.send_keys('c')
compose_box = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[role='dialog']")))

# Get 'To' field
to_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[aria-label='To recipients']")))
# enter recipient email
to_input.send_keys(email_recipient)
# Go to next input (subject)
to_input.send_keys(Keys.TAB)
to_input.send_keys(Keys.TAB)

# Get subject field
subject_input = browser.switch_to.active_element
# enter subject text
subject_input.send_keys(email_subject)
# Go to next input (body)
subject_input.send_keys(Keys.TAB)

# Get Message Body
body_input = browser.switch_to.active_element
# enter body text
body_input.send_keys(email_body)
# send email
body_input.send_keys(Keys.TAB)

send_button = browser.switch_to.active_element
send_button.click()
print("email sent successfully!")

# Keep the browser open for a while to see the result
time.sleep(5)
browser.quit()


