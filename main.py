# import as globals
from imports import *
from Data import *
# import as objects
import debug
import glob

log.watermark()

# userdata collecting process


def get_userdata():
    global userdata
    global userdata_confirmed

    userdata = ask.userdata()

    if userdata != {}: 
        log.recap(userdata)
        userdata_confirmed = ask.confirm('Is this information correct ?')
    else:
        userdata_confirmed = False

if ENV == 'dev':
    # automatically remove files such as cover arts
    userdata = debug.userdata
    log.recap(userdata)
else:
    userdata = {}
    # handle re-asking
    get_userdata()
    while not userdata_confirmed:
        get_userdata()


# make new object with userdata (when its confirmed correct by user)
log.new_step()
# delete temporary MoviePy sound files
for filename in glob.glob(cwd_path()+'*TEMP_MPY*'):
    log.debug(f'Deleting temporary file {unix_slashes(filename)}...')
    os.remove(filename)
    log.debug(f'Deleted successfully.')

track = Data(userdata)

# recreate non-ideal situation to test audio files renaming, cover art & video generation
if ENV == 'dev': 
    log.warn('Recreating unideal initial file conditions...')
    debug.init(track)

log.new_step()
# rename tracks badly named
track.audio.rename()

log.new_step()
# add metadata to audio files
track.audio.apply_metadata()

# show fetched tracks
tracklist = '\n'.join(track.audio.lists['names'])
log.info(f"Tracklist:\n{tracklist}")
del tracklist


# getting cover arts
log.new_step()
if not track.cover.exists('landscape'):
    log.fatal('Landscape cover art not found')

if not track.cover.exists('square'):
    log.warn(
        'Square cover art not found.\nCropping the landscape version to make a square one...')
    crop_direction = ask.choices('What part of it do you want to keep ?', [
                                 'left', 'center', 'right'], shortcuts=True)
    log.debug(crop_direction)
    track.cover.make_square(crop_direction)
    del crop_direction
else:
    log.info('All cover art versions (square and landscape) found!')

log.new_step()
missing_vids = track.video.missing()
if len(missing_vids) > 0:
    missing_vids_str = '\n'.join(
        [re.sub(f'3$', r'4', filename(i)) for i in missing_vids]) # display video file names
    log.warn(f'{len(missing_vids)} video(s) missing:\n{missing_vids_str}')
    video_creation_confirmed = ask.confirm(
        'Want to generate videos automatically ? (this will take quite some time)\nNote that you can use Ctrl-C at any time to stop the script, if the video creation process gets too long or stuck.\nIf it gets stuck, please report the issue on github (ewen-lbh/mx3-publishr)')
    if video_creation_confirmed:
        for filename in missing_vids:
            track.video.create(filename)
    else:
        log.debug('Video creation step skipped. Your album will not be uploaded to YouTube.')
else:
    log.info('All videos found! \nThis saved you a sh*t ton of processing time :D')
