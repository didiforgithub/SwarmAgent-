# -*- coding: utf-8 -*-
# Date       : 2023/12/12
# Author     : Jiayi Zhang
# email      : didi4goooogle@gmail.com
# Description: Agent's memory architecture

from typing import Dict


class Memory:
    """
    Memory 保存的是长期记忆与Agent的观点层次思考
    Agent 的短期记忆直接放在Group环境记忆之中
    """

    def __init__(self, storage_path: str, summaries={}, opinions={}, relationships={}, conversation_history={}):
        """
        summaries: {
            ‘time-step’: {
                'group info': '',
                'content': ''
            },
        }

        opinions: {
            'event name':{
                'opinion': ''
                'reason':''
            }
        }

        relationships: {
            'agent name': {
                ‘relationship’: '',
                ‘description’:'',
                'closeness':''
            }
        }
        """
        self.summaries: Dict = summaries
        self.opinions: Dict = opinions  # LIST[Dict]，存储对某件事的观点
        self.relationships: Dict = relationships  # LIST[DICT] 存储与某个人的关系
        self.conversation_history: Dict = conversation_history
        self.storage_path = storage_path

    def add_summaries(self, content):
        pass


    def retrieve(self):
        '''
        针对summaries与opinions的记忆检索，较低概率出现失忆事件
        '''
        pass

    def recollect(self, content):
        """
        针对conversation_history的记忆检索，较高概率出现失忆事件
        失忆事件触发
        """
        pass

    def summary(self, chat_snippet:[]):
        """
        引入Summary机制，针对近期发生的事件进行总结，随后添加到summaries中
        """
        result = chat_snippet
        self.add_summaries(result)

    def criticize(self):
        """
        引入Criticize机制，对短期记忆进行批判性思考，思考这一记忆是否会影响自己的观点或者改变原有的计划
        :return:
        """
        pass
