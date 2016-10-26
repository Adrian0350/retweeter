from twython import TwythonStreamer
from tasks import retweet, post_to_slack
from config import settings
import sqlite3


class Retweeter(TwythonStreamer):
    def is_follower(self, user_id):
        conn = sqlite3.connect(settings['db_path'])
        c = conn.cursor()
        c.execute("""SELECT id FROM followers WHERE id='%s'""" % user_id)
        res = c.fetchone() is not None
        conn.close()
        return res

    def on_success(self, data):
        # only retweet if it's not a retweet
        if 'retweeted_status' not in data:
            # only retweets to followers of the specified account (unless there's no account specified)
            if 'only_followers_of' not in settings or self.is_follower(data['user']['id_str']):
                retweet.delay(data['id'])
                post_to_slack.delay(data)

    def on_error(self, status_code, data):
        print data
        print status_code

tw = settings['twitter']
stream = Retweeter(tw['APP_KEY'], tw['APP_SECRET'], tw['OAUTH_TOKEN'], tw['OAUTH_TOKEN_SECRET'])

stream.statuses.filter(track=settings['what_to_track'])
