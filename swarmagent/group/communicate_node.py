from .group import BaseGroup
from typing import List
from ..agent.agent import Agent


class CommunicateNode(BaseGroup):
    def __init__(self, name: str, agent_list: List[Agent], storage_path: str, description: str = '',
                 curr_agent: List[Agent] = []):
        super().__init__(group_name=name, agent_list=agent_list, description=description, storage_path=storage_path,
                         curr_agents=curr_agent)
        pass

    def run(self):
        pass

    def load(self):
        pass

    def save(self):
        pass

    def communicate(self):
        # TODO 在Communicate里面进行交流，获取信息
        pass
