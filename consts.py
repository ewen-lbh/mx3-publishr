# === CORE ===
PRIMITIVE_TYPES = (int, str, bool, float, dict, set, list)

# === ENV ===
# set to 'prod' when using the script normally.
ENV = 'dev'

# === FILES ===
BASEPATHS = {}
FILENAME_SCHEMES = {}
# Cover art consts
BASEPATHS['cover'] = 'D:/Users/ewenl/Desktop/GRAPHISM/Sync/Covers/'
FILENAME_SCHEMES['cover'] = '[collection] cover art ([format]).png'
COVERS_FILENAME_REGEX = r'(.+) cover art (.+)\.png'

# Music videos consts
VIDEOS_COVERART_FORMAT_USED = 'landscape'
BASEPATHS['video'] = 'D:/Users/ewenl/Desktop/GRAPHISM/Mx3 YT/'
FILENAME_SCHEMES['video'] = '[artist] - [track].mp4'
VIDEOS_FILENAME_REGEX = r'(.+) - (.+)\.\w{3,}'

# Audio file consts
BASEPATHS['audio'] = 'D:/Users/ewenl/Documents/Image-Line/Data/FL Studio/Projects/#DONE/'
FILENAME_SCHEMES['audio'] = '[tracknumber] - [artist] - [track].mp3'
AUDIOS_FILENAME_REGEX = r'(\d{2,}) - (.+) - (.+)\.\w{3,}$'

# === FIELDS ===
# Common to [artist], [track] and [collection]
FIELDS_FORBIDDEN_CHARS = ['.', '<', '>', '/', '\\']

# Kinds
COLLECTION_KINDS = ['ep', 'album']
AVAIL_KINDS = ['ep', 'album', 'single', 'remix']

# Your artist name
SELF_NAME = 'Mx3'

# What to append at the end of remixes' track names
REMIX_TRACK_SUFFIX = ' ('+SELF_NAME+' Remix)'

# What to appnd at the end of singles' collection names
SINGLE_COLLECTION_SUFFIX = ' - Single'

# === CLI ===
USER_INPUT_INDICATOR = ">> "
LOG_TYPE_SEPARATOR = '|'
LOG_TYPES = {
    "info": " ",
    "debug": "D",
    "success": "S",
    "warn": "!",
    "error": "E",
    "question": "?",
    "fatal": "FATAL",
}

# ===Features===

# Don't ask if you created the track or not
# (ask the artist only if userdata['track'] equals 'remix')
AUTO_DETECT_OC = True

# Add (SELF_NAME Remix) at the end of the track name automatically,
# if the user didn't enter it manually
AUTO_ADD_REMIX_SUFFIX = True

# Add - Single at the end of the collection name automatically,
# if the user didn't enter it manually:
AUTO_ADD_SINGLE_SUFFIX = False

# Compatibility level for special characters such as "↴" or "↓"
# 0: Extended ASCII only
# 1: cmd.exe-compatible
# 2: Full UTF-8 charset
SPECIAL_CHARS_COMPATIBILITY_LEVEL = 1

# Verbose output: show debug logs (log.debug methods)
VERBOSE_OUTPUT = False

# --- Special chars ---
SPECIAL_CHARS = {}

if SPECIAL_CHARS_COMPATIBILITY_LEVEL >= 0:
    SPECIAL_CHARS['drarr'] = '┐'
    SPECIAL_CHARS['rarr'] = '->'
    SPECIAL_CHARS['rArr'] = '=>'
    SPECIAL_CHARS['orarr'] = ''
    SPECIAL_CHARS['curarr'] = ''
    SPECIAL_CHARS['ox'] = '(X)'

if SPECIAL_CHARS_COMPATIBILITY_LEVEL >= 1:
    SPECIAL_CHARS['drarr'] = '↓'
    SPECIAL_CHARS['rarr'] = '→'

if SPECIAL_CHARS_COMPATIBILITY_LEVEL >= 2:
    SPECIAL_CHARS['drarr'] = '↴'
    SPECIAL_CHARS['orarr'] = '↻'
    SPECIAL_CHARS['curarr'] = '↷'
    SPECIAL_CHARS['dl'] = '⥙'
    SPECIAL_CHARS['ox'] = '⦻'

# === WATERMARK ===
def _list_logvariants():
    logvariants = str()
    for k in LOG_TYPES:
        v = LOG_TYPES[k]
        k = k.title()
        if k == 'Debug' and not VERBOSE_OUTPUT: k+=' (deactivated)'
        logvariants += f'             - "{v}{LOG_TYPE_SEPARATOR}" {k}\n'
    return logvariants

# TODO move this out of consts
# TODO use pyfiglet instead of harcoded logos
WATERMARK = """
                      __  __  __  __  _____   _       
                     |  \/  | \ \/ / |___ /  ( )  ___ 
                     | |\/| |  \  /    |_ \  |/  / __|
                     | |  | |  /  \   ___) |     \__ \\
                     |_|  |_| /_/\_\ |____/      |___/                                                               

.______    __    __  .______    __       __       _______. __    __  .______      
|   _  \  |  |  |  | |   _  \  |  |     |  |     /       ||  |  |  | |   _  \     
|  |_)  | |  |  |  | |  |_)  | |  |     |  |    |   (----`|  |__|  | |  |_)  |    
|   ___/  |  |  |  | |   _  <  |  |     |  |     \   \    |   __   | |      /     
|  |      |  `--'  | |  |_)  | |  `----.|  | .----)   |   |  |  |  | |  |\  \----.
| _|       \______/  |______/  |_______||__| |_______/    |__|  |__| | _| `._____|    

                       Get music out, without trouble.

                             
                             ====WEBSITE====
                            mx3creations.com

                           ====REPOSITORY====
                     github.com/ewen-lbh/mx3-publishr
            
                       ====SCRIPT INFORMATIONS====
                  Each message is preceded by <character>%(logsep)s.
           The <character> indicates the type of message you're getting.
            
                      Here's the list of all characters:
%(logvariants_list)s
            
                  In the same way, "%(userinput)s" indicates that 
                         user input is requested.
            
                           %(rArr)s  Let's start!
            
"""  % {
'logsep':LOG_TYPE_SEPARATOR, 
'userinput':USER_INPUT_INDICATOR, 
'rArr':SPECIAL_CHARS['rArr'],
'logvariants_list':_list_logvariants()
}

del _list_logvariants