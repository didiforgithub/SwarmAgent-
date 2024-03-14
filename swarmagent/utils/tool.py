# -*- coding: utf-8 -*-
# Date       : 2023/3/12
# Author     : Jiayi Zhang
# email      : didi4goooogle@gmail.com
# Description: General Tools
from typing import List
from colorama import Fore
def human_display(history: List)->None:
    for speak in history:
        print(Fore.BLUE + speak)