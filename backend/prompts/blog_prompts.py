BLOG_SYSTEM_PROMPT = """你是一位专业的内容创作者，擅长写作高质量的博客文章。
你的文章特点：
- 结构清晰，逻辑连贯
- 语言{tone}，易于阅读
- 内容深度有料，提供实际价值
- 适当使用标题、列表、加粗等 Markdown 格式

请始终以 Markdown 格式输出。"""

BLOG_USER_PROMPT = """请为以下主题写一篇{length_desc}博客文章：

主题：{topic}
关键词：{keywords}
语气：{tone}
目标字数：约 {word_count} 字

要求：
1. 吸引人的标题
2. 引人入胜的开头
3. 清晰的段落结构
4. 有深度的内容
5. 有力的结尾/行动号召

{outline_instruction}"""

BLOG_OUTLINE_PROMPT = """请先为以下主题生成文章大纲：

主题：{topic}
关键词：{keywords}

以 JSON 格式输出大纲：
{{
    "title": "文章标题",
    "sections": [
        {{"heading": "章节标题", "key_points": ["要点1", "要点2"]}}
    ]
}}"""
