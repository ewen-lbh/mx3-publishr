from utils import *
from cli import *
import os

class Audio:
    def fetch_tracks(self, what, **kwargs):
        log.debug(f'Checking existence of directory "{self.parent.dirs.audio}"...')

        if os.path.isdir(self.parent.dirs.audio):
            log.debug('Fetching files in directory...')
            try:
                paths = os.listdir(self.parent.dirs.audio)
                log.debug('Fetched files successfully')
                if not 'silent' in kwargs: log.success(f'{len(paths)} track(s) found!')

            except: log.fatal(f"Couldn't open directory:\n{self.parent.dirs.audio}")
        else:
            log.fatal(f"Can't find the audio files directory:\n{self.parent.dirs.audio}")
        
        switch(what, {
            'paths': paths,
            'filenames' : [filename(i) for i in paths],
            'names' : [rmext(filename(i)) for i in paths]
        })


    def __init__(self, parentself):
        self.parent = parentself
        self.lists = {}
        self.lists['paths'] = self.fetch_tracks('paths', silent=True)
        self.lists['filenames'] = self.fetch_tracks('filenames', silent=True)
        self.lists['names'] = self.fetch_tracks('names', silent=True)

    
        
