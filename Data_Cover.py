import math

from PIL import Image

from cli import *


class Cover:
	def __init__(self, parentself):
		self.parent = parentself
		self.lists = {}
		self.update_lists()

	def get(self, what):
		base = self.parent.dirs.cover

		filename = scheme(FILENAME_SCHEMES['cover'], {
			'artist'    : self.parent.artist,
			'collection': self.parent.collection,
			'format'    : what
		})

		return base + filename

	def make_square(self, direction='center'):
		im = Image.open(self.get('landscape'))
		w, h = im.size  # Get dimensions
		log.debug(f"Image dimensions:{w} by {h}")
		neww = math.floor(w / 2)
		newh = h
		if w != 1920 or h != 1080:
			log.warn("Image dimensions aren't regular (1920x1080)")

		if direction == 'right':
			left = w - neww
			bottom = 0
			right = w
			top = newh
			direction_msg = 'to the right'

		elif direction == 'left':
			left = 0
			bottom = 0
			right = neww
			top = newh
			direction_msg = 'to the left'

		else:
			left = (w - neww) / 2
			bottom = 0
			right = (w + neww) / 2
			top = newh
			direction_msg = 'in the center'

		log.info("Cropping " + direction_msg + '...')
		im.crop((left, bottom, right, top)).save(self.get('square'))

		log.success(f"Square cover art successfully saved under the name:\n{self.get('square')}")
		self.update_lists()
		im.close()

	def make_lowres(self):
		if ask.confirm('Create low resolution version of cover arts ?', task_name='website'):
			for src in self.lists['paths']:
				png = Image.open(src)
				png.load()  # required for png.split()

				background = Image.new("RGB", png.size, (255, 255, 255))
				background.paste(png, mask=png.split()[3])  # 3 is the alpha channel

				background.save(self.parent.dirs.cover + chext(filename(src), 'jpg'), 'JPEG', quality=80)

	def exists(self, what):
		log.debug(f'Checking existence of file {self.get(what)}')
		return os.path.isfile(self.get(what))

	def update_lists(self):
		log.debug('Fetching cover arts ...')
		self.lists['paths'] = [self.parent.dirs.cover + i for i in os.listdir(self.parent.dirs.cover)]
		self.lists['filenames'] = [filename(i) for i in self.lists['paths']]
		self.lists['names'] = [rmext(i) for i in self.lists['filenames']]

	def delete_lowres(self):
		for cover_art in [i for i in os.listdir(self.parent.dirs.cover) if '.jpg' in i]:
			os.remove(self.parent.dirs.cover + cover_art)