import datetime
import json
import os
import shutil
import time

from selenium import webdriver

import credentials
from cli import log, ask
from consts import WEBSITE_PATHS, LOCAL_WEBSITE_ROOT, COLLECTION_KINDS, FILENAME_SCHEMES, CHROMEDRIVER_PATH, PMA_URL
from ftplib import FTP
from utils import scheme, filename, intpadding


class Website:
    def __init__(self, parentself):
        self.parent = parentself

        from credentials import FTP_CREDENTIALS
        self.credentials = FTP_CREDENTIALS
        # recursive replace of all collection/kind placeholders
        self._web_kinds_map = {
            'album': 'albums',
            'ep': 'ep',
            'remix': 'remixes',
            'single': 'singletracks'
        }
        self._pretty_kinds_map = {
            'album': 'Album',
            'ep': 'EP',
            'remix': 'Remix',
            'single': 'Single'
        }
        self.web_kind = self._web_kinds_map[self.parent.kind]
        self.local_website_root = LOCAL_WEBSITE_ROOT

        self.paths = {}
        for k, v in WEBSITE_PATHS.items():
            if isinstance(v, str):
                self.paths[k] = scheme(v, {
                    'collection': self.parent.collection,
                    'kind': self.web_kind,
                })
        self.paths['covers_dirs'] = []
        for i in WEBSITE_PATHS['covers_dirs']:
            self.paths['covers_dirs'].append(scheme(i, {
                'collection': self.parent.collection,
                'kind': self.web_kind,
            }))

        # add cover_dirs base.
        self.paths['real_covers_dirs'] = []
        for i in self.paths['covers_dirs']:
            self.paths['real_covers_dirs'].append(self.paths['covers_dirs_base']+i)


    def upload(self):
        # initial setup
        ftp = FTP(**self.credentials)
        ftp.cwd(self.paths["base"])
        os.chdir(self.local_website_root)
        filepaths = {}
        upload_audio_related = False

        if upload_audio_related:
            # create dirs (if they don't exist already)
            ftp.mkd(self.paths["audios_dir"])
            if not os.path.isdir(self.paths['audios_dir']): os.mkdir(self.paths["audios_dir"])

            # full album
            if self.parent.kind in COLLECTION_KINDS:
                filepaths['full_album'] = scheme(WEBSITE_PATHS['full_album'], {
                    'kind_pretty': self._pretty_kinds_map[self.parent.kind]
                })
                log.debug(f'Navigating to {self.paths["audios_dir"]}')
                ftp.cwd(self.paths["audios_dir"])
                log.info(f'Uploading the full album file...')
                with open(self.parent.audio.full_album_path, 'rb') as f:
                    ftp.storbinary(f'STOR {filepaths["full_album"]}', f)
                    shutil.copyfile(src=self.parent.audio.full_album_path,
                                    dst=self.local_website_root + self.paths["audios_dir"] + filepaths['full_album'])

            # audio files
            for path in self.parent.audio.lists['paths']:
                upload_filename = self.parent.audio.get('track', filename(path)) + '.mp3'
                log.info(f'Uploading {filename(path)} as {upload_filename}...')
                with open(path, 'rb') as f:
                    ftp.storbinary(f'STOR {upload_filename}', f)
                    shutil.copyfile(path, self.local_website_root + self.paths["audios_dir"] + upload_filename)

            print(ftp.dir())

        # cover arts (the toughest !)
        for cover_dir in self.paths['real_covers_dirs']:
            ftp.cwd(self.paths['base'])
            ftp.cwd(cover_dir)
            fullres = 'fullres_' in cover_dir
            square = 'square' in cover_dir
            dst_ext = '.png' if fullres else '.jpg'
            dst_filename = scheme(self.paths['covers'], {
                'extension': dst_ext
            })

            src_folder = self.parent.dirs.cover
            src_filename = scheme(FILENAME_SCHEMES['cover'], {
                'collection': self.parent.collection,
                'format': 'square' if square else 'landscape'
            })

            log.info(f'Uploading {src_filename} as {dst_filename}...')
            with open(src_folder+src_filename, 'rb') as f:
                ftp.storbinary(f'STOR {dst_filename}', f)
                # todo fix this
                shutil.copyfile(src_folder+src_filename, self.local_website_root+cover_dir+'/'+dst_filename)


        print(ftp.dir())

    def database(self):
        now = datetime.datetime.now()
        date_Ymd = str(f'{now.year}-{intpadding(now.month, strsize=2)}-{intpadding(now.day, strsize=2)}')

        browser = webdriver.Chrome(CHROMEDRIVER_PATH)
        browser.get(PMA_URL)
        browser.find_element_by_xpath('//*[@id="input_password"]').send_keys(credentials.DB_CREDENTIALS['pwd'])
        browser.find_element_by_xpath('//*[@id="input_username"]').send_keys(credentials.DB_CREDENTIALS['id'])
        browser.find_element_by_xpath('//*[@id="input_go"]').click()
        time.sleep(2)
        browser.find_element_by_xpath('//*[@id="pma_navigation_tree_content"]/ul/li[2]/a').click()
        time.sleep(1.5)
        browser.find_element_by_xpath('//*[@id="pma_navigation_tree_content"]/ul/li[2]/div[4]/ul/li[6]/a').click()
        time.sleep(2.5)
        browser.find_element_by_xpath('//*[@id="pma_ignore_all_errors_popup"]').click()
        time.sleep(0.5)
        browser.find_element_by_xpath('//*[@id="topmenu"]/li[5]/a').click()
        time.sleep(0.5)
        browser.find_element_by_xpath('//*[@id="field_2_3"]').send_keys(self.web_kind)
        browser.find_element_by_xpath('//*[@id="field_5_3"]').send_keys(self.parent.collection)
        browser.find_element_by_xpath('//*[@id="field_6_3"]').clear()
        browser.find_element_by_xpath('//*[@id="field_6_3"]').send_keys(self.parent.artist)
        browser.find_element_by_xpath('//*[@id="field_7_3"]').send_keys(date_Ymd)
        browser.find_element_by_xpath('//*[@id="field_11_3"]').send_keys('nolink' if 'youtube' in self.parent.skipped_tasks else '')  # todo youtube url
        browser.find_element_by_xpath('//*[@id="field_12_3"]').send_keys(self.parent.descriptions['en'])
        browser.find_element_by_xpath('//*[@id="field_13_3"]').send_keys(self.parent.descriptions['fr'])
        browser.find_element_by_xpath('//*[@id="field_14_3"]').send_keys(json.dumps([self.parent.audio.get('track', filename(i)) for i in self.parent.audio.lists['paths']])) # get track names
        if ask.confirm('Add this to the database ?'):
            browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')  # scroll to bottom
            browser.find_element_by_xpath('//*[@id="buttonYes"]').click()
        else:
            log.warn('Cancelled.')
        browser.quit()

