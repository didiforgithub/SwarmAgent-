# -*- coding: utf-8 -*-
# Date       : 2023/12/12
# Author     : Jiayi Zhang
# email      : didi4goooogle@gmail.com
# Description: Agent architecture


from memory import Memory
from ..engine.llm_engine import OpenAILLM
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
        self.llm = OpenAILLM()

        self.load()
        pass

    def task_react(self, task_prompt: str, json_mode=False):
        agent_prompt = f"""
        You are identified as {self.name}. 
        Your profile description is '{self.profile}'. 
        Always bear in mind, your distinct personality, interpersonal relationships, and perspectives on various matters greatly influence your thought process and decision making.
        """
        final_prompt = agent_prompt + task_prompt
        return self.llm.get_response(final_prompt, json_mode=json_mode)

    def initiative_react(self):
        """
        Agent 在Group中 主动进行 Function Calling 的过程
        可能的任务：总结信息，发起讨论，
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

