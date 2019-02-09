import datetime
import subprocess

import yt_upload
from imports import *

class YouTube:
    def __init__(self, parentself):
        self.parent = parentself
        # tags from track list
        self.tags   = [self.parent.audio.get('track',i) for i in  self.parent.audio.lists['names']]
        # add collection, artist and kind to tags
        self.tags.extend([self.parent.artist, self.parent.collection, self.parent.kind])
        # add generic tags from consts
        self.tags += YOUTUBE_GENERIC_TAGS

        from credentials import YT_CREDENTIALS
        self.credentials = YT_CREDENTIALS

        # todo video_url
        self.video_url = 'nolink'

    def get_upload_data(self, video_path):
        metadata = {
            'title': self.get_video_title(video_path),
            'description': self.get_description(video_path),
            'category': '22',  # 22 = Music category
            'keywords': ', '.join(YOUTUBE_GENERIC_TAGS+filename(rmext(video_path)).split()),  # adds each word of the audio file (without extension) as a tag
            'privacyStatus': 'private',
            # 'auth_host_name': 'localhost',
            # 'auth_host_port': '8888',
            'logging_level': 'DEBUG',
            'file': video_path
        }
        return metadata

    def upload(self, data):
        upload_data = self.get_upload_data(data) if isinstance(data, str) else data



        vid_id = yt_upload.upload_video(upload_data)
        log.success(f'Video with ID "{vid_id or "error"}" was successfully uploaded')
        return vid_id

    def get_track_title(self, video_path):
        return re.sub(r'(.+)\.$', r'\1', self.parent.audio.get('track', chext(filename(video_path), '.mp4')))

    def get_description(self, video_path=None):
        title = self.get_track_title(video_path) if video_path is not None else CLI_STYLING_CODES['DARK_RED']+'track title'+CLI_STYLING_CODES['ENDC']
        def _escape_trackname(string):
            return string.replace('_', '~_').replace(' ', '_')
        return scheme(YOUTUBE_DESCRIPTION_SCHEME, {
            'en_desc': self.parent.descriptions['en'],
            'fr_desc': self.parent.descriptions['fr'],
            'kind_pretty': self.parent.kind if self.parent.kind is not 'ep' else 'EP',  # changes "ep" to "EP"
            'trackID': self.parent.audio.web_track_id,
            'escaped_trackname': _escape_trackname(title),
            'trackname': title
        })

    def get_video_title(self, video_path=None):
        return scheme(YOUTUBE_TITLE_SCHEME, {
            'artist': self.parent.artist,
            'title': self.get_track_title(video_path) if video_path is not None else CLI_STYLING_CODES['DARK_RED']+'track title'+CLI_STYLING_CODES['ENDC'],
            'collection': self.parent.collection,
            'kind': self.parent.kind
        })

    def create_playlist(self):
        output = subprocess.check_output('py ')






