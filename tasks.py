from celery import Celery
from twython import Twython
from config import settings
import requests

app = Celery('tasks', broker=settings['celery_broker'])
app.conf.CELERY_ACCEPT_CONTENT = ['json']
app.conf.CELERY_TASK_SERIALIZER = 'json'

@app.task
def retweet(tweet_id):
    tw = settings['twitter']
    twitter = Twython(tw['APP_KEY'], tw['APP_SECRET'], tw['OAUTH_TOKEN'], tw['OAUTH_TOKEN_SECRET'])
    twitter.retweet(id=tweet_id)

@app.task
def post_to_slack(tweet):
    requests.post(settings['slack_url'], json={
        'text': '<https://twitter.com/%s/status/%s|New tweet> using the hashtag' % (tweet['user']['screen_name'], tweet['id_str'])
    })
