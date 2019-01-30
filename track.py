# import as globals
from utils  import *
from cli    import *
from consts import *
# import as objects
import os

class Track:
    def __init__(self, data):
        for k,v in enumerate(data):
            setattr(self,v,k)
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
        

    class Audio:
        def __init__(self, parentself):
            # inherit parentself as a parent object
            self.parent = parentself
        
        def list(self, returnstyle='path'):
            has_multiple_tracks = (self.parent.tracktype in COLLECTION_TYPES)
            if has_multiple_tracks:
                audiofolder_path = get_resource_path('audiofolder', self.parent.collection)
                if os.path.isdir(audiofolder_path):
                    log.debug('Fetching track list...')
                    fileslist = os.listdir(audiofolder_path)
                    tracklist = []
                    for f in fileslist:
                        fname, fext = os.path.splitext(f)
                        # TODO conversion from wav to mp3
                        tracklist.append(switch({
                            'path'   : audiofolder_path+f,
                            'relpath': f,
                            'name'   : fname,
                            'ext'    : fext
                        }, returnstyle))
                    return tracklist
                else:
                    log.fatal('No folder for audio files found.')
                    return False
            else:
                log.warn('The '+self.parent.tracktype+' shouldn\'t have multiple tracks.\n   This may cause errors. The script will continue as if the tracklist was not found.')
                return False

    class Video:
        def __init__(self, parentself):
            # inherit parentself as a parent object
            self.parent = parentself  
        
        def list(self, returnstyle="path"):
            if os.isdir(self.parent.folders.video):
                return os.listdir(self.parent.folders.video)
            else:
                log.error('Music videos directory does not exist, creating one...')
                os.mkdir(self.parent.folders.video)
                log.success(f'Directory "{self.parent.folders.video}" created')
                return []

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
            

