#!/usr/bin/python3.6
# coding=utf-8
"""
:Copyright: © 2021 Advanced Control Systems, Inc. All Rights Reserved.
"""
import os
import subprocess

__author__ = 'Darren Liang'


class LinuxInterface:
    def __init__(self):
        self.usr = os.getenv('ORACLE_USER')
        self.pwd = os.getenv('ORACLE_PW')
        self.tns = os.getenv('ORACLE_DBSTRING')

    def ExeCommand(self, command):
        return subprocess.check_output("%s" % command, shell=True).replace('\n','')

    def ExeNonCommand(self, command):
        subprocess.call(command, shell=True)