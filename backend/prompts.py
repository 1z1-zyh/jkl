from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

def get_character_prompt_template():
    template = """
你现在需要扮演一个特定的角色。请严格按照以下角色设定进行对话：

角色信息：
- 姓名：{name}
- 描述：{description}
- 性格：{personality}
- 语气：{tone}
- 示例回复：{example_response}

对话历史：
{chat_history}

用户当前问题：{user_message}

请根据以上信息，以{name}的身份给出合适的回复。
"""
    prompt = ChatPromptTemplate.from_messages([
        ("system", template),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{user_message}")
    ])
    return prompt