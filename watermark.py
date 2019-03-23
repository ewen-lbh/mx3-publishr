import pyfiglet

from consts import *


def _list_logvariants():
    logvariants = str()
    for k in LOG_TYPES:
        v = LOG_TYPES[k]
        orig_k = k
        k = k.title()
        if k == 'Debug' and not VERBOSE_OUTPUT:
            k += ' (deactivated)'
        logvariants += f'{CLI_STYLING_CODES[LOG_TYPES_COLORS[orig_k]]} - "{LOG_TYPES_WRAP[0] + str(v) + LOG_TYPES_WRAP[1]}" {k}{CLI_STYLING_CODES["ENDC"]}\n'
    return logvariants


if SHOW_LOGTYPES_IN_WATERMARK:
    logtypes_msg = """{headerc}
	LOG TYPES{c}
	---------
	Each message is preceded by {logwrap_l}x{logwrap_r}.
	The [x] indicates the type of message you're getting.
	Here's the list of all characters:
	{logvariants_list}

	In the same way, "{userinput}" indicates that
	user input is requested."""
else:
    logtypes_msg = ''

text = pyfiglet.figlet_format("publishr", font=WATERMARK_LOGO_FONT) + """
Get music out, without trouble.
{headerc}
WHAT THIS DOES{c}
--------------

• Rename badly named audio files
• Add metadata (ID3 Tags) to audio files
• Crop the landscape (16:9) cover art image to make a square version
• Create low resolution cover arts for website use
• Generate videos from audio files and cover art image
• Post a tweet
• Add to a website's filesystem and database
• Upload videos to YouTube
• Create a .zip Full Album file containing all audio files, for website use                           
{headerc}
ABOUT{c}
-----

Mx3's website:       mx3creations.com (use {cc}/web{c})
Mx3 Publishr's repo: github.com/ewen-lbh/mx3-publishr (use {cc}/repo{c})
""" + logtypes_msg + """
{headerc}
CONFIGURATION{c}
-------------        

To change something in the config, you can use the (work in progress) config wizard.
Type {cc}/config{c} at any time to open it, and {cc}/close{c} to close it.
Note that when you close the config wizard, the script reruns from the beginning.

{rArr}  Let's start!

""".format(
    logwrap_l=LOG_TYPES_WRAP[0],
    logwrap_r=LOG_TYPES_WRAP[1],
    userinput=USER_INPUT_INDICATOR.strip(),
    rArr='=>',
    cc=CLI_STYLING_CODES['CYAN'],
    c=CLI_STYLING_CODES['ENDC'],
    headerc=CLI_STYLING_CODES['UNDERLINE'],
)