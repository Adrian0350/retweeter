from celery import Celery
from twython import Twython
from config import settings

app = Celery('tasks', broker=settings['celery_broker'])

@app.task
def retweet(tweet_id):
    tw = settings['twitter']
    twitter = Twython(tw['APP_KEY'], tw['APP_SECRET'], tw['OAUTH_TOKEN'], tw['OAUTH_TOKEN_SECRET'])
    twitter.retweet(id=tweet_id)
