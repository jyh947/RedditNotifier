import praw
import time
import os.path
import smtplib
import threading
import ConfigParser
import tkMessageBox
import Tkinter as tk

class ParseInput(object):
    def Gmail(self, gui):
        gui.GMAIL_USERNAME = gui.GMAIL_USERNAME_entry.get()
        gui.GMAIL_PASSWORD = gui.GMAIL_PASSWORD_entry.get()

        gui.GMAIL_USERNAME = check_gmail_username(gui.GMAIL_USERNAME)
        gui.GMAIL_USERNAME_entry.delete(0, 'end')

        if gui.GMAIL_USERNAME == None:
            tkMessageBox.showerror(title = 'Error!', message = 'Bad Gmail username!', parent = gui.gui)
            return
        gui.GMAIL_USERNAME_entry.insert(0, gui.GMAIL_USERNAME)
        if len(gui.GMAIL_PASSWORD) == 0:
            tkMessageBox.showerror(title = 'Error!', message = 'Please enter a Gmail password!', parent = gui.gui)
            return

        self.server = smtplib.SMTP('smtp.gmail.com', 587)
        self.server.ehlo()
        self.server.starttls()

        try:
            self.server.login(gui.GMAIL_USERNAME, gui.GMAIL_PASSWORD)
            print 'Correct password!'
            gui.GMAIL_LOGIN_var.set('Logged Into Gmail!')
            if gui.REDDIT_LOGIN_var.get() == 'Logged Into Reddit!':
                gui.START_button['state'] = 'normal'
        except Exception as detail:
            tkMessageBox.showerror(title = 'Error!', message = 'Message from Gmail:\n' + str(detail), parent = gui.gui)
            print detail
            print 'Incorrect password! Please try again!'
            gui.START_button['state'] = 'disabled'
            gui.GMAIL_LOGIN_var.set('Not Logged In!')

    def Reddit(self, gui):
        gui.REDDIT_USERNAME = gui.REDDIT_USERNAME_entry.get()
        gui.REDDIT_PASSWORD = gui.REDDIT_PASSWORD_entry.get()

        gui.REDDIT_USERNAME = check_reddit_username(gui.REDDIT_USERNAME)
        gui.REDDIT_USERNAME_entry.delete(0, 'end')
        if gui.REDDIT_USERNAME == None:
            tkMessageBox.showerror(title = 'Error!', message = 'Bad Reddit username!', parent = gui.gui)
            return
        gui.REDDIT_USERNAME_entry.insert(0, gui.REDDIT_USERNAME)
        if len(gui.REDDIT_PASSWORD) == 0:
            tkMessageBox.showerror(title = 'Error!', message = 'Please enter a Reddit password!', parent = gui.gui)
            return

        self.reddit = praw.Reddit(user_agent = 'string checker by /u/PC4U v2.0')

        try:
            user = self.reddit.get_redditor(gui.REDDIT_USERNAME)
        except Exception as detail:
            tkMessageBox.showerror(title = 'Error!', message = 'Message from Reddit:\n' + str(detail), parent = gui.gui)
            print detail
            print 'Incorrect password! Please try again!'
            gui.REDDIT_LOGIN_var.set('Not Logged In!')
            gui.START_button['state'] = 'disabled'
            return
        if user.link_karma < 2:
            tkMessageBox.showerror(title = 'Error!', message = 'You must have at least 1 link karma!', parent = gui.gui)
            return
            
        # authentication
        try:
            self.reddit.login(gui.REDDIT_USERNAME, gui.REDDIT_PASSWORD)
            print 'Correct password!'
            gui.REDDIT_LOGIN_var.set('Logged Into Reddit!')
            if gui.GMAIL_LOGIN_var.get() == 'Logged Into Gmail!':
                gui.START_button['state'] = 'normal'
        except Exception as detail:
            tkMessageBox.showerror(title = 'Error!', message = 'Message from Reddit:\n' + str(detail), parent = gui.gui)
            print detail
            print 'Incorrect password! Please try again!'
            gui.REDDIT_LOGIN_var.set('Not Logged In!')
            gui.START_button['state'] = 'disabled'

    def Save(self, gui, startup):
        if startup:
            self.search_terms = []
            self.subreddits = []
            self.all_posts = []
            self.messages_to_notify_user_about = []
            self.messages_already_sent = []
        if not os.path.exists('config.cfg') and startup:
            return
        gui.sleep_time = gui.sleep_time_entry.get()
        gui.search_term = gui.search_term_entry.get()
        gui.subreddit_string = gui.subreddit_string_entry.get()
        gui.TARGET_EMAIL = gui.TARGET_EMAIL_entry.get()
        gui.GMAIL_USERNAME = gui.GMAIL_USERNAME_entry.get()
        gui.REDDIT_USERNAME = gui.REDDIT_USERNAME_entry.get()

        # Do error checking here
        gui.sleep_term = check_sleep_time(gui.sleep_time)
        gui.sleep_time_entry.delete(0, 'end')
        if gui.sleep_time == None:
            tkMessageBox.showerror(title = 'Error!', message = 'Bad sleep time!', parent = gui.gui)
        else:
            gui.sleep_time_entry.insert(0, gui.sleep_time)

        new_search_term_list, gui.search_term = clean_list_string(gui.search_term, False, gui)
        gui.search_term_entry.delete(0, 'end')
        if gui.search_term == None:
            tkMessageBox.showerror(title = 'Error!', message = 'All search terms were invalid or none were entered!', parent = gui.gui)
        else:
            gui.search_term_entry.insert(0, gui.search_term)

        new_subreddit_list, gui.subreddit_string = clean_list_string(gui.subreddit_string, True, gui)
        gui.subreddit_string_entry.delete(0, 'end')
        if gui.subreddit_string == None:
            tkMessageBox.showerror(title = 'Error!', message = 'All subreddits were invalid or none were entered!', parent = gui.gui)
        else:
            gui.subreddit_string_entry.insert(0, gui.subreddit_string)

        gui.TARGET_EMAIL = check_target_email(gui.TARGET_EMAIL)
        gui.TARGET_EMAIL_entry.delete(0, 'end')
        if gui.TARGET_EMAIL == None:
            tkMessageBox.showerror(title = 'Error!', message = 'Bad target email!', parent = gui.gui)
        else:
            gui.TARGET_EMAIL_entry.insert(0, gui.TARGET_EMAIL)

        gui.GMAIL_USERNAME = check_gmail_username(gui.GMAIL_USERNAME)
        gui.GMAIL_USERNAME_entry.delete(0, 'end')
        if gui.GMAIL_USERNAME == None:
            tkMessageBox.showerror(title = 'Error!', message = 'Bad Gmail username!', parent = gui.gui)
        else:
            gui.GMAIL_USERNAME_entry.insert(0, gui.GMAIL_USERNAME)

        gui.REDDIT_USERNAME = check_reddit_username(gui.REDDIT_USERNAME)
        gui.REDDIT_USERNAME_entry.delete(0, 'end')
        if gui.REDDIT_USERNAME == None:
            tkMessageBox.showerror(title = 'Error!', message = 'Bad Reddit username!', parent = gui.gui)
        else:
            gui.REDDIT_USERNAME_entry.insert(0, gui.REDDIT_USERNAME)

        cfgfile = open('config.cfg','w')
        Config = ConfigParser.ConfigParser()
        Config.add_section('Main')
        Config.set('Main', 'sleep_time', gui.sleep_term)
        Config.set('Main', 'search_term', gui.search_term)
        Config.set('Main', 'subreddit_string', gui.subreddit_string)
        Config.set('Main', 'TARGET_EMAIL', gui.TARGET_EMAIL)
        Config.set('Main', 'GMAIL_USERNAME', gui.GMAIL_USERNAME)
        Config.set('Main', 'REDDIT_USERNAME', gui.REDDIT_USERNAME)
        Config.write(cfgfile)
        cfgfile.close()
        gui.TEXT_var.set('Saved settings to "config.cfg"\n\n\n')

        thread = threading.Thread(target = lambda: set_output(gui))
        thread.start()
        print 'Saving worked!'

    def Start(self, gui):
        # Disable buttons here
        gui.GMAIL_USERNAME_entry['state'] = 'disabled'
        gui.GMAIL_PASSWORD_entry['state'] = 'disabled'
        gui.GMAIL_LOGIN_button['state'] = 'disabled'
        gui.REDDIT_USERNAME_entry['state'] = 'disabled'
        gui.REDDIT_PASSWORD_entry['state'] = 'disabled'
        gui.REDDIT_LOGIN_button['state'] = 'disabled'
        gui.sleep_time_entry['state'] = 'disabled'
        gui.search_term_entry['state'] = 'disabled'
        gui.subreddit_string_entry['state'] = 'disabled'
        gui.TARGET_EMAIL_entry['state'] = 'disabled'
        gui.SAVE_button['state'] = 'disabled'

        if not gui.START_button_var.get():
            set_to_normal(gui)
            return
        if gui.GMAIL_LOGIN_var.get() != 'Logged Into Gmail!' or gui.REDDIT_LOGIN_var.get() != 'Logged Into Reddit!':
            set_to_normal(gui)
            tkMessageBox.showerror(title = 'Error!', message = 'Please login to both Gmail and Reddit!', parent = gui.gui)
            return

        gui.sleep_time = gui.sleep_time_entry.get()
        gui.search_term = gui.search_term_entry.get()
        gui.subreddit_string = gui.subreddit_string_entry.get()
        gui.TARGET_EMAIL = gui.TARGET_EMAIL_entry.get()

        #do input checking here
        gui.sleep_time = check_sleep_time(gui.sleep_time)
        gui.sleep_time_entry.delete(0, 'end')
        if gui.sleep_time == None:
            set_to_normal(gui)
            tkMessageBox.showerror(title = 'Error!', message = 'Bad sleep time!', parent = gui.gui)
            return
        else:
            gui.sleep_time_entry.insert(0, gui.sleep_time)

        gui.TARGET_EMAIL = check_target_email(gui.TARGET_EMAIL)
        gui.TARGET_EMAIL_entry.delete(0, 'end')
        if gui.TARGET_EMAIL == None:
            set_to_normal(gui)
            tkMessageBox.showerror(title = 'Error!', message = 'Bad target email!', parent = gui.gui)
            return
        else:
            gui.TARGET_EMAIL_entry.insert(0, gui.TARGET_EMAIL)

        new_subreddit_list = []

        self.search_terms, gui.search_term = clean_list_string(gui.search_term, False, gui)
        gui.search_term_entry.delete(0, 'end')
        if gui.search_term == None:
            set_to_normal(gui)
            tkMessageBox.showerror(title = 'Error!', message = 'All search terms were invalid or none were entered!', parent = gui.gui)
            return
        else:
            gui.search_term_entry.insert(0, gui.search_term)

        new_subreddit_list, gui.subreddit_string = clean_list_string(gui.subreddit_string, True, gui)
        gui.subreddit_string_entry.delete(0, 'end')
        if gui.subreddit_string == None:
            set_to_normal(gui)
            tkMessageBox.showerror(title = 'Error!', message = 'All subreddits were invalid or none were entered!', parent = gui.gui)
            return
        else:
            gui.subreddit_string_entry.insert(0, gui.subreddit_string)
        for subreddit in new_subreddit_list:
            self.subreddits.append(self.reddit.get_subreddit(subreddit))

        def looping(self, gui):
            stale_post_time = 600
            while gui.START_button_var.get():
                gui.TEXT_var.set('\n\n\n')
                # get current time
                current_time = time.time()
                posts_this_round = []
                # get 10 new posts and place into all_posts
                for subreddit in self.subreddits:
                    posts_to_grab = 10
                    max_posts = 320
                    prev_posts = 6000
                    new_posts = 6000
                    while prev_posts == new_posts:
                        prev_posts = posts_to_grab
                        new_posts = 0
                        posts_this_subreddit = []
                        for submission in subreddit.get_new(limit = posts_to_grab):
                            if submission not in self.all_posts and submission not in posts_this_round and (current_time - submission.created_utc) < stale_post_time:
                                posts_this_subreddit.append(submission)
                                new_posts += 1
                        if posts_to_grab >= max_posts:
                            break
                        posts_to_grab *= 2
                    for post in posts_this_subreddit:
                        if post not in posts_this_round:
                            posts_this_round.append(post)
                current_text = 'Found ' + str(len(posts_this_round)) + ' new posts that have been added to the array\n\n\n'
                print 'Found', len(posts_this_round), 'new posts that have been added to the array'
                gui.TEXT_var.set(current_text)
                # put new posts with search term into messages_to_notify_user_about
                not_notified_posts = 0
                for new_post in posts_this_round:
                    for search_term_iter in self.search_terms:
                        if new_post.title.lower().find(search_term_iter) != -1 and new_post not in self.messages_to_notify_user_about:
                            self.messages_to_notify_user_about.append(new_post)
                            not_notified_posts += 1
                        elif new_post.is_self and new_post.selftext.lower().find(search_term_iter) != -1 and new_post not in self.messages_to_notify_user_about:
                            self.messages_to_notify_user_about.append(new_post)
                            not_notified_posts += 1
                current_text = current_text.strip('\n')
                current_text += '\nFound ' + str(not_notified_posts) + ' new posts that need to be sent to the user\n\n'
                print 'Found', not_notified_posts, 'new posts that need to be sent to the user'
                gui.TEXT_var.set(current_text)
                # put all posts that need to be sent to the user in messages_already_sent
                for to_send in self.messages_to_notify_user_about:
                    if to_send not in self.messages_already_sent:
                        message_to_send = 'New post with something from ' + gui.search_term + ' in it from /r/' + str(to_send.subreddit) + '\n\n' + to_send.permalink + '\n\n'
                        if to_send.is_self:
                            message_to_send += 'Self text here:\n\n'
                            message_to_send += to_send.selftext
                        self.reddit.send_message(gui.REDDIT_USERNAME, 'New message found!', message_to_send)
                        self.server.sendmail(gui.GMAIL_USERNAME, gui.TARGET_EMAIL, message_to_send)
                        self.messages_already_sent.append(to_send)

                # push new posts into queue
                for post in posts_this_round:
                    self.all_posts.append(post)

                # clear posts older than 'stale_post_time' seconds old
                print 'Clean-up time'
                cleanup(self.all_posts, current_time, stale_post_time)
                cleanup(self.messages_to_notify_user_about, current_time, stale_post_time)
                cleanup(self.messages_already_sent, current_time, stale_post_time)
                current_text_backup = current_text
                #let script sleep for 'sleep_time' seconds
                for integer in range(gui.sleep_time):
                    current_text = current_text.strip('\n')
                    print 'Waiting', gui.sleep_time - integer, 'seconds'
                    current_text += '\nWaiting ' + str(gui.sleep_time - integer) + ' seconds\n'
                    gui.TEXT_var.set(current_text)
                    current_text = current_text_backup
                    time.sleep(1)
                    if not gui.START_button_var.get():
                        set_to_normal(gui)
                        print 'Exiting thread'
                        gui.TEXT_var.set('Automation Stopped!\n\n\n')
                        thread = threading.Thread(target = lambda: set_output(gui))
                        thread.start()
                        gui.one_loop = False
                        return

            set_to_normal(gui)
            print 'Exiting thread'
            gui.TEXT_var.set('Automation Stopped!\n\n\n')
            thread = threading.Thread(target = lambda: set_output(gui))
            thread.start()
            gui.one_loop = False

        if not gui.one_loop:
            gui.one_loop = True
            thread = threading.Thread(target = lambda: looping(self, gui))
            thread.start()
        else:
            print 'One thread is already active'

class GUI(object):
    def init(self):
        self.parse_object = ParseInput()

        self.one_loop = False
        self.gui = tk.Tk()
        self.gui.title('Reddit Notifier by /u/PC4U')
        self.gui.resizable(False, False)
        self.gui.protocol("WM_DELETE_WINDOW", lambda: on_closing(self))

        self.mainframe = tk.Frame(self.gui)
        self.mainframe.grid(column = 0, row = 0, padx = 10, pady = 10)
        self.mainframe.columnconfigure(0, weight = 1)
        self.mainframe.rowconfigure(0, weight = 1)

        self.title = tk.StringVar()
        self.sleep_time = tk.StringVar()
        self.sleep_time_var = tk.StringVar()
        self.search_term = tk.StringVar()
        self.search_term_var = tk.StringVar()
        self.subreddit_string = tk.StringVar()
        self.subreddit_string_var = tk.StringVar()
        self.TARGET_EMAIL = tk.StringVar()
        self.TARGET_EMAIL_var = tk.StringVar()
        self.GMAIL_USERNAME = tk.StringVar()
        self.GMAIL_USERNAME_var = tk.StringVar()
        self.GMAIL_PASSWORD = tk.StringVar()
        self.GMAIL_PASSWORD_var = tk.StringVar()
        self.GMAIL_LOGIN_var = tk.StringVar()
        self.REDDIT_USERNAME = tk.StringVar()
        self.REDDIT_USERNAME_var = tk.StringVar()
        self.REDDIT_PASSWORD = tk.StringVar()
        self.REDDIT_PASSWORD_var = tk.StringVar()
        self.REDDIT_LOGIN_var = tk.StringVar()
        self.OUTPUT_var = tk.StringVar()
        self.TEXT_var = tk.StringVar()
        self.START_button_var = tk.IntVar()

        self.title.set('This is a robot will automatically scan all the subreddits\n' +
        'that you list for all the search term(s) you list and notify you\n' +
        'whenever it finds a new post with those search term(s) in said new post.\n' +
        'The robot will use your Gmail account to send an email to the target email.\n' +
        'The robot will use your Reddit account to send a message to the same Reddit account.\n')
        self.title_label = tk.Label(self.mainframe, textvariable = self.title)
        self.title_label.grid(column = 1, row = 0, columnspan = 2)

        self.GMAIL_USERNAME_var.set('Gmail Username: ')
        self.GMAIL_USERNAME_label = tk.Label(self.mainframe, textvariable = self.GMAIL_USERNAME_var)
        self.GMAIL_USERNAME_label.grid(column = 1, row = 1, sticky = 'W')
        self.GMAIL_USERNAME_entry = tk.Entry(self.mainframe, width = 30, textvariable = self.GMAIL_USERNAME)
        self.GMAIL_USERNAME_entry.grid(column = 2, row = 1, sticky = 'W')

        self.GMAIL_PASSWORD_var.set('Gmail Password: ')
        self.GMAIL_PASSWORD_label = tk.Label(self.mainframe, textvariable = self.GMAIL_PASSWORD_var)
        self.GMAIL_PASSWORD_label.grid(column = 1, row = 2, sticky = 'W')
        self.GMAIL_PASSWORD_entry = tk.Entry(self.mainframe, width = 30, textvariable = self.GMAIL_PASSWORD, show = '*')
        self.GMAIL_PASSWORD_entry.grid(column = 2, row = 2, sticky = 'W')

        self.GMAIL_LOGIN_var.set('Not Logged In!')
        self.GMAIL_LOGIN_label = tk.Label(self.mainframe, textvariable = self.GMAIL_LOGIN_var)
        self.GMAIL_LOGIN_label.grid(column = 2, row = 3, sticky = 'W')
        self.GMAIL_LOGIN_button = tk.Button(self.mainframe, text='Log Into Gmail', command = lambda: self.parse_object.Gmail(self))
        self.GMAIL_LOGIN_button.grid(column = 1, row = 3, sticky = 'W')

        self.REDDIT_USERNAME_var.set('Reddit Username: ')
        self.REDDIT_USERNAME_label = tk.Label(self.mainframe, textvariable = self.REDDIT_USERNAME_var)
        self.REDDIT_USERNAME_label.grid(column = 1, row = 4, sticky = 'W')
        self.REDDIT_USERNAME_entry = tk.Entry(self.mainframe, width = 30, textvariable = self.REDDIT_USERNAME)
        self.REDDIT_USERNAME_entry.grid(column = 2, row = 4, sticky = 'W')

        self.REDDIT_PASSWORD_var.set('Reddit Password: ')
        self.REDDIT_PASSWORD_label = tk.Label(self.mainframe, textvariable = self.REDDIT_PASSWORD_var)
        self.REDDIT_PASSWORD_label.grid(column = 1, row = 5, sticky = 'W')
        self.REDDIT_PASSWORD_entry = tk.Entry(self.mainframe, width = 30, textvariable = self.REDDIT_PASSWORD, show = '*')
        self.REDDIT_PASSWORD_entry.grid(column = 2, row = 5, sticky = 'W')

        self.REDDIT_LOGIN_var.set('Not Logged In!')
        self.REDDIT_LOGIN_label = tk.Label(self.mainframe, textvariable = self.REDDIT_LOGIN_var)
        self.REDDIT_LOGIN_label.grid(column = 2, row = 6, sticky = 'W')
        self.REDDIT_LOGIN_button = tk.Button(self.mainframe, text='Log Into Reddit', command = lambda: self.parse_object.Reddit(self))
        self.REDDIT_LOGIN_button.grid(column = 1, row = 6, sticky = 'W')

        self.sleep_time_var.set('Sleep Time (seconds, between 30 and 600): ')
        self.sleep_time_label = tk.Label(self.mainframe, textvariable = self.sleep_time_var)
        self.sleep_time_label.grid(column = 1, row = 7, sticky = 'W')
        self.sleep_time_entry = tk.Entry(self.mainframe, width = 7, textvariable = self.sleep_time)
        self.sleep_time_entry.grid(column = 2, row = 7, sticky = 'W')

        self.search_term_var.set('Search Term(s), seperate by comma: ')
        self.search_term_label = tk.Label(self.mainframe, textvariable = self.search_term_var)
        self.search_term_label.grid(column = 1, row = 8, sticky = 'W')
        self.search_term_entry = tk.Entry(self.mainframe, width = 30, textvariable = self.search_term)
        self.search_term_entry.grid(column = 2, row = 8, sticky = 'W')

        self.subreddit_string_var.set('Subreddits to search through, seperate by comma: ')
        self.subreddit_string_label = tk.Label(self.mainframe, textvariable = self.subreddit_string_var)
        self.subreddit_string_label.grid(column = 1, row = 9, sticky = 'W')
        self.subreddit_string_entry = tk.Entry(self.mainframe, width = 30, textvariable = self.subreddit_string)
        self.subreddit_string_entry.grid(column = 2, row = 9, sticky = 'W')

        self.TARGET_EMAIL_var.set('Target Email (email to notify about new messages): ')
        self.TARGET_EMAIL_label = tk.Label(self.mainframe, textvariable = self.TARGET_EMAIL_var)
        self.TARGET_EMAIL_label.grid(column = 1, row = 10, sticky = 'W')
        self.TARGET_EMAIL_entry = tk.Entry(self.mainframe, width = 30, textvariable = self.TARGET_EMAIL)
        self.TARGET_EMAIL_entry.grid(column = 2, row = 10, sticky = 'W')

        self.SAVE_button = tk.Button(self.mainframe, text='Save data to config.cfg', command = lambda: self.parse_object.Save(self, False))
        self.SAVE_button.grid(column = 1, row = 11, sticky = 'W')

        self.START_button = tk.Checkbutton(self.mainframe, text='Start Automation', command = lambda: self.parse_object.Start(self), variable = self.START_button_var, state = 'disabled')
        self.START_button.grid(column = 2, row = 11, sticky = 'W')

        self.OUTPUT_var.set('Output:')
        self.OUTPUT = tk.Label(self.mainframe, textvariable = self.OUTPUT_var)
        self.OUTPUT.grid(column = 1, row = 12, columnspan = 2, sticky = 'W')

        self.TEXT_var.set('\n\n\n')
        self.TEXT = tk.Label(self.mainframe, textvariable = self.TEXT_var, justify = 'left')
        self.TEXT.grid(column = 1, row = 13, columnspan = 2, sticky = 'W')

        get_config_data(self)
        self.parse_object.Save(self, True)

def on_closing(gui):
    gui.START_button.deselect()
    gui.gui.quit()

def cleanup(list, current_time, stale_post_time):
    for post in list:
        if (current_time - post.created_utc) > stale_post_time:
            list.remove(post)

def get_config_data(gui):
    if not os.path.exists('config.cfg'):
        gui.TARGET_EMAIL_entry.insert(0, 'example@gmail.com')
        gui.sleep_time_entry.insert(0, '30')
        return
        
    Config = ConfigParser.ConfigParser()
    Config.read('config.cfg')

    try:
        gui.sleep_time = int(Config.get('Main', 'sleep_time'))
        gui.sleep_time = check_sleep_time(gui.sleep_time)
        gui.sleep_time_entry.delete(0, 'end')
        if gui.sleep_time == None:
            tkMessageBox.showerror(title = 'Error!', message = 'Bad sleep time!', parent = gui.gui)
        else:
            gui.sleep_time_entry.insert(0, gui.sleep_time)
    except Exception as detail:
        print 'Missing sleep_time'

    try:
        gui.search_term = Config.get('Main', 'search_term')
        new_search_term_list, gui.search_term = clean_list_string(gui.search_term, False, gui)
        gui.search_term_entry.delete(0, 'end')
        if gui.search_term == None:
            tkMessageBox.showerror(title = 'Error!', message = 'All search terms were invalid or none were entered!', parent = gui.gui)
        else:
            gui.search_term_entry.insert(0, gui.search_term)
    except Exception as detail:
        print 'Missing search_term'

    try:
        gui.subreddit_string = Config.get('Main', 'subreddit_string')
        new_subreddit_list, gui.subreddit_string = clean_list_string(gui.subreddit_string, True, gui)
        gui.subreddit_string_entry.delete(0, 'end')
        if gui.subreddit_string == None:
            tkMessageBox.showerror(title = 'Error!', message = 'All subreddits were invalid or none were entered!', parent = gui.gui)
        else:
            gui.subreddit_string_entry.insert(0, gui.subreddit_string)
    except Exception as detail:
        print 'Missing subreddit_string'

    try:
        gui.TARGET_EMAIL = Config.get('Main', 'TARGET_EMAIL')
        gui.TARGET_EMAIL = check_target_email(gui.TARGET_EMAIL)
        gui.TARGET_EMAIL_entry.delete(0, 'end')
        if gui.TARGET_EMAIL == None:
            tkMessageBox.showerror(title = 'Error!', message = 'Bad target email!', parent = gui.gui)
        else:
            gui.TARGET_EMAIL_entry.insert(0, gui.TARGET_EMAIL)
    except Exception as detail:
        print 'Missing TARGET_EMAIL'

    try:
        gui.GMAIL_USERNAME = Config.get('Main', 'GMAIL_USERNAME')
        gui.GMAIL_USERNAME = check_gmail_username(gui.GMAIL_USERNAME)
        gui.GMAIL_USERNAME_entry.delete(0, 'end')
        if gui.GMAIL_USERNAME == None:
            tkMessageBox.showerror(title = 'Error!', message = 'Bad Gmail username!', parent = gui.gui)
        else:
            gui.GMAIL_USERNAME_entry.insert(0, gui.GMAIL_USERNAME)
    except Exception as detail:
        print 'Missing GMAIL_USERNAME'

    try:
        gui.REDDIT_USERNAME = Config.get('Main', 'REDDIT_USERNAME')
        gui.REDDIT_USERNAME = check_reddit_username(gui.REDDIT_USERNAME)
        gui.REDDIT_USERNAME_entry.delete(0, 'end')
        if gui.REDDIT_USERNAME == None:
            tkMessageBox.showerror(title = 'Error!', message = 'Bad Reddit username!', parent = gui.gui)
        else:
            gui.REDDIT_USERNAME_entry.insert(0, gui.REDDIT_USERNAME)
    except Exception as detail:
        print 'Missing REDDIT_USERNAME'
        
def set_output(gui):
    time.sleep(3)
    gui.TEXT_var.set('\n\n\n')

def check_gmail_username(string):
    string = string.strip()
    if len(string) == 0:
        return None
    string = string.replace(' ', '')
    if string.find('@gmail.com') == -1:
        string += '@gmail.com'
    string = check_target_email(string)
    return string

def check_reddit_username(string):
    string = string.replace(' ', '')
    for char in string:
        if not char.isalnum() and char != '_' and char != '-':
            print 'bad', char
            return None
    return string

def check_sleep_time(string):
    try:
        string = int(string)
    except Exception as detail:
        return None
    if string > 600 or string < 30:
        return None
    return string

def check_subreddits(string):
    string = string.strip()
    if len(string) == 0:
        return None
    if len(string) < 22 and string.find('-') == -1 and string[0] != '_' and len(string) > 0:
        for char in string:
            if not char.isdigit() and not char.isalpha() and char != '_':
                return None
    else:
        return None
    return string

def check_target_email(string):
    string = string.strip()
    if string == 'example@gmail.com':
        return None
    if len(string) == 0:
        return None
    if string.find('@') == -1:
        return None
    substring = string.split('@')
    if substring[0].find('@') != -1 or substring[1].find('@') != -1:
        return None
    if len(substring) > 2:
        return None
    if substring[1].find('.') == -1:
        return None
    return string

def clean_list_string(string, subreddit, gui):
    string = string.strip()
    string_list = string.split(',')
    new_string_list = []
    new_string = ''
    for it in string_list:
        it = it.strip()
        if subreddit:
            result = check_subreddits(it)
            if result == None or result.isspace() or len(result) == 0:
                tkMessageBox.showerror(title = 'Error!', message = 'Subreddit: "' + it + '" does not exist!', parent = gui.gui)
            else:
                print 'Adding', result
                new_string_list.append(result)
                new_string += result + ', '
        else:
            print 'Adding', it
            new_string_list.append(it)
            new_string += it + ', '
    new_string = new_string.strip(', ')
    return new_string_list, new_string

def set_to_normal(gui):
    gui.START_button.deselect()
    gui.GMAIL_USERNAME_entry['state'] = 'normal'
    gui.GMAIL_PASSWORD_entry['state'] = 'normal'
    gui.GMAIL_LOGIN_button['state'] = 'normal'
    gui.REDDIT_USERNAME_entry['state'] = 'normal'
    gui.REDDIT_PASSWORD_entry['state'] = 'normal'
    gui.REDDIT_LOGIN_button['state'] = 'normal'
    gui.sleep_time_entry['state'] = 'normal'
    gui.search_term_entry['state'] = 'normal'
    gui.subreddit_string_entry['state'] = 'normal'
    gui.TARGET_EMAIL_entry['state'] = 'normal'
    gui.SAVE_button['state'] = 'normal'

if __name__ == '__main__':
    gui = GUI()
    gui.init()
    gui.gui.mainloop()
