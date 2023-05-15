# Automatic-Zoom-Join
This a proof of concept and project for my IT/CS2 class that was developed into a program to automatically log in to, join, and leave zoom meetings.

This program uses Selenium WebDriver to log you in to Zoom, or Google, with the user inputting login method and information.
* It was challenging to log in to Zoom with Google, as there is no direct link, or idenitfier/name for the buttom, so I had to use XPath.

This program then takes in the time to join and leave the meeting, and when it is time to join uses PyAutoGUI to click on the pop-up confirming that the user wants to open the Zoom meeting, as that is outside Selenium's scope.
If zoom attempts to download, the program will use PyAutoGUI to click on the "keep download" button, and then launch zoom.
Finally, at the end time of the meeting it uses the taskkill command to terminate the Zoom.exe process.

## Update 1.3 ##
* Added default filepaths for the various buttons so the user doesn't have to input the filepath every time, unless the default filepath is invalid

## Update 1.2 ##
* Fixed error with Zoom starting a download instead of launching
* Fixed error with program crashing after sign in is blocked by Google, now asks the user to pick a method again
* Added confidence modifiers to PyAutoGUI functions due to screenshot pixels not matching what PyAutoGUI sees
* Added end time, terminates Zoom.exe process when the time is reached
    ### Quality of Life Changes: ###
    * Improved efficiency with functions, added docstrings
    * Improved readability of input statements
    * Added more error handling; added an option to submit a new issue on GitHub

### Errors: ###
* There is an error with Chrome blocking sign in due to an "unsecure browser" because it is automated.
* There is an error with Zoom sign in timing out, likely due to the same reason.

### Working on: ###
* Possibly using undetected-chromedriver to bypass restrictions on logins through what Google thinks is an "unsecure browser"

` Initially created with Mohammed Musawwir for Dr. Eric Wu's Information Technology and Cybersecurity class in 2021, and taking inspiration from sai Anish Malla for PyAutoGUI and datetime. Improved to add more functionality, error handling, and bug fixes. Last updated May 2023. `
