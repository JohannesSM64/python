#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" A command shell implementation that aims to be simple and free of
historical baggage. It is hence not compliant with POSIX sh. """

# Current features are:
# - Basic line editing, history and file name completion (readline)
# - Multi-word arguments with '"
# - Escape the next character with \
# - Comment until EOL with #
# - Directory changing with cd
# - cd history undo and redo with cdu and cdr

# TODO:
# - Piping with |
# - Globbing with *

# Written by Johannes Langøy, 2010. Public domain.
# Updated 2014.

import os
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
    """ Split an input line into a list of arguments. """
    result = []
    acc = ''
    inquotes = False
    backslashed = False

    for c in line:
        if c == '\\':
            backslashed = True
            continue
        if not backslashed and c == '#':
            break
        if not backslashed and c in ['"', "'"]:
            inquotes = not inquotes
            continue
        if not backslashed and c in [' ', '\t']:
            if inquotes:
                acc += c
            else:
                if len(acc) > 0:
                    result.append(acc)
                acc = ''
        else:
            acc += c
        backslashed = False

    if len(acc) > 0:
        result.append(acc)
    return result

def process(line):
    """ Process a command line. """
    line = parse(line)
    if not line:
        return

    # If the first word on the command line equals the name of a shell
    # builtin, call it with the args provided. If not, execute it as an
    # external command with the args provided.
    if line[0] in builtins:
        builtins[line[0]](*line[1:])
    else:
        try:
            subprocess.call(line)
        except OSError as inst:
            print('shell: {0}'.format(inst))

def main():
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
