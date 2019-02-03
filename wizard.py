from imports import *
# noinspection PyUnresolvedReferences
import Data  # even tho I don't need this, color codes will not work w/o it.

def arr2str(arr, glue='\n'):
    return glue.join(arr)


cc = CLI_STYLING_CODES['CYAN']
drc = CLI_STYLING_CODES['DARK_RED']
yc = CLI_STYLING_CODES['YELLOW']
c = CLI_STYLING_CODES['ENDC'] + CLI_STYLING_CODES['WHITE']
USER_INPUT_INDICATOR = '    /'
avail_cmds = ('list', 'set', 'reset', 'describe', 'help', 'enable', 'disable', 'get')
exit_cmds = ('exit', 'close', 'shutdown')


commands_descriptions = {
    'List all settings': f'{cc}list{c}',
    'Set': f'{cc}<settings name> = <value>{c}',
    'Enable/Disable' : f'{cc}<enable|disable> <setting name>{c}\nEquivalent to <setting name> = <True|False>',
    'Get': f'{cc}<setting name>{c}',
    'Reset': f'{cc}reset <setting name>{c}\nNote that the default values are the one set in {yc}consts.py{c} at the start of the script',
    'Describe' : f'{cc}describe <setting name>{c}\n{drc}WORK IN PROGRESS, Not functionnal yet{c}\nGet description of setting by looking at comments above the const definition.\nReturn "undefined" when no comments are found',
    'Show this': f'{cc}help{c}',
}

log.section("Configuration wizard")
help = f"""=== Commands:

"""+arr2str(kv_pairs(commands_descriptions, '[k] --> /[v]', end='\n'))+f"""


=== Settings names:
Each settings name corresponds to a constant from the {yc}consts.py{c} file, then, the following rules are applied:
"""+arr2str(kv_pairs({'_':' ','a-zA-Z':'A-Z'}, '/cArrow'))+f"""
(In other words, underscores are replaced by spaces, and all letters are uppercase'd)


=== Example:
{cc}lists accent color = MAGENTA{c} sets the {yc}LISTS_ACCENT_COLOR{c} const to {yc}'MAGENTA'{c}.




"""
log.info(help)

def parse(cmd):
    tokens = cmd.split()
    if len(tokens) > 1:
        if '=' in tokens:
            sep_pos = tokens.index('=')
            setting_name = arr2str(tokens[0:sep_pos], ' ')
            setting_value = arr2str(tokens[sep_pos+1:], ' ')
            args = [setting_name, setting_value]
            func = 'set'
        elif tokens[0] in ('disable','enable'):
            args = arr2str([x for i,x in enumerate(tokens) if i != 0], ' ')
            func = tokens[0]
        else:
            args = tokens[1]
            func = tokens[0]
    else:
        args = []
        func = tokens[0]
    return func, args

def exec(stuff):
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
    else:
        log.error('Command not found.')

def quote(string):
    return "'"+str(string).replace('\'', '\\\'')+"'"


def get_consts(method="log"):
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
        colored.append(prop+' : '+value)
    if method != 'log': return pairs
    log.info(arr2str(colored, ''))


reset_map = get_consts('return')
avail_props = reset_map.keys()

def set_const(args):
    name = args[0]
    value = args[1]
    value = quote(value) if value not in ('True','False') else value
    const_name = name.replace(' ','_').upper()
    if name not in avail_props: log.error(f'"{name}" setting does not exist')
    else:
        with open('consts.py', 'r', encoding='utf8') as f:
            raw_datas = f.readlines()

        success = False
        for i, l in enumerate(raw_datas):
            if re.match(f'({const_name} = )([^=]+)', l):
                log.debug(f'setting {const_name} to {value}')
                raw_datas[i] = re.sub(f'({const_name} = )([^=]+)', r'\1' + value, l)
                success = True

        with open('test.txt', 'w', encoding='utf8') as f:
            f.write(''.join(raw_datas))

        if not success: log.error(f'"{name}" setting not found')
        else: log.info(f'{yc}{name}{c} = {value}')

def get_const(name):

    const_name = name.replace(' ','_').upper()
    with open('consts.py', 'r', encoding='utf8') as f:
        raw_datas = f.readlines()

    success = False
    for i, l in enumerate(raw_datas):
        if re.match(f'({const_name} = )([^=]+)', l):
            value = re.sub(f'({const_name} = )([^=]+)', r'\2', l)
            log.info(f"{yc}{name}{c} = {value}")
            success = True

    if not success: log.error(f'"{name}" setting does not exist')

def show_help():
    log.info(help)

def reset(args):
    set_const([args, reset_map[args]])




cmd = str()
while True:
    cmd = str(input(USER_INPUT_INDICATOR))
    while parse(cmd)[0] not in avail_cmds+exit_cmds:
        log.error(f'"{cmd}" is not a valid command')
        cmd = str(input(USER_INPUT_INDICATOR))
    if cmd in exit_cmds:
        log.fatal('Script closed.')
    exec(parse(cmd))
