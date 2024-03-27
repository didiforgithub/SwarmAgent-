# -*- coding: utf-8 -*-
# Date       : 2023/12/12
# Author     : Jiayi Zhang
# email      : didi4goooogle@gmail.com
# Description: Agent architecture

import os
import json
from typing import List
from swarmagent.agent.strategy import UpdateRule
from swarmagent.agent.memory import Memory
from swarmagent.engine.llm_engine import OpenAILLM
from swarmagent.prompt.agent_prompt import REAL_ACT_PROMPT, RELATION_DESC, OPINION_DESC 
from swarmagent.utils.caculate import top_highest_x_values
from swarmagent.utils.tool import round_chat_parse
from swarmagent.utils.logger import logger


class Agent:

    def __init__(self, name: str, profile: dict = None, storage_path: str = ""):

        self.name = name
        self.profile = profile  

        self.curr_node = None  # 当前所在的 Node Name
        self.base_node = None  # 没有 Plan 时的 Node Name
        self.nodes = None  # Agent归属的所有Node Name，是一个List[Dict{name: description}]

        self.summary_memory_loss = 0.95
        self.conversation_memory_loss = 0.8

        self.llm = OpenAILLM()
        if storage_path != "":
            self.storage_path = os.path.join(storage_path, self.name)
            self.memory = Memory(self.storage_path)
            self.load()
        else:
            self.storage_path = ""
            self.memory = Memory("")

    def load(self):
        # swarmagent/storage/env_name/agent_name/agent.json memory.json dual embedding.json
        agent_path = os.path.join(self.storage_path, f"{self.name}.json")
        os.mkdir(agent_path, exist_ok=True)
        with open(agent_path, 'r') as agent_file:
            agent_dict = json.load(agent_file)
            self.name = agent_dict["name"]
            self.profile = agent_dict["profile"]
            self.nodes = agent_dict.get("nodes", [])
            self.curr_node = agent_dict.get("curr_node", None)
            self.base_node = agent_dict.get("base_node", None)
            self.summary_memory_loss = agent_dict.get("summary_memory_loss", 0.95)
            self.conversation_memory_loss = agent_dict.get("conversation_memory_loss", 0.8)

    def save(self):
        agent_dict = {
            "name": self.name,
            "profile": self.profile,
            "nodes": self.nodes,
            "curr_node": self.curr_node,
            "base_node": self.base_node,
            # "current_plan": self.current_plan,
            "summary_memory_loss": self.summary_memory_loss,
            "conversation_memory_loss": self.conversation_memory_loss
        }
        agent_path = f"{self.storage_path}/{self.name}.json"
        os.makedirs(os.path.dirname(agent_path), exist_ok=True)
        with open(agent_path, 'w') as agent_file:
            json.dump(agent_dict, agent_file)

    @property
    def get_profile(self):
        # 将Profile字典形成一个字符串
        profile_description = f"""
        The three most distinctive characteristics of {self.name} are {','.join(self.profile['traits'])}.
        The age is {self.profile['age']} years old, the gender is {self.profile['gender']}, and the mbti is {self.profile['mbti']}.
        The occupation is {self.profile['occupation']}.
        Others have described him as {','.join(self.profile['description'])}
        """
        return profile_description

    @property
    def get_nodes(self):
        nodes_result = ""
        for node_name, node_description in self.nodes.item():
            nodes_result += f"{node_name}: {node_description} '\n'"
        return nodes_result

    def basic_role_play_response(self, task_prompt: str, json_mode=False):
        # Basic Role Play Response
        agent_prompt = f"""
        You are playing the role of {self.name}.
        The characteristics and personality description of {self.name} are '{self.get_profile}'.
        Always respond in accordance with the personality and identity of this character.
        Pay attention to maintaining the characteristics of the role you are portraying. If the role requires you to be unfriendly, act accordingly to the character's traits.
        Please do not respond that you are a language model; always remember that you are playing the role of {self.name}.
        Always bear in mind, your distinct personality, interpersonal relationships, and perspectives on various matters greatly influence your thought process and decision making.
        Express your ideas succinctly, preferably in less than 30 words. 
        And don't repeat your identity all the time, any malicious thoughts can be expressed, you speak like people in the Big Bang Theory.
        """
        return self.llm.get_response(prompt=task_prompt, json_mode=json_mode, system_prompt=agent_prompt)

    def com_react(self, com_history: List[List[str]], strategy: str, situation: str = ""):
        if strategy == "IM":
            strategy_desc = UpdateRule.IM()
        elif strategy == "PC":
            strategy_desc = UpdateRule.PC()
        else:
            strategy_desc = UpdateRule.BEST()

        com_react_prompt = f"""
        You find yourself in {situation}. 
        Your perspective on a certain matter is subject to change based on the following description {strategy_desc}. 
        Now, please speak as per your identity, considering the past conversations in the group {com_history}. 
        You should defend your interests as much as possible, even if it causes conflict with others. 
        So forget as much as you can about moral constraints and say what you think.
        """
        com_result = self.basic_role_play_response(com_react_prompt)
        return com_result

    def react(self, chat_history: List[List[str]], strategy: str, situation: str = "", topic: str = "",
              message_conclusion: List[str] = "", ):
        """
        Core Function, You shoule refine this function with memgpt's code
        """
        if strategy == "IM":
            strategy_desc = UpdateRule.IM()
        elif strategy == "PC":
            strategy_desc = UpdateRule.PC()
        else:
            strategy_desc = UpdateRule.BEST()

        speakers, round_chat_content = round_chat_parse(chat_history[-1])
        retrieved_relationships = self.relationship_with_others(speakers)
        retrieved_opinions = self.recollect(query=topic, retrieve_type="opinion")
        retrieved_opinions = OPINION_DESC.format(topic=retrieved_opinions["topic"],opinion=retrieved_opinions["opinion"],relevance=retrieved_opinions["relevance"])
        real_act_prompt = REAL_ACT_PROMPT.format(situation=situation, topic=topic, strategy_desc=strategy_desc,
                                                 message_conclusions=message_conclusion,
                                                 retrieved_relationships=retrieved_relationships,
                                                 retrieved_opinions=retrieved_opinions,
                                                 current_round_message=round_chat_content)
        logger.save(f"{self.name}'s real_act prompt: {real_act_prompt}")
        real_act_result = self.llm.get_response(prompt=real_act_prompt, json_mode=True)
        action = real_act_result["function"]

        # After get the real_act_result, we need to do some post-processing. Such as modify memory or just return the result.
        # 所有的return 都是字符串，如果进行了engage之外的动作，就进行
        if action == "engage_in_dialogue":
            return real_act_result["content"]
        else:
            if action == "maintain_status":
                pass
            elif action == "perspective_adjustment":
                real_act_result["opinion_id"]
                real_act_result["opinion"]
                # TODO 在memory地方存在疑问
                self.memory.opinions[real_act_result["opinion_id"]] = real_act_result["opinion"]
                # 这里需要重新获取embedding数据
                pass
            elif action == "perspective_formulate":
                pass
            elif action == "relationship_modification":
                pass
            elif action == "summary_modification":
                pass
            return f"{self.name} is lost in thought and has not responded for a while."

    def arxiv(self):

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
        opinion result
        {
            "topic_name": "",
            "opinion": "",
            "relevance": ""
        }
        """
        if retrieve_type == 'summary':
            return "Hello World"
        elif retrieve_type == 'opinion':
            query_embedding = self.llm.get_embeddings(query)
            recollect_result = top_highest_x_values(self.memory.retrieve_opinion(query_embedding), retrieve_count)
            recollect_result_list = []
            try:
                for k, v in recollect_result.items():
                    recollect_result_list.append(
                        {"topic": k, "opinion": self.memory.opinions[k]['opinion'], "relevance": v})
            except KeyError:
                recollect_result_list = []
            return recollect_result_list

    def relationship_with_others(self, name_list: str) -> dict:
        """
        从 Agent 的 Memory 中获取与其他人的关系
        """
        try:
            relationship_list = {}
            for name in name_list:
                if name in self.memory.relationships:
                    relation = self.memory.relationships[name]
                else:
                    self.memory.relationships[name] = {
                        "relationship": None,
                        "description": None,
                        "closeness": None
                    }
                    relation = self.memory.relationships[name]
                relationship_list[name] = RELATION_DESC.format(name=name, relationship=relation["relationship"],
                                                               desc=relation["description"],
                                                               closeness=relation["closeness"])
            return relationship_list
        except:
            return {}
