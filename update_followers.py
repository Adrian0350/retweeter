import os
import sqlite3
import cPickle
from collections import OrderedDict
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

status = OrderedDict()
if os.path.isfile(settings['update_status_path']):
    f = open(settings['update_status_path'], 'rb')
    status = cPickle.load(f)
    f.close()

if not status:
    status = OrderedDict([(k, None) for k in settings['only_followers_of']])

try:
    for account, next_cursor in status.iteritems():
        while next_cursor != '0':
            res = twitter.get_followers_ids(screen_name=account, stringify_ids=True, cursor=next_cursor)
            for user_id in res['ids']:
                c.execute("""INSERT OR IGNORE INTO followers(id) VALUES ('%s')""" % user_id)
                conn.commit()
            next_cursor = res['next_cursor_str']
            status[account] = next_cursor
except:
    pass

status = OrderedDict([item for item in status.iteritems() if item[1] != '0'])
f = open(settings['update_status_path'], 'wb')
cPickle.dump(status, f, cPickle.HIGHEST_PROTOCOL)
f.close()

conn.close()
