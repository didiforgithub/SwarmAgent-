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
        self.core_agent: Agent = None
        self.topic_list = []
        self.consensus_result = {}

    def run(self, current_time_step, public_message_dict: Dict, discuss_rounds=3):
        # discuss_round 指代的是一个Agent发言的轮数
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
        # 判断讨论话题,基于Topic List，让Core_agent判断此轮的讨论话题是从原来的Topic_list中取，还是开启新的Topic
        discussion_topic = self.judge_topic(public_message=publish_message)
        # 进行讨论，生成共识到结果之中，目前使用一个简单版本
        # self.discuss(current_time_step,discuss_topic=discussion_topic, discuss_rounds=discuss_rounds)
        self.discuss_old(current_time_step, discuss_topic=discussion_topic, discuss_rounds=discuss_rounds)
        # 基于讨论结果，Agent开始自由移动
        self.refresh_agent(discuss_topic=discussion_topic, discuss_history=self.topic_list)

    def judge_core_agent(self, public_message):
        # TODO 判断外界信息是否会改变内部权力结构
        pass

    def judge_topic(self, public_message):
        # TODO 需要根据存储的内部话题与外界信息决定要不要更改话题
        discussion_topic = "Hello World"
        return discussion_topic

    def discuss_old(self, current_time_step, discuss_topic, discuss_rounds):
        """
        典型无序合作方式，所有Agent获取其他人的信息，随后进行统一整合发言
        """
        current_rounds_history = []
        round_history = {}
        # 采用 LLMchat 中的无序合作模式，使得每一个人获取所有信息，最后形成一个共识
        for single_round in range(discuss_rounds):
            temp_history = {}
            for single_agent in self.current_agents:
                temp_history[single_agent.name] = single_agent.initiative_react(discuss_topic, round_history)
            round_history = temp_history
            current_rounds_history.append(round_history)
        # 利用 Core Agent 形成共识,形成后添加到集合当中去
        current_consensus = self.consensus(discuss_topic, round_history)
        self.consensus_result[current_time_step] = current_consensus
        return current_consensus

    def discuss(self, current_time_step, discuss_topic, discuss_rounds):
        # TODO 核心代码
        #   1. Agent在群体之中如何进行主动性的交互 —— 利用Function Calling
        #   2. Agent在群体之中如何产生共识？ —— 需要一个论文作为理论基础
        #   最后如果产生共识就将共识结果放入到self.consensus_result中
        #   考虑连贯性设计，所以如果是新的讨论，需要将之前的讨论结果放入到讨论中

        pass

    def refresh_agent(self, discuss_topic, discuss_history):
        """
        TODO 根据讨论的结果，刷新Agent的信息
        - Agent 对这一轮讨论进行信息总结
        - Agent 判断是否会改变自己对某事件的观点
        - Agent 判断是否会改变自己对某个人的关系
        - Agent 判断是否会改变自己的Plan
        - Agent 基于当前Plan，改变自己的Curr_node
        """
        pass

    def consensus(self, discuss_topic, discussion_history):
        # 1.20 TODO
        #       1. 构建 针对 opinion，relation，memory 的 retrieve
        #       2. 构建refresh agent prompt
        #       3. 构建 JSON Load & Save 方法，先做 Load 再做 Save

        relevant_opinions = "与世无争"
        relevant_relation = "与世无争"
        consensus_prompt = f"""
        Within a team, you, in collaboration with {self.current_agents}, are engaging in discussions regarding {discuss_topic}. 
        Your stance is encapsulated in {relevant_opinions}.
        The dynamics of your relations with the rest of the team members are defined by {relevant_relation}. 
        The record tracing the team discussion from its inception to conclusion is defined as {discussion_history}. 
        Please distill the consensus reached during the discussion and highlight the point that aligns most closely with your thoughts on {discuss_topic}. If no such consensus is found, respond with "None".
        Please express it in JSON format, specifically as such:
        {
        "consensus": ""
        }
        """
        return self.core_agent.task_react(consensus_prompt, json_mode=True)["consensus"]

# TODO 下一步工作，完善react代码，思考一个合适的Prompt让人类做出反应
# 目的是查找一下，Agent如何面对一个情况做出反应，需要涉及到怎样的一个心理机制
# 参考 Camel Role Play 代码 + Humanoid Agent代码
