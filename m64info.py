#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import array
from collections import OrderedDict

filename = sys.argv[1]
buffer = open(filename, 'rb')

header = buffer.read(1024)
input  = buffer.read()

hinfo = OrderedDict([
   ('frame_count',    header[12:16]),
   ('rerecord_count', header[16:20]),
   ('VI/s',           header[20]),
   ('controllers',    header[21]),
   ('rom_name',       header[196:228]),
   ('rom_crc32',      header[228:232]),
   ('video_plugin',   header[290:354]),
   ('sound_plugin',   header[354:418]),
   ('input_plugin',   header[418:482]),
   ('rsp_plugin',     header[482:546]),
   ('author',        header[546:768]),
   ('description',    header[768:1024])
])

dec_hinfo = OrderedDict([
   ('frame_count',    array.array('I', hinfo['frame_count']).pop()),
   ('rerecord_count', array.array('I', hinfo['rerecord_count']).pop()),
   ('VI/s',           hinfo['VI/s']),
   ('controllers',    hinfo['controllers']),
   ('rom_name',       hinfo['rom_name'].rstrip(b'\x00').decode('ascii')),
   ('rom_crc32',      '%x' % array.array('I', hinfo['rom_crc32']).pop()),
   ('video_plugin',   hinfo['video_plugin'].rstrip(b'\x00').decode('ascii')),
   ('sound_plugin',   hinfo['sound_plugin'].rstrip(b'\x00').decode('ascii')),
   ('input_plugin',   hinfo['input_plugin'].rstrip(b'\x00').decode('ascii')),
   ('rsp_plugin',     hinfo['rsp_plugin'].rstrip(b'\x00').decode('ascii')),
   ('author',         hinfo['author'].rstrip(b'\x00').decode('utf-8')),
   ('description',    hinfo['description'].rstrip(b'\x00').decode('utf-8'))
])

if __name__ == '__main__':
   for i in dec_hinfo:
      print('{}: {}'.format(i, dec_hinfo[i]))
