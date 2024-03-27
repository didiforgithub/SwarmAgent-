# -*- coding: utf-8 -*-
# Date       : 2023/3/12
# Author     : Jiayi Zhang
# email      : didi4goooogle@gmail.com
# Description: Group Consenus Based on Complex Network Update Rule

from swarmagent.engine.llm_engine import OpenAILLM
from swarmagent.agent.agent import Agent
from swarmagent.utils.tool import human_display  
from swarmagent.prompt.group_prompt import CONCLUSION_PROMPT
from swarmagent.utils.logger import logger
from typing import List


class ComGroup:

    def __init__(self, name:str, members: List[Agent], description: str, strategy: str = "BEST"):
        self.name = name
        self.members = members
        self.description = description
        self.strategy = strategy
        self.cur_idea = None
        self.llm = OpenAILLM()

    @property
    def get_members(self):
        members_list = []
        for member in self.members:
            members_list.append(member.name)
        return members_list

    def run(self, idea: str, intervene: bool = False, rounds: int = 20) -> List[List[str]]:
        self.cur_idea = idea
        debate_history = [[f"Situation:{self.description}", f"Topic: {idea}"]]
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

    def debate(self, chat_history: List[List[str]], conclusion_history: List[str]):
        """
        Group debate function. You can choose agent's react mode here (real_act or com_react)
        """
        current_history_conclusion = self.com_group_conclusion(chat_history, conclusion_history)
        conclusion_history.append(current_history_conclusion)
        current_history = []
        for member in self.members:
            # com_react
            # member_response = member.com_react(situation=self.cur_idea, com_history=history, strategy=self.strategy)
            # real react
            member_response = member.react(chat_history=chat_history, situation=self.description,
                                           strategy=self.strategy, topic=self.cur_idea,
                                           message_conclusion=conclusion_history)
            current_history.append(f"{member.name}:: {member_response}")
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
