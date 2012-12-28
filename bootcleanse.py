#!/usr/bin/env python
# -*- coding: utf-8 -*-

## TODO  add support for bootable logical partitions

import os
import sys
from subprocess import Popen, PIPE


REMOVE_MBR_CODE = False
REMOVE_BOOT_FLAG = False

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

def dd(pipe, i, o, *extra):
    cmd = ['sudo', 'dd']
    if i is not None:
        cmd += ['if=%s' % i]
    if o is not None:
        cmd += ['of=%s' % o]
    cmd += extra
    ch0 = sys.stdin
    ch1 = PIPE if (type(pipe) is str) or pipe else sys.stdout
    ch2 = PIPE if (type(pipe) is str) or pipe else sys.stderr
    if type(pipe) is str:
        cmd = ['\'' + a.replace('\'', '\'\\\'\'') + '\'' for a in cmd]
        cmd = ' '.join(cmd)
        cmd = 'echo -e \'%s\' | %s' % (pipe, cmd)
        cmd = ['sudo', 'sh', '-c', cmd]
    return Popen(cmd, stdin=ch0, stdout=ch1, stderr=ch2).communicate()

for mbr in mbrs:
    if REMOVE_MBR_CODE:
        dd(False, '/dev/zero', mbr, 'bs=440', 'count=1')
    if REMOVE_BOOT_FLAG:
        p = 0
        status = dd(True, mbr, None, 'bs=1', 'count=1', 'skip=%i' % (446 + 16 * p))
        status = hex(status[0][0] & 127)[2:]
        if len(status) == 1:
            status = '0' + status
        status = '\\x' + status
        dd(status, None, mbr, 'bs=1', 'count=1', 'seek=%i' % (446 + 16 * p))

