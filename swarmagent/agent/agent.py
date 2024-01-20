# -*- coding: utf-8 -*-
# Date       : 2023/12/12
# Author     : Jiayi Zhang
# email      : didi4goooogle@gmail.com
# Description: Agent architecture

import os
import json
from memory import Memory
from ..engine.llm_engine import OpenAILLM
from ..utils.caculate import top_highest_x_values

class Agent:

    def __init__(self, name: str, storage_path: str):
        """
        使用 name 区分 Agent，信息统一从 Storage 中读取出来
        """
        # 基本信息
        self.name = name                        # 姓名
        self.profile = None                     # 个人详细信息
        # 空间关系
        self.curr_node = None                   # 当前所在的Node
        self.base_node = None                   # 没有Plan时的Node
        self.nodes = None                       # Agent归属的所有Node
        # 记忆
        # storage_path: Env_name/agent/
        # TODO 需要再次设计一下记忆的结构
        m_save_path = f"{storage_path}/{self.name}"
        self.memory = Memory(m_save_path)
        self.os_memory_loss = 0.95
        self.c_memory_loss = 0.8
        # 计划
        self.current_plan = None                # 当前的计划
        self.llm = OpenAILLM()

        self.load()

    def load(self):
        # 从storage_path中读取JSON文件
        # 直接对拥有Load函数的类进行初始化就OK，不需要单独写一个Load函数
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
        TODO 在 SwarmAgent 中，所有的交互目的都是为了交流，因此需要找一个论文进行交流次数设置的支撑
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

    def recollect(self, query: str, retrieve_type: str, retrieve_count=3):
        """
        Agent 的回忆 action
        """
        if retrieve_type == 'summary':
            return "Hello World"
        elif retrieve_type == 'opinion':
            query_embedding = self.llm.get_embeddings(query)
            recollect_result = top_highest_x_values(self.memory.retrieve_opinion(query_embedding), retrieve_count)
            # 这里返回的是一个字典
            return recollect_result

    def relationship_with_others(self, other_name: str):
        """
        从 Agent 的 Memory 中获取与其他人的关系
        """
        try:
            relation = self.memory.relationships[other_name]
            return relation
        except KeyError:
            return None

    def save(self):
        """
        Agent Memory & Profile Save
        :return:
        """
        pass

