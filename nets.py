#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Open a wiki/search engine query in your web browser. """

# Written by Johannes Langøy, 2010-2011. Public domain.

import sys
import webbrowser
import urllib.parse

sitedict = {
    'wiki':  'http://en.wikipedia.org/wiki/{}',
    'awiki': 'http://wiki.archlinux.org/index.php/{}',
    'aur':   'http://aur.archlinux.org/packages.php?K={}&do_Search=Go',
    'ddg':   'http://ddg.gg/?q={}'
}

def open_site(kw, term):
    """ Open the site associated with the keyword in sitedict. """
    webbrowser.open(sitedict[kw].format(urllib.parse.quote(term)))

if __name__ == '__main__':
    import os

    def available_sites():
        print('Available sites:')
        for i in sitedict:
            print('* {}: {}'.format(i, sitedict[i]))

    if not sys.argv[2:]:
        print('Usage: {} site term'.format(os.path.basename(sys.argv[0])))
        available_sites()
        sys.exit(1)

    try:
        open_site(sys.argv[1], sys.argv[2])
    except KeyError:
        print('No such site in sitedict: {}'.format(sys.argv[1]))
        available_sites()
        sys.exit(1)
