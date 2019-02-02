from imports import *
import os
import re
DELETE_VIDEO = False

userdata = {
    'kind' : 'album',
    'artist' : 'Mx3',
    'collection' : 'Etymology',
}


def init(Data_obj):
    # remove square cover art
    coverartsqr = Data_obj.cover.get('square')
    try:
        os.remove(coverartsqr)
    except FileNotFoundError: 
        # if the file doesnt exist, no need to delete
        pass
    del coverartsqr

    # remove a video if none is missing
    if len(Data_obj.video.missing()) <= 0 and DELETE_VIDEO:
        try:
            os.remove(Data_obj.dirs.video+os.listdir(Data_obj.dirs.video)[0])
        except FileNotFoundError:
            log.debug(f'Failed to delete a video file')

    # rename audio files badly
    for filename in os.listdir(Data_obj.dirs.audio):
        os.rename(Data_obj.dirs.audio+filename, Data_obj.dirs.audio+re.sub(r'(\w{2,}) - (.+) - (.+\.mp3)', r'\3', filename))