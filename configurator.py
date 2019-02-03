

def run(show_help=True, silent=False, on_exit=None):
    from cli import log
    import re
    # noinspection PyUnresolvedReferences
    import Data  # even tho I don't need this, color codes will not work w/o it.
    import webbrowser
    from utils import kv_pairs
    from consts import CLI_STYLING_CODES

    def arr2str(arr, glue='\n'):
        return glue.join(arr)

    cc = CLI_STYLING_CODES['CYAN']
    drc = CLI_STYLING_CODES['DARK_RED']
    yc = CLI_STYLING_CODES['YELLOW']
    c = CLI_STYLING_CODES['ENDC'] + CLI_STYLING_CODES['WHITE']
    USER_INPUT_INDICATOR = '    /'
    avail_cmds = ('list', 'set', 'reset', 'describe', 'help', 'enable', 'disable', 'get', 'reset all', 'open', 'reload')
    exit_cmds = ('exit', 'close', 'shutdown')

    commands_descriptions = {
        'List all settings': f'{cc}list{c}',
        'Open config file': f'{cc}open{c}\nOpen the config file for manual editing.\nUseful for editing dicts/lists that span across multiple lines',
        'Set': f'{cc}<settings name> = <value>{c}',
        'Enable/Disable': f'{cc}<enable|disable> <setting name>{c}\nEquivalent to <setting name> = <True|False>',
        'Get': f'{cc}<setting name>{c}',
        'Reset': f'{cc}reset <setting name|*>{c}\nNote that the default values are the one set in {yc}consts.py{c} at the start of the script\nTo reset all settings, use {cc}reset *{c} or {cc}reset all{c}',
        'Describe': f'{cc}describe <setting name>{c}\n{drc}NOT FUNCTIONAL FOR NOW{c}\nGet description of setting by looking at comments above the const definition.\nReturn "undefined" when no comments are found',
        'Show this': f'{cc}help{c}',
        'Reload': f'{cc}reload{c}\nUpdate the script to take in account modifications to settings.\nNote that the values used for {cc}reset{c} will be set to what\'s in the file {yc}after{c} the reload.'
    }
    if not silent: log.section("Configuration wizard")
    if not silent: log.warn(f"""WARNING: THIS SCRIPT IS STILL BUGGY
ITS RECOMMENDED TO EDIT MANUALLY THE SETTINGS FILE
USING THE COMMAND {c}/{cc}open{c}""")
    help_text = f"""=== Commands:
    
""" + arr2str(kv_pairs(commands_descriptions, '[k] --> /[v]', end='\n')) + f"""


=== Settings names:
Each settings name corresponds to a constant from the {yc}consts.py{c} file, then, the following rules are applied:
""" + arr2str(kv_pairs({'_': ' ', 'a-zA-Z': 'A-Z'}, '/cArrow')) + f"""
(In other words, underscores are replaced by spaces, and all letters are uppercase'd)


=== Example:
{cc}lists accent color = MAGENTA{c} sets the {yc}LISTS_ACCENT_COLOR{c} const to {yc}'MAGENTA'{c}.




    """
    if show_help: log.info(help_text)

    def parse(cmd):
        tokens = cmd.split()
        if len(tokens) > 1:
            if '=' in tokens:
                sep_pos = tokens.index('=')
                setting_name = arr2str(tokens[0:sep_pos], ' ')
                setting_value = arr2str(tokens[sep_pos + 1:], ' ')
                args = [setting_name, setting_value]
                func = 'set'
            elif tokens[0] in ('disable', 'enable', 'get'):
                args = arr2str([x for i, x in enumerate(tokens) if i != 0], ' ')
                func = tokens[0]
            else:
                args = tokens[1]
                func = tokens[0]
        else:
            args = []
            func = tokens[0]
        return func, args

    def consts_open():
        log.debug(f'Opening {yc}consts.py{c}')
        webbrowser.open('consts.py')

    def execute_cmd(stuff):
        func, args_list = stuff
        if func == 'list':
            get_consts()
        elif func == 'help':
            show_help()
        elif func == 'set':
            set_const(args_list)
        elif func == 'get':
            get_const(args_list)
        elif func == 'enable':
            set_const((args_list, 'True'))
        elif func == 'disable':
            set_const((args_list, 'False'))
        elif func == 'reset':
            reset(args_list)
        elif func == 'open':
            consts_open()
        elif func == 'reload':
            reload()
        else:
            log.error('Command not found.')

    def quote(string):
        return "'" + str(string).replace('\'', '\\\'') + "'"

    def get_consts(method="log"):
        if method == 'raw':
            with open('consts.py', 'r', encoding='utf8') as f:
                return f.read()
        consts = [i for i in open('consts.py', 'r', encoding='utf8') if re.match('[A-Z_]+ = .+', i)]
        colored = list()
        props = list()
        pairs = dict()
        for i in consts:
            prop = re.sub(r'([A-Z_]+) = ([^=]+)', r'\1', i)
            prop = prop.replace('_', ' ').lower()
            value = re.sub(r'([A-Z_]+) = ([^=]+)', r'\2', i)
            props.append(prop)
            pairs[prop] = value
            prop = yc + prop + c
            colored.append(prop + ' : ' + value)
        if method != 'log': return pairs
        log.info(arr2str(colored, ''))

    reset_map = get_consts('return')
    avail_props = reset_map.keys()
    original_data = get_consts('raw')

    def set_const(args):
        name = args[0]
        value = args[1]
        value = quote(value) if value not in ('True', 'False') else value
        const_name = name.replace(' ', '_').upper()
        if name not in avail_props:
            log.error(f'"{name}" setting does not exist')
        else:
            with open('consts.py', 'r', encoding='utf8') as f:
                raw_datas = f.readlines()

            success = False
            for i, l in enumerate(raw_datas):
                if re.match(f'({const_name} = )([^=]+)', l):
                    log.debug(f'setting {const_name} to {value}')
                    raw_datas[i] = re.sub(f'({const_name} = )([^=]+)', r'\1' + value, l)
                    success = True

            with open('consts.py', 'w', encoding='utf8') as f:
                f.write(''.join(raw_datas))

            if not success:
                log.error(f'"{name}" setting not found')
            else:
                log.info(f'{yc}{name}{c} = {value}')

    def get_const(name):

        const_name = name.replace(' ', '_').upper()
        with open('consts.py', 'r', encoding='utf8') as f:
            raw_datas = f.readlines()

        success = False
        for i, l in enumerate(raw_datas):
            if re.match(f'({const_name} = )([^=]+)', l):
                value = re.sub(f'({const_name} = )([^=]+)', r'\2', l)
                log.info(f"{yc}{name}{c} = {value}\n")
                success = True

        if not success: log.error(f'"{name}" setting does not exist')

    def show_help():
        log.info(help_text)

    def reset(args):
        if args in ('*', 'all'):
            reset_all()
        else:
            set_const([args, reset_map[args]])

    def reset_all():
        global original_data
        with open('consts.py', 'w', encoding='utf8') as f:
            f.write(original_data)
            log.info('All data has been reset.')

    while True:
        cmd = str(input(USER_INPUT_INDICATOR))
        while parse(cmd)[0] not in avail_cmds + exit_cmds:
            log.error(f'"{cmd}" is not a valid command')
            cmd = str(input(USER_INPUT_INDICATOR))
        if cmd in exit_cmds:
            if on_exit is None:
                log.fatal('Script closed.')
            else:
                log.info('Closing out of config wizard')
                on_exit()
        execute_cmd(parse(cmd))

def reload():
    from cli import log
    log.debug(f'Reloading consts.py')
    run(show_help=False, silent=True)


if __name__ == "__main__":
    run()
