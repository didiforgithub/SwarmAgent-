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
        self.name = name           # 姓名
        self.profile = None        # 个人详细信息
        self.opinions = None       # LIST[Dict]，存储对某件事的观点
        self.base_node = None      # 没有Plan时的位置
        self.nodes = None          # LIST[Dict]，存储所有的Node,包括Discussion Group
        self.memory = None         # Agent Memory
        self.current_plan = None   # 当前的计划

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

    def daily_plan(self):
        """
        Agent 进行日常规划
        """
        pass

    def temp_plan(self):
        """
        Agent 进行临时规划
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

