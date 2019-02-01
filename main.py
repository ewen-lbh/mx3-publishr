# import as globals
from utils import *
from cli import *
from consts import *
from Data import *
from pprint import pprint
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
track = Data(userdata)

# getting cover arts
if not track.cover.exists('landscape'): log.fatal('Landscape cover art not found')

if not track.cover.exists('square'):
    log.warn('Square cover art not found.\nCropping the landscape version to make a square one...')
    crop_direction = ask.choices('What part of it do you want to keep ?',['left','center','right'], shortcuts=True)
    track.cover.make_square(crop_direction)
    del crop_direction
else:
    log.info('All cover art versions (square and landscape) found !')