from group import BaseGroup
from typing import List
from ..agent.agent import Agent


class DiscussionGroup(BaseGroup):
    def __init__(self, name: str, description: str, agent_list: List[Agent]):
        super().__init__(name, description, agent_list)
        pass

    def run(self):
        pass
