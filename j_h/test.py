#!/usr/bin/env python
#-*- coding:utf-8 -*-

e = ('Please keep filesize under %s M. Current filesize %s M') % (
int(1048576 / 1024 / 2024), int(4234532432 / 1024 / 1024))
print(e)
