from cli import *
import consts
from utils import *
from pprint import pprint

log.watermark()

if consts.ENV != 'dev': 
    log.fatal('Whoops! \nScript still in construction! \nCome back later!')