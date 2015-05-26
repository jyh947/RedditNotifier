# RedditNotifier
### by jyh947

#### Introduction
This is a robot for Reddit browsing, coded entirely in Python.  The purpose of this robot is to notify the user whenever the robot finds a new post containing a specific string in a list of subreddits.
#### Requirements
The user for this robot must have a Gmail account and a Reddit account with more than 1 link karma.  They must also have Python 2.7.9 with [praw]( https://praw.readthedocs.org/en/v2.1.21/), the Python Reddit api wrapper.
#### Permissions
You must allow "less secure applications" to access your gmail account.  You can do that by going [here](https://www.google.com/settings/security/lesssecureapps).  Feel free to read through any of my Python code, I am not doing anything malicious with my robot.
#### Installation
##### Python 2.7.9
To run the script, you must have the latest version of Python 2 because Tkinter, the GUI library requires the latest version of Python 2.7.  Download it [here](https://www.python.org/downloads/release/python-279/)
##### pip
If you have Python 2.7.9 installed, you should already have pip.  Using pip is the easiest way to install praw, which this program requires.  If for some reason your computer somehow does not have pip, install it from [here]( https://pypi.python.org/pypi/pip)
##### Praw
In order to install praw, go to the location where your pip application is installed in cmd.  For a majority of people, it should be in `C:\Python27\Scripts`.  Just go to the scripts folder within the folder where Python is installed in a command window.  For non-coders who don’t know what you’re doing, open a cmd window by pressing the Start button for Windows and looking for cmd.  For Mac users, open a terminal window.  Switch to the folder where pip is installed by typing `cd <location>` (for most Windows users, <location should be C:\Python27\Scripts> or wherever your scripts folder is.  Then type in `pip install praw` and wait until the download done.
##### My Script
Download my script, `notify.py`, and place it in your favorite folder.  Now, open your terminal/cmd window and type in `<location of python>\python.exe <location of my script>\notify.py`.  I would type something like `C:\Python27\python.exe C:\Users\jyh947\Documents\Python\notify.py` in my terminal window and then the program should be running!  If you added a shortcut to Python to your path variable, good for you, do what you want to.
#### Basic Usage
This following section will go over basic operations for using the robot.
##### Gmail
You must have a Gmail account to use this robot.  Log in using your username (you have the choice to include the “@gmail.com” or not) and password.  Pressing “Log Into Gmail” should momentarily freeze the client.  To the right of the “Log Into Gmail” button is a label showing your login status.  Make sure the label says “Logged Into Gmail!” before proceeding.
##### Reddit
You must also have a Reddit account (with a link karma count above 1) to use this robot.  Log in using your username and password.  Pressing “Log Into Reddit” should momentarily freeze the client.  To the right of the “Log Into Reddit” button is a label showing your login status.  Make sure the label says “Logged Into Reddit!” before proceeding.
##### Timing
Enter a number between 30 and 600 for the time between each request that you want the robot to make to the server.  Praw requires the minimum to be 30, as any number below 30 will return a cached request, rather than a new one.  The upper limit is 600 seconds to set a reasonable ceiling.
##### Search Terms
Add each term that you want to search in each subreddit, separated by comma.  These words or strings are not limited by anything besides a comma.
##### Subreddits
Add a list of every subreddit that you want the robot to search through, each subreddit being separated by a comma.
##### Target Email
You must enter a target email, which will be notified whenever the robot finds a new post in the subreddit(s) that has one of the search term(s) that you’re looking for.  You could even enter your cell phone’s mms/sms email address to receive a text message. 
##### Save Data
You have the ability to save data to a `config.cfg` file, which will reside in the same folder as my `notify.py` script.  Pressing the “Save data to config.cfg” button will save your Gmail username, Reddit username, sleep time, search term(s), subreddit list, and target email information.
##### Start Automation
After logging into Gmail and Reddit, you should be able to check the “Start Automation” checkbox.  If the sleep time, search term(s), or subreddit list entries are incorrect, you will be notified.  The automation will not start until all the fields are valid.  By starting the automation process, the robot will automatically scan all the subreddits that you list for all the search term(s) you list and notify you whenever it finds a new post with those search term(s) to both your own Reddit account inbox and the target email that you entered.
##### Output
The output section will update with information about what the robot is doing.  It might make no sense to you. More or less, it’s just there to tell you that the robot is still running.
