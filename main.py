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
else:
    # handle re-asking
    get_userdata()
    while not userdata_confirmed:
        get_userdata()


# make new object with userdata (when its confirmed correct by user)
track = Data(userdata)


pprint(track.audio.fetch_tracks('paths'))
