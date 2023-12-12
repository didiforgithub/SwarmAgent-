# -*- coding: utf-8 -*-
# Date       : 2023/12/12
# Author     : Jiayi Zhang
# email      : didi4goooogle@gmail.com
# Description: Agent's Scratch/Profile architecture

class Profile:

    def __init__(self, name):
        """
        比较重要的一点，我们需要在这里进行抽象，思考Agent应该具有哪些必要的属性
        1. name
        2. power
        3. character
        4. opinion, {event: sth, opinion: sth}
        5. relation, {target: sb, opinion: sth}
        6. ?
        7. ...
        """
        pass

    def load(self):
        pass

    def save(self):
        pass

    def generation(self):
        """
        自动生成模块，这是美好幻想
        :return:
        """
        pass
