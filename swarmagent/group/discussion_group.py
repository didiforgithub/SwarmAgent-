from group import BaseGroup
from typing import List, Dict
from ..agent.agent import Agent


class DiscussionGroup(BaseGroup):
    def __init__(self, name: str, description: str, agent_list: List[Agent], curr_agent: List[Agent] = None):
        """
        self.name = group_name
        self.description = description
        self.group_memory = []
        self.members = agent_list          # Group 成员
        self.current_agents = curr_agents  # Group 当前时间步上的成员
        """
        super().__init__(name, description, agent_list, curr_agent)
        self.core_agent = None
        self.topic_list = []
        self.consensus_result = {}
    def run(self,current_time_step,public_message_dict: Dict, discuss_round=10):
        """
        1. Discussion Group Run
        - 接受传参数进来的Public Message
        - 判断几个问题
            - 是否维持原有的Core Agent
            - 由该轮次的Core Agent 决定是否讨论，如果讨论，围绕什么话题进行讨论；
                - 这里会提供之前围绕什么话题进行的讨论，与上次讨论的概括，考虑要不要继续讨论
        - 讨论启动
            - Config 对每个时间步里面开启讨论的Group行动轮次进行配置
            - 进行复杂的Action循环，怎么组织其中Agent的决策Action是个问题
        - 讨论结束
            - 对 Agent 状态进行更新
        """
        # 接受 Publish Message
        publish_message = f'Public Message: {", ".join([f"{k}:{v}" for k, v in public_message_dict["message"].items()])}'
        # 判断是否维持原有的Core Agent —— TODO 这里使用一个简单的投票机制，之后去与权利分配结合在一起
        self.judge_core_agent(public_message=publish_message)
        # 判断讨论话题,基于Topic List判断此轮的讨论话题是要新开一个还是延续下去
        discussion_topic = self.judge_topic(public_message=publish_message)
        # 进行讨论，生成共识到结果之中
        self.discuss(current_time_step,discuss_topic=discussion_topic, discuss_round=discuss_round)
        # 基于讨论结果，Agent开始自由移动
        self.refresh_agent(discuss_topic=discussion_topic, discuss_history=self.topic_list)

    def judge_core_agent(self, public_message):
        # TODO 判断外界信息是否会改变内部权力结构
        pass

    def judge_topic(self, public_message):
        # TODO 需要根据存储的内部话题与外界信息决定要不要更改话题
        discussion_topic = "Hello World"
        return discussion_topic

    def discuss(self,current_time_step,discuss_topic, discuss_round):
        # TODO 实现核心贡献，在多代理系统让Agent进行主动性的讨论
        # TODO 最后如果产生共识就将共识结果放入到self.consensus_result中
        # TODO 考虑连贯性设计，所以如果是新的讨论，需要将之前的讨论结果放入到讨论中
        pass

    def refresh_agent(self,discuss_topic,discuss_history):
        """
        TODO 根据讨论的结果，刷新Agent的信息
        - Agent 对这一轮讨论进行信息总结
        - Agent 判断是否会改变自己对某事件的观点
        - Agent 判断是否会改变自己对某个人的关系
        - Agent 判断是否会改变自己的Plan
        - Agent 基于当前Plan，改变自己的Curr_node
        """
        pass

    def get_consensus(self, current_time_step):
        # 根据时间步获取共识结果
        return self.consensus_result[current_time_step]
