# -*- coding: utf-8 -*-
# Date       : 2023/3/26
# Author     : Jiayi Zhang
# email      : didi4goooogle@gmail.com
# Description: logger tools
import os
from swarmagent.config.config import load_config

config = load_config()

class logger:
    def __init__(self):
        pass

    @staticmethod
    def console_save(content):
        with open(config["LOG_PATH"], "a") as file:
            file.write(content + "\n")

    @staticmethod
    def topic_save(content, topic):
        topic_path = os.path.join(config["RESULT_PATH"], f"{topic}/history.txt")
        with open(topic_path, "w") as file:
            file.write(content)

    @staticmethod
    def agent_save(content, name):
        agent_path = os.path.join(config["RESULT_PATH"], f"{name}/action.txt")
        with open(agent_path, "a") as file:
            file.write(content + "\n")
