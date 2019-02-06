# === CORE ===
import pyfiglet


PRIMITIVE_TYPES = (int, str, bool, float, dict, set, list)

# === ENV ===
# testing mode: set to true while testing/debugging
TESTING_MODE = True
# recreates "initial file conditions" by deleting files generated by script (to restart fresh)
# if set to False, TESTING_MODE just enables debugdata instead of userdata requests
TESTING_DESTRUCTIVE = False

# === FILES ===
PATH_DRIVE = 'D:'
CHROMEDRIVER_PATH = PATH_DRIVE+'/Users/ewenl/Documents/Chromedriver/chromedriver.exe'
BASEPATHS = dict()
FILENAME_SCHEMES = dict()
# Cover art consts
BASEPATHS['cover'] = PATH_DRIVE+'/Users/ewenl/Desktop/GRAPHISM/Sync/Covers/'
FILENAME_SCHEMES['cover'] = '[collection] cover art ([format]).png'
COVERS_FILENAME_REGEX = r'(.+) cover art (.+)\.png'

# Music videos consts
VIDEOS_COVERART_FORMAT_USED = 'landscape'
BASEPATHS['video'] = PATH_DRIVE+'/Users/ewenl/Desktop/GRAPHISM/Mx3 YT/'
FILENAME_SCHEMES['video'] = '[artist] - [track].mp4'
VIDEOS_FILENAME_REGEX = r'(.+) - (.+)\.\w{3,}'

# Audio file consts
BASEPATHS['audio'] = PATH_DRIVE + '/Users/ewenl/Documents/Image-Line/Data/FL Studio/Projects/#DONE/'
FILENAME_SCHEMES['audio'] = '[tracknumber] - [artist] - [track].mp3'
AUDIOS_FILENAME_REGEX = r'(\d{2,}) - (.+) - (.+)\.\w{3,}$'
SUPPORTED_AUDIO_FORMATS = ['.mp3']

# === FIELDS ===
# Common to [artist], [track] and [collection]
FIELDS_FORBIDDEN_CHARS = ['.', '<', '>', '/', '\\']

# Kinds
COLLECTION_KINDS = ['ep', 'album']
AVAIL_KINDS = ['ep', 'album', 'single', 'remix']

# Your artist name & website
SELF_NAME = 'Mx3'
SELF_WEBSITE = {
    'pretty': 'mx3creations.com',
    'full': 'https://mx3creations.com/'
}

# What to append at the end of remixes' track names
REMIX_TRACK_SUFFIX = ' ('+SELF_NAME+' Remix)'

# What to append at the end of singles' collection names
SINGLE_COLLECTION_SUFFIX = ' - Single'

# --- YouTube ---
# YouTube generic tags (will be added to artist, collection, kind and track names tags)
YOUTUBE_GENERIC_TAGS = [
    'Chronéis',
    'Kronéys',
    'Cronéis',
    'Croneis',
    'Kroneys',
    'Chroneis',
    'Cronéys',
    'Croneys',
    'Kronéis',
    'Kroneis',
    'Ewen',
    'Le',
    'Bihan',
    'Minecraft',
    'WyxxyW',
    'WyxyW',
    'Wixxiew',
    'Wixiew'
]
YOUTUBE_TITLE_SCHEME = '[artist] - [title] ([collection] [kind])'
YOUTUBE_DESCRIPTION_SCHEME = """
[en_desc]
///
[fr_desc]
_____________
DOWNLOADS
The [kind_pretty]:
https://mx3creations.com/track/[trackID]
Just the track "[trackname]"
https://mx3creations.com/track/[trackID]?play[escaped_trackname]
Everything:
Site: https://mx3creations.com/music
___________________
CONNECT WITH ME
Twitter: https://twitter.com/mx3_fr
Facebook: https://facebook.com/mx3fr
Instagram: https://instagram.com/mx3_fr
GitHub: https://github.com/ewen-lbh
"""
# --- Social Medias ---
SOCIAL_MEDIAS_BODY_SCHEME = '[new_word] [kind]: "[title]" !\nÉcoutez-le ici: https://mx3creations.com/track/[trackID]\n#posttofb' if not TESTING_MODE else """Ceci est un test! 
Je suis en train de créer un script d\'automatisation en python
https://github.com/ewen-lbh/mx3-publishr #posttofb"""
SOCIAL_MEDIAS_IMAGES = {
    'ig': 'square',
    'fb': 'landscape',
    'tw': 'landscape'
}

# --- Database ---
DB_FIELDS_SCHEMES = {
    'type': '`[kind]`',
    'release_date': '`[timestamp]`',
    'ytUrl': '`https://youtube.com/watch?v=[ytID]`',
    'EN__track_description': '`[track_description_EN]`',
    'FR__track_description': '`[track_description_FR]`',
    'track_names': '`[json_tracklist]`',
    'artist': '`[artist]`',
    'track_durations': '`[json_track_durations]`'
}
DB_NAME = 'mx3'
DB_TABLE = 'musiclist'
# phpmyadmin url
PMA_URL = 'https://mx3creations.com/phpmyadmin'
DB_QUERY_SCHEME = f'INSERT INTO {DB_NAME}.{DB_TABLE} ([keys]) VALUES ([values])'

# --- Website Filesystem ---
# collection_pretty: first letter uppercased
# kind_pretty: first letter uppercased and "EP" instead of "ep"
WEBSITE_PATHS = {
    'base': '/www/new/resources/',
    'covers_dirs_base': 'images/cover-arts/',

    'covers_dirs': ['fullres_square/[kind]/', 'fullres_landscape/[kind]/', 'square/[kind]/', 'landscape/[kind]/'],
    'audios_dir': 'audio/[kind]/[collection]',

    'covers': '[collection][extension]',
    'full_album': 'Full [kind_pretty].zip',
}
LOCAL_WEBSITE_ROOT = 'C:/wamp-projects/main-website/new/resources/'
# --- ID3 Tags ---
COVERS_DESCRIPTION = f'Artwork by {SELF_NAME} - {SELF_WEBSITE["pretty"]}'

# === CLI ===
USER_INPUT_INDICATOR = "  > "
LOG_TYPES_WRAP = ('[', ']')
LOG_TYPES = {
    "info": "i",
    "debug": "D",
    "success": "S",
    "warn": "!",
    "error": "x",
    "question": "?",
    "fatal": "FATAL",
}
LOG_TYPES_COLORS = {
    "info": "WHITE",
    "debug": "DARK_GREY",
    "success": "GREEN",
    "warn": "DARK_YELLOW",
    "error": "DARK_RED",
    "question": "CYAN",
    "fatal": "RED",
    "plain" : "WHITE"
}

CLI_STYLING_CODES = {
    'BLACK': '\033[30m',
    'DARK_RED': '\033[31m',
    'DARK_GREEN': '\033[32m',
    'DARK_YELLOW': '\033[33m',
    'DARK_BLUE': '\033[34m',
    'DARK_MAGENTA': '\033[35m',
    'DARK_CYAN': '\033[36m',
    'GREY': '\033[37m',
    'DARK_GREY': '\033[90m',
    'RED': '\033[91m',
    'GREEN': '\033[92m',
    'YELLOW': '\033[93m',
    'BLUE': '\033[94m',
    'MAGENTA': '\033[95m',
    'CYAN': '\033[96m',
    'WHITE': '\033[97m',

    'BOLD': '\033[1m',
    'FAINT': '\033[2m',
    'UNDERLINE': '\033[4m',
    'BLINK': '\033[5m',
    'FRAME': '\033[51m',
    'CIRCLE' : '\033[52m',

    'ENDC': '\033[0m'
}
COLORED_TEXT_REGEX = r'.\[\d+m'
SECTION_WRAP = (' ', ' ')
SECTION_UPPERCASE = True
SECTION_COLOR = 'BLUE'
LISTS_ACCENT_COLOR = 'DARK_CYAN'

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
VERBOSE_OUTPUT = True
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
        orig_k = k
        k = k.title()
        if k == 'Debug' and not VERBOSE_OUTPUT:
            k += ' (deactivated)'
        logvariants += f'{CLI_STYLING_CODES[LOG_TYPES_COLORS[orig_k]]} - "{LOG_TYPES_WRAP[0]+str(v)+LOG_TYPES_WRAP[1]}" {k}{CLI_STYLING_CODES["ENDC"]}\n'
    return logvariants


# TODO move this out of consts
# TODO fetch github description to put it here ?
WATERMARK_FONT = 'ogre'
WATERMARK = pyfiglet.figlet_format("publishr", font=WATERMARK_FONT)+"""
Get music out, without trouble.

                             
{headerc}WEBSITE{c}
mx3creations.com

{headerc}REPOSITORY{c}
github.com/ewen-lbh/mx3-publishr
            
{headerc}LOG TYPES{c}
Each message is preceded by {logwrap_l}x{logwrap_r}.
The [x] indicates the type of message you're getting.
            
Here's the list of all characters:
{logvariants_list}
            
In the same way, "{userinput}" indicates that 
user input is requested.

{headerc}CONFIGURATION{c}              
To change something in the config, you can use the (work in progress) config wizard.
Type {cc}/config{c} at any time to open it, and {cc}/close{c} to close it.
Note that when you close the config wizard, the script reruns from the beginning.
            
{rArr}  Let's start!
            
""" .format(
    logwrap_l=LOG_TYPES_WRAP[0],
    logwrap_r=LOG_TYPES_WRAP[1],
    userinput=USER_INPUT_INDICATOR.strip(),
    rArr=SPECIAL_CHARS['rArr'],
    logvariants_list=_list_logvariants(),
    cc=CLI_STYLING_CODES['CYAN'],
    c=CLI_STYLING_CODES['ENDC'],
    headerc=CLI_STYLING_CODES[SECTION_COLOR]
)

del _list_logvariants
