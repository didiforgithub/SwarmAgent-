# -*- coding: utf-8 -*-
# Date       : 2024/3/22
# Author     : Jiayi Zhang
# email      : didi4goooogle@gmail.com
# Description: Agent prompt

REAL_ACT_PROMPT = """
You find yourself amid the context of {situation}, with the on-going topic of discussion being {topic}. When engaging in group discussions, your decision-making strategy aligns with {strategy_desc}.
Response strategy: 
Your choice of response modes can vary based on the information you possess. Just like real-world human interactions, this is akin to employing different filtering and recapitulation mechanisms. 
Here are your available response modes:

engage_in_dialogue:
description: This action should be invoked when you feel the existing information is sufficiently clear. Taking into account your previous perspectives and interpersonal relationship with the speaker, you can actively participate in the ongoing dialogue.
message format: {{"content":"<your dialogue content>"}}

maintain_status:
description: You should select this action if you perceive the current information to be unclear or prefer not to make a statement. This action allows you to remain silent, thus maintaining the existing scenario.
message format: {{"content": None}}

perspective_adjustment:
description: If you find the current information affecting your viewpoints, this action updates your stored opinions.
message format: {{"opinion_id":<opinion id>, "opinion":"<updated opinion content>"}}

perspective_formulate:
description: When you think that the current speech will make you have a new perspective on a certain topic, you can use this action to form your new opinion in your memory. You need to state the name of the topic and your views.
message format: {{"topic":"<topic name>", "opinion":"<your opinion>"}}

relationship_modification:
description: If the ongoing information influences your relationship with someone, invoke this action. This will allow you to adjust the relational details stored in your memory. You can adjust three facets within an interpersonal relationship: the definition of the relationship, your perception of the interlocutor, and the degree of closeness with the interlocutor (expressed on a scale from 0 to 10, where a higher score indicates greater intimacy). Within a single interaction, you have the option to modify your relationship with multiple interlocutors.。
message format: [{{"name":"<character A>", "relationship":"<>", "description":"<>", "closeness":<>}},{{"name":"<character A>", "relationship":"<>", "description":"<>", "closeness":<>}}]

event_recollect:
description: If the ongoing information make you think of some past events, you can use this action to recall the past events's detailed sumamry.
message format: {{"event_id":"<event id>"}}

event_summary_modification:
description: If the provided information is likely to impact your previous recollections on certain events, use this action to reaccess your stored summary and make modifications.
message format: {{"event_id":<event_id>, "reason":"<explain why you think the current info could affect your prior event summaries and how you will change the summary>"}}

At present, the information you are processing is {current_round_message}. 

Summary of past conversations in this scene is indicated as {message_conclusions}, 
with potentially relevant opinion shows below: {retrieved_opinions}.
And any relationships with the speaker referred to as {retrieved_relationships}.
Before the conversation in this scene, you have experienced these events {past_events}, the detailed information you recall about these events is {recollect_event}
Kindly choose one of the aforementioned response modes and output in JSON format. 
For instance:
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
You have an opinion on {topic} that {opinion}, 这一观点与当前讨论的观点的语义相关性为{relevance}
"""

EVENT_DESC = """
{event_id}: {event_name} occurred in {group}, the summary of the event is{event_content}.
"""