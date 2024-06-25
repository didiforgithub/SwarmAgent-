# -*- coding: utf-8 -*-
# Date       : 2023/4/15
# Author     : Jiayi Zhang
# email      : didi4goooogle@gmail.com
# Description: Basic Environment

from typing import List
from swarmagent.group.com_group import ComGroup


class Environment:
    def __init__(self, name, desc, topic, group_list:List[ComGroup], rounds) -> None:
        self.name = name
        self.desc = desc
        self.topic = topic
        self.group_list = group_list
        self.rounds = rounds
        self.message_pool = []
        self.env_idea = f"在环境'{self.desc}'中，群体们讨论的主题为{self.topic}" # 组合name desc topic

    def complete_group_desc(self):
        pass

    def run(self, intervene:bool):
        for round in range(self.rounds):
            self.message_pool.append({})
            for group in self.group_list:
                group_message = group.run_in_env(outside_message=str(self.message_pool), intervene=intervene)
                print(f"group_messasge: {group_message}")
                self.message_pool[round+1][group.name] = group_message

        return self.message_pool



