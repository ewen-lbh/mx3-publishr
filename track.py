# import as globals
from utils       import *
from cli         import *
from consts      import *
from pprint      import pprint
from PIL         import Image
from mutagen.mp3 import MP3
from shutil      import copyfile

# import as objects
import os
import numpy          as np
import moviepy.editor as mp

class Track:
    def __init__(self, data):
        for k,v in data.items():
            setattr(self,k,v)
        self.rawdata = data
        self.folders = self.Folders(self)
        self.cover = self.Cover(self)
        self.audio = self.Audio(self)
        self.video = self.Video(self)
        
    class Folders:
        def __init__(self, parentself):
            # inherit parentself as a parent object
            self.parent = parentself
            for k in BASEPATHS:
                setattr(self, k, BASEPATHS[k]+'/'+str(self.parent.collection)+'/')
    class Cover:
        def __init__(self, parentself):
            # inherit parentself as a parent object
            self.parent = parentself
        def format(self, format):
            scheme = FILENAME_SCHEMES['covers']
            return scheme.replace(f'[format]', str(format)).replace(f'[collection]', str(self.parent.collection))
        

    class Audio:
        def __init__(self, parentself):
            # inherit parentself as a parent object
            self.parent = parentself
        
        def format(self, **kwargs):
            scheme = FILENAME_SCHEMES['audios']
            for k, v in kwargs.items():
                scheme = scheme.replace(f'[{k}]', str(v))
            return scheme
        
        def list(self, returnstyle='path'):
            has_multiple_tracks = (self.parent.kind in COLLECTION_TYPES)
            if has_multiple_tracks:
                if os.path.isdir(self.parent.folders.audios):
                    log.debug('Fetching track list...')
                    fileslist = os.listdir(self.parent.folders.audios)
                    tracklist = []
                    for f in fileslist:
                        fname, fext = os.path.splitext(f)
                        # TODO conversion from wav to mp3
                        tracklist.append(switch({
                            'path'   : self.parent.folders.audios+f,
                            'relpath': f,
                            'name'   : fname,
                            'ext'    : fext
                        }, returnstyle))
                    return tracklist
                else:
                    log.fatal('No folder for audio files found.')
                    return False
            else:
                log.warn('The '+self.parent.kind+' shouldn\'t have multiple tracks.\n   This may cause errors. The script will continue as if the tracklist was not found.')
                return False
        def rename(self):
            regex_artistname = r'(.+) - (.+)'
            regex_full = AUDIOS_FILENAME_REGEX

            log.debug('Fetching tracklist for filename correction...')

            filenames = [get_filename(i) for i in os.listdir(path)]
            renamed_count = 0

            for i, filename in enumerate(filenames):
                if re.match(regex_full, filename):
                    renamed = False
                elif re.match(regex_artistname, filename):
                    renamed = intpadding(i)+' - '+filename
                    log.info('Assumed "'+filename+'" is of format <artist> - <track>')
                else :
                    renamed = intpadding(i)+' - '+artist+' - '+filename
                    log.info('Assumed "'+filename+'" is of format <track>')
                if renamed: 
                    log.info('Renaming '+filename+' to '+renamed)
                    try: 
                        os.rename(path+filename, path+renamed)
                        renamed_count+=1
                    except: 
                        log.error(f'Failed to rename {filename} to {renamed}.')
                        error_count+=1

            if renamed_count > 0:
                log.success(f'Renamed {renamed_count} file(s) successfully.')
                if error_count > 0: log.warn(f'Failed to rename {error_count} files')
            else:
                log.info('All files were already named correctly.')

    class Video:
        def __init__(self, parentself):
            # inherit parentself as a parent object
            self.parent = parentself  
        
        def list(self, returnstyle="path"):
            if os.isdir(self.parent.folders.videos):
                return os.listdir(self.parent.folders.videos)
            else:
                log.error('Music videos directory does not exist, creating one...')
                try:
                    os.mkdir(self.parent.folders.videos)
                    log.success(f'Directory "{self.parent.folders.videos}" created')
                except:
                    log.error(f'Failed to create directory:\n{self.parent.folders.videos}')
                return []

        def format(self, **kwargs):
            scheme = FILENAME_SCHEMES['videos']
            for k, v in kwargs.items():
                scheme = scheme.replace(f'[{k}]', str(v))
            return scheme

        def missing(self, retunstyle='path'):
            log.info('Getting missing videos...')
            videolist = self.list()
            tracklist = self.parent.audio.list()
            if len(videolist) == len(tracklist):
                log.info(f'No video missing')
                return []
            else:
                if returnstyle == 'path':
                    videos = videolist
                    audios = tracklist
                else:
                    videos = [filename(i) for i in videolist]
                    audios = [filename(i) for i in tracklist]

                missing_vids = list(set(audios) - set(videos))
                missing_vids_str = '\n'.join(missing_vids)
                log.info(f'Missing {len(missing_vids)} video(s):{missing_vids_str}')
                return missing_vids

        def create(self, trackname):
            filename = self.parent.

            log.debug('Getting duration from the audio file...')
            # Get length of video from the audio file
            duration = MP3(audio).info.length
            log.debug('Audio file duration : '+str(duration)+' seconds')
            duration = int(np.ceil(duration))
            log.debug('Future video duration : '+str(duration)+' seconds')

            log.debug('Getting audio data...')
            audio = mp.AudioFileClip(audio)
            log.debug('Getting image data...')
            image = mp.ImageClip(img, duration=duration)

            log.debug('Combining image and audio...')
            video = image.set_audio(audio)

            log.info('Writing file to "'+filename+'" with 30 fps...')
            video.write_videofile(self.parent.folders.videos+filename, fps=30, codec='libx264')
            log.success('Done!')
                
