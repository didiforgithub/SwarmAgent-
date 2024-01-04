# -*- coding: utf-8 -*-
# Date       : 2023/11/27
# Author     : Jiayi Zhang
# email      : didi4goooogle@gmail.com
# Description: 方案2 Env实现
import os
from typing import List
from ..group.discussion_group import DiscussionGroup
from ..group.communicate_node import CommunicateNode


# TODO 1 当前 Decision Group 需要包含所有的 Agent ，之后有更合适的结构可以换一下
# TODO 2 这里 的生成方式可以是全自动配置，半自动配置，手动配置

class Environment:

    def __init__(self, name: str, simulation_topic: str, decision_group_counts=2, agent_counts=10, auto_generate=True):
        if agent_counts < decision_group_counts:
            raise Exception("Agent counts should be larger than decision group counts")
        self.name = name
        self.simulation_topic = simulation_topic

        self.decision_group_counts = decision_group_counts
        self.discussion_groups = []
        self.communicate_nodes = []

        self.agent_counts = agent_counts
        self.agent_list = []

        self.publish_message = []            # List[Dict] 里面装的是每一时间步下，不同Discussion Group的共识输出

        self.storage_path = os.path.join("../storage/", self.name)
        self.step_list = None
        self.auto_generate = auto_generate
        if self.auto_generate:
            self._init_simulation()

    def _init_simulation(self):
        # 这里就是原来的自动生成模块
        # TODO 1. 基于Simulation Topic 生成决策组信息
        # TODO 2. 基于Simulation Topic, agent_counts 与决策组信息 生成带有各种关系的Agent
        # TODO 3. 基于前置信息生成 Info 组，启动自动化的Simulation
        # 将所有信息存储到一个JSON之中，用户不满意直接去JSON里面改

        pass

    def _validate_simulation(self) -> bool:
        # 在模拟开始前进行验证, 检验一下是否已经满足要求
        if self.auto_generate:
            return True
        if not self.discussion_groups:
            print("Exception: Decision Group should be added first")
            return False
        if not self.communicate_nodes:
            print("Exception: Info Group should be added first")
            return False

    def add_discussion_group(self, discussion_groups: List[DiscussionGroup]) -> None:
        if self.auto_generate:
            raise Exception("Decision Group should not be added manually")
        # 首先检查Decision Group 配置与 Env 中的是否一致
        agent_counts = sum(len(decision_group.members) for decision_group in discussion_groups)
        if agent_counts != self.agent_counts:
            raise Exception("Agent counts should be equal to the counts you set")
        if len(discussion_groups) != self.decision_group_counts:
            raise Exception("Decision Group counts should be equal to the counts you set")
        for decision_group in discussion_groups:
            self.discussion_groups.append(decision_group)
            self.agent_list += decision_group.members

    def add_communicate_node(self, communicate_nodes: List[CommunicateNode]) -> None:

        if self.auto_generate:
            raise Exception("Communicate Node should not be added manually")
        if len(self.discussion_groups) == 0:
            raise Exception("Discussion Group should be added first")
        # TODO 代码逻辑风格一致，这里可以修改成先验证AgentList，再进行添加
        for node in communicate_nodes:
            for member in node.members:
                if member not in self.agent_list:
                    raise Exception(f"Member {member} of Communicate Node {node.name} is not in the Agent List")
        self.communicate_nodes = communicate_nodes


    def run(self, days: int):
        """
        根据输入的时间轮数，遍历环境中的Group，判断是否展开Group的讨论行为
        随后基于下一轮的时间，将Agent安排到Plan产生的Group之中
        """
        # 检查是否满足模拟要求
        self._validate_simulation()
        # TODO 1 基于 Self.storage 里面的 JSON 初始化世界
        # 分支1 如果为空，在Load里面进行Plan等自动化生成
        # 分支2 如果存在，直接加载，继续模拟
        self.load()
        # TODO 2 基于时间步，执行 Step() 方法
        # 这里是生成一个列表，给定days，生成days*6个时间步
        self.step_list = [f'{i+1}-{j+1}' for i in range(days) for j in range(6)]
        for step in self.step_list:
            self.forward(step)
        # TODO 3 模拟完成后，返回一个所有 Group 的共识
        return self.final_consensus()


    def publish(self):
        """
        发布公开信息，考虑一下什么类型的Group能够接收到
        """
        pass

    def forward(self, current_time_step: str):
        # TODO 补充具体的模拟逻辑
        pass

    def final_consensus(self):
        # TODO 返回所有Group的最终共识列表
        return self.publish_message[-1]
    
    def save(self):
        """
        保存当前环境中各个Group的状态
        """
        pass

    def load(self):
        """
        加载JSON文件
        """
        # TODO 加载 JSON 文件，完成所有 Group 与 Agent 的初始化
        
        pass
