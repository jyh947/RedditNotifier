import praw
import time
import smtplib
import getpass

def cleanup(list, current_time, stale_post_time):
    for post in list:
        if (current_time - post.created_utc) > stale_post_time:
            list.remove(post)

if __name__ == '__main__':
    # DEFINITIONS
    stale_post_time = 600
    sleep_time = 30
    search_term = 'giveaway'
    subreddit_string = 'pcmasterrace'

    # Get email
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    GMAIL_USERNAME = raw_input('Gmail address (can include or exclude @gmail.com): ')
    GMAIL_USERNAME.replace(' ', '')
    if GMAIL_USERNAME.find('@gmail.com') == -1:
        GMAIL_USERNAME += '@gmail.com'

    correct_password = False
    while not correct_password:
        try:
            server.login(GMAIL_USERNAME, getpass.getpass('Gmail Password: '))
            correct_password = True
        except Exception:
            print 'Incorrect password! Please try again!'

    TARGET_EMAIL = raw_input('Target email to notify you at: ')
    TARGET_EMAIL.replace(' ', '')

    # get username from console
    REDDIT_USERNAME = raw_input('Reddit Username: ')
    REDDIT_PASS = ''

    # name program and do karma background check
    r = praw.Reddit(user_agent = 'string checker by /u/pc4u v1.0')
    user = r.get_redditor(REDDIT_USERNAME)
    if user.link_karma < 2:
        print 'You must have more than 1 link karma point'
        exit(1)

    # authentication
    correct_password = False
    while not correct_password:
        try:
            r.login(REDDIT_USERNAME, REDDIT_PASS) # get this from config.py or from user
            correct_password = True
        except Exception:
            print 'Incorrect password! Please try again!'

    subreddit  = r.get_subreddit(subreddit_string)
    all_posts = []
    messages_to_notify_user_about = []
    messages_already_sent = []

    while True:
        # get current time
        current_time = time.time()
        
        # get 20 new posts and place into all_posts
        posts_to_grab = 10
        new_posts = 10
        while posts_to_grab == new_posts:
            new_posts = 0
            posts_this_round = []
            for submission in subreddit.get_new(limit = posts_to_grab):
                if submission not in all_posts and (current_time - submission.created_utc) < stale_post_time:
                    posts_this_round.append(submission)
                    new_posts += 1
            posts_to_grab *= 2

        print 'Found', new_posts, 'new posts that have been added to the array'

        # put new posts with search term into messages_to_notify_user_about
        not_notified_posts = 0
        for new_post in posts_this_round:
            if new_post.title.lower().find(search_term) != -1 and new_post not in messages_to_notify_user_about:
                messages_to_notify_user_about.append(new_post)
                not_notified_posts += 1
            elif new_post.is_self and new_post.selftext.lower().find(search_term) != -1:
                messages_to_notify_user_about.append(new_post)
                not_notified_posts += 1

        print 'Found', not_notified_posts, 'new posts that need to be sent to the user'

        # put all posts that need to be sent to the user in messages_already_sent
        for to_send in messages_to_notify_user_about:
            if to_send not in messages_already_sent:
                message_to_send = 'New post with '+ search_term +' in it from the /r/' + subreddit_string + '\n\n' + to_send.permalink + '\n\n'
                if to_send.is_self:
                    message_to_send += 'Self text here:\n\n'
                    message_to_send += to_send.selftext
                r.send_message(REDDIT_USERNAME, 'New ' + search_term + '!', message_to_send)
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
        time.sleep(sleep_time)