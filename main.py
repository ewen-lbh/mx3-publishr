# import as globals
from imports import *
from Data import *
# import as objects
import debugdata

log.watermark()

# userdata collecting process
def get_userdata():
    global userdata
    global userdata_confirmed

    # if not ask.confirm('Ask for data ?'):
    #     userdata = debugdata.userdata
    # else:
    #     userdata = ask.userdata()

    log.recap(userdata)

    userdata_confirmed = ask.confirm('Is this information correct ?')

if ENV == 'dev':
    userdata = debugdata.userdata
    log.recap(userdata)
else:
    # handle re-asking
    get_userdata()
    while not userdata_confirmed:
        get_userdata()


# make new object with userdata (when its confirmed correct by user)
log.new_step()
track = Data(userdata)

# rename tracks badly named
track.audio.rename()

# show fetched tracks
tracklist = '\n'.join(track.audio.lists['names'])
log.info(f"Tracklist:\n{tracklist}")
del tracklist



# getting cover arts
log.new_step()
if not track.cover.exists('landscape'): log.fatal('Landscape cover art not found')

if not track.cover.exists('square'):
    log.warn('Square cover art not found.\nCropping the landscape version to make a square one...')
    crop_direction = ask.choices('What part of it do you want to keep ?',['left','center','right'], shortcuts=True)
    log.debug(crop_direction)
    track.cover.make_square(crop_direction)
    del crop_direction
else:
    log.info('All cover art versions (square and landscape) found!')

log.new_step()
missing_vids = track.video.missing()
if len(missing_vids) > 0:
    missing_vids_str = '\n'.join([chext(filename(i) ,'mp4') for i in missing_vids])
    log.warn(f'{len(missing_vids)} video(s) missing:\n{missing_vids_str}')
    video_creation_confirmed = ask.confirm('Want to generate videos automatically ? (this will take quite some time)\nNote that you can use Ctrl-C at any time to stop the script, if the video creation process gets too long or stuck.\nIf it gets stuck, please report the issue on github (ewen-lbh/mx3-publishr)')
    if video_creation_confirmed:
        for filename in missing_vids:
            track.video.create(filename)
    else:
        log.fatal('Action cancelled.')
else:
    log.info('All videos found! \nThis saved you a sh*t ton of processing time :D')