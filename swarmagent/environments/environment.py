# -*- coding: utf-8 -*-
# Date       : 2023/11/27
# Author     : Jiayi Zhang
# email      : didi4goooogle@gmail.com
# Description: 方案2 Env实现

from autogeneration import generate
from ..group.decision_group import DecisionGroup
from ..group.info_group import InfoGroup
from typing import List


# TODO 1 当前 Decision Group 需要包含所有的 Agent ，之后有更合适的结构可以换一下
# TODO 2 这里 的生成方式可以是全自动配置，半自动配置，手动配置

class Environment:

    def __init__(self, simulation_topic: str, decision_group_counts=2, agent_counts=10, auto_generate=True):
        if agent_counts < decision_group_counts:
            raise Exception("Agent counts should be larger than decision group counts")
        self.simulation_topic = simulation_topic
        self.decision_group_counts = decision_group_counts
        self.decision_groups = []
        self.info_groups = []
        self.agent_counts = agent_counts
        self.agent_list = []
        self.publish_message = {}
        self.auto_generate = auto_generate
        if self.auto_generate:
            self._init_simulation()

    def _init_simulation(self):
        # 这里就是原来的自动生成模块
        # TODO 1. 基于Simulation Topic 生成决策组信息
        # TODO 2. 基于Simulation Topic, agent_counts 与决策组信息 生成带有各种关系的Agent
        # TODO 3. 基于前置信息生成 Info 组，启动自动化的Simulation

        pass

    def _validate_simulation(self) -> bool:
        # 在模拟开始前进行验证, 检验一下是否已经满足要求
        if self.auto_generate:
            return True
        if not self.decision_groups:
            print("Exception: Decision Group should be added first")
            return False
        if not self.info_groups:
            print("Exception: Info Group should be added first")
            return False

    def add_decision_group(self, decision_groups: List[DecisionGroup]) -> None:
        if self.auto_generate:
            raise Exception("Decision Group should not be added manually")
        # 首先检查Decision Group 配置与 Env 中的是否一致
        agent_counts = sum(len(decision_group.members) for decision_group in decision_groups)
        if agent_counts != self.agent_counts:
            raise Exception("Agent counts should be equal to the counts you set")
        if len(decision_groups) != self.decision_group_counts:
            raise Exception("Decision Group counts should be equal to the counts you set")
        for decision_group in decision_groups:
            self.decision_groups.append(decision_group)
            self.agent_list += decision_group.members

    def add_info_group(self, info_groups: List[InfoGroup]) -> None:

        if self.auto_generate:
            raise Exception("Decision Group should not be added manually")
        # 检查是否所有的Info Group member 都在Env 的Agent List 之中（Env的Agent List 是由Decision Group 决定的）
        if len(self.decision_groups) == 0:
            raise Exception("Decision Group should be added first")
        # TODO 代码逻辑风格一致，这里可以修改成先验证AgentList，再进行添加
        for info_group in info_groups:
            # 检查Info Groups中所有info group的members是否都在self.agent_list之中
            for member in info_group.members:
                if member not in self.agent_list:
                    raise Exception(f"Member {member} of Info Group {info_group.name} is not in the Agent List")
        self.info_groups = info_groups


    def run(self):
        """
        根据输入的时间轮数，遍历环境中的Group，判断是否展开Group的讨论行为
        随后基于下一轮的时间，将Agent安排到Plan产生的Group之中
        """
        self._validate_simulation()
        pass

    def publish(self):
        """
        发布公开信息，考虑一下什么类型的Group能够接收到
        """
        pass

    def timestep(self):
        pass
    
    def save(self):
        """
        保存当前环境中各个Group的状态
        """
        pass

    def load(self):
        """
        加载环境与当前环境中Group状态
        """
        pass
