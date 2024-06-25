# -*- coding: utf-8 -*-
# Date       : 2024/3/26
# Author     : Jiayi Zhang
# email      : didi4goooogle@gmail.com
# Description: Group Prompt

CONCLUSION_PROMPT = """
在特定的情境 {situation} 中，参与人员 {members} 正就话题 {topic} 进行深入讨论。 
目前的讨论内容被记录为 {current_chat}，而过去的讨论摘要则被记为 {conclusions_past}。 
你的工作是提炼出当前对话中的关键信息，并做出简洁而全面的总结。 
这包括记录参与者间的主要共识或分歧点，或是对话中出现的任何重要信息。 
在进行总结时，不要附上私人看法，只关注讨论中出现的事实。 
请按照以下示例的 Python 可读的 JSON 格式来提供你的总结：{{"conclusion":"<内容>"}}。
"""

GROUP_IN_ENV_IDEA_PROMPT = """
在场景：{situation}之中，这些成员:{members}即将开始新一轮的讨论，你需要依据环境中的最新消息以及群体过去讨论的总结，来为这次讨论产出话题。
环境中其他群体的消息为{messages}，群体过去的讨论记录为{group_memory}。
请你综合考虑其他群体的消息对你们群体的影响，并基于之前的讨论结果，生成本次讨论的话题。
请按照以下示例的 Python 可读的 JSON 格式来提供你的话题：{{"topic":"<话题>"}}。
"""