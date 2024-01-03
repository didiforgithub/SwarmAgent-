# -*- coding: utf-8 -*-
# Date       : 2023/12/12
# Author     : Jiayi Zhang
# email      : didi4goooogle@gmail.com
# Description: Agent architecture


from memory import Memory
from agentprofile import Profile


class Agent:

    def __init__(self, name: str):
        """
        使用 name 区分 Agent，信息统一从 Storage 中读取出来
        """
        self.name = name
        self.memory = None
        self.profile = None
        self.load()
        pass

    def perceive(self):
        """
        Agent 感知信息的方法
        """
        pass

    def react(self):
        """
        Agent 接受信息后做出反应
        """
        pass

    def execute(self):
        """
        Agent 执行动作
        """
        pass

    def plan(self):
        """
        Agent 进行日常规划与临时规划
        """
        pass

    def reflect(self):
        """
        Agent 进行总结性记忆反思与批判性记忆反思
        """
        pass

    def recollect(self):
        """
        Agent 检索记忆
        """
        pass

    def load(self):
        """
        Agent Memory & Profile Load
        """
        self.memory = Memory(self.name)
        self.profile = Profile(self.profile)

    def save(self):
        """
        Agent Memory & Profile Save
        :return:
        """
        pass
