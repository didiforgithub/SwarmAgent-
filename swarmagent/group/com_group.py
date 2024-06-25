# -*- coding: utf-8 -*-
# Date       : 2023/3/12
# Author     : Jiayi Zhang
# email      : didi4goooogle@gmail.com
# Description: Group Consenus Based on Complex Network Update Rule

import os
from swarmagent.engine.llm_engine import OpenAILLM
from swarmagent.agent.agent import Agent
from swarmagent.config.config import load_config
from swarmagent.utils.tool import human_display  
from swarmagent.prompt.group_prompt import CONCLUSION_PROMPT, GROUP_IN_ENV_IDEA_PROMPT
from swarmagent.utils.logger import logger
from typing import List

config = load_config()

class ComGroup:

    def __init__(self, name:str, members: List[Agent], description: str, strategy: str = "BEST"):
        self.name = name
        self.members = members
        self.group_description = description# TODO 这个地方需要修改，主要的点在于环境信息的添加
        self.env_description = None
        self.description = self.group_description
        self.strategy = strategy
        self.cur_idea = None
        self.group_memory = []
        self.llm = OpenAILLM()


    def complete_desc(self):
        self.description = f"你正处于这样的环境之中：{self.env_description}。/n在这样的大环境下，你所属的群体是{self.name}"

    @property
    def get_members(self):
        members_list = []
        for member in self.members:
            members_list.append(member.name)
        return members_list

    def run(self, idea: str, intervene: bool = False, rounds: int = 20) -> List[List[str]]:
        self.cur_idea = idea
        debate_history = [[f"Situation:{self.group_description}", f"Topic: {idea}"]]
        debate_conclusion_history = []

        # By parameter intervene, you can choose whether to intervene in the debate.
        if intervene:
            intervene_role = input("Please enter into intervene role:")
            while rounds != 0:
                result = self.debate(chat_history=debate_history, conclusion_history=debate_conclusion_history)
                debate_history = result["history"]
                if result['status'] == "consensus":
                    break
                human_display(result['history'][-1])
                intervene = input("Please enter intervene")
                debate_history[-1].append(f"{intervene_role}: {intervene}")
                rounds -= 1
        else:
            while rounds != 0:
                result = self.debate(chat_history=debate_history, conclusion_history=debate_conclusion_history)
                debate_history = result["history"]
                if result['status'] == "consensus":
                    break
                human_display(result['history'][-1])
                rounds -= 1
        
        # After finish debate, every agent need to update their memory by conclude the debate.
        for member in self.members:
            member.event_conclusion(group=self.name, topic=self.cur_idea, conclusion_message=debate_conclusion_history)
        return debate_history
    
    def run_in_env(self, outside_message:str, intervene: bool = False, rounds: int = 20) -> List[List[str]]:
        if self.env_description is None:
            return "请描述环境信息"
        
        self.cur_idea = self.llm.get_response(GROUP_IN_ENV_IDEA_PROMPT.format(situation=self.description, members=self.get_members, messages=outside_message, group_memory=self.group_memory)) 
        print(self.cur_idea)
        debate_history = [[f"Situation:{self.description}", f"Topic: {self.cur_idea}"]]
        debate_conclusion_history = []
        down = False
        # By parameter intervene, you can choose whether to intervene in the debate.
        if intervene:
            # intervene_role = input("Please enter into intervene role:")
            intervene_role = "社区管理人员，与所有小贩关系都非常友好的张平"
            while rounds != 0:
                result = self.debate(chat_history=debate_history, conclusion_history=debate_conclusion_history)
                debate_history = result["history"]
                if down:
                    break
                if result['status'] == "consensus":
                    down = True
                human_display(result['history'][-1])
                # intervene = input("Please enter intervene")
                intervene = "大家不要吵啦，我们可以联合社区管理协会一起来解决这个问题！"
                debate_history[-1].append(f"{intervene_role}:: {intervene}")
                rounds -= 1
        else:
            while rounds != 0:
                result = self.debate(chat_history=debate_history, conclusion_history=debate_conclusion_history)
                debate_history = result["history"]
                if result['status'] == "consensus":
                    break
                human_display(result['history'][-1])
                rounds -= 1
        
        # After finish debate, every agent need to update their memory by conclude the debate.
        for member in self.members:
            member.event_conclusion(group=self.name, topic=self.cur_idea, conclusion_message=debate_conclusion_history)
        self.group_memory.append({self.cur_idea : debate_conclusion_history[-1]})
        
        # TODO 这里代码写死了存储位置
        # group_exp_path = os.path.join(config["EXP_PATH"],f"community/{self.name}.txt")
        # with open(group_exp_path, "a") as file: 
        #     file.write(f"{debate_history}\n")

        # TODO 没有最终的意见汇总环节。

        return debate_conclusion_history[-1]
    

    def debate(self, chat_history: List[List[str]], conclusion_history: List[str]):
        """
        Group debate function. You can choose agent's react mode here (real_act or com_react)
        """
        current_history_conclusion = self.com_group_conclusion(chat_history, conclusion_history)
        conclusion_history.append(current_history_conclusion)
        current_history = []
        for member in self.members:
            # com_react
            # member_response = member.com_react(situation=self.description, topic=self.cur_idea, com_history=chat_history, strategy=self.strategy)
            # real react
            member_response = member.react(chat_history=chat_history, group=self.name, situation=self.description,
                                           strategy=self.strategy, topic=self.cur_idea,
                                           message_conclusion=conclusion_history)
            current_history.append(f"{member.name}:: {member_response}")
        
        group_exp_path = os.path.join(config["EXP_PATH"],f"community/{self.name}.txt")
        directory = os.path.dirname(group_exp_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        if not os.path.exists(group_exp_path):
            with open(group_exp_path, "w") as file:
                file.write(f"{current_history}\n")
        else:
            with open(group_exp_path, "a") as file:
                file.write(f"{current_history}\n")

        chat_history.append(current_history)
        debate_result = {"history": chat_history, 'status': self.judge_debate_result(current_history)}
        return debate_result

    def com_group_conclusion(self, chat_history: List[List[str]], conclusion_history: List[str]):
        conclusion_prompt = CONCLUSION_PROMPT.format(situation=self.description, members=self.get_members,
                                                     topic=self.cur_idea, current_chat=chat_history[-1],
                                                     conclusions_past=conclusion_history)
        conclusion_result = self.llm.get_response(prompt=conclusion_prompt, json_mode=True)
        return conclusion_result["conclusion"]

    def judge_debate_result(self, current_history):
        judge_prompt = f""" 
        As an impartial observer, please assess the recent round of conversation in the group named {current_history}. 
        Your task is to detect if there's an ongoing debate. Stable or gentle disagreements should be disregarded - focus on severe and ongoing disputes. 
        If there is a clear ongoing debate, please return "status":"debate". If there is apparent consensus or no significant conflict, please return "status":"consensus".
        All result should be format as json for python to parse.
        """
        judge_result = self.llm.get_response(prompt=judge_prompt, json_mode=True)
        judge_result = judge_result['status']
        return judge_result
