import datetime
import subprocess
import time

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

import credentials
import yt_upload
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

        from credentials import YT_CREDENTIALS
        self.credentials = YT_CREDENTIALS

        # todo video_url
        self.video_url = 'nolink'

    def get_upload_data(self, video_path):
        metadata = {
            'title': self.get_video_title(video_path),
            'description': self.get_description(video_path),
            'category': '22',  # 22 = Music category
            'keywords': ', '.join(YOUTUBE_GENERIC_TAGS+filename(rmext(video_path)).split()),  # adds each word of the audio file (without extension) as a tag
            'privacyStatus': 'private',
            # 'auth_host_name': 'localhost',
            # 'auth_host_port': '8888',
            'logging_level': 'DEBUG',
            'file': video_path
        }
        return metadata

    def upload(self, data):
        upload_data = self.get_upload_data(data) if isinstance(data, str) else data



        vid_id = yt_upload.upload_video(upload_data)
        log.success(f'Video with ID "{vid_id or "error"}" was successfully uploaded')
        return vid_id

    def get_track_title(self, video_path):
        return re.sub(r'(.+)\.$', r'\1', self.parent.audio.get('track', chext(filename(video_path), '.mp4')))

    def get_description(self, video_path=None):
        title = self.get_track_title(video_path) if video_path is not None else CLI_STYLING_CODES['DARK_RED']+'track title'+CLI_STYLING_CODES['ENDC']
        def _escape_trackname(string):
            return string.replace('_', '~_').replace(' ', '_')
        return scheme(YOUTUBE_DESCRIPTION_SCHEME, {
            'en_desc': self.parent.descriptions['en'],
            'fr_desc': self.parent.descriptions['fr'],
            'kind_pretty': self.parent.kind if self.parent.kind is not 'ep' else 'EP',  # changes "ep" to "EP"
            'trackID': self.parent.audio.web_track_id,
            'escaped_trackname': _escape_trackname(title),
            'trackname': title
        })

    def get_video_title(self, video_path=None):
        return scheme(YOUTUBE_TITLE_SCHEME, {
            'artist': self.parent.artist,
            'title': self.get_track_title(video_path) if video_path is not None else CLI_STYLING_CODES['DARK_RED']+'track title'+CLI_STYLING_CODES['ENDC'],
            'collection': self.parent.collection,
            'kind': self.parent.kind
        })

    def create_playlist(self):
        output = subprocess.check_output('py ')


    def signin(self):
        run()




def run():
    options = webdriver.chrome.options.Options()
    if YOUTUBE_BROWSER_HEADLESS: options.add_argument('--headless')
    browser = webdriver.Chrome(CHROMEDRIVER_PATH, options=options)

    browser.get('https://youtube.com/upload')
    time.sleep(2)

    browser.find_element_by_xpath('//*[@id="identifierId"]').send_keys('ewen.lebihan7@gmail.com')
    browser.find_element_by_xpath('//*[@id="identifierNext"]/content/span').click()
    time.sleep(2)

    browser.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input').send_keys(credentials.YT_ACCOUNT['pwd'])
    browser.find_element_by_xpath('//*[@id="passwordNext"]').click()
    time.sleep(2)

    phonechallenge_url = browser.current_url
    browser.find_element_by_xpath('//*[@id="view_container"]/div/div/div[2]/div/div[1]/div/form/content/div/div[1]').click()
    WebDriverWait(browser, 30).until(lambda driver: driver.current_url != phonechallenge_url); time.sleep(2)
    browser.find_element_by_xpath('//*[@id="identity-prompt-account-list"]/ul/label[1]/li/span/span[1]/input').click()
    browser.find_element_by_xpath('//*[@id="identity-prompt-confirm-button"]').click()
    time.sleep(2)

    browser.find_element_by_xpath('//*[@id="upload-prompt-box"]/div[2]/input').send_keys('D:/Users/ewenl/Videos/Plays.tv/Counter-Strike Global Offensive/2019_01_11_20_31_42-ses.mp4')
    time.sleep(2)
    
    form_xpath_base = '//*[@id="upload-item-0"]/div[3]/div[2]/div/div/div[1]/div[3]/form/div[1]/fieldset'
    browser.find_element_by_xpath(form_xpath_base+'[1]/div/label[1]/span/input').clear()
    browser.find_element_by_xpath(form_xpath_base+'[1]/div/label[1]/span/input').send_keys('Title')

    browser.find_element_by_xpath(form_xpath_base+'[1]/div/label[2]/span/textarea').clear()
    browser.find_element_by_xpath(form_xpath_base+'[1]/div/label[2]/span/textarea').send_keys('Description')

    # browser.find_element_by_xpath(form_xpath_base+'[1]/div/div/span/div/input[1]').send_keys('tag1, tag2')
    time.sleep(4)
    browser.find_element_by_xpath(form_xpath_base+'[2]/span/span[1]/button').click()
    time.sleep(1.75)
    browser.find_element_by_xpath('//*[@id="addto-list-panel"]/button').click()
    time.sleep(0.5)
    # the "clickcard-card-[n]" changes of n on every page load, need a different searching method.
    # browser.find_element_by_xpath('//*[@id="yt-uix-clickcard-card9"]/div[2]/div[2]/span/div/div[2]/form/div[1]/span/span/input').send_keys('Collection')
    # browser.find_element_by_xpath('//*[@id="yt-uix-clickcard-card16"]/div[2]/div[2]/span/div/div[2]/form/div[2]/div[1]/button/span').click()




    time.sleep(666)


if __name__ == '__main__':
    run()