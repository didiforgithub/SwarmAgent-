# -*- coding: utf-8 -*-
# Date       : 2023/3/12
# Author     : Jiayi Zhang
# email      : didi4goooogle@gmail.com
# Description: Group Consenus Based on Complex Network Update Rule

from swarmagent.engine.llm_engine import OpenAILLM
from swarmagent.agent.agent import Agent
from swarmagent.utils.tool import human_display  # 将history可视化成为人类容易理解的格式
from typing import List


class ComGroup:

    def __init__(self, members: List[Agent], description: str, strategy: str = "BEST"):
        self.members = members
        self.description = description
        self.strategy = strategy
        self.cur_idea = None
        self.llm = OpenAILLM()

    def run(self, idea: str, intervene: bool = False, rounds: int = 20) -> List[List[str]]:
        self.cur_idea = idea
        debate_history = [[f"Situation:{self.description}", f"Topic: {idea}"]]
        if intervene:
            intervene_role = input("Please enter into intervene role:")
            while rounds != 0:
                result = self.debate(history=debate_history)
                debate_history = result["history"]
                if result['status'] == "consensus":
                    break
                human_display(result['history'][-1])
                intervene = input("Please enter intervene")
                debate_history[-1].append(f"{intervene_role}: {intervene}")
                rounds -= 1
            return debate_history
        else:
            while rounds != 0:
                result = self.debate(history=debate_history)
                debate_history = result["history"]
                if result['status'] == "consensus":
                    break
                human_display(result['history'][-1])
                rounds -= 1
            return debate_history

    def debate(self, history: List[List[str]]):
        current_history = []
        for member in self.members:
            member_response = member.com_react(situation=self.cur_idea, com_history=history, strategy=self.strategy)
            current_history.append(f"{member.name}: {member_response}")
        history.append(current_history)
        debate_result = {"history": history, 'status': self.judge_debate_result(current_history)}
        return debate_result

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
