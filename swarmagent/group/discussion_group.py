import json
import os
from .group import BaseGroup
from typing import List, Dict
from ..agent.agent import Agent


class DiscussionGroup(BaseGroup):
    def __init__(self, name: str, agent_list: List[Agent], storage_path: str, description: str = '',
                 curr_agent: List[Agent] = []):
        """
        self.name = group_name
        self.description = description
        self.group_memory = []
        self.members = agent_list          # Group 成员
        self.current_agents = curr_agents  # Group 当前时间步上的成员
        self.storage_path = os.path.join(storage_path,self.name)
        """
        super().__init__(group_name=name, agent_list=agent_list, description=description, storage_path=storage_path,
                         curr_agents=curr_agent)
        self.core_agent: Agent = None
        self.topic_list = []
        self.consensus_result = {}
        self.load()

    def load(self):
        with open(self.storage_path + f"/{self.name}.json") as dis_file:
            dis_dict = json.load(dis_file)

            self.name = dis_dict["name"]
            self.description = dis_dict["description"]
            self.group_memory = dis_dict.get("group_memory", [])
            self.current_agents = dis_dict.get("current_agents", [])
            # 没有Load Self.members
            self.topic_list = dis_dict.get("topic_list", [])
            self.consensus_result = dis_dict.get("consensus_result", {})
            self.core_agent = dis_dict.get("core_agent", "")
            if self.core_agent != '':
                for agent in self.members:
                    if agent.name == self.core_agent:
                        self.core_agent = agent

    def save(self):
        # 创建输出字典
        dis_dict = {
            "name": self.name,
            "description": self.description,
            "group_memory": self.group_memory,
            "current_agents": self.current_agents,
            "topic_list": self.topic_list,
            "consensus_result": self.consensus_result,
            "core_agent": self.core_agent.name if self.core_agent is not None else ''
        }
        # 确保存储路径存在
        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path)
        # 保存字典为json文件
        with open(self.storage_path + f"/{self.name}.json", 'w') as f:
            json.dump(dis_dict, f)

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
            - config 对每个时间步里面开启讨论的Group行动轮次进行配置
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
        current_discussion_history = []
        round_history = {}
        # 采用 LLMchat 中的无序合作模式，使得每一个人获取所有信息，最后形成一个共识
        for single_round in range(discuss_rounds):
            temp_history = {}
            for single_agent in self.current_agents:
                # TODO 修改这个地方 Single Agent 的 react 模式为 Task react
                # discuss_topic, round_history
                temp_history[single_agent.name] = single_agent.task_react()
            round_history = temp_history
            current_discussion_history.append(round_history)
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
        """
        让 Core Agent 形成该群体的共识
        TODO Version 0.1 之后需要迭代更好的版本，找论文（群体共识是如何形成的）进行理论支撑
        """
        # 这个地方返回的是一个列表[Dict, Dict]
        # relevant_opinion_list = self.core_agent.recollect(query=discuss_topic, retrieve_type="opinion",
        #                                                   retrieve_count=3)
        # # TODO 对观点相关性的过滤需要进行修改
        # relevant_opinion_list = [op for op in relevant_opinion_list if op["relevance"] > 0]
        # if len(relevant_opinion_list) == 0:
        #     relevant_opinions = f"In reference to {discuss_topic}, I held no pre-existing opinions."
        # else:
        #     relevant_opinions = f"In reference to {discuss_topic}, I held {len(relevant_opinion_list)} related pre-existing opinions. '\n'"
        #     for opinion in relevant_opinion_list:
        #         relevant_opinions += f"Regarding {opinion['topic_name']}, my position is {opinion['opinion']}. '\n'"
        #
        relevant_relations = ""
        for other_agent in self.current_agents:
            relevant_relation = self.core_agent.relationship_with_others(other_agent.name)
            if relevant_relation is None:
                relevant_relations += f"I have yet to establish any contact with {other_agent.name} in the past. '\n'"
            else:
                relevant_relations += f"My relationship with {other_agent.name} can be characterized as {relevant_relation['relationship']}, the details of which include {relevant_relation['description']}. On a comprehensive intimacy scale that peaks at 10, our level of closeness stands at {relevant_relation['closeness']}.'\n'"

        relevant_opinions = self.core_agent.memory.opinions
        consensus_prompt = f"""
        Within a team, you, in collaboration with {self.current_agents}, are engaging in discussions regarding {discuss_topic}. 
        Your stance is encapsulated in {relevant_opinions}.
        The dynamics of your relations with the rest of the team members are defined by {relevant_relations}. 
        The record tracing the team discussion from its inception to conclusion is defined as {discussion_history}. 
        Please distill the consensus reached during the discussion and highlight the point that aligns most closely with your thoughts on {discuss_topic}. If no such consensus is found, respond with "None".
        Please express it in JSON format, specifically as such:
        {
        "consensus": ""
        }
        """
        return self.core_agent.task_react(consensus_prompt, json_mode=True)["consensus"]


# 1.20 TODO ? Forget Implement ?
#       1. 构建 针对 opinion，relation，memory 的 retrieve
#       2. 构建 refresh agent prompt
#       3. 构建 JSON Load & Save 方法，先做 Load 再做 Save

# 2.16 TODO How To Restart SwarmAgent
#       [ ] 1. Test for the discussion_group
#       [ ] 2. Test for the agent memory & init_act
#       [ ] 3. Test for the
