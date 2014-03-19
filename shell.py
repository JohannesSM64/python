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
# - Globbing with * ? [ ]

# Ideas:
# - Redirect output with > and 2>
# - Pass input from file with <
# - Run command in background with &
# - Conditionals (&& and ||)
# - Command name completion

# Written by Johannes Langøy, 2010. Public domain.
# Updated 2014.

from utils import *
import os
import sys
from glob import glob
import readline
import subprocess
import copy

# Contains commands that are executed on startup; currently primarily
# useful for defining aliases.
config = os.getenv('HOME') + '/.shellrc'

colors = dict(zip(['black', 'red', 'green', 'yellow', 'blue', 'magenta',
                   'cyan', 'reset'],
                  ['\001\033[{}m\002'.format(x) for x in range(30,38)]))

def prompt():
    result = colors['cyan']
    directory = os.getcwd()
    if directory != os.getenv('HOME'):
        result += directory.split('/')[-1]
    result += "> "
    result += colors['reset']
    return result

readline.parse_and_bind('tab: complete')
readline.set_completer_delims(' ')

earlierdirs = []
laterdirs = []
aliases = {}

def cd_helper(dir):
    try:
        if dir:
            os.chdir(dir)
        else:
            os.chdir(os.getenv('HOME'))
    except OSError as inst:
        print('cd: {0}'.format(inst))

def cd(dir=None, *ignore):
    """ Change directory. Defaults to the home directory. """
    curdir = os.getcwd()
    if cd_helper(dir):
        earlierdirs.append(curdir)

def cdu(*ignore):
    """ cd "undo"; go to previous working directory in history. """
    if not earlierdirs:
        print('cd: no further undo history.')
    else:
        laterdirs.append(os.getcwd())
        mydir = earlierdirs.pop()
        print(mydir)
        cd_helper(mydir)

def cdr(*ignore):
    """ cd "redo"; go to next working directory in history. """
    if not laterdirs:
        print('cd: no further redo history.')
    else:
        earlierdirs.append(os.getcwd())
        mydir = laterdirs.pop()
        print(mydir)
        cd_helper(mydir)

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
            aliases[name] = parse(line)
        else:
            try:
                print(aliases[name])
            except KeyError:
                print('shell: no such alias.')
    else:
        for i in aliases:
            print('{}: {}'.format(i, aliases[i]))

def source(filename=None, *ignore):
    """ Eval a file. """
    with open(filename) as f:
        for line in f.readlines():
            line = line.rstrip()
            if line: # nonblank
                process(parse(line))

builtins = {
    'cd' : cd,
    'cdu': cdu,
    'cdr': cdr,
    'get': getvar,
    'set': setvar,
    'alias': alias,
    'source': source
}

def parse(line):
    acc = ''
    cmd = []
    infile = False
    outfile = False
    result = []
    quoted = False
    escaped = False
    globbing = False
    endacc = False
    endcmd = False
    endloop = False
    firstword = True
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
        elif c in ["'",'"'] and not escaped:
            quoted = not quoted
        elif c in [' ','\t'] and not quoted and not escaped:
            endacc = True
        elif c in ['*','?','[',']'] and not quoted and not escaped:
            globbing = True
            acc += c
        elif c == ';' and not quoted and not escaped:
            endacc = True
            endcmd = True
        elif c == '|' and not quoted and not escaped:
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
            if globbing:
                cmd.extend(sorted(glob(acc)))
            elif firstword and acc in aliases:
                exert(aliases[acc][:-1], result, 0)
                cmd, infile, outfile = copy.deepcopy(aliases[acc][-1])
            else:
                cmd.append(acc)
            acc = ''
            firstword = False
            globbing = False
        if endcmd and cmd:
            if result and result[-1][2] == True:
                infile = True
            result.append((cmd, infile, outfile))
            cmd = []
            infile = False
            outfile = False
            firstword = True
        if endloop:
            break
        escaped = False
        endacc = False
        endcmd = False

    if quoted:
        print('shell: unclosed quotation.')
        return None

    return result

def process(parsed):
    def handle_parts(parts, last):
        func = subprocess.call
        cmd = parts[0][0]
        infile = parts[0][1]
        outfile = parts[0][2]

        ## Builtin?
        if cmd[0] in builtins:
            builtins[cmd[0]](*cmd[1:])
            if len(parts) > 1:
                handle_parts(parts[1:], None)
            return

        ## Input file
        if infile == True and last:
            infile = last.stdout
        else:
            infile = sys.stdin

        ## Output file
        if outfile == True:
            outfile = subprocess.PIPE
            func = subprocess.Popen
        else:
            outfile = sys.stdout

        ## Run
        last = func(cmd, stdin=infile, stdout=outfile)
        if len(parts) > 1:
            handle_parts(parts[1:], last)

    if parsed:
        try:
            handle_parts(parsed, None)
        except OSError as inst:
            print('shell: {}'.format(inst))

def main():
    os.environ['SHELL'] = 'sh' # workaround for a strange python issue

    source(config)

    while True:
        try:
            parsed = parse(input(prompt()))
            if parsed:
                process(parsed)
        except EOFError:
            print()
            break
        except KeyboardInterrupt:
            print()
            continue

if __name__ == '__main__':
    main()
