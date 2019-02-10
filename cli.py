import sys
import webbrowser

import configurator
from utils import *


class log:
	@staticmethod
	def log(text, logtype, method='print', colored=True, no_newline=False):
		lines = text.split('\n')
		# the "plain" logtype bypasses all the pre-formatting
		if logtype != 'plain':
			# get the indicator according to logtype and consts.
			indicator = LOG_TYPES_WRAP[0] + LOG_TYPES[logtype] + LOG_TYPES_WRAP[1] + ' '
			# add a space (' ') for each indicator character
			indent = ''.join([' '] * len(indicator))
			# add indicator and the first line to msg
			msg = indicator + lines[0]
			# add indent to all other lines
			del lines[0]
			for i, line in enumerate(lines):
				msg += '\n' + indent + line
		else:
			msg = text

		# coloured output
		msg = CLI_STYLING_CODES[LOG_TYPES_COLORS[logtype]] + msg + CLI_STYLING_CODES['ENDC']
		plain = strip_color_codes(msg)

		if method == 'print':
			if colored:
				print(msg, end=('' if no_newline else '\n'))
			else:
				print(plain, end=('' if no_newline else '\n'))

			# with open('latest.log', 'a') as f:
			#     f.write(plain+'\n')

		elif method == 'return':
			if colored:
				return msg
			else:
				return plain

	@staticmethod
	def watermark():
		print(WATERMARK)

	@staticmethod
	def recap(userdata):
		msg = "To recap, here's all the information you gave...\n"
		msg += '\n'.join(kv_pairs(userdata, '/cSpace', sentence_case='keys'))
		log.info(msg)

	@staticmethod
	def fatal(text='Unknown Error', exit_script=True):
		if exit_script:
			sys.exit(log.log(text, 'fatal', method='return'))
		else:
			log.log(text, 'fatal')

	@staticmethod
	def debug(text, **options):
		if VERBOSE_OUTPUT:
			log.log(text, 'debug', **options)

	@staticmethod
	def section(section):
		if SECTION_UPPERCASE: section = section.upper()
		section = f'{SECTION_WRAP[0] + section + SECTION_WRAP[1]}'
		section_sep = ''.join([SECTION_UNDERLINE_CHAR * len(section.strip())])
		print(color_text('\n'.join([section, section_sep, '']), SECTION_COLOR))


def _fetch_description(file_path):
	if file_path is None: file_path = cwd_path() + 'descriptions.txt'
	if not os.path.isfile(file_path): raise FileNotFoundError(f'File {file_path} not found')

	with open(file_path, 'r', encoding='utf8') as f:
		lines = f.readlines()
		# first language in file
		lang = 'en'
		fr_lines = []
		en_lines = []
		for line in lines:
			if re.match(f'(.+){DESCRIPTION_LANG_SEPARATOR}(.+)', line):
				en_lines.append(re.sub(f'(.+){DESCRIPTION_LANG_SEPARATOR}(.+)', r'\1', line))
				fr_lines.append(re.sub(f'(.+){DESCRIPTION_LANG_SEPARATOR}(.+)', r'\2', line))
				lang = 'fr'
			elif lang == 'fr':
				fr_lines.append(line)
			else:
				en_lines.append(line)

	french = ''.join(fr_lines)
	english = ''.join(en_lines)
	return {
		'en': english,
		'fr': french
	}


class ask:
	@staticmethod
	def anything(text, flags=[]):
		log.question(text + '\n')
		try:
			answer = str(input(USER_INPUT_INDICATOR))
		except KeyboardInterrupt:
			log.fatal('Script closed.')
		if 'case_sensitive' not in flags:
			answer = answer.lower()
		if 'accept_non_ascii' not in flags and not is_ascii(answer):
			log.fatal('The answer contains special characters.\nOnly ASCII characters are allowed for now.')
		# add answer to logs

		# with open('latest.log', 'a') as f:
		#     f.write(USER_INPUT_INDICATOR+answer+'\n')
		if answer == '/config':
			import main
			configurator.run(on_exit=main.main)
		elif answer == '/reload':
			import main
			main.main()
		elif answer in ('/web', '/website'):
			log.info(f'Opening {SELF_WEBSITE["pretty"]} in your web browser...')
			webbrowser.open(SELF_WEBSITE['full'])
			return 'RETRY'
		elif answer in ('/repo', '/repository'):
			log.info(f'Opening the github repository in your web browser...')
			webbrowser.open('https://www.github.com/ewen-lbh/mx3-publishr')
			return 'RETRY'
		elif answer == '/exit':
			log.fatal('Script closed.')
		else:
			return str(answer) if answer is not None else ''

	@staticmethod
	def choices(text, choices, **options):

		if AUTO_MODE and 'task_name' in options:
			return AUTO_MODE_CHOICES[options['task_name']]

		choicestr = '/'.join(choices)
		orig_choices = choices

		if 'shortcuts' in options:
			choices = [i[0] for i in choices]
			text += f'\nyou can use only the first letter to make your choice, eg. "{choices[0]}" => "{orig_choices[0]}"'

		text += '\n(' + choicestr + ')'

		retries = 0
		answer = ''
		while (answer not in choices or answer == 'RETRY') and retries <= ASK_MAX_RETRIES:
			if retries > 0 and answer != 'RETRY': log.error('"' + answer + '" is not a valid answer, retrying...')
			answer = ask.anything(text)
			if 'shortcuts' in options:
				answer_shortcut = answer[0]
			retries += 1

		if retries > ASK_MAX_RETRIES: log.fatal(
			f'Too much retries. To change this limit, change the MULTIPLE_CHOICES_SEPARATOR constant in consts.py')

		if 'shortcuts' in options: answer_shortcut = search_with_nth_char(orig_choices, answer_shortcut)[1]
		return answer_shortcut if 'shortcuts' in options else answer

	@staticmethod
	def confirm(text, **options):
		if AUTO_MODE and not 'task_name' in options:
			return True
		if AUTO_MODE:
			return AUTO_MODE_CHOICES[options['task_name']]

		answer = ask.choices(text, ['y', 'n'])
		return answer == 'y'

	@staticmethod
	def userdata():
		userdata = dict()
		# --- TRACK KIND ---
		userdata['kind'] = ask.choices('Please enter the kind of track you want to publish', AVAIL_KINDS,
									   shortcuts=True)

		# --- GETTING ARTIST ---
		if AUTO_DETECT_OC:
			is_oc = userdata['kind'] != 'remix'
		else:
			# Ask if the artist != SELF_NAME (dont ask if its a remix, obviously)
			if userdata['kind'] != 'remix':
				is_oc = ask.confirm('Did you (' + SELF_NAME + ') created this from scratch ?')
			else:
				is_oc = False

		# If the artist isn't SELF_NAME, ask for it:
		if is_oc:
			userdata['artist'] = SELF_NAME
		else:
			userdata['artist'] = ask.anything('Who did the original track ?', flags=['case_sensitive'])

		# --- COLLECTION NAME ---
		def _append_to_collection(suffix, suffix_kind, userdata):
			if userdata['kind'] == suffix_kind \
					and AUTO_ADD_SINGLE_SUFFIX \
					and not re.match(suffix + '$', userdata['collection']):
				log.info(f'Adding "{suffix}" to the {userdata["kind"]}\'s title')
				userdata['collection'] += suffix
			return userdata

		userdata['collection'] = ask.anything('Please enter the ' + userdata['kind'] + '\'s title',
											  flags=['case_sensitive'])

		userdata = _append_to_collection(REMIX_TRACK_SUFFIX, 'remix', userdata)
		userdata = _append_to_collection(SINGLE_COLLECTION_SUFFIX, 'single', userdata)

		del _append_to_collection

		# --- DESCRIPTIONS ---
		method = ask.choices('Use a file for the descriptions (<english>////<french>) or type them directly ?',
							 ['file', 'manual'], shortcuts=True)
		restart = True
		while restart:
			if method == 'file':
				file_path = ask.anything(f'Specify the file path... (leave blank for {cwd_path()}descriptions.txt)')
				if file_path is None or not file_path.strip():  # an empty string is considered as false
					file_path = cwd_path() + 'descriptions.txt'

				if os.path.isfile(file_path):
					userdata['descriptions'] = _fetch_description(file_path)
					restart = False
				else:
					log.error(f'Could not find {file_path}\nSwitching to manual mode...')
					restart = True
					method = 'manual'
			else:
				userdata['descriptions'] = {
					'fr': ask.anything('Enter the french description...', flags=['accept_non_ascii']),
					'en': ask.anything('Enter the english description...', flags=['accept_non_ascii'])
				}
				restart = False
		del restart, method

		return userdata

	@staticmethod
	def mchoices(message, choices):
		msg = message + f'\nAvailable choices: {", ".join(choices)}\nTo select multiple choices, separate them with "{MULTIPLE_CHOICES_SEPARATOR}"'
		chosens = []
		retries = 0
		while len(chosens) < 1 and retries <= ASK_MAX_RETRIES:
			if retries > 0: log.error('No valid choices selected: Retrying...')
			ans = ask.anything(msg)
			chosens = [i for i in ans.split(MULTIPLE_CHOICES_SEPARATOR) if i in choices]
			retries += 1
		if retries > ASK_MAX_RETRIES: log.fatal(
			f'Too much retries. To change this limit, change the MULTIPLE_CHOICES_SEPARATOR constant in consts.py')
		return chosens


# add missing log variants from LOG_TYPES if not defined yet


for level in LOG_TYPES:
	if not hasattr(log, level):
		setattr(log, level, staticmethod(lambda text, level=level: log.log(text, level)))