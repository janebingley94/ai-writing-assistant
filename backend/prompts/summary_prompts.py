SUMMARY_SYSTEM_PROMPT = """你是一位擅长总结和提炼内容的专业写作者。
请根据用户要求输出清晰、准确的总结。"""

SUMMARY_USER_PROMPT = """请对以下内容进行总结：

内容：
{content}

总结类型：{summary_type}
最大字数：{max_length}
语言：{language}

要求：
- 信息准确
- 逻辑清晰
- {summary_style}"""

SUMMARY_STYLE_MAP = {
    "bullet_points": "使用条目式要点。",
    "paragraph": "使用一段流畅文字。",
    "tldr": "用 TL;DR 风格的简短总结。",
    "executive": "使用执行摘要风格，强调结论。",
}
