import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

def get_characters():
    try:
        response = requests.get(f"{API_BASE_URL}/api/characters")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"获取角色列表失败: {e}")
        return []

def chat_with_character(character_id, message):
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/chat/{character_id}",
            params={"user_message": message}
        )
        response.raise_for_status()
        result = response.json()
        return result.get("response", "")
    except Exception as e:
        st.error(f"发送消息失败: {e}")
        return ""

def main():
    st.set_page_config(
        page_title="角色扮演AI助手",
        page_icon="🎭",
        layout="wide"
    )
    
    st.title("🎭 角色扮演AI助手")
    st.subheader("基于LangChain的智能对话系统")
    
    if "characters" not in st.session_state:
        st.session_state.characters = get_characters()
    
    if "selected_character" not in st.session_state:
        st.session_state.selected_character = None
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.sidebar.title("角色选择")
        if st.session_state.characters:
            for char in st.session_state.characters:
                if st.button(char["name"], key=char["id"]):
                    st.session_state.selected_character = char
                    st.session_state.chat_history = []
        else:
            st.write("正在加载角色列表...")
    
    with col2:
        if st.session_state.selected_character:
            char = st.session_state.selected_character
            st.header(f"与 {char['name']} 对话")
            st.write(f"**角色描述:** {char['description']}")
            st.write(f"**性格特点:** {char['personality']}")
            
            for message in st.session_state.chat_history:
                with st.chat_message(message["role"]):
                    st.write(message["content"])
            
            user_input = st.chat_input("请输入消息...")
            if user_input:
                st.session_state.chat_history.append({
                    "role": "user",
                    "content": user_input
                })
                
                with st.chat_message("user"):
                    st.write(user_input)
                
                with st.chat_message("assistant"):
                    with st.spinner("思考中..."):
                        response = chat_with_character(char["id"], user_input)
                        st.write(response)
                
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": response
                })
        else:
            st.info("请从左侧选择一个角色开始对话")

if __name__ == "__main__":
    main()