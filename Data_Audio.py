from utils import *
from cli import *
import os

class Audio:
    def get(self, what, name):
        repl_group = {
            'tracknumber' : r'\1',
            'artist' : r'\2',
            'track' : r'\3',
            'name' : r'\3'
        }
        return re.sub(AUDIOS_FILENAME_REGEX, repl_group[what], name)

    def fetch_tracks(self, what, **options):
        log.debug(f'Checking existence of directory "{self.parent.dirs.audio}"...')

        if os.path.isdir(self.parent.dirs.audio):
            log.debug('Fetching files in directory...')
            try:
                paths = [self.parent.dirs.audio+i for i in os.listdir(self.parent.dirs.audio)]
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

    def rename(self):
        regex_artistname = r'(.+) - (.+)'
        regex_full = r'(\d{2,}) - (.+) - (.+)'

        log.debug('Fetching tracklist for filename correction...')

        filenames = os.listdir(self.parent.dirs.audio)
        renamed_count = 0

        for i, filename in enumerate(filenames):
            if re.match(regex_full, filename):
                renamed = False
            elif ask.confirm(f'File {filename} is not in a good format. Do you want to rename it automatically ?\nNote that the tracknumber will be assigned randomly (though 2 files won\'t have the same number)'):
                if re.match(regex_artistname, filename):
                    renamed = intpadding(i+1)+' - '+filename # we add +1 to the index to avoid having a "00" tracknumber.
                    log.warn('Assumed "'+filename+'" is of format <artist> - <track>')
                else:
                    artist = self.parent.artist
                    renamed = intpadding(i+1)+' - '+artist+' - '+filename # we add +1 to the index to avoid having a "00" tracknumber.
                    log.warn('Assumed "'+filename+'" is of format <track>')
                if renamed: 
                    log.debug('Renaming '+filename+' to '+renamed)
                    os.rename(path+filename, path+renamed)
                    renamed_count+=1
            else:
                log.fatal('User chose to close the script')

        if renamed_count > 0:
            log.success(f'Renamed {renamed_count} files successfully.')
        else:
            log.info('All files were named correctly. Good job !')

    def __init__(self, parentself):
        self.parent = parentself
        self.lists = {}
        self.lists['paths'] = self.fetch_tracks('paths')
        self.lists['filenames'] = [filename(i) for i in self.lists['paths']]
        self.lists['names'] = [rmext(i) for i in self.lists['filenames']]

    
        
