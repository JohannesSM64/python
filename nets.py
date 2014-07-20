#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Open a wiki/search engine query in your web browser.
"""
# Written by Johannes Langøy, 2010-2014. Public domain.

import sys
import webbrowser
import urllib.parse

sites = {
    'd':   {'name': 'Duck Duck Go',
            'url': 'http://ddg.gg/?q={}'},
    'y':   {'name': 'Yandex',
            'url': 'http://www.yandex.com/yandsearch?text={}'},
    'w':   {'name': 'English Wikipedia',
            'url': 'http://en.wikipedia.org/w/index.php?title=Special:Search&search={}'},
    'nw':  {'name': 'Norwegian Wikipedia',
            'url': 'http://no.wikipedia.org/w/index.php?title=Special:Search&search={}'},
    'm':   {'name': 'Metapedia',
            'url': 'http://en.metapedia.org/w/index.php?title=Special:Search&search={}'},
    'aw':  {'name': 'Arch Linux Wiki',
            'url': 'http://wiki.archlinux.org/index.php?title=Special:Search&search={}'},
    'aur': {'name': 'Arch User Repository',
            'url': 'http://aur.archlinux.org/packages.php?K={}&do_Search=Go'}
}

def open_site(kw, term):
    """ Open the site associated with the keyword in sites. """
    try:
        webbrowser.open(sites[kw]['url'].format(urllib.parse.quote(term)))
    except KeyError:
        print("No such site: " + kw)

if __name__ == '__main__':
    import os

    if len(sys.argv) < 3:
        print('Usage: {} site term'.format(os.path.basename(sys.argv[0])))
        print('Available sites:')
        for i in sites:
            print('* {}: {}'.format(i, sites[i]['name']))
        sys.exit(1)

    open_site(sys.argv[1], ' '.join(sys.argv[2:]))
