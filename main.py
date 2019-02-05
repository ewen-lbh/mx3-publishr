from pprint import pprint

from Data import *
import debug
import glob
import datetime
from cli import *
from utils import *
import importlib

def main():
    import consts as c
    importlib.reload(c)
    log.watermark()
    # latest.log header
    with open('latest.log', 'w') as f:
        f.write(f'====== log generated {datetime.date.today().strftime("%B %d, %Y")} ======\n\n\n'.upper())
        f.write(c.WATERMARK)

    # userdata collecting process
    def get_userdata():
        global userdata
        global userdata_confirmed

        userdata = ask.userdata()

        if userdata != {}:
            log.recap(userdata)
            userdata_confirmed = ask.confirm('Is this information correct ?')
        else:
            userdata_confirmed = False

    if c.TESTING_MODE:
        # automatically remove files such as cover arts
        userdata = debug.userdata
        log.recap(userdata)
    else:
        userdata = {}
        # handle re-asking
        get_userdata()
        while not userdata_confirmed:
            get_userdata()

    # delete temporary MoviePy sound files
    temp_files = glob.glob(cwd_path() + '*TEMP_MPY*')
    if len(temp_files) > 0:
        log.section('Cleaning temporary files')
        for filename in temp_files:
            log.debug(f'Deleting temporary file {unix_slashes(filename)}...')
            os.remove(filename)
            log.debug(f'Deleted successfully.')
            log.success('Cleaned all temporary files !')
    del temp_files

    # make new object with userdata (when its confirmed correct by user)
    log.section('Getting tracks')
    track = Data(userdata)

    # recreate non-ideal situation to test audio files renaming, cover art & video generation
    if c.TESTING_MODE:
        log.section('Debugging initial steps')
        log.warn('Recreating initial file conditions...')
        debug.init(track)

    log.section('Renaming audio files')
    # rename tracks badly named
    # TODO don't show this section if no files to rename
    track.audio.rename()

    log.section('Applying metadata')
    # add metadata to audio files
    track.audio.apply_metadata()

    # getting cover arts
    log.section('Fixing missing cover arts')
    if not track.cover.exists('landscape'):
        log.fatal('Landscape cover art not found')

    if not track.cover.exists('square'):
        log.warn(
            'Square cover art not found.\nCropping the landscape version to make a square one...')
        crop_direction = ask.choices('What part of it do you want to keep ?', ['left', 'center', 'right'], shortcuts=True)
        track.cover.make_square(crop_direction)
        del crop_direction
    else:
        log.info('All cover art versions (square and landscape) found!')

    log.section('Generating missing videos')
    missing_vids = track.video.missing()
    if len(missing_vids) > 0:
        missing_vids_str = '\n'.join(
            [re.sub(f'3$', r'4', filename(i)) for i in missing_vids])  # display video file names
        log.warn(f'{len(missing_vids)} video(s) missing:\n{missing_vids_str}')
        video_creation_confirmed = ask.confirm(
            'Want to generate videos automatically ? (this will take quite some time)\n' +
            'Note that you can use Ctrl-C at any time to stop the script\n' +
            'If it gets stuck, please report the issue on github (ewen-lbh/mx3-publishr)')
        if video_creation_confirmed:
            for filename in missing_vids:
                track.video.create(filename)
        else:
            log.debug('Video creation step skipped. Your album will not be uploaded to YouTube.')
    else:
        log.info('All videos found! \nThis saved you a sh*t ton of processing time :D')

    if track.kind in COLLECTION_KINDS:
        log.section(f'Full {track.kind} zip file')
        # pprint(vars(track))
        track.audio.make_zip_file()


if __name__ == '__main__':
    main()
