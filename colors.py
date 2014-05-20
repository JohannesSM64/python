# -*- coding: utf-8 -*-
"""
Access ANSI color codes.
Usage example: print(fg_colors['red'] + "Hello World!" + fg_colors['default'])
"""
# Written by Johannes Langøy, 2014. Public domain.

__all__ = ['fg', 'bg']

def ansi_code(x):
    return '\001\033[{}m\002'.format(x)

fg = dict(zip(['black', 'red', 'green', 'yellow', 'blue', 'magenta',
                      'cyan', 'white'],
                     [ansi_code(x) for x in range(30,38)]))

fg['default'] = ansi_code(39)

bg = dict(zip(['black', 'red', 'green', 'yellow', 'blue', 'magenta',
                      'cyan', 'white'],
                     [ansi_code(x) for x in range(40,48)]))

bg['default'] = ansi_code(49)
