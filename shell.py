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
# - Multiple commands with ;
# - Piping with |

# TODO:
# - Fix aliases: support ;|

# Ideas:
# - Redirect output with > and 2>
# - Pass input from file with <
# - Run command in background with &
# - Conditionals (&& and ||)
# - Globbing with * ? [ ]

# Written by Johannes Langøy, 2010. Public domain.
# Updated 2014.

from utils import *
import os
import sys
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

def alias(name=None, line=None, *ignore):
    """ Interface to aliases. """
    if name:
        if line:
            aliases[name] = line
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
    acc = ''
    cmd = []
    result = []
    quoted = False
    escaped = False
    endacc = False
    endcmd = False
    endloop = False
    infile = False
    outfile = False
    glob = False
    count = 0
    lastchar = len(line)-1

    for count, c in enumerate(line):
        if c == '#':
            endloop = True
        elif c == '\\':
            if escaped:
                acc += c
            else:
                escaped = True
                continue
        elif c == "'" and not escaped:
            quoted = not quoted
        elif c in [' ','\t'] and not True in (quoted, escaped):
            endacc = True
        elif c == ';' and not True in (quoted, escaped):
            endacc = True
            endcmd = True
        elif c == '|' and not True in (quoted, escaped):
            endacc = True
            endcmd = True
            outfile = True
        else:
            acc += c

        if count == lastchar:
            endloop = True
        if endloop:
            endacc = True
            endcmd = True
        if endacc and acc:
            cmd.append(acc)
            acc = ''
        if endcmd and cmd:
            if result and result[-1][2] == True: # outfile for last
                infile = True
            else:
                infile = False
            result.append((cmd, infile, outfile))
            cmd = []
        if endloop:
            break
        escaped = False
        endacc = False
        endcmd = False
        infile = False
        outfile = False

    if quoted:
        print('shell: unclosed quotation.')
        return None

    return result

def process(parsed):
    """ Process a command line. """
    def handle_parts(parts, last):
        func = subprocess.call
        cmd = parts[0][0]
        infile = parts[0][1]
        outfile = parts[0][2]

        ## Input file
        if infile == True:
            infile = last.stdout
        elif infile == False:
            infile = sys.stdin
        else:
            infile = open(infile)

        ## Output file
        if outfile == True:
            outfile = subprocess.PIPE
            func = subprocess.Popen
        elif outfile == False:
            outfile = sys.stdout
        else:
            outfile = open(outfile)

        ## Run
        last = func(cmd, stdin=infile, stdout=outfile)
        if len(parts) > 1:
            handle_parts(parts[1:], last)

    if parsed[0][0][0] in builtins:
        builtins[parsed[0][0][0]](*parsed[0][0][1:])
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
                    process(parse(line))

    while True:
        try:
            line = input('@ ')
            if line:
                process(parse(line))
        except EOFError:
            print()
            break
        except KeyboardInterrupt:
            print()
            continue

if __name__ == '__main__':
    main()
