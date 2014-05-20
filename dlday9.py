#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This can be used to download Day[9]'s Brood War commentary videos. To use it,
you need to have movgrab installed, and opening post from this thread saved as
day9post.txt: http://www.teamliquid.net/forum/brood-war/335184-day-bw-dailies
"""
# Written by Johannes Langøy, 2014. Public domain.

import subprocess, re

for i in re.findall('(http://blip.+)\[/url\]',
                    open('day9post.txt').read()):
    subprocess.call(["movgrab", i])
