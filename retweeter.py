from twython import TwythonStreamer
from tasks import retweet, post_to_slack
from config import settings


class Retweeter(TwythonStreamer):
    def on_success(self, data):
        if 'retweeted_status' not in data:
            retweet.delay(data['id'])
            post_to_slack.delay(data)

    def on_error(self, status_code, data):
        print data
        print status_code

tw = settings['twitter']
stream = Retweeter(tw['APP_KEY'], tw['APP_SECRET'], tw['OAUTH_TOKEN'], tw['OAUTH_TOKEN_SECRET'])

stream.statuses.filter(track=settings['what_to_track'])
