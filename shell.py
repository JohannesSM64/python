#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" A command shell implementation that aims to be simple and free of
historical baggage. It is hence not compliant with POSIX sh. """

# Current features are:
# - A basic parser which understands spaces, quotes, backslashes and
# comments
# - Directory changing with cd, and directory history "undo" and
# "redo" with cdu and cdr

# TODO:
# - Piping with |

# Written by Johannes Langøy, 2010. Public domain.
# Updated 2014.

import re
import os
import sys
import subprocess

def get_cmdline(prompt):
    """ Get and return command line from stdin, using prompt if
    interactive. """
    try:
        if sys.stdin.isatty():
            cmdline = input(prompt)
        else:
            cmdline = input()
    except EOFError:
        sys.exit()
    return cmdline

def parse(line):
    """ Split an input line into a list of arguments. """
    result = []
    word = ''
    inquotes = False
    inparens = False
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
        if not backslashed and c == '(':
            inparens = True
            continue
        if not backslashed and c == ')':
            output = subprocess.Popen(parse(word), stdout=subprocess.PIPE).stdout.read()
            if output[-1] == 10: #newline
                result.append(output[:-1])
            else:
                result.append(output)
            inparens = False
            word=''
            continue
        if not backslashed and c == ' ':
            if inquotes or inparens:
                word += c
            else:
                if len(word) > 0:
                    result.append(word)
                word = ''
        else:
            word += c
        backslashed = False

    if len(word) > 0:
        result.append(word)
    return result

# Used later for cd history.
earlierdirs = []
laterdirs   = []

def cd(dir=None):
    """ Change directory. Defaults to the home directory. """
    earlierdirs.append(os.getcwd())
    if dir:
        try:
            os.chdir(dir)
        except OSError as inst:
            print('cd: {0}'.format(inst))
    else:
        os.chdir(os.path.expanduser('~'))

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
    # Put arguments into the env.
    for i, s in enumerate(sys.argv):
        os.environ[str(i)] = s

    while True:
        try:
            cmdline = get_cmdline(os.getenv('PROMPT') or '@ ')
            process(cmdline)
        except KeyboardInterrupt:
            continue

if __name__ == '__main__':
    main()
