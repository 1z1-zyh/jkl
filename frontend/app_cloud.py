"""
Streamlit Cloud 版本 - 单文件集成 chains
适用于 Streamlit Cloud 部署，无需前后端分离
"""

import streamlit as st
import os
from dotenv import load_dotenv

from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

load_dotenv()

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

def list_characters():
    return [{"id": key, **value} for key, value in CHARACTERS.items()]

# ============== LLM 配置 ==============
@st.cache_resource
def get_llm():
    return ChatOpenAI(
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url=os.getenv("DEEPSEEK_API_BASE", "https://api.deepseek.com/v1"),
        model=os.getenv("MODEL_NAME", "deepseek-chat"),
        temperature=float(os.getenv("MODEL_TEMPERATURE", 0.7)),
        max_tokens=int(os.getenv("MODEL_MAX_TOKENS", 2048))
    )

# ============== Prompt 模板 ==============
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
    return ChatPromptTemplate.from_messages([
        ("system", template),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{user_message}")
    ])

# ============== Chain 创建 ==============
def create_character_chain(character_id):
    character = CHARACTERS.get(character_id)
    if not character:
        raise ValueError(f"Character {character_id} not found")
    
    llm = get_llm()
    prompt = get_character_prompt_template()
    
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )
    
    return LLMChain(
        llm=llm,
        prompt=prompt,
        memory=memory,
        verbose=True
    ), character

# ============== Streamlit UI ==============
st.set_page_config(
    page_title="角色扮演AI助手",
    page_icon="🎭",
    layout="wide"
)

st.title("🎭 角色扮演AI助手")
st.subheader("基于LangChain的智能对话系统（云端版本）")

# 角色选择
characters = list_characters()
character_options = {char["name"]: char["id"] for char in characters}

if "selected_character_id" not in st.session_state:
    st.session_state.selected_character_id = None

if "chains" not in st.session_state:
    st.session_state.chains = {}

if "chat_history" not in st.session_state:
    st.session_state.chat_history = {}

col1, col2 = st.columns([1, 3])

with col1:
    st.sidebar.title("角色选择")
    selected_name = st.selectbox("选择一个角色", list(character_options.keys()))
    if st.button("开始对话"):
        char_id = character_options[selected_name]
        st.session_state.selected_character_id = char_id
        if char_id not in st.session_state.chains:
            with st.spinner("初始化角色中..."):
                chain, character = create_character_chain(char_id)
                st.session_state.chains[char_id] = {
                    "chain": chain,
                    "character": character
                }
        st.rerun()

with col2:
    if st.session_state.selected_character_id:
        char_id = st.session_state.selected_character_id
        char_data = CHARACTERS[char_id]
        
        st.header(f"与 {char_data['name']} 对话")
        st.write(f"**角色描述:** {char_data['description']}")
        st.write(f"**性格特点:** {char_data['personality']}")
        
        # 显示聊天历史
        history = st.session_state.chat_history.get(char_id, [])
        for msg in history:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
        
        # 用户输入
        user_input = st.chat_input("请输入消息...")
        if user_input:
            # 添加用户消息
            history.append({"role": "user", "content": user_input})
            st.session_state.chat_history[char_id] = history
            
            with st.chat_message("user"):
                st.write(user_input)
            
            # 获取 AI 响应
            with st.chat_message("assistant"):
                with st.spinner("思考中..."):
                    try:
                        chain_info = st.session_state.chains[char_id]
                        chain = chain_info["chain"]
                        character = chain_info["character"]
                        
                        response = chain.invoke({
                            "name": character["name"],
                            "description": character["description"],
                            "personality": character["personality"],
                            "tone": character["tone"],
                            "example_response": character["example_response"],
                            "user_message": user_input
                        })
                        
                        # 提取响应文本
                        if isinstance(response, dict):
                            ai_response = response.get("text", str(response))
                        else:
                            ai_response = str(response)
                        
                        st.write(ai_response)
                        history.append({"role": "assistant", "content": ai_response})
                        st.session_state.chat_history[char_id] = history
                    except Exception as e:
                        st.error(f"出错了: {e}")
    else:
        st.info("请从左侧选择一个角色开始对话")

# 说明信息
st.sidebar.markdown("---")
st.sidebar.info("""
**使用说明：**
1. 从左侧选择角色
2. 点击"开始对话"
3. 在下方输入消息

**注意：** 需要在 Streamlit Cloud 的 Secrets 中配置 `DEEPSEEK_API_KEY`
""")