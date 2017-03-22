import os

settings = {
    'twitter': {
        'APP_KEY': os.environ['TW_APP_KEY'],
        'APP_SECRET': os.environ['TW_APP_SECRET'],
        'OAUTH_TOKEN': os.environ['TW_OAUTH_TOKEN'],
        'OAUTH_TOKEN_SECRET': os.environ['TW_OAUTH_SECRET'],
    },
    'celery_broker': os.environ['CELERY_BROKER'],
    'slack_url': '',
    'db_path': '',
    'update_status_path': '',
    'only_followers_of': [''],
    'what_to_track': os.environ['WHAT_TO_TRACK']
}
