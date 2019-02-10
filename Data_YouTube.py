from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

import debug
from Data import *

from utils import *


class YouTube:
	def __init__(self, parentself):
		self.service = self.auth()
		self.parent = parentself
		# tags from track list
		self.tags = [self.parent.audio.get('track', i) for i in self.parent.audio.lists['names']]
		# add collection, artist and kind to tags
		self.tags.extend([self.parent.artist, self.parent.collection, self.parent.kind])
		# add generic tags from consts
		self.tags += YOUTUBE_GENERIC_TAGS

		from credentials import YT_CREDENTIALS
		self.credentials = YT_CREDENTIALS

		# todo video_url
		self.video_url = 'nolink'

	def get_upload_data(self, video_path):
		data = {
			'snippet': {
				'categoryId'     : 22,  # 22 : Music category
				'defaultLanguage': 'en',
				'description'    : self.get_description(video_path),
				'tags'           : ', '.join(YOUTUBE_GENERIC_TAGS + \
				                             filename(rmext(video_path)).split()
				                             ),
				'title'          : self.get_video_title(video_path),
			},
			'status' : {
				'privacyStatus'      : 'private',
				'license'            : '',
				'embeddable'         : '',
				'publicStatsViewable': '',
			},
		}
		return data

	def get_track_title(self, video_path):
		return re.sub(r'(.+)\.$', r'\1', self.parent.audio.get('track', chext(filename(video_path), '.mp4')))

	def get_description(self, video_path=None):
		title = self.get_track_title(video_path) if video_path is not None else CLI_STYLING_CODES[
			                                                                        'DARK_RED'] + 'track title' + \
		                                                                        CLI_STYLING_CODES['ENDC']

		def _escape_trackname(string):
			return string.replace('_', '~_').replace(' ', '_')

		return scheme(YOUTUBE_DESCRIPTION_SCHEME, {
			'en_desc'          : self.parent.descriptions['en'],
			'fr_desc'          : self.parent.descriptions['fr'],
			'kind_pretty'      : self.parent.kind if self.parent.kind is not 'ep' else 'EP',  # changes "ep" to "EP"
			'trackID'          : self.parent.audio.web_track_id,
			'escaped_trackname': _escape_trackname(title),
			'trackname'        : title
		})

	def get_video_title(self, video_path=None):
		return scheme(YOUTUBE_TITLE_SCHEME, {
			'artist'    : self.parent.artist,
			'title'     : self.get_track_title(video_path) if video_path is not None else CLI_STYLING_CODES[
				                                                                              'DARK_RED'] +
			                                                                              'track title' +
			                                                                              CLI_STYLING_CODES['ENDC'],
			'collection': self.parent.collection,
			'kind'      : self.parent.kind
		})

	def auth(self):
		flow = InstalledAppFlow.from_client_secrets_file('secure/youtube_credentials.json',
		                                                 ['https://www.googleapis.com/auth/youtube.force-ssl'])
		credentials = flow.run_console()
		return build('youtube', 'v3', credentials=credentials)


	# creates a new youtube playlist with the album's name and return its id
	def create_playlist(self):
		service = self.service

		body = {
			'snippet': {
				'title'      : self.parent.collection,
				'description': '\n///\n'.join(self.parent.descriptions),
			},
			'status' : {
				'privacyStatus': 'public'
			}
		}

		response = service.playlists().insert(
			body=body,
		    part='snippet,status'
		).execute()

		return response['id']

	# returns the ID of the playlist in which the videos will be added
	def get_playlist(self):
		if self.parent.kind in list(YOUTUBE_KIND_PLAYLISTS.items()):
			return switch(self.parent.kind, YOUTUBE_KIND_PLAYLISTS)
		else:
			return self.create_playlist()


	def upload_video(self):
		file = self.parent.video.lists['paths'][0]
		body = self.get_upload_data(file)

		request = self.service.videos().insert(
			body=body,
			media_body=MediaFileUpload(file, chunksize=-1, resumable=True),
			part='snippet,status'
		)

		return resumable_upload(request, 'video', 'insert')



if __name__ == '__main__':
	track = Data(debug.userdata)
	playlist_id = track.youtube.get_playlist()
	track.youtube.upload_video()