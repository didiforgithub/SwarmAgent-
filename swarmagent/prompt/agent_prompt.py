# -*- coding: utf-8 -*-
# Date       : 2024/3/22
# Author     : Jiayi Zhang
# email      : didi4goooogle@gmail.com
# Description: Agent prompt

# REAL_ACT_PROMPT = """
# You find yourself amid the context of {situation}, with the on-going topic of discussion being {topic}. When engaging in group discussions, your decision-making strategy aligns with {strategy_desc}.
# Response strategy: 
# Your choice of response modes can vary based on the information you possess. Just like real-world human interactions, this is akin to employing different filtering and recapitulation mechanisms. 
# Here are your available response modes:

# engage_in_dialogue:
# description: This action should be invoked when you feel the existing information is sufficiently clear. Taking into account your previous perspectives and interpersonal relationship with the speaker, you can actively participate in the ongoing dialogue.
# message format: {{"content":"<your dialogue content>"}}

# maintain_status:
# description: You should select this action if you perceive the current information to be unclear or prefer not to make a statement. This action allows you to remain silent, thus maintaining the existing scenario.
# message format: {{"content": None}}

# perspective_adjustment:
# description: If you find the current information affecting your viewpoints, this action updates your stored opinions.
# message format: {{"opinion_id":<opinion id>, "opinion":"<updated opinion content>"}}

# perspective_formulate:
# description: When you think that the current speech will make you have a new perspective on a certain topic, you can use this action to form your new opinion in your memory. You need to state the name of the topic and your views.
# message format: {{"topic":"<topic name>", "opinion":"<your opinion>"}}

# relationship_modification:
# description: If the ongoing information influences your relationship with someone, invoke this action. This will allow you to adjust the relational details stored in your memory. You can adjust three facets within an interpersonal relationship: the definition of the relationship, your perception of the interlocutor, and the degree of closeness with the interlocutor (expressed on a scale from 0 to 10, where a higher score indicates greater intimacy). Within a single interaction, you have the option to modify your relationship with multiple interlocutors.。
# message format: [{{"name":"<character A>", "relationship":"<>", "description":"<>", "closeness":<>}},{{"name":"<character A>", "relationship":"<>", "description":"<>", "closeness":<>}}]

# event_recollect:
# description: If the ongoing information make you think of some past events, you can use this action to recall the past events's detailed sumamry.
# message format: {{"event_id":"<event id>"}}

# event_summary_modification:
# description: If the provided information is likely to impact your previous recollections on certain events, use this action to reaccess your stored summary and make modifications.
# message format: {{"event_id":<event_id>, "reason":"<explain why you think the current info could affect your prior event summaries and how you will change the summary>"}}

# At present, the information you are processing is {current_round_message}. 

# Summary of past conversations in this scene is indicated as {message_conclusions}, 
# with potentially relevant opinion shows below: {retrieved_opinions}.
# And any relationships with the speaker referred to as {retrieved_relationships}.
# Before the conversation in this scene, you have experienced these events {past_events}, the detailed information you recall about these events is {recollect_event}
# Kindly choose one of the aforementioned response modes and output in JSON format. 
# For instance:
# {{
#     "function":"<desired action>",
#     "message":"<based on action's message format>"
# }}
# """

REAL_ACT_PROMPT = """
你发现自己处于{situation}的情境中，你目前归属的群体是{group}。在这个群体中，当前讨论的主题是{topic}。在参与群组讨论时，你的决策策略与{strategy_desc}保持一致。

响应策略：
你可以根据所掌握的信息选择不同的响应方式。就像现实世界中的人际互动一样，这类似于采用不同的过滤和概括机制。
以下是你可以使用的响应方式：

engage_in_dialogue:
描述：当你认为现有信息足够清晰时，应该调用这个动作。考虑到你之前的观点和与发言者之间的人际关系，你可以积极参与正在进行的对话。请你注意，你的对话应该有效的与上一轮对话中的其他人产生交互，而不能自说自话。
消息格式：{{"content":"<你的对话内容>"}}

maintain_status:
描述：如果你认为当前信息不清晰或不愿意发表声明，应选择这个动作。这个动作可以让你保持沉默，从而维持现有的场景。
消息格式：{{"content": None}}

perspective_adjustment:
描述：如果你发现当前信息影响了你的观点，这个动作会更新你存储的意见。
消息格式：{{"opinion_id"：<意见id>, "opinion":"<更新的意见内容>"}}

perspective_formulate:
描述：当你认为当前的发言会让你对某个话题产生新的看法时，你可以使用这个动作来在你的记忆中形成你的新意见。你需要陈述话题的名称和你的观点。
消息格式：{{"topic":"<话题名称>", "opinion":"<你的意见>"}}

relationship_modification:
描述：如果正在进行的信息影响了你与某人的关系，调用这个动作。这将允许你调整存储在记忆中的关系细节。你可以在一个人际关系中调整三个方面：关系的定义、你对对话者的看法以及与对话者的亲密程度（以0到10的尺度表示，分数越高表示越亲密）。在一次互动中，你可以选择修改与多个对话者的关系。
消息格式：[{{"name":"<角色A>", "relationship":"<>", "description":"<>", "closeness":<>}},{{"name":"<角色A>", "relationship":"<>", "description":"<>", "closeness":<>}}]

event_recollect:
描述：如果正在进行的信息让你想起一些过去的事件，你可以使用这个动作来回忆过去事件的详细摘要。
消息格式：{{"event_id":"<事件id>"}}

event_summary_modification:
描述：如果提供的信息可能会影响你对某些事件之前的回顾，使用这个动作重新访问你存储的摘要并进行修改。
消息格式：{{"event_id"：<事件id>, "reason":"<解释为什么你认为当前信息可能会影响你之前的事件摘要，以及你将如何改变摘要>"}}



此场景中过往对话的总结表示为{message_conclusions}。
目前，上一轮聊天记录是{current_round_message}，请记住，在一个对话场景中，你需要做的是基于你的一切逻辑，去与其他人产生交互，所以上一轮聊天记录这一个要素至关重要。
下面展示了可能相关的意见：{retrieved_opinions}。
与发言者的关系被称为{retrieved_relationships}。
在这场对话之前，你经历了这些事件{past_events}，你对这些事件回忆的详细信息是{recollect_event}。
请从上述响应方式中选择一种，并以JSON格式输出。
例如:
{{
    "function":"<desired action>",
    "message":"<based on action's message format>"
}}
"""


EVENT_CONCLUSION_PROMPT = """
Summarize the events occurring within the {group} from your perspective, relating to the opinion of {retrieved_opinion}. 
The dialogue during these events is summarized as {message_conclusion}. 
Please frame your conclusion on this event and devise a title, along with a summary context. Return these contents in JSON format:
{{
    "name":<event name>,
    "content":<summary context>
}}
"""

RELATION_DESC = """
Your relationship with {name} is {relationship}. Your impression of him is {desc}. Your closeness to him is {closeness}
"""

OPINION_DESC = """
你对'{topic}'的观点为'{opinion}'。这一观点与当前讨论的观点的语义相关性为{relevance}，这一主题在你记忆中的id为{id}
"""

EVENT_DESC = """
{event_id}: {event_name} occurred in {group}, the summary of the event is{event_content}.
"""