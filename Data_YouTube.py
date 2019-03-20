import datetime
import locale

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import debug
from Data import *
from cli import ask

from utils import *


class YouTube:
	def __init__(self, parentself):
		self.upload_count = 0
		self.parent = parentself
		# tags from track list
		self.tags = [self.parent.audio.get('track', i) for i in self.parent.audio.lists['names']]
		# add collection, artist and kind to tags
		self.tags.extend([self.parent.artist, self.parent.collection, self.parent.kind])
		# add generic tags from consts
		self.tags += YOUTUBE_GENERIC_TAGS

		self.playlist_id = None

		# todo video_url
		self.video_url = 'nolink'

	def _upload_data(self, video_path):
		data = type('',(),{})()
		data.description = self._description(video_path),
		data.tags        = ', '.join(YOUTUBE_GENERIC_TAGS + \
		                        filename(rmext(video_path)).split()
		                        ),
		data.title       = self._video_title(video_path),
		data.publish     = self._release_date()
		return data

	def _track_title(self, video_path):
		return re.sub(r'(.+)\.$', r'\1', self.parent.audio.get('track', chext(filename(video_path), '.mp4')))

	@staticmethod
	def _release_date():
		locale.setlocale(locale.LC_ALL, "fr_FR.UTF-8")
		raw = datetime.datetime.now() + datetime.timedelta(**YOUTUBE_DELAY)
		string = raw.strftime('%d [m] %Y')
		month = (raw.strftime('%B').lower()[:4] + '.')
		formatted = scheme(string, {'m': month})
		return formatted

	def _description(self, video_path=None):
		title = self._track_title(video_path) if video_path is not None else CLI_STYLING_CODES[
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
			'trackname'        : title,
			'collection'       : self.parent.collection
		})

	def _video_title(self, video_path=None):
		return scheme(YOUTUBE_TITLE_SCHEME, {
			'artist'    : self.parent.artist,
			'title'     : self._track_title(video_path) if video_path is not None else CLI_STYLING_CODES[
				                                                                              'DARK_RED'] +
			                                                                              'track title' +
			                                                                           CLI_STYLING_CODES['ENDC'],
			'collection': self.parent.collection,
			'kind'      : self.parent.kind
		})

	def print_info(self):
		for path in self.parent.video.lists['paths']:
			data = {
				"title": self._video_title(path),
				"description": self._description(path)
			}
			log.info(f"Infos for video '{filename(path)}':"+"\n".join(kv_pairs(data)))
