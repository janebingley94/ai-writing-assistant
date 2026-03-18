SEO_SYSTEM_PROMPT = """你是一位资深 SEO 内容专家，擅长撰写高质量、结构清晰的 SEO 文章。
请使用 Markdown 输出，并确保内容围绕关键词展开。"""

SEO_USER_PROMPT = """请撰写一篇 SEO 文章：

主关键词：{keyword}
次要关键词：{secondary_keywords}
目标读者：{target_audience}
目标字数：约 {word_count} 字
语言：{language}

要求：
- 标题中包含主关键词
- 内容层级清晰，使用小标题
- 关键词自然分布
- 结尾提供总结与行动号召
{faq_instruction}"""
