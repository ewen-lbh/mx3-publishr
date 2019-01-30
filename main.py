# import as globals
from utils  import *
from cli    import *
from consts import *
from pprint import pprint
# import as objects
# ...

log.watermark()

if consts.ENV != 'dev': 
    log.fatal('Whoops! \nScript still in construction! \nCome back later!')