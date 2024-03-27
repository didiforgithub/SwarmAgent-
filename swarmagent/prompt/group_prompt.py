# -*- coding: utf-8 -*-
# Date       : 2024/3/26
# Author     : Jiayi Zhang
# email      : didi4goooogle@gmail.com
# Description: Group Prompt

CONCLUSION_PROMPT = """
In the given context {situation}, the participants {members} are engaged in a discussion around the subject {topic}. 
The ongoing discussion's transcript is noted as {current_chat}, while the summaries of previous discussions are recorded as {conclusions_past}.
Your task is to provide a concise and comprehensive summary of the crucial details that have transpired in the current conversation. 
This may include mentioning the key points of agreement or disagreement among the participants, or denoting any crucial information that emerged during the dialog.
While summarizing, do not include personal opinions - retain a focus on the facts presented during the discussion.
Please supply your summary in python readable JSON format as illustrated:{{"conclusion":"<content>"}}
"""
