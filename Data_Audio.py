from imports import *
import os
import eyed3
import datetime

class Audio:
    def get(self, what, filename):
        repl_group = {
            'tracknumber' : r'\1',
            'artist' : r'\2',
            'track' : r'\3',
            'name' : r'\3'
        }
        return re.sub(AUDIOS_FILENAME_REGEX, repl_group[what], filename)

    def fetch_tracks(self, what, **options):
        directory = self.parent.dirs.audio

        log.debug(f'Checking existence of directory "{directory}"...')

        if os.path.isdir(directory):
            log.debug('Fetching files in directory...')
            paths = [directory+i for i in os.listdir(directory) if is_ascii(i)]

            if len(paths) > 0:
                log.debug('Fetched files successfully')
                if not 'silent' in options: log.success(f'{len(paths)} track(s) found!')

            else: log.fatal(f'No files found in directory:\n{directory}')
        else:
            log.warn(f'Creating audio files directory')
            os.mkdir(directory)
            log.fatal(f"Can't find the audio files directory:\n{directory}")
        
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
            renaming_confirmed = ask.confirm(f'Some files are not in a good naming format. Do you want to rename them automatically ?\nNote that the tracknumbers will be assigned randomly (though 2 files won\'t have the same number)')
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

    def apply_metadata(self):
        # get date components for eyed3's custom Date() class
        date_Y = int(datetime.date.today().strftime('%Y'))
        date_m = int(datetime.date.today().strftime('%m'))
        date_d = int(datetime.date.today().strftime('%d'))

        metadata = {
            "artist" : self.parent.artist,
            "album" : self.parent.collection,
            "cover path" : self.parent.cover.get('square'),
            "date" : f'{date_d}/{date_m}/{date_Y}'
        }
        log.info('Metadata to apply:\n'+'\n'.join(kv_pairs(metadata)))

        for filepath in self.lists['paths']:
            noext = rmext(filename(filepath))
            log.debug('Loading file into eyed3...')
            audiofile = eyed3.load(filepath)

            # artist
            audiofile.tag.artist = audiofile.tag.album_artist = metadata['artist']
            # title
            audiofile.tag.title = self.get('track', filename(filepath))
            # album title
            audiofile.tag.album = metadata['album']
            # track number (current, total)
            audiofile.tag.track_num = (self.get('tracknumber', filename(filepath)), len(self.lists['paths']))
            # release date YYYY-MM-dd
            audiofile.tag.original_release_date = audiofile.tag.release_date = audiofile.tag.recording_date = eyed3.core.Date(date_Y, month=date_m, day=date_d)
            # album arts (type, imagedata, imagetype, description)
            audiofile.tag.images.set = (3, metadata['cover path'], 'image/png', COVERS_DESCRIPTION)

            log.debug(f'Saving tags to {filename(filepath)}...')
            try:
                audiofile.tag.save()
            except Exception as e:
                log.error('@eyed3:'+str(e))
            
        log.success('Applied metadata to all audio files')
            
            
            

    def __init__(self, parentself):
        self.parent = parentself
        self.lists = {}
        self.update_lists()

    def update_lists(self):
        self.lists['paths'] = self.fetch_tracks('paths')
        self.lists['filenames'] = [filename(i) for i in self.lists['paths']]
        self.lists['names'] = [rmext(i) for i in self.lists['filenames']]

    
        
