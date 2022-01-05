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

# from core.i18n              import _
from core.OracleInterface   import OracleInterface
# from core.conf              import AppConfig


# GUI TITLE
TITLE = "GOI Assistant"

# DB INFO
def connect_database():
    USER  = os.getenv('ORACLE_USER', 'acs_qa')
    PSWD  = os.getenv('ORACLE_PW'  , 'acs_qa')
    TNS   = os.getenv('ORACLE_DBSTRING', 'emsa')
    PRISMdb = OracleInterface(USER, PSWD, TNS)
    return PRISMdb

# CONFIG
# CONF_PATH = "/home/acs/DB/Convert/ATO_SCRIPTS/ADMS_APP/Config.ini"
# APP_CONF  = AppConfig(CONF_PATH)

# LOG INFO
LOG_FILENAME = 'GOI_Assistant.log'
LOG_FORMAT   = '%(asctime)s [%(process)d] %(levelname)s %(name)s: %(message)s'
LOG_FOLDER   = '/home/acs/tmp'