from consts import *
from utils import *
import sys


class log:
    @staticmethod
    def log(text, logtype, method='print'):
        lines = text.split('\n')
        # get the indicator according to logtype and consts.
        indicator = LOG_TYPES_WRAP[0]+LOG_TYPES[logtype]+LOG_TYPES_WRAP[1]+' '
        # add a space (' ') for each indicator character
        indent = ''.join([' '] * len(indicator))
        # add indicator and the first line to msg
        msg = indicator+lines[0]
        # add indent to all other lines
        del lines[0]
        for i, line in enumerate(lines):
            msg += '\n'+indent+line
        if method == 'print':
            print(msg)
            with open('latest.log', 'a') as f:
                f.write(msg+'\n')

        elif method == 'return':
            return msg

    @staticmethod
    def watermark():
        print(WATERMARK)

    @staticmethod
    def recap(userdata):
        msg = "To recap, here's all the information you gave..."
        for prop, val in userdata.items():
            msg += f"\n{prop.title()}: {truncate(val, 30)}"
        log.info(msg)


    @staticmethod
    def fatal(text='Unknown Error', errmsg=None, exit_script=True):
        if exit_script: 
            sys.exit(log.log(text, 'fatal', method='return'))
        else:
            log.log(text, 'fatal')

    @staticmethod
    def debug(text):
        if VERBOSE_OUTPUT:
            log.log(text, 'debug')

    @staticmethod
    def section(section):
        if SECTION_UPPERCASE: section = section.upper()
        print(f'\n\n\n{SECTION_WRAP[0]+section+SECTION_WRAP[1]}\n')


class ask:
    @staticmethod
    def anything(text, flags=[]):
        log.question(text+'\n')
        try:
            answer = input(USER_INPUT_INDICATOR)
        except KeyboardInterrupt:
            sys.exit('Script closed.')
        if not 'case_sensitive' in flags:
            answer = answer.lower()
        if not 'accept_non_ascii' in flags and not is_ascii(answer):
            log.fatal('The answer contains special characters.\nOnly ASCII characters are allowed for now.')
        return answer


    @staticmethod
    def choices(text, choices, **options):

        choicestr = '/'.join(choices)
        
        if 'shortcuts' in options:
            orig_choices = choices
            choices = [i[0] for i in choices]
            text += f'\nyou can use only the first letter to make your choice, eg. "{choices[0]}" = "{orig_choices[0]}"'

        text += '\n('+choicestr+')'

        answer = ask.anything(text)

        if 'shortcuts' in options: answer = answer[0]

        while answer not in choices:
            log.error('"'+answer+'" is not a valid answer, retrying...')
            answer = ask.anything(text)

        if 'shortcuts' in options: answer = search_with_nth_char(orig_choices, answer)[1]
        return answer
    @staticmethod
    def confirm(text):
        answer = ask.choices(text, ['y', 'n'])
        return answer == 'y'

    @staticmethod
    def userdata():
        userdata = dict()
        # --- TRACK KIND ---
        userdata['kind'] = ask.choices('Please enter the kind of track you want to publish',AVAIL_KINDS, shortcuts=True)
        
        # --- GETTING ARTIST ---
        if AUTO_DETECT_OC:
            is_oc = userdata['kind'] != 'remix'
        else:
            # Ask if the artist != SELF_NAME (dont ask if its a remix, obviously)
            if userdata['kind'] != 'remix':
                is_oc = ask.confirm('Did you ('+SELF_NAME+') created this from scratch ?')
            else:
                is_oc = False

        # If the artist isn't SELF_NAME, ask for it:
        if is_oc:
            userdata['artist'] = SELF_NAME
        else:
            userdata['artist'] = ask.anything('Who did the original track ?', flags=['case_sensitive'])
            
        # --- COLLECTION NAME ---
        userdata['collection'] = ask.anything('Please enter the '+userdata['kind']+' name', flags=['case_sensitive'])

        return userdata


# add missing log variants from LOG_TYPES if not defined yet
for level in LOG_TYPES: 
    if not hasattr(log, level):
        setattr(log, level, staticmethod(lambda text, level=level: log.log(text, level)))