from utils import *
import os

class Data:
    from Data_Dirs import Dirs
    from Data_Cover import Cover
    from Data_Audio import Audio
    from Data_Video import Video

    from Data_Twitter import Twitter
    from Data_Facebook import Facebook
    from Data_Instagram import Instagram
    from Data_Database import Database
    from Data_Website import Website
    from Data_YouTube import YouTube

    def __init__(self, rawdata=None, **kwargs):
        # Decide wether to import data from dict or from keyword args
        if rawdata is not None: data = rawdata
        else: data = kwargs
        # programmatically add all data dict items as object properties
        for k, v in data.items():
            setattr(self, k, v)
        
        # define inner classes and passes parent self to them
        self.dirs  = self.Dirs (self)
        self.cover = self.Cover(self)
        self.audio = self.Audio(self)
        self.video = self.Video(self)

        self.twitter    = self.Twitter(self)
        self.facebook   = self.Facebook(self)
        self.instagram  = self.Instagram(self)
        self.database   = self.Database(self)
        self.website    = self.Website(self)
        self.youtube    = self.YouTube(self)