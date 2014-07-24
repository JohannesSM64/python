# -*- coding: utf-8 -*-
"""
Access ANSI color codes.
Usage example: print(fg_colors['red'] + "Hello World!" + fg_colors['default'])
"""
# Written by Johannes Langøy, 2014. Public domain.

__all__ = ['fg', 'bg']

def ansi_code(x):
    return '\033[{}m'.format(x)

fg = dict(zip(['black', 'red', 'green', 'yellow', 'blue', 'magenta',
               'cyan', 'white', 'default'],
              map(ansi_code, list(range(30,38)) + [39])))

bg = dict(zip(['black', 'red', 'green', 'yellow', 'blue', 'magenta',
               'cyan', 'white', 'default'],
              map(ansi_code, list(range(40,48)) + [49])))
