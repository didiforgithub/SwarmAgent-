# -*- coding: utf-8 -*-
# Date       : 2023/3/26
# Author     : Jiayi Zhang
# email      : didi4goooogle@gmail.com
# Description: logger tools
from swarmagent.config.config import load_config

config = load_config()

class logger:
    def __init__(self):
        pass

    @staticmethod
    def save(content):
        with open(config["LOG_PATH"], "a") as file:
            file.write(content + "\n")
            
