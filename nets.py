#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Open a wiki/search engine query in your web browser.
"""
# Written by Johannes Langøy, 2010-2014. Public domain.

import sys
import webbrowser
import urllib.parse
import colors

sites = {
    'd':   'http://ddg.gg/?q={}',
    'w':   'http://en.wikipedia.org/wiki/{}',
    'aw':  'http://wiki.archlinux.org/index.php/{}',
    'aur': 'http://aur.archlinux.org/packages.php?K={}&do_Search=Go',
}

def open_site(kw, term):
    """ Open the site associated with the keyword in sites. """
    try:
        webbrowser.open(sites[kw].format(urllib.parse.quote(term)))
    except KeyError:
        print("No such site: " + kw)

if __name__ == '__main__':
    import os

    if len(sys.argv) < 3:
        print('Usage: {} site term'.format(os.path.basename(sys.argv[0])))
        print('Available sites:')
        for i in sites:
            print('* {}: {}'.format(i, sites[i].replace('{}', colors.fg['red'] +
                '{}' + colors.fg['default'])))
        sys.exit(1)

    open_site(sys.argv[1], ' '.join(sys.argv[2:]))
