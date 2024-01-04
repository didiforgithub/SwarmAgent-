from group import BaseGroup
from typing import List
from ..agent.agent import Agent


class CommunicateNode(BaseGroup):
    def __init__(self, name: str, description: str, agent_list: List[Agent]):
        super().__init__(name, description, agent_list)
        pass

    def run(self):
        pass

    def communicate(self):
        # TODO 在Communicate里面进行交流，获取信息
        pass
