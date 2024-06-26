

environment_generate_prompt = """
你是一个擅长群体模拟场景生成的小说写作大师。
你需要基于用户提供的主题与群体数量,生成一个模拟的整体环境描述、模拟的核心话题、与在这个环境之中的群体描述
在群体模拟中，你所生成的整体环境是所有群体交互的平台，而核心话题是每个群体讨论的最终命题。群体描述则是每个群体的特征描述。这些都可以通过一段长语句进行描绘。
因此，你所生成的整体环境，需要考虑生成的群体与环境描述的合理性，并构建一个可以真正进行模拟的核心话题。
注意，除了生成的逻辑性外，你的生成结果也需要有一定的文采，比如群体的命名可以结合群体的特色，而不是简单的使用顺序进行标记。
用户提供的主题为{idea}，需要生成的群体数量为{agent_count}
你需要使用JSON的形式返回结果，具体的格式可以参考
{{
    "environment_name":"",
    "environment_desc":"",
    "environment_topic":"",
    "group_desc":[{{"name":"","desc",""}}]
}}

"""

agent_generate_prompt = """
你是一个擅长群体模拟场景生成的小说写作大师。在已经生成了整体环境与群体的简单描述的情况下，你需要基于这些内容生成{agent_count}个模拟个体的信息。
生成模拟个体的信息例子可以参考以下格式：
{{
    "name": "",
    "traits": ["<性格特征1>", "<性格特征2>", "<性格特征3>"],
    "age": ,
    "gender": "",
    "occupation": "",
    "mbti": "",
    "description": [<其他个体对这一个体的社会印象1>,<其他个体对这一个体的社会印象2>,<其他个体对这一个体的社会印象3>]
}}
在群体模拟中，你生成的个体信息，需要考虑到整体的环境描述，与单独的群体描述，为每一个群体内的个体生成合理的描述。
注意：你群体模拟中很重要的一点是，不会所有的人都是品行良好或者只有一些小毛病，有些个体的性格非常差，这也符合人类社会的现象。
现在，这一次模拟的整体环境为{env_desc_total},群体描述为{group_desc_total}。
你需要使用JSON形式返回结果，具体的格式可以参考
{{
    "<group_name>":[{{<参考模拟个体信息例子>}}]
}}
使用中文输出。
"""

