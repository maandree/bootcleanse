#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from subprocess import Popen, PIPE


mbrs = []

for arg in sys.argv[1:]:
    mbrs.append(arg)
    print('Remove MBR code from ' + arg)
    if not (('a' <= arg[-1]) and (arg[-1] <= 'z') and (arg[:-1] in ('/dev/sd', '/dev/hd'))):
        print('\033[01;33mWarning:\033[21;39m Does not match /dev/(sd|hd)[a-z]')

print()
print('If you are not sure what you are doing, you may want')
print('to back up the first 512 byte of each defected file.')
print('To back up run `dd if=DEVICE bs=512 count=1 > DEV.backup`.')
print('To restore run `dd of=DEVICE bs=512 count=1 is=DEV.backup`.')
print()
print('\033[01mProcessed? [yes/no]\033[21m')

while True:
    yn = input()
    if yn == 'yes':
        break
    if yn == 'no':
        exit(128)
    print('Only ‘yes’ and ‘no’ is valid')


for mbr in mbrs:
    Popen(['sudo', 'dd', 'if=/dev/zero', 'of=' + mbr, 'bs=440', 'count=1'], stdin=PIPE, stdout=PIPE, stderr=PIPE).communicate()

