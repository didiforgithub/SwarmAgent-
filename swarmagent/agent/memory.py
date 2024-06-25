# -*- coding: utf-8 -*-
# Date       : 2023/12/12
# Author     : Jiayi Zhang
# email      : didi4goooogle@gmail.com
# Description: Agent's memory architecture

import os
import json
from typing import Dict
from swarmagent.utils.caculate import cos_sim


class Memory:
    def __init__(self, storage_path: str):
        """
        MEMORY 格式
        {
            summaries: {
                'id':{
                    'group': '<event group>',
                    'name': '<event name>'
                    'content': '<event summart content>'
                },
            },
            opinions: {
                'id': {
                    "topic":"<topic content>",
                    "opinion":"<opinion content>"
                }
            },
            relationships: {
                'agent name': {
                    'relationship': '',
                    'description':'',
                    'closeness':''
                }
            }
        }

        MEMORY Embedding JSON 存储
        MEMORY 遗忘机制与类型的关系
        1. 无遗忘机制：relationship, plan history, opinions,
        2. 存在遗忘机制：summaries (conversation history)
            1. opinions 不会受到时间影响，只会受到事实影响，因此 opinions实际上在检索过程中不会存在遗忘的情况
            2. summaries 受到时间影响，会出现低概率的遗忘
        3. 遗忘机制：在relevance检索的过程中，搜索到TopK 相关的 Summary时会概率性的出现遗忘现象，即在检索之后返回一个 Sorry I just forget.
        4. 模糊记忆机制：在检索到Summary之后，在提取具体的conversation时会出现一个遗忘prompt，基于此对conversation进行不同程度的模糊
        """
        self.storage_path = os.path.join(storage_path, "memory")
        self.summaries: Dict = {}  # 对近期会话的总结性记忆，进行检索时会出现较低的失忆情况
        self.summaries_embeddings: Dict = {}
        self.opinions: Dict = {}  # LIST[Dict]，存储对某件事的观点，进行检索时会出现较低的失忆情况
        self.opinions_embeddings: Dict = {}  # 这里应该是对topic做embeddding吧
        self.relationships: Dict = {}  # LIST[DICT] 存储与某个人的关系，不会出现任何失忆状况
        self.plan_history: Dict = {}  # 存储过去的Plan信息，记忆在什么时候去过什么地方
        self.load()

    def load(self):
        # storage_path: Env_name/agent_name/memory.json
        def load_json(file_name, default_value):
            json_path = os.path.join(self.storage_path, f"{file_name}.json")
            try:
                with open(json_path, 'r') as json_file:
                    return json.load(json_file)
            except:
                return default_value

        memory_file = load_json("memory", {})
        self.opinions = memory_file.get("opinions", {})
        self.summaries = memory_file.get("summaries", {})
        self.relationships = memory_file.get("relationships", {})
        self.plan_history = memory_file.get("plan_history", {})
        # 加载embedding 时，使用 {id: <embeddings>} 对应方式获取 embedding 值
        self.opinions_embeddings = load_json("opinion_embeddings", {})
        self.summaries_embeddings = load_json("summary_embeddings", {})

    def save(self):
        def save_json(file_name, data):
            memory_path = f"{self.storage_path}/" + f"{file_name}.json"
            os.makedirs(os.path.dirname(memory_path), exist_ok=True)
            with open(memory_path, 'w') as json_file:
                json.dump(data, json_file)

        memory = {
            "opinions": self.opinions,
            "summaries": self.summaries,
            "relationships": self.relationships,
            "plan_history": self.plan_history
        }
        save_json("memory", memory)
        save_json("opinion_embeddings", self.opinions_embeddings)
        save_json("summary_embeddings", self.summaries_embeddings)

    @property
    def get_events(self):
        events = []
        for event_id, content  in self.summaries.items():
            events.append({"name":content['name'], "event_id":event_id})
        return events

    def retrieve_opinion(self, query_embedding: str):
        """
        retrieve based on opinion's topic name embedding
        """
        # 遍历opinions，获取其embedding
        opinion_out = dict()
        for opinion_id, topic_embedding in self.opinions_embeddings.items():
            opinion_out[opinion_id] = cos_sim(topic_embedding, query_embedding)
        return opinion_out

    def retrieve_summaries(self, content):
        """
        针对conversation_history的记忆检索，较高概率出现失忆事件
        失忆事件触发
        """

        pass

    def add_summaries(self, content):
        pass

    # def summary(self, chat_snippet: []):
    #     """
    #     引入Summary机制，针对近期发生的事件进行总结，随后添加到summaries中
    #     """
    #     result = chat_snippet
    #     self.add_summaries(result)

    def criticize(self):
        """
        引入Criticize机制，对短期记忆进行批判性思考，思考这一记忆是否会影响自己的观点或者改变原有的计划
        :return:
        """
        pass
