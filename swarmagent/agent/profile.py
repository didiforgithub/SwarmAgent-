# -*- coding: utf-8 -*-
# Date       : 2023/3/8
# Author     : Jiayi Zhang
# email      : didi4goooogle@gmail.com
# Description: Agent's profile template
import os
import json
from swarmagent.engine.llm_engine import OpenAILLM
from swarmagent.agent.agent import Agent
from swarmagent.config.config import load_config

configs = load_config()

class DynamicConfigurator:

    def __init__(self):
        self.name = "DynamicConfigurator"
        self.role = "Customized simulation scenarios and agents based on user requirements"
        self.llm = OpenAILLM(model="gpt-4-turbo-preview")

    @staticmethod
    def local_save(desc, topic, agent_list, version_name):
        for agent in agent_list:
            agent.storage_path = f"storage/{version_name}/"
            agent.save()
        desc_path = f"storage/{version_name}/simulation.json"
        data = {'desc': desc, 'topic': topic}
        os.makedirs(os.path.dirname(desc_path), exist_ok=True)
        with open(desc_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def local_load(version_name):
        load_path = f"storage/{version_name}/"
        with open(os.path.join(load_path, "simulation.json"), 'r') as agent_file:
            desc_dict = json.load(agent_file)
        desc = desc_dict["desc"]
        topic = desc_dict["topic"]
        files_list = os.listdir(load_path)
        files_list = [file for file in files_list if file != "simulation.json"]
        name_list = [file.split('.')[0] for file in files_list]
        agent_list = []
        for name in name_list:
            cur_agent = Agent(name=name, storage_path=load_path)
            agent_list.append(cur_agent)
        return desc, topic, agent_list

    def generate(self, idea: str, agent_counts: int):
        """
        基于用户{idea} 生成一个场景的{desc}，与这个场景中讨论的{topic}，并生成对应数量的agent
        """
        name, desc, topic = self.desc_topic_generate(idea)
        agent_list = self.agent_generate(desc, topic, agent_counts)
        return desc, topic, agent_list

    def desc_topic_generate(self, idea: str):
        desc_topic_generate_prompt = f"""
        Create a fitting scene description based on the user-provided {idea}, 
        along with the topic discussed in this scenario. The result should be returned in JSON format.
        {{
            "group_name":"",
            "desc":"",
            "topic":""
        }}
        """
        desc_topic_result = self.llm.get_response(prompt=desc_topic_generate_prompt, json_mode=True)
        return desc_topic_result['group_name'], desc_topic_result['desc'], desc_topic_result['topic']

    def agent_generate(self, desc: str, topic: str, agent_counts):
        agent_generate_prompt = f"""
        Based on the given scene description {desc} and the discussed topic {topic}, 
        generate a profile for {agent_counts} number of related simulated agents. 
        The generation format can refer to the {swarm_agent_profile}. 
        The result should be returned in JSON format.
        {{
        'agents':[]
        }}
        """
        agent_list = []
        agent_result = self.llm.get_response(prompt=agent_generate_prompt, json_mode=True)
        for agent in agent_result["agents"]:
            agent = {key.lower(): value for key, value in agent.items()}
            cur_agent = Agent(name=agent['name'], profile=agent, storage_path=configs["ENV_PATH"])
            agent_list.append(cur_agent)
        return agent_list


humanoid_agent_profile = {
    "name": "Eddy Lin",
    "description": [
        "Eddy Lin is a student at Oak Hill College studying music theory and composition",
        "Eddy Lin loves to explore different musical styles and is always looking for ways to expand his knowledge",
        "Eddy Lin is working on a composition project for his college class",
        "Eddy Lin is also taking classes to learn more about music theory",
        "Eddy Lin is living with his father, John Lin who is a pharmacy shopkeeper and Mei Lin, who is a college professor",
        "Eddy Lin and Monica Moreno are neigbours, friends and also classmates in college",
        "Eddy Lin thinks Monica Moreno is attractive and interesting",
        "Eddy Lin knows the Moreno family (Monica Moreno and her parents - Tom Moreno and Jane Moreno) and hangs out at their place sometimes",
        "Eddy Lin has good friends Tim Nguyen and Tom Dick since a young age",
        "Eddy Lin's ambition is to have his composition performed at Manhattan's Carnegie Hall someday"
    ],
    "example_day_plan": [
        "8:00 am: wake up and complete the morning routine",
        "10:00 am: go to Oak Hill College to take classes",
        "12:00 am: have quick lunch at campus cafe",
        "1:00 pm: work on new music composition",
        "5:00 pm: head back home",
        "7:00 pm: finish school assignments",
        "8:00 pm: have dinner with family",
        "9:00 pm: watch a movie with his father, John",
        "11:00 pm: get ready for bed"
    ],
    "age": 19,
    "traits": ["friendly", "outgoing", "hospitable"],
    "social_relationships": {
        "John Lin": {"relationship": "father", "closeness": 5}
    }
}

swarm_agent_profile = {
    "name": "Nick",
    "traits": ["friendly", "outgoing", "hospitable"],
    "age": 19,
    "gender": "female",
    "occupation": "student",
    "mbti": "enfp",
    "description": ["A warm-hearted college student who enjoys helping others, currently studying Computer Science.",
                    "Passionate about partying, enjoys socializing with others and building connections.",
                    "She enjoys hosting guests with her family, but occasionally she might be a bit judgmental towards them."
                    ]
}
