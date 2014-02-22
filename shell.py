#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" A command shell implementation that aims to be simple and free of
historical baggage. It is hence not compliant with POSIX sh. """

# Current features are:
# - Basic line editing, history and file name completion (readline)
# - Directory changing with cd
# - cd history undo and redo with cdu and cdr
# - Access environment variables with get and set
# - Multi-word arguments with '"
# - Escape the next character with \
# - Comment until EOL with #
# - Piping with |
# - Globbing with * ? [ ]

# Written by Johannes Langøy, 2010. Public domain.
# Updated 2014.

import os
from glob import glob
import readline
import subprocess

readline.parse_and_bind('tab: complete')

def cd(dir=None):
    """ Change directory. Defaults to the home directory. """
    earlierdirs.append(os.getcwd())
    try:
        if dir:
            os.chdir(dir)
        else:
            os.chdir(os.getenv('HOME'))
    except OSError as inst:
        print('cd: {0}'.format(inst))

# Used for cd history.
earlierdirs = []
laterdirs   = []

def cdu():
    """ cd "undo"; go to previous working directory in history. """
    if not earlierdirs:
        print('cd: no further undo history.')
    else:
        laterdirs.append(os.getcwd())
        mydir = earlierdirs.pop()
        print(mydir)
        cd(mydir)

def cdr():
    """ cd "redo"; go to next working directory in history. """
    if not laterdirs:
        print('cd: no further redo history.')
    else:
        earlierdirs.append(os.getcwd())
        mydir = laterdirs.pop()
        print(mydir)
        cd(mydir)

def getvar(arg):
    """ Get an environment variable. """
    print(os.getenv(arg))

def setvar(var, val):
    """ Set an environment variable. """
    os.environ[var] = val

builtins = {
    'cd' : cd,
    'cdu': cdu,
    'cdr': cdr,
    'get': getvar,
    'set': setvar
}

def parse(line):
    """ Take an input line and return a list of commands, each element
    a list consisting of command name and arguments. """
    result = []
    part = []
    acc = ''
    inquotes = False
    backslashed = False
    globbing = False

    for c in line:
        if c == '\\':
            if backslashed:
                acc += c
            else:
                backslashed = True
                continue
        elif not backslashed and not inquotes and c in ['*','?','[',']']:
            globbing = True
            acc += c
        elif not backslashed and not inquotes and c == '#':
            break
        elif not backslashed and not inquotes and c == '|':
            #-- Begin duplicated code
            if len(acc) > 0:
                if globbing:
                    globbing = False
                    files = sorted(glob(acc))
                    if files:
                        part.extend(files)
                    else:
                        print("shell: no matches found: {}".format(acc))
                        return []
                else:
                    part.append(acc)
                acc = ''
            #-- End duplicated code
            result.append(part)
            part = []
        elif not backslashed and c in ['"',"'"]:
            inquotes = not inquotes
            continue
        elif not backslashed and c in [' ','\t']:
            if inquotes:
                acc += c
            else:
                #-- Begin duplicated code
                if len(acc) > 0:
                    if globbing:
                        globbing = False
                        files = sorted(glob(acc))
                        if files:
                            part.extend(files)
                        else:
                            print("shell: no matches found: {}".format(acc))
                            return []
                    else:
                        part.append(acc)
                    acc = ''
                #-- End duplicated code
        else:
            acc += c
        backslashed = False

    #-- Begin duplicated code
    if len(acc) > 0:
        if globbing:
            globbing = False
            files = sorted(glob(acc))
            if files:
                part.extend(files)
            else:
                print("shell: no matches found: {}".format(acc))
                return []
        else:
            part.append(acc)
        acc = ''
    #-- End duplicated code
    if len(part) > 0:
        result.append(part)
    return result

def process(line):
    """ Process a command line. """
    parsed = parse(line)
    if not parsed:
        return

    def handle_parts(parts, pipe):
        if len(parts) == 1:
            if pipe:
                subprocess.call(parts[0], stdin=pipe.stdout)
            else:
                subprocess.call(parts[0])
        else:
            if pipe:
                pipe = subprocess.Popen(parts[0], stdout=-1,
                                        stdin=pipe.stdout)
            else:
                pipe = subprocess.Popen(parts[0], stdout=-1)
            handle_parts(parts[1:], pipe)

    if parsed[0][0] in builtins:
        builtins[parsed[0][0]](*parsed[0][1:])
    else:
        try:
            handle_parts(parsed, None)
        except OSError as inst:
            print('shell: {}'.format(inst))

def main():
    os.environ['SHELL'] = 'shell.py'
    while True:
        try:
            process(input('@ '))
        except EOFError:
            print()
            break
        except KeyboardInterrupt:
            print()
            continue

if __name__ == '__main__':
    main()
