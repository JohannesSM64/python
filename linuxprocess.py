#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinuxProcess(pid) creates an object through which you can access information
about the given process, such as command line and working directory.
"""
# Written by Johannes Langøy, 2011-2014. Public domain.

import os
import re

class LinuxProcess(object):
    """ Linux process object with info from /proc/. """

    def __init__(self, num):
        self.num = num
        self.path = "/proc/{}/".format(num)
        if not os.path.exists(self.path):
            raise Exception("There is no process with ID {}.".format(num))

    @property
    def stat(self):
        stat = open(self.path + "stat").read().split()
        self._stat = { "pid"                   : stat[0],
                       "comm"                  : stat[1],
                       "state"                 : stat[2],
                       "ppid"                  : stat[3],
                       "pgrp"                  : stat[4],
                       "session"               : stat[5],
                       "tty_nr"                : stat[6],
                       "tpgid"                 : stat[7],
                       "flags"                 : stat[8],
                       "minflt"                : stat[9],
                       "cminflt"               : stat[10],
                       "majflt"                : stat[11],
                       "cmajflt"               : stat[12],
                       "utime"                 : stat[13],
                       "stime"                 : stat[14],
                       "cutime"                : stat[15],
                       "cstime"                : stat[16],
                       "priority"              : stat[17],
                       "nice"                  : stat[18],
                       "num_threads"           : stat[19],
                       "itrealvalue"           : stat[20],
                       "starttime"             : stat[21],
                       "vsize"                 : stat[22],
                       "rss"                   : stat[23],
                       "rsslim"                : stat[24],
                       "startcode"             : stat[25],
                       "endcode"               : stat[26],
                       "startstack"            : stat[27],
                       "kstkesp"               : stat[28],
                       "kstkeip"               : stat[29],
                       "signal"                : stat[30],
                       "blocked"               : stat[31],
                       "sigignore"             : stat[32],
                       "sigcatch"              : stat[33],
                       "wchan"                 : stat[34],
                       "nswap"                 : stat[35],
                       "cnswap"                : stat[36],
                       "exit_signal"           : stat[37],
                       "processor"             : stat[38],
                       "rt_priority"           : stat[39],
                       "policy"                : stat[40],
                       "delayacct_blkio_ticks" : stat[41],
                       "guest_time"            : stat[42],
                       "cguest_time"           : stat[43], }
        return self._stat

    @property
    def cmdline(self):
        self._cmdline = open(self.path + "cmdline").read().rstrip('\x00').split('\x00')
        return self._cmdline

    @property
    def environ(self):
        self._environ = {pair[0]: pair[1] for pair in [entry.split('=') for entry in open(self.path + "environ").read().rstrip('\x00').split('\x00')]}
        return self._environ

    @property
    def cwd(self):
        self._cwd = os.readlink(self.path + "cwd")
        return self._cwd

    @property
    def mounts(self):
        self._mounts = open(self.path + "mounts").read().split('\n')[1:]
        return self._mounts

if __name__ == '__main__':
    kthreads = []
    nonkthreads = []
    for p in [LinuxProcess(m) for m in os.listdir("/proc/") if re.match(r"[0-9]+", m)]:
        if p.stat["pgrp"] == "0":
            kthreads.append(p)
        else:
            nonkthreads.append(p)

    print("kthreads:")
    for i in kthreads:
        print("{}: {}".format(i.num, i.stat["comm"]))
    print("\nother processes:")
    for i in nonkthreads:
        print("{}: {}".format(i.num, ' '.join(i.cmdline)))
