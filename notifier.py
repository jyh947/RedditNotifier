import praw
import time
import smtplib
import getpass
import Tkinter as tk
import ConfigParser
import tkMessageBox
import threading

class ParseInput(object):
    def Gmail(self):
        global gui
        global server
        global GMAIL_USERNAME
        global GMAIL_LOGIN_var
        global GMAIL_USERNAME_entry
        global GMAIL_PASSWORD_entry

        GMAIL_USERNAME = GMAIL_USERNAME_entry.get()
        GMAIL_PASSWORD = GMAIL_PASSWORD_entry.get()
        GMAIL_USERNAME.replace(' ', '')
        if GMAIL_USERNAME.find('@gmail.com') == -1:
            GMAIL_USERNAME += '@gmail.com'

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        try:
            server.login(GMAIL_USERNAME, GMAIL_PASSWORD)
            print 'Correct password!'
            GMAIL_LOGIN_var.set('Logged Into Gmail!')
            return 1
        except Exception as detail:
            tkMessageBox.showerror(title = 'Error!', message = 'Your Gmail password is incorrect!', parent = gui)
            print detail
            print 'Incorrect password! Please try again!'
            GMAIL_LOGIN_var.set('Not Logged In!')
            return 0
    def Reddit(self):
        global reddit
        global gui
        global REDDIT_USERNAME
        global REDDIT_LOGIN_var
        global REDDIT_USERNAME_entry
        global REDDIT_PASSWORD_entry

        REDDIT_USERNAME = REDDIT_USERNAME_entry.get()
        REDDIT_PASSWORD = REDDIT_PASSWORD_entry.get()
        if len(REDDIT_PASSWORD) == 0:
            REDDIT_PASSWORD += 'a'
        reddit = praw.Reddit(user_agent = 'string checker by /u/PC4U v1.1')
        try:
            user = reddit.get_redditor(REDDIT_USERNAME)
        except Exception as detail:
            tkMessageBox.showerror(title = 'Error!', message = 'Your Reddit username does not exist!', parent = gui)
            print detail
            print 'Incorrect password! Please try again!'
            REDDIT_LOGIN_var.set('Not Logged In!')
            return 0
        if user.link_karma < 0:
            tkMessageBox.showerror(title = 'Error!', message = 'You must have at least 1 link karma!', parent = gui)
            return 0
        # authentication
        try:
            reddit.login(REDDIT_USERNAME, REDDIT_PASSWORD)
            print 'Correct password!'
            REDDIT_LOGIN_var.set('Logged Into Reddit!')
            return 1
        except Exception as detail:
            tkMessageBox.showerror(title = 'Error!', message = 'Your Reddit password is incorrect!', parent = gui)
            print detail
            print 'Incorrect password! Please try again!'
            REDDIT_LOGIN_var.set('Not Logged In!')
            return 0

    def Save(self):
        global sleep_time_entry
        global search_term_entry
        global subreddit_string_entry
        global TARGET_EMAIL_entry
        global GMAIL_USERNAME_entry
        global REDDIT_USERNAME_entry
        global sleep_time
        global search_term
        global subreddit_string
        global TARGET_EMAIL

        sleep_time = int(sleep_time_entry.get())
        search_term = search_term_entry.get()
        subreddit_string = subreddit_string_entry.get()
        TARGET_EMAIL = TARGET_EMAIL_entry.get()
        TEMP_GMAIL_USERNAME = GMAIL_USERNAME_entry.get()
        TEMP_REDDIT_USERNAME = REDDIT_USERNAME_entry.get()

        cfgfile = open('config.cfg','w')
        Config = ConfigParser.ConfigParser()
        Config.add_section('Main')
        Config.set('Main', 'sleep_time', sleep_time)
        Config.set('Main', 'search_term', search_term)
        Config.set('Main', 'subreddit_string', subreddit_string)
        Config.set('Main', 'TARGET_EMAIL', TARGET_EMAIL)
        Config.set('Main', 'GMAIL_USERNAME', TEMP_GMAIL_USERNAME)
        Config.set('Main', 'REDDIT_USERNAME', TEMP_REDDIT_USERNAME)
        Config.write(cfgfile)
        cfgfile.close()
        print 'Saving worked!'

    def Start(self):
        global gui
        global reddit
        global server
        global sleep_time_entry
        global search_term_entry
        global subreddit_string_entry
        global TARGET_EMAIL_entry
        global sleep_time
        global search_term
        global subreddit_string
        global TARGET_EMAIL
        global GMAIL_USERNAME
        global REDDIT_USERNAME
        global GMAIL_LOGIN_var
        global REDDIT_LOGIN_var
        global START_button
        global START_button_var
        global one_loop

        if not START_button_var.get():
            return 0
        if GMAIL_LOGIN_var.get() != 'Logged Into Gmail!' or REDDIT_LOGIN_var.get() != 'Logged Into Reddit!':
            START_button.deselect()
            tkMessageBox.showerror(title = 'Error!', message = 'Please login to both Gmail and Reddit!', parent = gui)
            return 0

        sleep_time = int(sleep_time_entry.get())
        search_term = search_term_entry.get()
        subreddit_string = subreddit_string_entry.get()
        TARGET_EMAIL = TARGET_EMAIL_entry.get()
        stale_post_time = 600

        search_terms = []
        subreddits = []
        all_posts = []
        messages_to_notify_user_about = []
        messages_already_sent = []

        search_term_list = search_term.split(',')
        for search_term_iter in search_term_list:
            search_term_iter = search_term_iter.strip()
            print 'Adding', search_term_iter
            search_terms.append(search_term_iter)

        subreddit_string_list = subreddit_string.split(',')
        for subreddit in subreddit_string_list:
            subreddit = subreddit.strip()
            print 'Adding', subreddit
            if subreddit.isalnum() or subreddit.find('_'):
                subreddits.append(reddit.get_subreddit(subreddit))
            else:
                tkMessageBox.showerror(title = 'Error!', message = 'Subreddit: "' + subreddit + '" does not exist!', parent = gui)
        def looping():
            global one_loop
            while START_button_var.get():
                # get current time
                current_time = time.time()
                posts_this_round = []
                # get 10 new posts and place into all_posts
                for subreddit in subreddits:
                    posts_to_grab = 10
                    prev_posts = 6000
                    new_posts = 6000
                    while prev_posts == new_posts:
                        prev_posts = posts_to_grab
                        new_posts = 0
                        posts_this_subreddit = []
                        for submission in subreddit.get_new(limit = posts_to_grab):
                            if submission not in all_posts and submission not in posts_this_round and (current_time - submission.created_utc) < stale_post_time:
                                posts_this_subreddit.append(submission)
                                new_posts += 1
                        posts_to_grab *= 2
                    for post in posts_this_subreddit:
                        if post not in posts_this_round:
                            posts_this_round.append(post)

                print 'Found', len(posts_this_round), 'new posts that have been added to the array'

                # put new posts with search term into messages_to_notify_user_about
                not_notified_posts = 0
                for new_post in posts_this_round:
                    for temp_search_term in search_terms:
                        if new_post.title.lower().find(temp_search_term) != -1 and new_post not in messages_to_notify_user_about:
                            messages_to_notify_user_about.append(new_post)
                            not_notified_posts += 1
                        elif new_post.is_self and new_post.selftext.lower().find(temp_search_term) != -1 and new_post not in messages_to_notify_user_about:
                            messages_to_notify_user_about.append(new_post)
                            not_notified_posts += 1

                print 'Found', not_notified_posts, 'new posts that need to be sent to the user'

                # put all posts that need to be sent to the user in messages_already_sent
                for to_send in messages_to_notify_user_about:
                    if to_send not in messages_already_sent:
                        message_to_send = 'New post with something from ' + search_term + ' in it from /r/' + str(to_send.subreddit) + '\n\n' + to_send.permalink + '\n\n'
                        if to_send.is_self:
                            message_to_send += 'Self text here:\n\n'
                            message_to_send += to_send.selftext
                        reddit.send_message(REDDIT_USERNAME, 'New message found!', message_to_send)
                        server.sendmail(GMAIL_USERNAME, TARGET_EMAIL, message_to_send)
                        messages_already_sent.append(to_send)

                # push new posts into queue
                for post in posts_this_round:
                    all_posts.append(post)

                # clear posts older than 'stale_post_time' seconds old
                print 'Clean-up time'
                cleanup(all_posts, current_time, stale_post_time)
                cleanup(messages_to_notify_user_about, current_time, stale_post_time)
                cleanup(messages_already_sent, current_time, stale_post_time)

                #let script sleep for 'sleep_time' seconds
                print 'Waiting', sleep_time, 'seconds'
                for integer in range(sleep_time):
                    time.sleep(1)
                    if not START_button_var.get():
                        print 'Exiting thread'
                        one_loop = False
                        return
            print 'Exiting thread'
            one_loop = False
        if not one_loop:
            one_loop = True
            thread = threading.Thread(target = looping)
            thread.start() # start parallel computation
        else:
            print 'One thread is already active'
        
def cleanup(list, current_time, stale_post_time):
    for post in list:
        if (current_time - post.created_utc) > stale_post_time:
            list.remove(post)

def get_config_data():
    global sleep_time_entry
    global search_term_entry
    global subreddit_string_entry
    global TARGET_EMAIL_entry
    global sleep_time
    global search_term
    global subreddit_string
    global TARGET_EMAIL
    global GMAIL_USERNAME
    global GMAIL_USERNAME_entry
    global REDDIT_USERNAME
    global REDDIT_USERNAME_entry

    Config = ConfigParser.ConfigParser()
    Config.read('config.cfg')
    try:
        sleep_time = int(Config.get('Main', 'sleep_time'))
        sleep_time_entry.insert(0, sleep_time)
    except Exception as detail:
        print 'Missing sleep_time'
    try:
        search_term = Config.get('Main', 'search_term')
        search_term_entry.insert(0, search_term)
    except Exception as detail:
        print 'Missing search_term'
    try:
        subreddit_string = Config.get('Main', 'subreddit_string')
        subreddit_string_entry.insert(0, subreddit_string)
    except Exception as detail:
        print 'Missing subreddit_string'
    try:
        TARGET_EMAIL = Config.get('Main', 'TARGET_EMAIL')
        TARGET_EMAIL_entry.insert(0, TARGET_EMAIL)
    except Exception as detail:
        print 'Missing TARGET_EMAIL'
    try:
        GMAIL_USERNAME = Config.get('Main', 'GMAIL_USERNAME')
        GMAIL_USERNAME_entry.insert(0, GMAIL_USERNAME)
    except Exception as detail:
        print 'Missing GMAIL_USERNAME'
    try:
        REDDIT_USERNAME = Config.get('Main', 'REDDIT_USERNAME')
        REDDIT_USERNAME_entry.insert(0, REDDIT_USERNAME)
    except Exception as detail:
        print 'Missing REDDIT_USERNAME'

def create_gui():
    global gui
    global sleep_time_entry
    global search_term_entry
    global subreddit_string_entry
    global TARGET_EMAIL_entry
    global GMAIL_USERNAME_entry
    global GMAIL_PASSWORD_entry
    global REDDIT_USERNAME_entry
    global REDDIT_PASSWORD_entry
    global GMAIL_LOGIN_var
    global REDDIT_LOGIN_var
    global START_button
    global START_button_var
    global one_loop
    parse_object = ParseInput()

    one_loop = False
    gui = tk.Tk()
    gui.title('Reddit Notifier by /u/PC4U')

    mainframe = tk.Frame(gui)
    mainframe.grid(column = 0, row = 0, padx = 10, pady = 10)
    mainframe.columnconfigure(0, weight = 1)
    mainframe.rowconfigure(0, weight = 1)

    sleep_time = tk.StringVar()
    search_term = tk.StringVar()
    subreddit_string = tk.StringVar()
    TARGET_EMAIL = tk.StringVar()
    GMAIL_USERNAME = tk.StringVar()
    GMAIL_PASSWORD = tk.StringVar()
    REDDIT_USERNAME = tk.StringVar()
    REDDIT_PASSWORD = tk.StringVar()

    GMAIL_USERNAME_var = tk.StringVar()
    GMAIL_USERNAME_var.set('Gmail Username: ')
    GMAIL_USERNAME_label = tk.Label(mainframe, textvariable = GMAIL_USERNAME_var)
    GMAIL_USERNAME_label.grid(column = 1, row = 1)
    GMAIL_USERNAME_entry = tk.Entry(mainframe, width = 30, textvariable = GMAIL_USERNAME)
    GMAIL_USERNAME_entry.grid(column = 2, row = 1)

    GMAIL_PASSWORD_var = tk.StringVar()
    GMAIL_PASSWORD_var.set('Gmail Password: ')
    GMAIL_PASSWORD_label = tk.Label(mainframe, textvariable = GMAIL_PASSWORD_var)
    GMAIL_PASSWORD_label.grid(column = 1, row = 2)
    GMAIL_PASSWORD_entry = tk.Entry(mainframe, width = 30, textvariable = GMAIL_PASSWORD, show = '*')
    GMAIL_PASSWORD_entry.grid(column = 2, row = 2)

    GMAIL_LOGIN_var = tk.StringVar()
    GMAIL_LOGIN_var.set('Not Logged In!')
    GMAIL_LOGIN_label = tk.Label(mainframe, textvariable = GMAIL_LOGIN_var)
    GMAIL_LOGIN_label.grid(column = 2, row = 3)
    GMAIL_LOGIN_button = tk.Button(mainframe, text='Log Into Gmail', command = parse_object.Gmail)
    GMAIL_LOGIN_button.grid(column = 1, row = 3)

    REDDIT_USERNAME_var = tk.StringVar()
    REDDIT_USERNAME_var.set('Reddit Username: ')
    REDDIT_USERNAME_label = tk.Label(mainframe, textvariable = REDDIT_USERNAME_var)
    REDDIT_USERNAME_label.grid(column = 1, row = 4)
    REDDIT_USERNAME_entry = tk.Entry(mainframe, width = 30, textvariable = REDDIT_USERNAME)
    REDDIT_USERNAME_entry.grid(column = 2, row = 4)

    REDDIT_PASSWORD_var = tk.StringVar()
    REDDIT_PASSWORD_var.set('Reddit Password: ')
    REDDIT_PASSWORD_label = tk.Label(mainframe, textvariable = REDDIT_PASSWORD_var)
    REDDIT_PASSWORD_label.grid(column = 1, row = 5)
    REDDIT_PASSWORD_entry = tk.Entry(mainframe, width = 30, textvariable = REDDIT_PASSWORD, show = '*')
    REDDIT_PASSWORD_entry.grid(column = 2, row = 5)

    REDDIT_LOGIN_var = tk.StringVar()
    REDDIT_LOGIN_var.set('Not Logged In!')
    REDDIT_LOGIN_label = tk.Label(mainframe, textvariable = REDDIT_LOGIN_var)
    REDDIT_LOGIN_label.grid(column = 2, row = 6)
    REDDIT_LOGIN_button = tk.Button(mainframe, text='Log Into Reddit', command = parse_object.Reddit)
    REDDIT_LOGIN_button.grid(column = 1, row = 6)

    sleep_time_var = tk.StringVar()
    sleep_time_var.set('Sleep Time (seconds, between 30 and 600): ')
    sleep_time_label = tk.Label(mainframe, textvariable = sleep_time_var)
    sleep_time_label.grid(column = 1, row = 7)
    sleep_time_entry = tk.Entry(mainframe, width = 7, textvariable = sleep_time)
    sleep_time_entry.grid(column = 2, row = 7)

    search_term_var = tk.StringVar()
    search_term_var.set('Search Term(s), seperate by comma: ')
    search_term_label = tk.Label(mainframe, textvariable = search_term_var)
    search_term_label.grid(column = 1, row = 8)
    search_term_entry = tk.Entry(mainframe, width = 30, textvariable = search_term)
    search_term_entry.grid(column = 2, row = 8)

    subreddit_string_var = tk.StringVar()
    subreddit_string_var.set('Subreddits to search through, seperate by comma: ')
    subreddit_string_label = tk.Label(mainframe, textvariable = subreddit_string_var)
    subreddit_string_label.grid(column = 1, row = 9)
    subreddit_string_entry = tk.Entry(mainframe, width = 30, textvariable = subreddit_string)
    subreddit_string_entry.grid(column = 2, row = 9)

    TARGET_EMAIL_var = tk.StringVar()
    TARGET_EMAIL_var.set('Target Email: ')
    TARGET_EMAIL_label = tk.Label(mainframe, textvariable = TARGET_EMAIL_var)
    TARGET_EMAIL_label.grid(column = 1, row = 10)
    TARGET_EMAIL_entry = tk.Entry(mainframe, width = 30, textvariable = TARGET_EMAIL)
    TARGET_EMAIL_entry.grid(column = 2, row = 10)

    START_button_var = tk.IntVar()
    START_button = tk.Checkbutton(mainframe, text='Start Automation', command = parse_object.Start, variable = START_button_var)
    START_button.grid(column = 1, row = 11)

    SAVE_button = tk.Button(mainframe, text='Save data to config.cfg', command = parse_object.Save)
    SAVE_button.grid(column = 2, row = 11)

    get_config_data()

    gui.mainloop()

if __name__ == '__main__':
    create_gui()
