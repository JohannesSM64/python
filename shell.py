#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" A command shell implementation that aims to be simple and free of
historical baggage. It is hence not compliant with POSIX sh. """

# Current features are:
# - Directory changing with cd, and directory history "undo" and
# "redo" with cdu and cdr
# - Multiple commands on one line with &
# - Comments with # to EOL

# TODO:
# - Text inside parentheses will be executed as a command and its
# output inserted
# - Piping with |

# Written by Johannes Langøy, 2010. Public domain.

import re
import os
import sys
import shlex
import subprocess

def rehash():
    """ Generate available completions for external commands. """
    global extprogs
    extprogs = []
    for d in os.getenv('PATH').split(':'):
        if os.path.isdir(d):
            extprogs.extend(os.listdir(d))

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

def lexer(s):
    """ Helper for lexing and handling syntax errors. """
    try:
        return shlex.split(s, comments=True)
    except ValueError as inst:
        print('shell: {0}'.format(inst))

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
    parts = [lexer(i) for i in line.split('&')]

    for part in parts:
        # Check if the first word on the command line corresponds to
        # the name of a shell builtin, and if so, call it with the
        # args provided. If not, execute it as an external command
        # with the args provided.
        if not part:
            continue
        if part[0] in builtins:
            builtins[part[0]](*part[1:])
        else:
            try:
                subprocess.call(part)
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
