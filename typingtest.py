#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
See how many lines you can type out in a set time.
"""
# Written by Johannes Langøy, 2010. Public domain.

import sys
import time
import signal
import random

try:
    import readline
except ImportError:
    pass

en_linelist = [
    "Political language is designed to make lies sound truthful and murder respectable, and to give an appearance of solidity to pure wind.",
    "Only two things are infinite, the universe and human stupidity, and I'm not sure about the former.",
    "finalised virtual hyperstationary factory class",
    "In our world, every storm has an end. Every night brings a new morning.",
    "The men the European public admires most extravagantly are the most daring liars; the men they detest most violently are those who try to tell them the truth.",
    "I contend that we are both atheists, I just believe in one fewer god than you do. When you understand why you dismiss all the other possible gods, you will understand why I dismiss yours.",
    "history (n): A series of lies on which we agree"
]

random.shuffle(en_linelist)

cleared_lines = 0

def en_run():
    global cleared_lines
    active_line = en_linelist.pop(0)
    en_linelist.append(active_line)
    print(active_line)
    input_line = input()
    if input_line == active_line:
        cleared_lines += 1
        print()
    else:
        print("YOU FAIL!")
        exit()

def time_up(*ignore):
    print("\n=================================\nYou cleared {} lines. Gratz.".format(cleared_lines))
    exit()

def main():
    signal.signal(signal.SIGALRM, time_up)
    if len(sys.argv) > 1:
        signal.alarm(int(sys.argv[1]))
    else:
        signal.alarm(30)
    while True:
        try:
            en_run()
        except KeyboardInterrupt:
            exit()

if __name__ == '__main__':
    main()
