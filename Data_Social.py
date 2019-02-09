import json
import urllib

import tweepy

from cli import log, ask
from consts import *
from credentials import TW_CREDENTIALS
from utils import scheme


class Social:
    def __init__(self, parentself):
        self.parent = parentself
        self.msg_body = scheme(SOCIAL_MEDIAS_BODY_SCHEME, {
            'kind': self.parent.kind,
            'new_word': 'Nouvel' if self.parent.kind in ('ep', 'album') else 'Nouveau',
            'trackID': str(self.parent.audio.web_track_id),
            'title': self.parent.collection
        })

    def twitter(self):
        # auth
        log.debug('Connecting to twitter...')
        consumer_key = TW_CREDENTIALS['consumer_key']
        consumer_secret = TW_CREDENTIALS['consumer_secret']
        access_token = TW_CREDENTIALS['access_token']
        access_token_secret = TW_CREDENTIALS['access_token_secret']
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        # api creation
        twapi = tweepy.API(auth)

        # posting
        log.info(f'Tweet message:\n{self.msg_body}')
        if not TESTING_MODE:
            if ask.confirm(f'Do you want to tweet this?', task_name='tweet'):
                twapi.update_with_media(self.parent.cover.get('landscape'), self.msg_body)
                log.success('Tweet posted')
            else:
                log.warn('Tweet cancelled')
                self.parent.skipped_tasks.append('tweet')
        else:
            log.warn('Tweeting is disabled in testing mode.\nDisable testing mode by typing /config and then disable testing mode')
            self.parent.skipped_tasks.append('tweet')


