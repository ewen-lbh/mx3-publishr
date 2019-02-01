from imports import *
from mutagen.mp3 import MP3
import moviepy.editor as mp

class Video:
    def __init__(self, parentself):
        self.parent = parentself

    def missing(self):
        # if the video folder isnt there, create one and return all tracks as videos to make (since no video exists)
        if not os.path.isdir(self.parent.dirs.video): 
            log.warn('Video folder path not found, creating one...')
            os.mkdir(self.parent.dirs.video)
            log.debug(f'Created directory {self.parent.dirs.video}')
            return self.parent.audio.lists['paths']


        return list(set(self.parent.audio.lists['paths']) - set(os.listdir(self.parent.dirs.video)))

    def create(self, audio):
        img = self.parent.cover.get('landscape')
        videofilename = self.parent.audio.get('name', rmext(filename(audio)))+'.mp4'
        destfolder = self.parent.dirs.video

        log.debug('Getting duration from the audio file...')
        # Get length of video from the audio file
        duration = MP3(audio).info.length
        log.debug('Audio file duration : '+str(duration)+' seconds')
        duration = int(np.ceil(duration))
        log.info('Future video duration : '+str(duration)+' seconds')

        log.debug('Getting audio data...')
        audio = mp.AudioFileClip(audio)
        log.debug('Getting image data...')
        image = mp.ImageClip(img, duration=duration)

        log.debug('Combining image and audio...')
        video = image.set_audio(audio)

        log.info('Writing file to "'+videofilename+'" with 30 fps...')
        video.write_videofile(destfolder+videofilename, fps=30, codec='libx264')
        log.success('Done!')