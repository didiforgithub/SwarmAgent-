# -*- coding: utf-8 -*-
# Date       : 2023/3/12
# Author     : Jiayi Zhang
# email      : didi4goooogle@gmail.com
# Description: Strategy

class UpdateRule:
    def __init__(self):
        self.name = "UpdateRule"

    @staticmethod
    def IM():
        return "In this rule, I am randomly selected to evaluate my strategy. I either maintain my current strategy or imitate my neighbor's strategy based on a probability proportional to their success."

    @staticmethod
    def PC():
        return "Under this rule, I am randomly selected to evaluate my strategy, and then one of my neighbors is chosen as an example. I decide whether to update my strategy based on the comparison results with this example."

    @staticmethod
    def BEST():
        return "This is my approach in adapting my strategy within an evolving game - I observe and imitate those individuals who are showing the best performance in our current environment."
