import glob
import importlib
import debug

from Data import *
from cli import *
from utils import *


def main():
	import consts as c
	importlib.reload(c)
	log.watermark()
	# latest.log header

	# with open('latest.log', 'w') as f:
	#     f.write(f'====== log generated {datetime.date.today().strftime("%B %d, %Y")} ======\n\n\n'.upper())
	#     f.write(strip_color_codes(c.WATERMARK))

	if c.TESTING_MODE:
		# automatically remove files such as cover arts
		userdata = debug.userdata
		log.recap(userdata)
	else:
		userdata = {}
		# handle re-asking
		userdata_confirmed = False
		while not userdata_confirmed:
			userdata = ask.userdata()
			log.recap(userdata)
			userdata_confirmed = ask.confirm('Is this information correct ?')

	# if AUTO_MODE_ASK:
	# 	log.section('Automatic mode')
	# 	ask.userdata()
	# todo fix this asking userdata again instead of doing its job

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
	if c.TESTING_MODE and c.DESTRUCTIVE_TESTING:
		log.section('Debugging initial steps')
		log.warn('Recreating initial file conditions...')
		debug.init(track)

	_to_be_renamed = track.audio.preview_renames()
	if _to_be_renamed:  # an empty array ('[]') is considered as false)
		log.section('Renaming audio files')
		# rename tracks badly named
		track.audio.rename(_to_be_renamed)
	else:
		print('All good!')

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
		crop_direction = ask.choices('What part of it do you want to keep ?', ['left', 'center', 'right'],
									 shortcuts=True, task_name='cover_arts_crop_direction')
		track.cover.make_square(crop_direction)
		del crop_direction
	else:
		log.info('All cover art versions (square and landscape) found!')

	log.section('Creating low resolution cover arts')
	# if no jpg are found
	if len([i for i in os.listdir(track.dirs.cover) if '.jpg' in i]) == 0:
		track.cover.make_lowres()

	log.section('Generating missing videos')
	track.video.update_lists()
	missing_vids = track.video.missing()
	if len(missing_vids) > 0:
		missing_vids_str = '\n'.join(track.video.missing('video'))  # display video file names
		log.warn(f'{len(missing_vids)} video(s) missing:\n{missing_vids_str}')
		video_creation_confirmed = ask.confirm(
			'Want to generate videos automatically ? (this will take quite some time)\n' +
			'Note that you can use Ctrl-C at any time to stop the script\n' +
			'If it gets stuck, please report the issue on github (ewen-lbh/mx3-publishr)',
			task_name='create_videos')
		if video_creation_confirmed:
			for filename in missing_vids:
				track.video.create(filename)
			track.video.update_lists()
		else:
			log.debug('Video creation step skipped. Your album will not be uploaded to YouTube.')
	else:
		log.info('All videos found! \nThis saved you a sh*t ton of processing time :D')

	if track.kind in COLLECTION_KINDS:
		log.section(f'Full {track.kind} zip file')
		if ask.confirm('Make this zip file ?', task_name='create_zip_file'):
			track.audio.make_zip_file()
		else:
			log.warn('Full album .zip creation skipped.')

	log.section('Website uploading')
	if ask.confirm('Upload to the website ?', task_name='website'):
		track.website.upload()
	else:
		log.warn('Website uploading cancelled.')

	log.section('Website database insertion')
	log.info('Data to be added:\n' + '\n'.join(kv_pairs(track.website.get_db_data(), used_scheme='/cSpace')))
	if ask.confirm('Add to the website\'s database ?', task_name='database'):
		track.website.database()
	else:
		log.warn('Database insertion skipped.')

	log.section('Tweeting the new track')
	track.social.twitter()

	log.section('Uploading to YouTube')
	track.youtube.print_info()

	track.cover.delete_lowres()

	log.log('\n\n\n----------------------', logtype='plain')
	log.success('All tasks finished :D')
	log.info(SCRIPT_END_MESSAGE)


if __name__ == '__main__':
	main()