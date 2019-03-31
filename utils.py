import http.client
import os
import random
import shlex
import time
from subprocess import Popen, PIPE

import httplib2
from googleapiclient.errors import HttpError

from consts import *
import re

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

# replace "[placeholder]" with value
def scheme(scheme, data):
    scheme = scheme.replace('\\[', '&OPENING_BRACKET;').replace('\\]', '&CLOSING_BRACKET;')
    for placeholder, value in data.items():
        scheme = scheme.replace(f'[{placeholder}]', str(value))
    scheme = scheme.replace('&OPENING_BRACKET;','[').replace('&CLOSING_BRACKET;',']')
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

# CLI: apply a terminal styling code
def color_text(text, color):
    if color not in CLI_STYLING_CODES:
        raise ValueError(f'\'{color}\' is not available. Look for the CLI_COLORS constant.')
    else:
        return CLI_STYLING_CODES[color]+text+CLI_STYLING_CODES['ENDC']

def strip_color_codes(text):
    return re.sub(COLORED_TEXT_REGEX, '', text)


# takes seconds to turn them into HH:mm:ss
# credit: https://arcpy.wordpress.com/2012/04/20/146/
def duration_format(sec_elapsed):
    h = int(sec_elapsed / (60 * 60))
    m = int((sec_elapsed % (60 * 60)) / 60)
    s = sec_elapsed % 60.
    return "{}:{:>02}:{:>05.2f}".format(h, m, s)


# === Core ===
def switch(var, binding, default=None):
    for key, value in binding.items():
        if var == key: return value
    return default

# === Types & encodings handling ===
def is_primitive(var):
    return type(var) in PRIMITIVE_TYPES

def get_primitive_vars(obj):
    props = vars(obj)
    primitives = {}
    for key, value in props.items():
        if is_primitive(value): primitives[key] = value
    return primitives

# https://stackoverflow.com/questions/196345/
def is_ascii(s):
    return all(ord(c) < 128 for c in s)

# === Filename manipulation ===
def getext(filename):
    return re.sub(r'(\.\w+)$', r'\1', filename.strip())

def addext(filename, ext):
    return f'{filename}.{ext}'

def rmext(filename):
    return re.sub(r'(\.\w+)', '', filename)

def chext(filename, new_extension):
    return addext(rmext(filename), new_extension)

def truncate(string, max_length, append=''):
    if len(string) > max_length:
        return string[:max_length] + append
    else:
        return string

def filename(path):
    return re.sub(r'(?:(?:.+)/)+([^/]+\.\w{3})$', r'\1', path)

def is_supported_audio_file(filename):
    return getext(filename) in SUPPORTED_AUDIO_FORMATS

# get tracknumber from file name
def tracknumber(filename):
    return re.sub(AUDIOS_FILENAME_REGEX, r'\1',filename)

def cwd_path():
    return unix_slashes(os.getcwd())+'/'

def unix_slashes(path):
    return path.replace('\\', '/')

# === ARRAY & DICTS MANIPULATIONS ===
# dig through an array, searching for a match against the nth letter of a string
# return a double (index, value) of the first match, returns None if nothing found.
# Primarly used for the 'shortcuts' option of cli.ask.choices()
def search_with_nth_char(array, search, nth=1):
    for i, v in enumerate(array):
        if search == v[nth-1]: return i, v
    return None

# credit: https://stackoverflow.com/a/11668135/9943464
def flatten(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        try:
            items.extend(flatten(v, '%s%s%s' % (parent_key, k, sep)).items())
        except AttributeError:
            items.append(('%s%s' % (parent_key, k), v))
    return dict(items)

# return list of key-value pairs from dictionnary, following used_scheme parameter.
# [k] = the keys
# [v] = the values
def kv_pairs(dictionary,
             used_scheme="[k]: [v]",
             center=True,
             align='left',
             sentence_case=False,
             end=''
             ):
    # flatten dictionary
    dictionary = flatten(dictionary, sep='>')
    # returned list
    retlist = list()
    # SCHEME PRESETS
    color = CLI_STYLING_CODES[LISTS_ACCENT_COLOR]
    roloc = CLI_STYLING_CODES['ENDC']  # similarly to if and fi, color and roloc

    if used_scheme == '/cArrow':
        # colored arrow, white keys & values
        separator   = ' => '
        used_scheme = f"[k] {color}=>{roloc} [v]"
    elif used_scheme == '/cSemicolon':
        # separate with :, colored keys, white pairs
        separator   = ': '
        used_scheme = f"{color}[k]{roloc}: [v]"
    elif used_scheme == '/cQuotes':
        # separate with a space, colored keys, white pairs, double-quotes-surrounded values
        separator   = ' "'
        used_scheme = f"{color}[k]{roloc} \"[v]\""
    elif used_scheme == '/cSpace':
        # separate with a space, colored keys, white pairs
        separator   = ' '
        used_scheme = f"{color}[k]{roloc} [v]"
    else:
        separator = used_scheme.replace('[k]', '').replace('[v]', '')

    # Centering
    def spaces_to_add(string, separator=None):
        # get the difference of length between the dictionary's longest key and the current string
        nb_spaces = len(max(dictionary.keys(), key=len)) - len(string)
        # add separator to count if set
        if separator is not None: nb_spaces += len(separator)
        # return a string of nb_spaces spaces
        return ' ' * nb_spaces

    # for each key-value pair
    for k, v in dictionary.items():
        # title casing
        fk = sentence(k) if sentence_case in ('keys', 'both') else k
        fv = sentence(v) if sentence_case in ('values', 'both') else v
        # centering & aligning keys
        if center:
            if align == 'right': fk = spaces_to_add(fk)+fk
            else: fk += spaces_to_add(k)
        # handling of values with newlines
        if '\n' in fv:
            # add number of spaces equivalent to the longest key + the separator
            fv = fv.replace('\n', '\n' +''.join([' '] * (len(max(dictionary.keys(), key=len)) + len(separator))))
        # add the character defined in end=
        fv += end
        # make a string
        string = scheme(used_scheme, {'k':fk, 'v':fv})
        # add it to the list
        retlist.append(string)
    return retlist
def exclude_keys(dictionary, exclude_keys):
    return {k: dictionary[k] for k in set(list(dictionary.keys())) - set(exclude_keys)}

# === SUBPROCESS UTILS
# catch stdout of subprocess call.
# credit: https://stackoverflow.com/a/21000308/9943464
def catch_stdout(cmd):
    """
    Execute the external command and get its exitcode, stdout and stderr.
    /!\ Modified to only return out
    """
    args = shlex.split(cmd)

    proc = Popen(args, stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()
    exitcode = proc.returncode
    #
    return out


# === YOUTUBE DATA API FUNCTIONS

# Explicitly tell the underlying HTTP transport library not to retry, since
# we are handling retry logic ourselves.
httplib2.RETRIES = 1

# Maximum number of times to retry before giving up.
MAX_RETRIES = 10

# Always retry when these exceptions are raised.
RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError, http.client.NotConnected,
  http.client.IncompleteRead, http.client.ImproperConnectionState,
  http.client.CannotSendRequest, http.client.CannotSendHeader,
  http.client.ResponseNotReady, http.client.BadStatusLine)

# Always retry when an apiclient.errors.HttpError with one of these status
# codes is raised.
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

def resumable_upload(request, resource, method):
  response = None
  error = None
  retry = 0
  while response is None:
    try:
      print("Uploading file...")
      status, response = request.next_chunk()
      if response is not None:
        if method == 'insert' and 'id' in response:
          print(response)
        elif method != 'insert' or 'id' not in response:
          print(response)
        else:
          exit("The upload failed with an unexpected response: %s" % response)
    except HttpError as e:
      if e.resp.status in RETRIABLE_STATUS_CODES:
        error = "A retriable HTTP error %d occurred:\n%s" % (e.resp.status,
                                                             e.content)
      else:
        raise
    except RETRIABLE_EXCEPTIONS as e:
      error = "A retriable error occurred: %s" % e

    if error is not None:
      print(error)
      retry += 1
      if retry > MAX_RETRIES:
        exit("No longer attempting to retry.")

      max_sleep = 2 ** retry
      sleep_seconds = random.random() * max_sleep
      print("Sleeping %f seconds and then retrying..." % sleep_seconds)
      time.sleep(sleep_seconds)

# Build a resource based on a list of properties given as key-value pairs.
# Leave properties with empty values out of the inserted resource.
def build_resource(properties):
  resource = {}
  for p in properties:
    # Given a key like "snippet.title", split into "snippet" and "title", where
    # "snippet" will be an object and "title" will be a property in that object.
    prop_array = p.split('.')
    ref = resource
    for pa in range(0, len(prop_array)):
      is_array = False
      key = prop_array[pa]

      # For properties that have array values, convert a name like
      # "snippet.tags[]" to snippet.tags, and set a flag to handle
      # the value as an array.
      if key[-2:] == '[]':
        key = key[0:len(key)-2:]
        is_array = True

      if pa == (len(prop_array) - 1):
        # Leave properties without values out of inserted resource.
        if properties[p]:
          if is_array:
            ref[key] = properties[p].split(',')
          else:
            ref[key] = properties[p]
      elif key not in ref:
        # For example, the property is "snippet.title", but the resource does
        # not yet have a "snippet" object. Create the snippet object here.
        # Setting "ref = ref[key]" means that in the next time through the
        # "for pa in range ..." loop, we will be setting a property in the
        # resource's "snippet" object.
        ref[key] = {}
        ref = ref[key]
      else:
        # For example, the property is "snippet.description", and the resource
        # already has a "snippet" object.
        ref = ref[key]
  return resource