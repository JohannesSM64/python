#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

fn = ''
lbuf = []

if len(sys.argv) > 1:
    fn = sys.argv[1]
    if os.path.exists(fn):
        lbuf = open(fn).readlines()

def print_line(index=None, *ignore):
    try:
        print(lbuf[int(index)][0:-1])
    except:
        print('?')

def delete_line(index=None, *ignore):
    try:
        lbuf.pop(int(index))
    except:
        print('?')

def insert_lines(index=None, *ignore):
    try:
        if not len(lbuf) >= int(index):
            print('?')
            return
        lines = sys.stdin.readlines()
        lines.reverse()
        for line in lines:
            lbuf.insert(int(index), line)
    except:
        print('?')

def set_filename(name=None, *ignore):
    global fn
    if name:
        fn = name
    else:
        print('?')

def write(*ignore):
    if not fn:
        print('?')
        return
    buf = ''
    for l in lbuf:
        buf += l
    print(open(fn, 'w').write(buf))

cmds = {
    'p': print_line,
    'd': delete_line,
    'i': insert_lines,
    'f': set_filename,
    'w': write,
    'q': sys.exit
}

while True:
    try:
        inp = input('> ').split()
    except:
        print('?')
        continue
    if inp and inp[0] in cmds:
        cmds[inp[0]](*inp[1:])
    else:
        print('?')
