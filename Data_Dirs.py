from consts import *

class Dirs:
    def __init__(self, parentself):
        self.parent = parentself
        self.audio = BASEPATHS['audio']+str(self.parent.collection)+'/'
        self.cover = BASEPATHS['cover']+str(self.parent.collection)+'/'
        self.video = BASEPATHS['video']+str(self.parent.collection)+'/'