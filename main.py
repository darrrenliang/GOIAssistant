#!/usr/bin/python3
# coding=utf-8
"""
:Copyright: © 2022 Advanced Control Systems, Inc. All Rights Reserved.

@Author: Darren Liang
@Date  : 2022-01-05
"""

import sys
import argparse
from goiassistant import mainwindow

def argsParser():
    # declare argumenet rule
    parser = argparse.ArgumentParser(description='Program for goi assistant')   
    parser.add_argument("-d", "--device" , type=int, help="goi device number")

    args = parser.parse_args()

    if args.device is None:
        print ("*** The goi device number is not found ***")
        sys.exit(-1)
    
    return args.device


if __name__ == '__main__':
    device_number = argsParser()
    sys.exit(mainwindow.main(device_number))