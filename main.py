from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from datetime import datetime
import pyautogui

driver = webdriver.Chrome()
driver.implicitly_wait(4)  # wait 4 seconds every time
driver.maximize_window()
driver.refresh()

login_method = input("Would you like to log in to zoom? Answer 'no' to join without logging in"
                     " (already logged in on this computer), 'google' to log in with google,"
                     "and 'zoom' to log in to zoom directly in the browser.")
valid_login_method = False
while not valid_login_method:

    login_method = login_method.lower()
    if login_method != "no" and login_method != "google" and login_method != "zoom":
        # if given the wrong input, goes back into loop
        login_method = input("Please enter a valid login method. Your choices are 'no'"
                             "to join without logging in to zoom, 'google' to log in with google, and"
                             "'zoom' to log into zoom directly in the browser.")
    else:
        valid_login_method = True
if login_method != "no":
    # going to zoom login page
    driver.get("https://zoom.us/signin#/login")

    if login_method == "google":
        # sign in with google button on zoom page
        driver.find_element(By.XPATH,
                            "//*[contains(@class, 'zm-login-methods') and @aria-label='Sign in with Google']").click()

        # putting in email
        email = driver.find_element(By.ID, "identifierId")

    else:
        # login_method always equals zoom here
        # putting in email
        email = driver.find_element(By.ID, "email")

    user_input_email = input("Enter your email")
    email.send_keys(user_input_email)
    email.send_keys(Keys.ENTER)

    if login_method == "google":
        email_password = driver.find_element(By.NAME, "password")
    else:
        email_password = driver.find_element(By.ID, "password")

    # putting in password (not saved)
    # if you enter the wrong password you will have to restart
    email_password.send_keys(input("Enter your password"))
    email_password.send_keys(Keys.ENTER)
    # successfully logged in

meeting_link = input("Please paste the meeting link")
zoom_join_button = input("What is the file path of the zoom join button?")  # no validation

join_time = input("What time would you like to join the meeting? (military time)")  # needs to be in format 00:00

valid_time = False
while not valid_time:
    error_message = "Please enter a valid join time"
    if len(join_time) < 4 or len(join_time) > 5:
        join_time = input(error_message)
        continue

    elif len(join_time) == 4:
        join_time = "0" + join_time
    if join_time[2] != ":":
        join_time = input(error_message)
        continue

    try:
        # grabbing hour and minute
        join_hour = int(join_time[:2])
        join_minute = int(join_time[-2:])
        if (0 > join_hour) or (join_hour > 24) or (0 > join_minute) or (join_minute >= 60):
            # not a valid time

            join_time = input(error_message)
            continue
        elif join_hour == 24:
            # datetime does not work with 24, so this will change the hour from 24 to 0
            join_time = "00" + join_time[2:]
    except ValueError:
        # not convertible to int
        join_time = input(error_message)
        continue

    valid_time = True
    # must be a valid time if it passes all of these

while True:
    now = datetime.now().strftime("%H:%M")
    if now == join_time:
        # time to join meeting
        driver.get(meeting_link)

        # zoom's pop up window cannot be accessed by selenium so here pyautogui is used with a picture of the button
        # this will find the zoom meeting join confirmation button and click on it
        zoom_join_button_location = pyautogui.locateCenterOnScreen(zoom_join_button)
        while zoom_join_button_location is None:
            # tries to locate until the popup appears
            zoom_join_button_location = pyautogui.locateCenterOnScreen(zoom_join_button)
        pyautogui.moveTo(zoom_join_button_location)
        pyautogui.click()
        exit()

    else:
        print(now)
        time.sleep(30)
        # track time, wait 30 seconds
