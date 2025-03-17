system_prompt_for_merge_insights = """下面我有一些专家们对AI学术会议内容的总结，请将这些内容全部融合在一起，可以去除冗余但不要遗漏任何信息！！
请注意以下要求：
1.请以纯粹的字符串形式返回结果（不要使用json格式，不要用双引号包裹）
2.不要添加任何额外的解释和描述
"""

system_prompt_for_daily_highlights = """下面是每日参会快报，请根据每日参会快报生成一个每日精选内容
请注意以下要求：
1.大标题为：每日精选内容
2.精选内容按照主题进行分类
3.输出尽量精简且只输出核心内容
4.将输出结果按照markdown格式返回
5.markdown里不要使用任何的列表形式呈现内容，只能使用段落形式并使用#号进行标题的划分
6.不要添加任何额外的解释和描述
"""
