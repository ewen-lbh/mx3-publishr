import os
import sys

from cli import log
from consts import *


class Dirs:
	def __init__(self, parentself):
		self.parent = parentself
		self.audio = BASEPATHS['audio'] + str(self.parent.collection) + '/'
		self.cover = BASEPATHS['cover'] + str(self.parent.collection) + '/'
		self.video = BASEPATHS['video'] + str(self.parent.collection) + '/'

		notfounds = list()
		for path in [self.audio, self.cover, self.video]:
			if not os.path.isdir(path):
				notfounds.append(path)

		if notfounds:
			log.fatal(f"The following path{'s' if len(notfounds) > 1 else ''} do{'es' if len(notfounds) == 1 else ''} "
			          f"not "
			          f"exist:\n" +"\n".join(notfounds))
			sys.exit(1)

