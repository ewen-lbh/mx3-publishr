from cli import *
import consts
from utils import *
from pprint import pprint

if consts.ENV != 'dev': 
    log.fatal('Whoops! \nScript still in construction! \nCome back later!')

log.watermark()
string='orjeog Ijire eofk ! 76  \n\t ejfoi'
log.fatal(sentence(string))