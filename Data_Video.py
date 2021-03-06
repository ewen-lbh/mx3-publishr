import math
import time
import os
import moviepy.editor as mp
from mutagen.mp3 import MP3
from cli import *




class Video:
	def __init__(self, parentself):
		self.parent = parentself
		self.lists = dict()
		self.update_lists()

	# returns audio file paths of tracks that doesn't have videos
	def missing(self, what='audio'):
		ext = switch(what, {
			'audio': '.mp3',
			'video': '.mp4'
		})
		# if the video folder isn't there, create one
		if not os.path.isdir(self.parent.dirs.video):
			log.warn('Video folder path not found, creating one...')
			os.mkdir(self.parent.dirs.video)
			log.debug(f'Created directory {self.parent.dirs.video}')

		audios = self.parent.audio.lists['names']
		videos = os.listdir(self.parent.dirs.video)
		videos = [rmext(filename(i)) for i in videos]
		missing_names = list(set(audios) - set(videos))
		return [self.parent.dirs.audio + name + ext for name in missing_names]

	def create(self, audio, **kwargs):
		img = self.parent.cover.get('landscape')
		video_file_name = self.parent.audio.get('name', rmext(filename(audio))) + '.mp4'
		dest_folder = self.parent.dirs.video
		try:
			fps = kwargs['fps']
		except KeyError:
			fps = 30

		log.debug('Getting duration from the audio file...')
		# Get length of video from the audio file
		duration = MP3(audio).info.length
		log.debug(f'Audio file duration : {duration_format(duration)}')
		duration = int(math.ceil(duration))
		log.info(f'Future video duration : {duration_format(duration)}')

		log.debug('Getting audio data...')
		audio = mp.AudioFileClip(audio)
		log.debug('Getting image data...')
		image = mp.ImageClip(img, duration=duration)

		log.debug('Combining image and audio...')
		video = image.set_audio(audio)

		log.info(f'Writing file to "{video_file_name}" with {fps} fps...')
		start_time = time.time()
		video.write_videofile(dest_folder + video_file_name, fps=fps, codec='libx264')
		end_time = time.time()
		log.success(f'Done!\nThe video {video_file_name} took {duration_format(end_time - start_time)} to make')

	def update_lists(self):
		log.debug('Updating video lists...')
		if not os.path.isdir(self.parent.dirs.video):
			log.warn(f'Videos folder not found. Creating directory:\n{self.parent.dirs.video}')
			os.mkdir(self.parent.dirs.video)

		self.lists['paths'] = [self.parent.dirs.video + i for i in os.listdir(self.parent.dirs.video)]
		self.lists['filenames'] = [filename(i) for i in self.lists['paths']]
		self.lists['names'] = [rmext(i) for i in self.lists['filenames']]