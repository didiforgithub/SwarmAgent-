# -*- coding: utf-8 -*-
# Date       : 2023/11/27
# Author     : Jiayi Zhang
# email      : didi4goooogle@gmail.com
# Description: 方案2 Env实现
import os
import json
from typing import List, Dict
from ..agent.agent import Agent
from .discussion_group import DiscussionGroup
from .communicate_node import CommunicateNode


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

    def __init__(self, name: str, simulation_topic: str, decision_group_counts=2, agent_counts=10, day_rounds=6,
                 auto_generate=True):
        # TODO 添加超参数，用于控制群体模拟效果，如设置信息茧房实验
        if agent_counts < decision_group_counts:
            raise Exception("Agent counts should be larger than decision group counts")
        self.name = name
        self.simulation_topic = simulation_topic

        self.decision_group_counts = decision_group_counts
        self.discussion_groups: List[DiscussionGroup] = []
        self.communicate_nodes: List[CommunicateNode] = []
        self.group2agent: Dict = {}

        self.agent_counts = agent_counts
        self.agent_list: List[Agent] = []

        self.publish_message: List[Dict] = []  # List[Dict] 里面装的是每一时间步下，不同Discussion Group的共识输出

        self.storage_path = os.path.join("swarmagent/storage", self.name)
        self.day_rounds = day_rounds
        self.step_list = None
        self.current_step = None
        # auto generate
        self.auto_generate = auto_generate
        if self.auto_generate:
            self._init_simulation()
        else:
            self.load()

    def load(self):
        """
        加载 JSON 文件，初始化environment与Group信息
        """
        # 1. 如果是空文件夹，完成所有JSON文件的文件创建
        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path)
            # TODO 这里应该与 Auto generate 配合进行
        # 2. 如果不是空文件夹，读取所有的JSON文件
        print(os.path.join(self.storage_path, "environment.json"))
        with open(os.path.join(self.storage_path, "environment.json"))as env_file:
            env_dict = json.load(env_file)

            # 初始化环境的基础信息
            self.name = env_dict["name"]
            self.simulation_topic = env_dict['simulation_topic']
            self.group2agent = env_dict["group2agent"]
            self.current_step = env_dict.get("current_step", "1-1")

            # 初始化 Agent 信息
            for agent_name in env_dict["agent_list"]:
                current_agent = Agent(name=agent_name, storage_path=os.path.join(self.storage_path, 'agent'))
                self.agent_list.append(current_agent)

            # 初始化 Decision Group 信息
            for dis_group_name in env_dict["discussion_groups"]:
                current_group_agents_name = self.group2agent[dis_group_name]
                current_group_agents = []
                for cur_agent_name in current_group_agents_name:
                    current_group_agents.append(self.get_agent(cur_agent_name))
                current_dec_group = DiscussionGroup(name=dis_group_name, agent_list=current_group_agents,
                                                    storage_path=os.path.join(self.storage_path, "discussion_group"))
                self.discussion_groups.append(current_dec_group)

            # TODO 初始化 Info Group 信息
            for com_node_name in env_dict["communicate_nodes"]:

                pass

    def save(self):
        """
        保存当前环境和Group信息至 JSON 文件
        """
        # 1. 准备保存的数据
        env_dict = {"name": self.name,
                    "simulation_topic": self.simulation_topic,
                    'decision_group_counts': self.decision_group_counts,
                    "group2agent": self.group2agent,
                    "current_step": self.current_step,
                    'agent_counts': self.agent_counts,
                    'day_rounds': self.day_rounds,
                    "agent_list": [agent.name for agent in self.agent_list],
                    "discussion_groups": [group.name for group in self.discussion_groups],
                    "communicate_nodes": [node.name for node in self.communicate_nodes]}

        # 2. 写入Json文件
        with open(self.storage_path + "/environment.json", 'w') as env_file:
            json.dump(env_dict, env_file)
        # 3. 调用下属 Class 进行Save
        # TODO 撰写 Save 函数
        for agent in self.agent_list:
            agent.save()
        for group in self.discussion_groups:
            group.save()
        for node in self.communicate_nodes:
            node.save()

    def get_agent(self, agent_name):
        for agent in self.agent_list:
            if agent.name == agent_name:
                return agent

    def run(self, days: int):
        """
        根据输入的时间轮数，遍历环境中的Group，判断是否展开Group的讨论行为
        随后基于下一轮的时间，将Agent安排到Plan产生的Group之中
        """
        # 检查是否满足模拟要求
        self._validate_simulation()
        # TODO 1 基于 Self.storage 里面的 JSON 初始化世界
        # 分支1 如果为空，
        # 分支2 如果存在，直接加载，继续模拟
        self.load()
        # TODO 2 基于时间步，执行 Step() 方法； 没有考虑断点的问题
        # 这里是生成一个列表，给定days，生成days*6个时间步
        self.step_list = [f'{i + 1}-{j + 1}' for i in range(days) for j in range(self.day_rounds)]
        for step in self.step_list:
            self.forward(step)
        # TODO 3 模拟完成后，返回一个所有 Group 的共识
        return self.publish_message[-1]

    @property
    def groups(self):
        return self.discussion_groups + self.communicate_nodes

    def _init_simulation(self):
        # 这里就是原来的自动生成模块
        # TODO 1. 基于Simulation Topic 生成决策组信息
        # TODO 2. 基于Simulation Topic, agent_counts 与决策组信息 生成带有各种关系的Agent
        # TODO 3. 基于前置信息生成 Info 组，启动自动化的Simulation
        # 将所有信息存储到一个JSON之中，用户不满意直接去JSON里面改
        return True

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
        for discussion_group in discussion_groups:
            self.discussion_groups.append(discussion_group)
            self.agent_list += discussion_group.members

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

    def publish(self, current_time_step: str, current_discussion_group: List[DiscussionGroup] = None) -> None:
        """
        发布公开信息
        """
        current_publish_message = {
            "time-step": current_time_step,
            "message": {}
        }
        if current_discussion_group is None:
            return None
        else:
            for group in current_discussion_group:
                current_publish_message["message"][group.name] = group.consensus_result[current_time_step]
                # TODO Publish Message 要不要修改成字典啊
            self.publish_message.append(current_publish_message)

    def forward(self, current_time_step: str) -> None:
        # TODO 在新一天开始（不包括第一天）的时候，判断是否需要
        """
        随时间步的模拟
        0. 依据Agent 的空间关系，刷新Group当前时间步的Agentlist
        1. Discussion Group 遍历操作
        - 判断 Discussion Group 人数，在这个时间段没人自动跳过
        - 所有 Discussion Group 接受 Publish Message，
        - Discussion Group Run
        2. Info Group 遍历操作
        -
        3. 发布公开信息
        """
        # 0. 依据 Agent 的空间关系，刷新 Group 当前时间步的 Agentlist
        self.refresh_group(current_time_step)
        # 1. Discussion Group 遍历操作
        # TODO 这里的操作出现了不健壮性，当Discussion没有的时候怎么办
        #   - 判断 Discussion Group 人数，在这个时间段没人自动跳过
        current_discussion_groups = [discussion for discussion in self.discussion_groups if
                                     len(discussion.current_agents) > 0]
        #   - 提供Public Message
        last_message = self.publish_message[-1]
        for current_discussion_group in current_discussion_groups:
            # TODO 在Discussion Group中补充Group的run方法
            current_discussion_group.run(current_time_step, last_message)
        # 2. Info Group 遍历操作
        current_communicate_nodes = [info for info in self.communicate_nodes if len(info.current_agents) > 0]
        for current_communicate_node in current_communicate_nodes:
            # TODO 在Communicate Node 中补充Group的run方法
            current_communicate_node.run()
        # 3. 发布公开信息
        self.publish(current_time_step)

    def refresh_group(self, current_time_step: str) -> None:
        # TODO 对于固定的时间步，应该按照Base Node进行安置，这里之后再进行修改
        # 刷新当前Group中的Current Agents
        for group in self.groups:
            group.current_agents = []
        # 刷新当前Agent的Curr Node，修改归属
        for agent in self.agent_list:
            agent_curr_node = agent.curr_node
            for group in self.groups:
                if agent_curr_node == group.name:
                    group.current_agents.append(agent)

    def save(self):
        """
        保存当前环境中各个Group的状态
        """
        pass
