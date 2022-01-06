#!/usr/bin/python3.6
# coding=utf-8

"""
:Copyright: © 2021 Advanced Control Systems, Inc. All Rights Reserved.
@Author: Darren Liang
@Date  : 2021-01-05
"""
import os
import logging
import configparser

logger = logging.getLogger(__name__)

class AppConfig:
    def __init__(self, path):
        self.path    = path
        self.content = configparser.RawConfigParser()
        self.content.optionxform = str 
        if not os.path.isfile(self.path):
            self.crete_new_config()
            logger.info('Config.ini file is not existed.')
        self.load_settings()

    def get_value(self, section, option):
        try:
            value = self.content.get(section, option)
            logger.debug(f'GET VALUE: {value} FROM [{section}, {option}]')
            return value
        except configparser.NoOptionError:
            return None
    
    def load_settings(self):
        self.content.read(self.path ,encoding="utf-8")
        return self.content
    
    def set_attr(self, section, option, value):
        self.content.set(section,option,value)
        logger.info(f'SET VALUE: {value} TO [{section}, {option}]')
        self.write_config()

    def delete_section(self):
        self.content.remove_section(section)
        self.write_config()
        
    def delete_option(self):
        self.content.remove_option(section)
        self.write_config()

    def crete_new_config(self):
        self.content.add_section("delay")
        self.content.set("delay","feeder","5")
        self.content.set("delay","point","5")
        self.content.set("delay","check","10")
        self.content.set("delay","task","5")
        self.content.set("delay","schedule","20")
        self.write_config()
    
    def write_config(self):
        # write back to config.ini file.
        with open(self.path, 'w' ,encoding="utf-8") as configfile:
            self.content.write(configfile)

if __name__ == '__main__':
    conf = Conf(PATH)
    content = conf.read_confing()
    
    # return config content
    print(content)

    # return all seciton in config.ini
    print(content.sections())

    # return section data
    print(content.options("delay"))

    # return all option in section
    print(content.items("delay"))

    # return string value
    print(content.get("Column", "idxes"))

    # return integer value
    print(content.get("Substation", "3C"))
