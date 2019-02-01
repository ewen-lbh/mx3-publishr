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

        audios = self.parent.audio.lists['names']
        videos = os.listdir(self.parent.dirs.video)
        videos = [rmext(filename(i)) for i in videos]
        return list(set(audios) - set(videos))

    def create(self, audio, **kwargs):
        img = self.parent.cover.get('landscape')
        videofilename = self.parent.audio.get('name', rmext(filename(audio)))+'.mp4'
        destfolder = self.parent.dirs.video
        fps = kwargs['fps'] or 30

        log.debug('Getting duration from the audio file...')
        # Get length of video from the audio file
        duration = MP3(audio).info.length
        log.debug(f'Audio file duration : {duration_format(duration)}')
        duration = int(np.ceil(duration))
        log.info(f'Future video duration : {duration_format(duration)}')

        log.debug('Getting audio data...')
        audio = mp.AudioFileClip(audio)
        log.debug('Getting image data...')
        image = mp.ImageClip(img, duration=duration)

        log.debug('Combining image and audio...')
        video = image.set_audio(audio)

        log.info(f'Writing file to "{videofilename}" with {fps} fps...')
        start_time = time.time()
        video.write_videofile(destfolder+videofilename, fps=fps, codec='libx264')
        end_time = time.time()
        log.success(f'Done!\nThe video {videofilename} took {duration_format(end_time - start_time)} to make')