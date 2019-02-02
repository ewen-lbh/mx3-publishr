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
        # pattern checking variables
        regex_artistname = r'(.+) - (.+)'
        regex_full = r'(\d{2,}) - (.+) - (.+)'

        # getting tracks to rename
        log.debug('Fetching tracklist for filename correction...')
        filenames = os.listdir(self.parent.dirs.audio)
        to_be_renamed = [i for i in filenames if not re.match(regex_full, i)]

        # if there are any tracks to rename...
        if len(to_be_renamed) > 0: 
            # ask for renaming confirmation...
            renaming_confirmed = ask.confirm(f'Some files are not in a good naming format. Do you want to rename it automatically ?\nNote that the tracknumber will be assigned randomly (though 2 files won\'t have the same number)')
            if not renaming_confirmed: log.fatal('User chose to close the script')

            # tracking variables
            renamed_count = 0
            renamed_all = []
            # data variables
            path = self.parent.dirs.audio
            artist = self.parent.artist

            # for each file to be renamed
            for i, filename in enumerate(to_be_renamed):
                # format cases handling
                if re.match(regex_artistname, filename):
                    renamed = intpadding(i+1)+' - '+filename # we add +1 to the index to avoid having a "00" tracknumber.
                    log.warn(f'Assumed "{filename}" is of format <artist> - <track>')
                else:
                    renamed = intpadding(i+1)+' - '+artist+' - '+filename # we add +1 to the index to avoid having a "00" tracknumber.
                    log.warn(f'Assumed "{filename}" is of format <track>')

                # renaming
                log.debug(f'Renaming {filename} to {renamed}')
                os.rename(path+filename, path+renamed)
                renamed_all.append(path+renamed)
                renamed_count+=1

                # loggging, updating lists
                log.success(f'Renamed {renamed_count} files successfully.')
                log.debug(f'Updating lists...')
                self.update_lists()
        else:
            log.debug('Nope! All good :D')

    def __init__(self, parentself):
        self.parent = parentself
        self.lists = {}
        self.update_lists()

    def update_lists(self):
        self.lists['paths'] = self.fetch_tracks('paths')
        self.lists['filenames'] = [filename(i) for i in self.lists['paths']]
        self.lists['names'] = [rmext(i) for i in self.lists['filenames']]

    
        
