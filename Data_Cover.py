from consts import *
from utils import *
from cli import *
import os
from PIL import Image
import numpy as np

class Cover:
    def __init__(self, parentself):
        self.parent = parentself

    def get(self, what):
        base = self.parent.dirs.cover

        filename = scheme(FILENAME_SCHEMES['cover'], {
            'artist' : self.parent.artist,
            'collection' : self.parent.collection,
            'format' : what
        })

        return base+filename

    def make_square(self, direction='center'):
        im = Image.open(self.get('landscape'))
        w, h = im.size   # Get dimensions
        log.debug(f"Image dimensions:{w} by {h}")
        neww = np.floor(w/2)
        newh = h
        if w != 1920 or h != 1080:
            log.warn("Image dimensions aren't regular (1920x1080)")

        if direction=='right':
            left = w - neww
            bottom = 0
            right = w
            top = newh
            direction_msg = 'to the right'

        elif direction=='left':
            left = 0
            bottom = 0
            right = neww
            top = newh
            direction_msg='to the left'

        else:
            left = (w - neww) / 2
            bottom = 0
            right = (w+neww) / 2
            top = newh
            direction_msg='in the center'

        log.debug("Cropping "+direction_msg+'...')

        im.crop((left,bottom,right,top)).save(self.get('square'))

        log.success(f"Square cover art successfully saved under the name:\n{self.get('square')}")
    
    def exists(self, what):
        log.debug(f'Checking existence of file {self.get(what)}')
        return os.path.isfile(self.get(what))
