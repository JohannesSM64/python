# -*- coding: utf-8 -*-

def ansi_code(x):
    return '\001\033[{}m\002'.format(x)

fg_colors = dict(zip(['black', 'red', 'green', 'yellow', 'blue', 'magenta',
                      'cyan', 'white'],
                     [ansi_code(x) for x in range(30,38)]))

fg_colors['default'] = ansi_code(39)

bg_colors = dict(zip(['black', 'red', 'green', 'yellow', 'blue', 'magenta',
                      'cyan', 'white'],
                     [ansi_code(x) for x in range(40,48)]))

bg_colors['default'] = ansi_code(49)
