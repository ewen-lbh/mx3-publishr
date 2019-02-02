from imports import *
class YouTube:
    def __init__(self, parentself):
        self.parent = parentself
        # tags from track list
        self.tags   = [self.parent.audio.get('track',i) for i in  self.parent.audio.lists['names']]
        # add collection, artist and kind to tags
        self.tags.extend([self.parent.artist, self.parent.collection, self.parent.kind])
        # add generic tags from consts
        self.tags += YOUTUBE_GENERIC_TAGS
