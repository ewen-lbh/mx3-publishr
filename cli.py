from consts import *
from utils import *
import sys


class log:
    @staticmethod
    def log(text, logtype):
        lines = text.split('\n')
        # get the indicator according to logtype and consts.
        indicator = LOG_TYPES[logtype]+LOG_TYPE_SEPARATOR+' '
        # add a space (' ') for each indicator character
        indent = ''.join([' '] * len(indicator))
        # add indicator and the first line to msg
        msg = indicator+lines[0]
        # add indent to all other lines
        del lines[0]
        for i, line in enumerate(lines):
            msg += '\n'+indent+line
        print(msg)

    def watermark():
        print(WATERMARK)

    def fatal(text='Internal Error', errmsg=None, exit_script=True):
        log.log(text, 'fatal')
        if exit_script:
            # if errmsg isn't provided, get it from the text,
            # but remove linebreaks, and add ellipsis if too long
            if errmsg is None: errmsg = truncate(
                text.replace('\\n', ' '), 50, '...')
            raise SystemExit(errmsg)

    def debug(text):
        if VERBOSE_OUTPUT:
            log.log(text, 'debug')


class ask:
    @staticmethod
    def anything(text, flags=[]):
        log.question(text+'\n')
        answer = input(USER_INPUT_INDICATOR)
        if not 'case_sensitive' in flags:
            answer = answer.lower()
        return answer

    @staticmethod
    def choices(text, choices):
        choicestr = '/'.join(choices)
        text += '\n('+choicestr+')'
        answer = ask.anything(text)
        while answer not in choices:
            log.error('"'+answer+'" is not a valid answer, retrying...')
            answer = ask.anything(text)
        return answer

    @staticmethod
    def confirm(text):
        answer = ask.choices(text, ['y', 'n'])
        return answer == 'y'

    @staticmethod
    def userdata():
        userdata = {}
        # --- TRACK TYPE ---
        userdata['type'] = ask.choices('Please enter the kind of track you want to publish',AVAIL_KINDS)
        
        # --- GETTING ARTIST ---
        if AUTO_DETECT_OC:
            is_oc = userdata['type'] != 'remix'
        else:
            # Ask if the artist != SELF_NAME (dont ask if its a remix, obviously)
            if userdata['type'] != 'remix':
                is_oc = ask.confirm('Did you ('+SELF_NAME+') created this from scratch ?')
            else:
                is_oc = False

        # If the artist isn't SELF_NAME, ask for it:
        if is_oc:
            userdata['artist'] = SELF_NAME
        else:
            userdata['artist'] = ask.anything('Who did the original track ?')
            
        # --- COLLECTION NAME ---
        userdata['collection'] = ask.anything('Please enter the '+userdata['type']+' name')

        return userdata


# add missing log variants from LOG_TYPES if not defined yet
for level in LOG_TYPES: 
    if not hasattr(log, level):
        setattr(log, level, staticmethod(lambda text, level=level: log.log(text, level)))