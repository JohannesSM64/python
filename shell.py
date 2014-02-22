#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" A command shell implementation that aims to be simple and free of
historical baggage. It is hence not compliant with POSIX sh. """

# Current features:
# - Basic line editing, history and file name completion (readline)
# - Directory changing with cd
# - cd history undo and redo with cdu and cdr
# - Access environment variables with get and set
# - Define and view aliases with alias
# - Startup commands are read from config file
# - Multi-word arguments with '"
# - Escape the next character with \
# - Comment until EOL with #
# - Piping with |
# - Globbing with * ? [ ]

# Ideas:
# - Redirect output with > and 2>
# - Multiple commands with ; and maybe &&
# - Run command in background with &
# - Pass input from file with <

# Written by Johannes Langøy, 2010. Public domain.
# Updated 2014.

from utils import *
import os
from glob import glob
import readline
import subprocess

config = os.path.expanduser('~/.shellrc')

readline.parse_and_bind('tab: complete')

earlierdirs = []
laterdirs = []
aliases = {}

def cd(dir=None, *ignore):
    """ Change directory. Defaults to the home directory. """
    earlierdirs.append(os.getcwd())
    try:
        if dir:
            os.chdir(dir)
        else:
            os.chdir(os.getenv('HOME'))
    except OSError as inst:
        print('cd: {0}'.format(inst))

def cdu(*ignore):
    """ cd "undo"; go to previous working directory in history. """
    if not earlierdirs:
        print('cd: no further undo history.')
    else:
        laterdirs.append(os.getcwd())
        mydir = earlierdirs.pop()
        print(mydir)
        cd(mydir)

def cdr(*ignore):
    """ cd "redo"; go to next working directory in history. """
    if not laterdirs:
        print('cd: no further redo history.')
    else:
        earlierdirs.append(os.getcwd())
        mydir = laterdirs.pop()
        print(mydir)
        cd(mydir)

def getvar(arg=None, *ignore):
    """ Get an environment variable. """
    if arg:
        print(os.getenv(arg))

def setvar(var=None, val=None, *ignore):
    """ Set an environment variable. """
    if var and val:
        os.environ[var] = val

def alias(name=None, *val):
    """ Interface to aliases. """
    if name:
        if val:
            aliases[name] = val
        else:
            try:
                print(aliases[name])
            except KeyError:
                print('shell: no such alias.')
    else:
        for i in aliases:
            print('{}: {}'.format(i, aliases[i]))

builtins = {
    'cd' : cd,
    'cdu': cdu,
    'cdr': cdr,
    'get': getvar,
    'set': setvar,
    'alias': alias
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
            # Add-handler code {{{
            if len(acc) > 0:
                if globbing:
                    globbing = False
                    files = sorted(glob(acc))
                    if files:
                        part.extend(files)
                    else:
                        print('shell: no matches found: {}'.format(acc))
                        return []
                else:
                    part.append(acc)
                acc = ''
            # }}}
            if len(part) > 0:
                result.append(part)
            part = []
        elif not backslashed and c in ['"',"'"]:
            inquotes = not inquotes
            continue
        elif not backslashed and c in [' ','\t']:
            if inquotes:
                acc += c
            else:
                # Add-handler code {{{
                if len(acc) > 0:
                    if globbing:
                        globbing = False
                        files = sorted(glob(acc))
                        if files:
                            part.extend(files)
                        else:
                            print('shell: no matches found: {}'.format(acc))
                            return []
                    else:
                        part.append(acc)
                    acc = ''
                #-- }}}
        else:
            acc += c
        backslashed = False

    # Add-handler code {{{
    if len(acc) > 0:
        if globbing:
            globbing = False
            files = sorted(glob(acc))
            if files:
                part.extend(files)
            else:
                print('shell: no matches found: {}'.format(acc))
                return []
        else:
            part.append(acc)
        acc = ''
    # }}}
    if len(part) > 0:
        result.append(part)

    if inquotes:
        print('shell: closing quote mark missing.')
        return []

    # Expand aliases.
    for part in result:
        if part[0] in aliases:
            exert(aliases[part.pop(0)], part, 0)

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
    os.environ['SHELL'] = 'sh' # workaround for a strange python issue

    if os.path.exists(config):
        with open(config) as f:
            for line in f.readlines():
                line = line.rstrip()
                if line: # nonblank
                    process(line)

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
