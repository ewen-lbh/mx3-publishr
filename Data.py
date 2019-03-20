import json

from cli import log
from utils import *


class Data:
	from Data_Dirs import Dirs
	from Data_Cover import Cover
	from Data_Audio import Audio
	from Data_Video import Video

	from Data_Website import Website
	from Data_YouTube import YouTube
	from Data_Social import Social

	def __init__(self, rawdata=None, **kwargs):
		if 'from_record' in kwargs:
			data = self.from_record()
		else:
			# Decide whether to import data from dict or from keyword args
			data = rawdata if not None else kwargs

		self.raw_data = data
			# programmatically add all data dict items as object properties
		for k, v in data.items():
			setattr(self, k, v)

		# define inner classes and passes parent self to them
		self.dirs = self.Dirs(self)
		self.cover = self.Cover(self)
		self.audio = self.Audio(self)
		self.video = self.Video(self)

		self.website = self.Website(self)
		# self.youtube = self.YouTube(self) # disabled youtube since it doesn't rly work
		self.social = self.Social(self)

		# Recap found tracks
		track_paths_map = dict(zip(self.audio.lists['names'], self.audio.lists['paths']))
		log.info('Audio track paths:\n' + '\n'.join(kv_pairs(track_paths_map, used_scheme='/cSpace')))


