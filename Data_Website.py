import os
import shutil

from cli import log
from consts import WEBSITE_PATHS, LOCAL_WEBSITE_ROOT, COLLECTION_KINDS, FILENAME_SCHEMES
from ftplib import FTP
from utils import scheme, filename


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
        ftp.cwd(self.paths['base'])
        for cover_dir in self.paths['real_covers_dirs']:
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


            # change back to base path for next CWD
            ftp.cwd(self.paths['base'])






        print(ftp.dir())