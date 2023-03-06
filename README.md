# Automatic-Zoom-Join
This a proof of concept and project for my IT/CS2 class that was developed into a program to automatically log in to, join, and leave zoom meetings.

This program uses Selenium WebDriver to log you in to Zoom, or Google, with the user inputting login method and information.
* It was challenging to log in to Zoom with Google, as there is no direct link, or idenitfier/name for the buttom, so I had to use XPath.

This program uses PyAutoGUI to click on the pop-up confirming that the user wants to open the Zoom meeting, as that is outside Selenium's scope.

### Errors: ###
* There is an error with Chrome blocking sign in due to an "unsecure browser" because it is automated.
* There is an error with Zoom not launching because it tries to install Zoom again

### Working on: ###
* More validation for user inputs
* End time for meetings to automatically leave
* Using WebDriverWait instead of time.sleep
* Possibly using undetected-chromedriver to bypass restrictions on logins through what Google thinks is an "unsecure browser"

` Made with Mohammed Musawwir and taking inspiration from Sai Anish Malla for PyAutoGUI and date/time. Made for Dr. Eric Wu's Information Technology and Cybersecurity class in 2021. Last updated March 2023. `
