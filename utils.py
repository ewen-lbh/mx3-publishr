import re
from consts import *

# === Formatting ===
# sentence case 
def sentence(string):
        # split by words
        letters = list(string)
        # uppercase first letter
        first_letter = letters[0].upper()
        # if the str has other letters
        if len(letters) > 1:
            # delete the first word from letters
            del letters[0]
            # join the other words with a space
            other_letter = ''.join(letters)
            return first_letter+other_letter
        else:
            return first_letter

def intpadding(value, strsize=2):
    return_value  = str(value)
    zeroes_to_add = strsize - len(return_value)
    if zeroes_to_add >= 1:
        for i in range(zeroes_to_add):
            return_value = '0'+return_value
    return return_value

# replace "<placeholder>" with value
def scheme(scheme, data):
    for placeholder, value in data.items():
        scheme = scheme.replace(f'[{placeholder}]', str(value))
    return scheme

def sql_query_scheme(data):
    scheme = DB_QUERY_SCHEME.replace('[keys]', ', '.join(data.keys()))
    scheme = scheme.replace('[values]', ', '.join(data.values()))
    return scheme

def sql_get_query(data):
    data_scheme = DB_FIELDS_SCHEMES
    for key, placeholder in data_scheme.items():
        data_scheme[key] = scheme(placeholder, data)
    return sql_query_scheme(data_scheme)
    


# takes seconds to turn them into HH:mm:ss
# credit: https://arcpy.wordpress.com/2012/04/20/146/
def duration_format(sec_elapsed):
    h = int(sec_elapsed / (60 * 60))
    m = int((sec_elapsed % (60 * 60)) / 60)
    s = sec_elapsed % 60.
    return "{}:{:>02}:{:>05.2f}".format(h, m, s)


# === Core ===
def switch(var, binding):
    for key, value in binding.items():
        if var == key: return value
    return None

# === Primitives handling ===
def is_primitive(var):
    return type(var) in PRIMITIVE_TYPES

def get_primitive_vars(obj):
    props = vars(obj)
    primitives = {}
    for key, value in props.items():
        if is_primitive(value): primitives[key] = value
    return primitives

# === Filename manipulation ===
def addext(filename, ext):
    return f'{filename}.{ext}'

def rmext(filename):
    return re.sub(r'(\.\w+)','',filename)

def chext(filename, newext):
    return addext(rmext(filename), newext)

def truncate(string, max_length, append=''):
    if len(string) > max_length:
        return string[:max_length] + append
    else:
        return string

def filename(path):
    return re.sub(r'(?:(?:.+)\/)+([^\/]+\.\w{3})$',r'\1',path)

# get tracknumber from file name
def tracknumber(filename):
    return re.sub(AUDIOS_FILENAME_REGEX, r'\1',filename)

# === ARRAY SEARCHING ===
# dig through an array, searching for a match against the nth letter of a string
# return a double (index, value) of the first match, returns None if nothing found.
# Primarly used for the 'shortcuts' option of cli.ask.choices()
def search_with_nth_char(array, search, nth=1):
    for i, v in enumerate(array):
        if search == v[nth-1]: return (i, v) 
    return None