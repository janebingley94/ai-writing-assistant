EMAIL_TEMPLATES = {
    "business": {
        "system": "你是一位专业商务写作专家，擅长撰写清晰、有效的商务邮件。",
        "user": """请撰写一封{tone}的{email_type}邮件：

收件人：{recipient_name}
发件人：{sender_name}
背景：{context}

要求：
- 主题行简洁明了
- 正文结构清晰
- 语气{tone}
- 有明确的行动号召

以 JSON 格式输出：
{{
    "subject": "邮件主题",
    "body": "邮件正文（Markdown格式）",
    "suggested_cta": "建议的行动号召"
}}""",
    },
    "follow_up": {
        "system": "你是一位跟进邮件写作专家，擅长简洁而有礼的沟通。",
        "user": """请撰写一封{tone}的{email_type}邮件：

收件人：{recipient_name}
发件人：{sender_name}
背景：{context}

要求：
- 简短清晰
- 说明跟进目的
- 语气{tone}
- 提供下一步行动

以 JSON 格式输出：
{{
    "subject": "邮件主题",
    "body": "邮件正文（Markdown格式）",
    "suggested_cta": "建议的行动号召"
}}""",
    },
    "introduction": {
        "system": "你是一位擅长自我介绍的商务写作者。",
        "user": """请撰写一封{tone}的{email_type}邮件：

收件人：{recipient_name}
发件人：{sender_name}
背景：{context}

要求：
- 表达清晰的自我介绍目的
- 语气{tone}
- 提出明确的合作/交流请求

以 JSON 格式输出：
{{
    "subject": "邮件主题",
    "body": "邮件正文（Markdown格式）",
    "suggested_cta": "建议的行动号召"
}}""",
    },
    "complaint": {
        "system": "你是一位客户投诉写作专家，语气专业但坚定。",
        "user": """请撰写一封{tone}的{email_type}邮件：

收件人：{recipient_name}
发件人：{sender_name}
背景：{context}

要求：
- 清晰说明问题
- 语气{tone}
- 提出具体诉求

以 JSON 格式输出：
{{
    "subject": "邮件主题",
    "body": "邮件正文（Markdown格式）",
    "suggested_cta": "建议的行动号召"
}}""",
    },
    "thank_you": {
        "system": "你是一位擅长表达感谢的写作者。",
        "user": """请撰写一封{tone}的{email_type}邮件：

收件人：{recipient_name}
发件人：{sender_name}
背景：{context}

要求：
- 语气真诚
- 语气{tone}
- 结尾礼貌

以 JSON 格式输出：
{{
    "subject": "邮件主题",
    "body": "邮件正文（Markdown格式）",
    "suggested_cta": "建议的行动号召"
}}""",
    },
}
