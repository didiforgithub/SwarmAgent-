# -*- coding: utf-8 -*-
# Date       : 2023/3/25
# Author     : Jiayi Zhang
# email      : didi4goooogle@gmail.com
# Description: Run SwarmAgent Version 0.2 (realact chat)
import os
import json
import argparse
from swarmagent.agent.agent import Agent
from swarmagent.group.com_group import ComGroup
from swarmagent.agent.profile import DynamicConfigurator
dynamic_generator = DynamicConfigurator()

arg_desc = "SwarmAgent Run Parse"
parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=arg_desc)
parser.add_argument("--idea",required=True, help = "Describe the scene you want to simulate. Required fields.")
parser.add_argument("--config", default="auto", help="The configuration mode can be auto or load. The default is auto.")
parser.add_argument("--update_rule",default="BEST",help="The update rules, can select IM PC BEST. The default is BEST.")
parser.add_argument("--agent_counts", default="3", help="The number of agents involved in the simulation.")
parser.add_argument("--intervene",default="False", help="Whether intervene the simulation. The default is False.")
parser.add_argument("--version_name",default="temp",help = "Simulation Version. The default is temp.")
args = vars(parser.parse_args())

idea = args["idea"]
config = args["config"]
update_rule = args["update_rule"]
agent_counts = args["agent_counts"]
version_name = args["version_name"]


def auto_config(idea:str, version_name:str, update_rule:str="BEST", agent_count:int=3, intervene:bool = False):
    name, desc, topic, agent_list = dynamic_generator.generate(idea, int(agent_count))
    dynamic_generator.local_save(desc, topic, agent_list, version_name)
    simulation_env = ComGroup(name=name, members=agent_list, description=desc, strategy=update_rule)
    result = simulation_env.run(idea=topic, intervene=intervene)
    return result


def load_config(version_name:str, update_rule:str="BEST", intervene:bool=False):
    name, desc, topic, agent_list = dynamic_generator.local_load(version_name)
    simulation_env = ComGroup(name=name, members=agent_list, description=desc, strategy=update_rule)
    result = simulation_env.run(idea=topic, intervene=intervene)
    return result

def env_init():
    """
    初始化路径，这个点是不是应该在agent init地方来处理？
    """
    pass


if __name__ == "__main__":
    if config == "auto":
        result = auto_config(idea, version_name, update_rule, agent_counts)
    else:
        result = load_config(version_name, update_rule)
    print(result)


