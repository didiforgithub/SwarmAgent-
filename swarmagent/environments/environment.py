# -*- coding: utf-8 -*-
# Date       : 2023/11/27
# Author     : Jiayi Zhang
# email      : didi4goooogle@gmail.com
# Description: 方案2 Env实现
import os
from typing import List
from ..group.discussion_group import DiscussionGroup
from ..group.communicate_node import CommunicateNode

class SwarmAgent:
    """
    生成模块
    - TODO 1 当前 Decision Group 需要包含所有的 Agent ，之后有更合适的结构可以换一下
    - TODO 2 这里 的生成方式可以是全自动配置，半自动配置，手动配置

    Group形成与消失
    1. 新的一天开始的时候基于 Agent 关系形成或消失掉 Info Group
    2. 新的一天会决定是否会从现在的Decision Group 退出，加入新的Group
    # TODO 如何处理这个形成与消失关系，不然等到v0.3再解决这个问题，先跑一天的
    """
    def __init__(self):
        pass


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

    def publish(self, current_time_step: str ) -> None:
        """
        发布公开信息，考虑一下什么类型的Group能够接收到
        """
        current_publish_message = {
            "time-step":current_time_step,
            "message":{}
        }
        for group in self.discussion_groups:
            current_publish_message["content"][group.name] = group.consensus()

    def forward(self, current_time_step: str) -> None:
        # TODO 在新一天开始（不包括第一天）的时候，判断是否需要
        """
        随时间步的模拟
        0. 依据Agent 的空间关系，刷新Group当前时间步的Agentlist
        1. Discussion Group 遍历操作
        - 判断 Discussion Group 人数，在这个时间段没人自动跳过
        - 所有 Discussion Group 接受 Publish Message，判断几个问题
            - 是否维持原有的Core Agent
            - 由该轮次的Core Agent 决定是否讨论，如果讨论，围绕什么话题进行讨论
        - 讨论启动
            - TODO Config 对每个时间步里面开启讨论的Group行动轮次进行配置
            - TODO 进行复杂的Action循环，怎么组织其中Agent的决策Action是个问题
        - 讨论结束
            - TODO 这里的操作总结为Agent的一个行为就可以，想个好听的名字
            - Agent 对这一轮讨论进行信息总结
            - Agent 判断是否会改变自己对某事件的观点
            - TODO Agent 判断是否会改变自己对某个人的关系
            - Agent 判断是否会改变自己的Plan
        - 修改 Agent 空间关系
        2. Info Group 遍历操作
        -
        3. Publish Message 获取公众环境
        """
        self.refresh_group(current_time_step)
        # T
        self.publish(current_time_step)

    def final_consensus(self):
        # TODO 返回所有Group的最终共识列表
        return self.publish_message[-1]

    def refresh_group(self,current_time_step:str):
        # 思考一下
        pass
    
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
        # 1. 如果是空文件夹，完成所有JSON文件的文件创建
        pass
