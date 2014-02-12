#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class LinuxProcess(object):
    """ Linux process object with info from /proc/. """

    def __init__(self, process):
        self.process = process

    @property
    def stat(self):
        stat = open("/proc/{}/stat".format(self.process)).read().split()
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
        self._cmdline = open("/proc/{}/cmdline".format(self.process)).read().rstrip('\x00').split('\x00')
        return self._cmdline

    @property
    def environ(self):
        self._environ = {pair[0]: pair[1] for pair in [entry.split('=') for entry in open("/proc/{}/environ".format(self.process)).read().rstrip('\x00').split('\x00')]}
        return self._environ

    @property
    def cwd(self):
        self._cwd = os.readlink("/proc/{}/cwd".format(self.process))
        return self._cwd

    @property
    def mounts(self):
        self._mounts = open("/proc/{}/mounts".format(self.process)).read().split('\n')[1:]
        return self._mounts

if __name__ == '__main__':
    import os
    import re

    kthreads = []
    nonkthreads = []
    for p in [LinuxProcess(m) for m in os.listdir("/proc/") if re.match(r"[0-9]+", m)]:
        if p.stat["pgrp"] == "0":
            kthreads.append(p)
        else:
            nonkthreads.append(p)

    print("kthreads:")
    for i in kthreads:
        print("{}: {}".format(i.process, i.stat["comm"]))
    print("\nother processes:")
    for i in nonkthreads:
        print("{}: {}".format(i.process, ' '.join(i.cmdline)))
