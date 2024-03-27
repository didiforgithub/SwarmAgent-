# -*- coding: utf-8 -*-
# Date       : 2023/3/26
# Author     : Jiayi Zhang
# email      : didi4goooogle@gmail.com
# Description: Config
import os
import yaml

CONFIG_PATH = "swarmagent/config/config.yaml"


def load_config(config_path=CONFIG_PATH):
    configs = dict(os.environ)
    with open(config_path, "r") as file:
        yaml_data = yaml.safe_load(file)
    configs.update(yaml_data)
    return configs
