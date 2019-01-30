import re
from consts import *

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

def truncate(string, max_length, append=''):
    if len(string) > max_length:
        return string[:max_length] + append
    else:
        return string

def filename(path):
    return re.sub(r'(?:(?:.+)\/)+([^\/]+)\.\w{3}$',r'\1',path)

# get tracknumber from file name
def tracknumber(filename):
    return re.sub(AUDIOS_FILENAME_REGEX, r'\1',filename)

def intpadding(value, strsize=2):
    return_value  = str(value)
    zeroes_to_add = strsize - len(return_value)
    if zeroes_to_add >= 1:
        for i in range(zeroes_to_add):
            return_value = '0'+return_value
    return return_value

def switch(data, key):
    return data[key]