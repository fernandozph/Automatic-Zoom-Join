import time
from datetime import datetime
import subprocess
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pyautogui

driver = webdriver.Chrome()
driver.implicitly_wait(4)  # wait 4 seconds every time
driver.maximize_window()
driver.refresh()


def fill_out_field(element_location, input_field):
    """fill_out_field asks user for input then fills out relevant field in the webpage and submits it

    Args:
        element_location (str): Where the element is located in the page, 
        typically located through driver.find_element()
        input_field (str): What should the user be inputting, e.g. email, password
    """
    input_keys = input("Please enter your " + input_field + "\n")
    element_location.send_keys(input_keys)
    element_location.send_keys(Keys.ENTER)


# getting the user's login method, making sure it is lowercase
login_method_question = ("Would you like to log in to Zoom? Answer 'no' to join without logging in "
                         "(already logged in on this computer), 'google' to log in with google, "
                         "and 'zoom' to log in to zoom directly in the browser. (Not case sensitive)\n")
login_method = input(login_method_question).lower()

# error message to pass into valid_login_method function, if user does not enter a valid login method
error_message_login_method = ("Please enter a valid login method. Your choices are 'no' "
                              "to join without logging in to zoom, 'google' to log in with google, and "
                              "'zoom' to log into zoom directly in the browser. (Not case sensitive)\n")


def valid_login_method(login_method_input, error_message):
    """valid_login_method checks to see if the user's input is a valid login method, and
    calls itself recursively if not.

    Args:
        login_method_input (str): What the user inputted as their login method
        error_message (str): The error message to be used when asking the user to
        input their login method again

    Returns:
        str: returns the login_method_input that was passed if it is valid,
        or calls itself recursively if the input is invalid
    """
    # checks to see if it is a valid method
    if login_method_input != "no" and login_method_input != "google" and login_method_input != "zoom":
        # if it is not a valid
        return valid_login_method(input(error_message).lower(), error_message)
    # returns the same value passed in if it is either 'no', 'google', or 'zoom'
    return login_method_input


# checks to see if it is a valid login method with
login_method = valid_login_method(login_method, error_message_login_method)


def get_login(picked_login_method):
    """get_login logs in to Zoom using the user's preferred login method
    (log in through Google, Zoom, or already logged in on the app)

    Args:
        picked_login_method (str): type of login method, should only be 'google', 'zoom', or 'no'
        The string passed into this argument should always be checked with valid_login_method beforehand

    Returns:
        Boolean: True if the program successfully logged in, False otherwise.
        Only current case where this would return False is if the user attempts
        to log in with Google, and then gets blocked and can't continue to
        input their password due to Google's browser security features.
    """

    if picked_login_method == "no":
        return True
        # valid login method, don't have to do anything other than return true for 'no' case
    # going to zoom login page
    driver.get("https://zoom.us/signin#/login")

    if picked_login_method == "google":
        # sign in with Google button on Zoom page
        driver.find_element(By.XPATH,
                            "//*[contains(@class, 'zm-login-methods') and @aria-label='Sign in with Google']").click()

        # putting in email
        email = driver.find_element(By.ID, "identifierId")
    else:  # login_method = "zoom"
        # putting in email
        email = driver.find_element(By.ID, "email")

    fill_out_field(email, "email")  # same way to fill out for both google and zoom

    if picked_login_method == "zoom":
        email_password = driver.find_element(By.ID, "password")
    # after this login_method == "google"
    elif len(driver.find_elements(By.NAME, "password")) > 0:
        # find_elements will return a list of elements, with no elements if it is not found,
        # whereas find_element will throw an error if it is not found
        email_password = driver.find_element(By.NAME, "password")
    else:
        """
        there are 0 elements with the name password on the page
        login_method is "google" but user was not able to get to the password page,
        most likely stopped by google's browser security check
        """
        print("Sorry, there was an error logging you in through Google. Please try again.")
        return False  # could not log in

    # putting in password (not saved)
    fill_out_field(email_password, "password")  # same way to fill out for both google and zoom
    # if the wrong password is entered a restart is necessary

    # successfully logged in
    return True  # returns true, finished logging in


# tries to log in, if it does not work it will keep trying until it works
while not get_login(login_method):
    login_method = input(login_method_question).lower()
    login_method = valid_login_method(login_method, error_message_login_method)


def is_valid_time(specified_time):
    """is_valid_time checks to see if the  time is valid. If it is a valid time, but not valid for datetime, e.g.
    the hour is 9 instead of 09, it will correct the error and return the corrected version. If the time is not
    correctable, it returns false.

    Args:
        specified_time (str): The time the user wants to join the meeting, in military time (XX:XX) format.
        Can correct for X:XX format and 24:XX format.

    Returns:
        str: Returns 'invalid' if it is an invalid time. Returns new_specified_time if it is a valid time, corrected
    or uncorrected
    """
    # making a separate variable so that it can be edited
    new_specified_time = specified_time
    if len(new_specified_time) == 4:
        new_specified_time = "0" + specified_time
    if (len(new_specified_time) != 5) or new_specified_time[2] != ":":
        return "invalid"
    try:
        # grabbing hour and minute
        specified_hour = int(new_specified_time[:2])
        specified_minute = int(new_specified_time[-2:])
        if (0 > specified_hour) or (specified_hour > 24) or (0 > specified_minute) or (specified_minute >= 60):
            # not a valid time
            return "invalid"

        elif specified_hour == 24:
            # datetime does not work with 24, so this will change the hour (first 2 characters) from 24 to 00
            new_specified_time = "00" + new_specified_time[2:]
    except ValueError:
        # not convertible to int
        return "invalid"
    return new_specified_time


meeting_link = input("Please paste the meeting link\n")  # no validation
zoom_join_button = input(
    "What is the file path of the zoom join button?\n")  # no validation

join_time = input("What time would you like to join the meeting? (military time)\n")  # needs to be in format 00:00
# getting valid join time, restarting if it is invalid
while is_valid_time(join_time) == "invalid":
    join_time = input("Please enter a valid join time\n")

end_time = input("What time would you like to end the meeting? (military time)\n")
while is_valid_time(end_time) == "invalid":
    end_time = input("Please enter a valid end time\n")


def locate_and_click(button_path, checks):
    """finds the button on the screen and clicks it. It will try to get the location one time
    and then again for whatever number checks is, if pyautogui's built-in wait time is not long enough.

    Args:
        button_path (str): The file path to the button
        checks (int): The number of additional times to try to get the location, in case locate returns None
        Must be an integer greater than 0
    """
    button_location = pyautogui.locateCenterOnScreen(button_path, grayscale=True, confidence=0.5)
    for i in range(checks):
        if button_location is None:
            button_location = pyautogui.locateCenterOnScreen(button_path, grayscale=True, confidence=0.5)
        else:
            break
    pyautogui.moveTo(button_location)
    pyautogui.click()


while True:
    now = datetime.now().strftime("%H:%M")
    print(now)
    if now == join_time:
        # time to join meeting
        driver.get(meeting_link)

        # zoom's pop up window cannot be accessed by selenium so here pyautogui is used with a picture of the button
        # this will find the Zoom meeting join confirmation button and click on it
        locate_and_click(zoom_join_button, 5)
        break

    else:
        time.sleep(30)
        # track time, wait 30 seconds
ask_zoom_launched = ("If zoom successfully launched, please input 'Y'. "
                     "If there is a keep/discard button on the bottom left corner input 'N'. "
                     "If there is some other error, please input 'O'.\n")
zoom_launched = input(ask_zoom_launched).upper()
while zoom_launched not in {"Y", "N", "O"}:
    # keeps asking until a valid input is entered.
    zoom_launched = input(ask_zoom_launched)

if zoom_launched == "N":
    # "N" means that instead of launching, Zoom tried to download.
    # so this clicks on the keep button and then clicks on the finished download to open it.
    keep_zoom_button = input("What is the file path of the keep zoom button?\n")
    locate_and_click(keep_zoom_button, 3)
    zoom_download_button = input("What is the file path of the zoom download button?\n")
    locate_and_click(zoom_download_button, 3)
elif zoom_launched == "O":
    # "O" means that there was an unforeseen error, takes user to GitHub to open a new issue.
    driver.get("https://github.com/fernandozph/Automatic-Zoom-Join/issues/new")
    print("Please submit a new issue, thank you.")
    input("Press enter to quit")
    exit()

while True:
    now = datetime.now().strftime("%H:%M")
    if now == end_time:
        subprocess.run("TASKKILL /F /IM zoom.exe")
        # runs command to kill zoom.exe
        # safe: https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/taskkill
        break
    else:
        print(now)
        time.sleep(30)
