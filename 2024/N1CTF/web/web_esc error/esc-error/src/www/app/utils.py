import os
import re
import string
import hashlib
import secrets

def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(secrets.choice(characters) for _ in range(length))
    return random_string

def generate_hash():
    suffer = generate_random_string(32) + '_'
    code = generate_random_string(4)
    hash = hashlib.sha256((suffer + code).encode()).hexdigest()
    return suffer, hash

def check_pow(suffer, hash, code):
    if hash == hashlib.sha256((suffer + code).encode()).hexdigest():
        return True
    
    return False

def unicode_decode(text):
    pattern = r'\\u([0-9A-Fa-f]{4})'

    def replace_match(match):
        unicode_value = int(match.group(1), 16)
        return chr(unicode_value)

    result = re.sub(pattern, replace_match, text)
    
    return result

def sql_waf(text):
    blacklist = ['master', 'change', 'outfile', 'slave', 'start', 'status', 'delete', 'drop', 'execute', 'alter', 'global', 'immediate']
    pattern = re.compile(r"|".join(blacklist), re.IGNORECASE)
    if pattern.search(text):
        return True
    else:
        return False

def checkpath(path, windows = False):
    token = '/'

    if re.match('^[A-Z]:/$', path[:3]):
        windows = True
    
    path = re.sub('/+', '/', path)

    if windows:
        path = path.replace('\\', '/')

    if path[0] == '/':
        path = '.' + path

    parts = path.split(token)
    paths = []

    for i in parts:
        if i == '..':
            if len(paths) > 0:
                paths.pop()
            else:
                return False
        elif i == '.':
            continue
        else:
            paths.append(i)
    
    return True

def getdir(path):
    if not checkpath(path):
        return None
    
    if path[0] == '/':
        path = '.' + path
    
    realpath = os.path.realpath(path)
    if realpath[-1] != '/':
        realpath = realpath + '/'
    return realpath