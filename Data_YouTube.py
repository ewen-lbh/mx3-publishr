import datetime
import subprocess

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

    def get_upload_data(self, video_path):
        title = re.sub(r'(.+)\.$', r'\1', self.parent.audio.get('track', chext(video_path, '.mp4')))

        def _escape_trackname(string):
            return string.replace('_', '~_').replace(' ', '_')

        metadata = {
            'title': scheme(YOUTUBE_TITLE_SCHEME, {
                'artist': self.parent.artist,
                'title': title,
                'collection': self.parent.collection,
                'kind': self.parent.kind
            }),
            # using repr() to escape newline (\n) chars
            'description': repr(scheme(YOUTUBE_DESCRIPTION_SCHEME, {
                'en_desc': self.parent.descriptions['en'],
                'fr_desc': self.parent.descriptions['fr'],
                'kind_pretty': self.parent.kind if self.parent.kind is not 'ep' else 'EP',  # changes "ep" to "EP"
                'trackID': self.parent.social._get_track_id(),
                'escaped_trackname': _escape_trackname(title),
                'trackname': title
            })),
            'category': 'Music',
            'tags': ', '.join(YOUTUBE_GENERIC_TAGS+filename(rmext(video_path)).split()),  # adds each word of the audio file (without extension) as a tag
            'publish-at': (datetime.datetime.now() + datetime.timedelta(**YOUTUBE_DELAY)).isoformat(),
            'client-secrets': cwd_path()+'.client_secrets.json'
        }
        flags = (
            'auth-browser',
            'open-link'
        )
        return metadata, flags, video_path

    def upload(self, data):
        upload_data = self.get_upload_data(data) if isinstance(data, str) else data
        metadata = upload_data[0]
        cmd_flags = upload_data[1]
        video_file = upload_data[2]

        cmd = 'py external_scripts/youtube-upload/youtube_upload '
        for k, v in metadata.items():
            cmd += f'--{k}="{v}" ' if k is not None and v is not None else ''
        for i in cmd_flags:
            cmd += f'--{i} ' if i is not None else ''
        cmd += video_file

        # log.debug(cmd)
        subprocess.call(cmd)





