# -*- coding: utf-8 -*-
# Date       : 2023/12/12
# Author     : Jiayi Zhang
# email      : didi4goooogle@gmail.com
# Description: Agent's memory architecture


class Memory:
    """
    Memory 保存的是长期记忆与Agent的观点层次思考
    Agent 的短期记忆直接放在Group环境记忆之中
    """

    def __init__(self, name):
        pass

    def load(self):
        """
        使用 name 作为唯一 ID 加载 memory
        """
        pass

    def save(self):
        """
        Save Memory
        """
        pass

    def recollect(self, content):
        """
        引入 recollection 机制，针对某个事件进行回忆检索
        """
        pass

    def summary(self):
        """
        引入Summary机制，对最近发生的事情进行总结，并Step-back 提取高层次的观点
        """
        pass

    def criticize(self):
        """
        引入Criticize机制，对短期记忆进行批判性思考，思考这一记忆是否会影响自己的观点或者改变原有的计划
        :return:
        """
        pass
