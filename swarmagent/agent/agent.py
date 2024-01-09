# -*- coding: utf-8 -*-
# Date       : 2023/12/12
# Author     : Jiayi Zhang
# email      : didi4goooogle@gmail.com
# Description: Agent architecture


from memory import Memory

class Agent:

    def __init__(self, name: str):
        """
        使用 name 区分 Agent，信息统一从 Storage 中读取出来
        """
        # 基本信息
        self.name = name                # 姓名
        self.profile = None             # 个人详细信息

        # 空间关系
        self.curr_node = None           # 当前所在的Node
        self.base_node = None           # 没有Plan时的Node
        self.nodes = None               # Agent归属的所有Node

        # 记忆
        self.memory: Memory             # Agent Memory

        # 计划
        self.current_plan = None        # 当前的计划

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

    def save(self):
        """
        Agent Memory & Profile Save
        :return:
        """
        pass

