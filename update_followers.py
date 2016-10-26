import sqlite3
from config import settings
from twython import Twython

conn = sqlite3.connect(settings['db_path'])

c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS followers
             (id TEXT PRIMARY KEY NOT NULL)''')
conn.commit()

# fetch the followers of the main account! only 15 requests every 15 minutes can be done
tw = settings['twitter']
twitter = Twython(tw['APP_KEY'], tw['APP_SECRET'], tw['OAUTH_TOKEN'], tw['OAUTH_TOKEN_SECRET'])

for account in settings['only_followers_of']:
    next_cursor = None
    while next_cursor != '0':
        res = twitter.get_followers_ids(screen_name=account, stringify_ids=True, cursor=next_cursor)
        for user_id in res['ids']:
            c.execute("""INSERT OR IGNORE INTO followers(id) VALUES ('%s')""" % user_id)
            conn.commit()
        next_cursor = res['next_cursor_str']

conn.close()
