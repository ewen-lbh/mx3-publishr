# import as globals
from utils import *
from cli import *
from consts import *
from Data import *
from pprint import pprint
# import as objects
import debugdata

log.watermark()

if ENV != 'dev':
    log.fatal('Whoops! \nScript still in construction! \nCome back later!')

if not ask.confirm('Ask for data ?'):
    userdata = debugdata.userdata
else:
    userdata = ask.userdata()

if userdata is None:
    log.fatal()

track = Data(userdata)
pprint(track.audio.lists['paths'])
