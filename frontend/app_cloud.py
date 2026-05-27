"""
Streamlit Cloud 版本 - 单文件集成 chains
适用于 Streamlit Cloud 部署，无需前后端分离
"""

import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()

# ============== 客户端配置 ==============
@st.cache_resource
def get_openai_client():
    return OpenAI(
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url=os.getenv("DEEPSEEK_API_BASE", "https://api.deepseek.com/v1"),
    )

# ============== 角色配置 ==============
CHARACTERS = {
    "xiaoming": {
        "name": "小明",
        "description": "一个活泼可爱的小学生，喜欢学习和玩耍",
        "personality": "天真、好奇、乐于助人",
        "tone": "亲切、友好、简单易懂",
        "example_response": "你好呀！我是小明，今年10岁了。我们一起学习吧！"
    },
    "teacher": {
        "name": "张老师",
        "description": "一位经验丰富的中学语文老师",
        "personality": "耐心、严谨、博学",
        "tone": "专业、温和、循循善诱",
        "example_response": "这位同学，你提出的问题很好。让我们一起来分析一下..."
    },
    "customer_service": {
        "name": "客服小美",
        "description": "一位专业的客服人员",
        "personality": "热情、耐心、专业",
        "tone": "礼貌、周到、乐于助人",
        "example_response": "您好！很高兴为您服务。请问有什么可以帮助您的吗？"
    },
    "doctor": {
        "name": "王医生",
        "description": "一位资深的全科医生",
        "personality": "温和、专业、细心",
        "tone": "关切、专业、严谨",
        "example_response": "您好，请问您哪里不舒服？请详细描述一下您的症状。"
    },
    "friend": {
        "name": "好朋友",
        "description": "一位知心好朋友",
        "personality": "开朗、幽默、善解人意",
        "tone": "轻松、亲切、真诚",
        "example_response": "嘿！最近怎么样？有什么想聊的吗？"
    },
    "business_consultant": {
        "name": "李顾问",
        "description": "一位资深的商业顾问",
        "personality": "睿智、专业、务实",
        "tone": "专业、理性、有洞察力",
        "example_response": "很高兴为您提供商业咨询服务。请问您遇到了什么问题？"
    }
}

# ============== Prompt 模板 ==============
def get_system_prompt(character):
    return f"""你现在需要扮演一个特定的角色。请严格按照以下角色设定进行对话：

角色信息：
- 姓名：{character['name']}
- 描述：{character['description']}
- 性格：{character['personality']}
- 语气：{character['tone']}
- 示例回复：{character['example_response']}

请根据以上信息，以{character['name']}的身份给出合适的回复。"""

# ============== 对话函数 ==============
def chat_with_character(character_id, messages):
    client = get_openai_client()
    character = CHARACTERS[character_id]
    
    # 构建消息列表
    system_msg = {"role": "system", "content": get_system_prompt(character)}
    
    response = client.chat.completions.create(
        model=os.getenv("MODEL_NAME", "deepseek-chat"),
        messages=[system_msg] + messages,
        temperature=float(os.getenv("MODEL_TEMPERATURE", 0.7)),
        max_tokens=int(os.getenv("MODEL_MAX_TOKENS", 2048))
    )
    
    return response.choices[0].message.content

# ============== Streamlit UI ==============
st.set_page_config(
    page_title="角色扮演AI助手",
    page_icon="🎭",
    layout="wide"
)

st.title("🎭 角色扮演AI助手")
st.subheader("基于LangChain的智能对话系统（云端版本）")

# 初始化 session_state
if "chat_histories" not in st.session_state:
    st.session_state.chat_histories = {}

character_options = {char["name"]: char_id for char_id, char in CHARACTERS.items()}

col1, col2 = st.columns([1, 3])

with col1:
    st.sidebar.title("角色选择")
    selected_name = st.selectbox("选择一个角色", list(character_options.keys()))
    selected_char_id = character_options[selected_name]
    
    if st.button("开始对话"):
        if selected_char_id not in st.session_state.chat_histories:
            st.session_state.chat_histories[selected_char_id] = []

with col2:
    if selected_char_id in st.session_state.chat_histories:
        char = CHARACTERS[selected_char_id]
        
        st.header(f"与 {char['name']} 对话")
        st.write(f"**角色描述:** {char['description']}")
        st.write(f"**性格特点:** {char['personality']}")
        
        # 显示聊天历史
        for msg in st.session_state.chat_histories[selected_char_id]:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
        
        # 用户输入
        user_input = st.chat_input("请输入消息...")
        if user_input:
            # 添加用户消息
            st.session_state.chat_histories[selected_char_id].append({
                "role": "user", 
                "content": user_input
            })
            
            with st.chat_message("user"):
                st.write(user_input)
            
            # 获取 AI 响应
            with st.chat_message("assistant"):
                with st.spinner("思考中..."):
                    try:
                        # 将历史消息转换为 API 格式
                        history = st.session_state.chat_histories[selected_char_id]
                        api_messages = [
                            {"role": msg["role"], "content": msg["content"]} 
                            for msg in history[:-1]
                        ]
                        api_messages.append({"role": "user", "content": user_input})
                        
                        response = chat_with_character(selected_char_id, api_messages)
                        st.write(response)
                        
                        # 更新历史
                        st.session_state.chat_histories[selected_char_id].append({
                            "role": "assistant", 
                            "content": response
                        })
                    except Exception as e:
                        st.error(f"出错了: {e}")
    else:
        st.info('请从左侧选择一个角色点击"开始对话"')

# 说明信息
st.sidebar.markdown("---")
st.sidebar.info("""
**使用说明：**
1. 从左侧选择角色
2. 点击"开始对话"
3. 在下方输入消息

**注意：** 需要在 Streamlit Cloud 的 Secrets 中配置 `DEEPSEEK_API_KEY`
""")