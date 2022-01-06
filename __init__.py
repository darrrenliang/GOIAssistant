#!/usr/bin/python3
# coding=utf-8
"""
:Copyright: © 2022 Advanced Control Systems, Inc. All Rights Reserved.

@Author: Darren Liang
@Date  : 2022-01-05
"""

import os
import logging
import logging.handlers

from core.OracleInterface   import OracleInterface
# from core.conf              import AppConfig


# GUI TITLE
TITLE = "GOI Assistant"

# DB INFO
def connect_database():
    USER  = ""
    PSWD  = ""
    TNS   = ""
    Mapdb = OracleInterface(USER, PSWD, TNS)
    Mapdb.ConnectTest()
    return Mapdb

# CONFIG
# CONF_PATH = ""
# APP_CONF  = AppConfig(CONF_PATH)

# LOG INFO
LOG_FILENAME = 'GOI_Assistant.log'
LOG_FORMAT   = '%(asctime)s [%(process)d] %(levelname)s %(name)s: %(message)s'
LOG_FOLDER   = ''


if __name__ == "__main__":
    USER  = ""
    PSWD  = ""
    TNS   = ""
    Mapdb = OracleInterface(USER, PSWD, TNS)
    Mapdb.ConnectTest()