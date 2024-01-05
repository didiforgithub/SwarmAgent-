from group import BaseGroup
from typing import List
from ..agent.agent import Agent


class DiscussionGroup(BaseGroup):
    def __init__(self, name: str, description: str, agent_list: List[Agent]):
        super().__init__(name, description, agent_list)
        self.core_agent = None
        pass

    def run(self):
        # 获取 publish message 信息，由 core_agent 主导进行什么讨论或者要不要换掉 core_agent
        pass

    def consensus(self):
        # TODO 生成共识
        return "hello world"
