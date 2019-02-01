from utils import *
from cli import *
import os

class Audio:
    def fetch_tracks(self, what, **options):
        log.debug(f'Checking existence of directory "{self.parent.dirs.audio}"...')

        if os.path.isdir(self.parent.dirs.audio):
            log.debug('Fetching files in directory...')
            try:
                paths = [BASEPATHS['audio']+i for i in os.listdir(self.parent.dirs.audio)]
                log.debug('Fetched files successfully')
                if not 'silent' in options: log.success(f'{len(paths)} track(s) found!')

            except: log.fatal(f"Couldn't open directory:\n{self.parent.dirs.audio}")
        else:
            log.fatal(f"Can't find the audio files directory:\n{self.parent.dirs.audio}")
        
        return switch(what, {
            'paths': paths,
            'filenames' : [filename(i) for i in paths],
            'names' : [rmext(filename(i)) for i in paths]
        })

    def __init__(self, parentself):
        self.parent = parentself
        self.lists = {}
        self.lists['paths'] = self.fetch_tracks('paths')
        self.lists['filenames'] = [filename(i) for i in self.lists['paths']]
        self.lists['names'] = [rmext(i) for i in self.lists['filenames']]

    
        
