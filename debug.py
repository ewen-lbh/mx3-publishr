import shutil

from imports import *
import os
import re
DELETE_VIDEO = False

userdata = {
    'kind' : 'album',
    'artist' : 'Mx3',
    'collection' : 'Etymology',
    'descriptions': {
        'fr': 'wesh wesh',
        'en': 'eef freef guys!'
    }
}


def init(Data_obj):
    # remove square cover art
    coverartsqr = Data_obj.cover.get('square')
    if os.path.isfile(coverartsqr):
        os.remove(coverartsqr)
        log.debug(f'Removed {filename(coverartsqr)}')
    del coverartsqr

    # remove a video if none is missing
    if len(Data_obj.video.missing()) <= 0 and DELETE_VIDEO:
        try:
            os.remove(Data_obj.dirs.video+os.listdir(Data_obj.dirs.video)[0])
            log.debug(f'Deleted a video file')
        except FileNotFoundError:
            log.debug(f'Failed to delete a video file')

    # rename audio files badly
    renamed_files_map = dict()
    for fname in Data_obj.audio.lists['filenames']:
        orig = Data_obj.dirs.audio+fname
        dest = Data_obj.dirs.audio+re.sub(r'(\w{2,}) - (.+) - (.+\.mp3)', r'\3', fname)
        renamed_files_map[filename(orig)] = filename(dest)
        os.rename(orig, dest)

    # delete zip file
    log.debug('Deleting the full album zip file')
    if os.path.isdir(Data_obj.dirs.audio+'full'): shutil.rmtree(Data_obj.dirs.audio+'full')

    # update lists
    Data_obj.audio.update_lists()

    log.info('Renamed following files:\n'+'\n'.join(kv_pairs(renamed_files_map, '/cArrow')))