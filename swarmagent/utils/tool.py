# -*- coding: utf-8 -*-
# Date       : 2023/3/12
# Author     : Jiayi Zhang
# email      : didi4goooogle@gmail.com
# Description: General Tools
import re
from typing import List
from colorama import Fore

def human_display(history: List)->None:
    for speak in history:
        print(Fore.BLUE + speak)

def round_chat_parse(round_chat_history):
    speakers = []
    content = ""
    for i in round_chat_history:
        speaker = re.split("::", i)[0]
        speakers.append(speaker)
        content += f"{speaker}:{re.split("::", i)[1]}"
        
    return speakers, content