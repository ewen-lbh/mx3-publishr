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

    def fatal(text, errmsg=None, exit_script=True):
        log.log(text, 'fatal')
        if exit_script:
            # if errmsg isn't provided, get it from the text,
            # but remove linebreaks, and add ellipsis if too long
            if errmsg is None: errmsg = truncate(
                text.replace('\\n', ' '), 20, '...')
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
        log.question(text)
        answer = ask.anything(text)
        while answer not in choices:
            log.error('"'+answer+'" is not a valid answer, retrying...')
            answer = ask.anything()
        return answer

    @staticmethod
    def confirm(text):
        answer = ask.choices(text, ['y', 'n'])
        return answer == 'y'


# add missing log variants from LOG_TYPES if not defined yet
for level in LOG_TYPES: 
    if not hasattr(log, level):
        setattr(log, level, staticmethod(lambda text, level=level: log.log(text, level)))