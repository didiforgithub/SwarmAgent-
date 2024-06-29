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
from swarmagent.prompt.generate_prompt import environment_generate_prompt, agent_generate_prompt

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
    
    def env_generate(self, idea: str, agent_counts, group_count):
        """
        
        """
        env_name, env_desc, env_topic, group_list = self.env_desc_generate(idea, group_count)
        env_total_desc = f"环境名称：{env_name}。环境描述：{env_desc}。环境的主要话题：{env_topic}。"
        group_desc_total = f"群体信息："
        for group in group_list:
            group_desc_total += f"{group['group_name']}：{group['desc']}。"
        group_agent_dict = self.env_agent_generate(agent_counts, env_total_desc, group_desc_total)
        # TODO 这里需要完成智能体的人际关系检查，从而完成智能体的社交关系检查
        # TODO 思考环境生成，是否要固定一下环境中必须的资源，比如说食物，水，空气等等/这个是可以由Generator生成的
        # TODO 这里先不管智能体的人际关系生成了
        
        pass

    def env_desc_generate(self, idea:str, group_count:int):
        """
        生成环境名称，描述，话题，以及初始Group的描述
        """
        result = self.llm.get_response(prompt=environment_generate_prompt.format(idea=idea, agent_count=group_count), json_mode=True)
        return result["environment_name"], result["environment_desc"], result["environment_topic"], result["group_desc"]
    
    def env_agent_generate(self, agent_count:int, env_desc_total:str, group_desc_total:str):
        result = self.llm.get_response(prompt=agent_generate_prompt.format(agent_count=agent_count, env_desc_total=env_desc_total, group_desc_total=group_desc_total), json_mode=True)
        return result
    
    def group_generate(self, idea: str, agent_counts: int):
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
