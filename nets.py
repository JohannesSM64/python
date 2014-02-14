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

    def error(text):
        print(text)
        print('Available sites:')
        for i in sitedict:
            print('* {}: {}'.format(i, sitedict[i]))
        sys.exit(1)

    if len(sys.argv) < 3:
        error('Usage: {} site term'.format(os.path.basename(sys.argv[0])))
    elif not sys.argv[1] in sitedict:
        error('No such site in sitedict: {}'.format(sys.argv[1]))

    open_site(sys.argv[1], sys.argv[2])
