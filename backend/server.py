import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from llm_config import get_deepseek_llm, has_api_key
from characters import CHARACTERS, get_character

load_dotenv()

app = FastAPI(
    title="Roleplay AI Assistant API",
    version="1.0",
    description="基于LangChain的角色扮演AI助手服务"
)

@app.get("/api/characters")
def list_characters():
    return [{"id": key, **value} for key, value in CHARACTERS.items()]

@app.get("/api/characters/{character_id}")
def get_character_info(character_id: str):
    character = get_character(character_id)
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    return character

@app.get("/api/health")
def health_check():
    return {"status": "running", "has_api_key": has_api_key()}

@app.post("/api/chat/{character_id}")
async def chat(character_id: str, user_message: str):
    character = get_character(character_id)
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    
    llm = get_deepseek_llm(role_id=character_id)
    if not llm:
        raise HTTPException(status_code=500, detail="API Key not configured")
    
    template = """
你现在需要扮演一个特定的角色。请严格按照以下角色设定进行对话：

角色信息：
- 姓名：{name}
- 描述：{description}
- 性格：{personality}
- 语气：{tone}
- 示例回复：{example_response}

用户当前问题：{user_message}

请根据以上信息，以{name}的身份给出合适的回复。
"""
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", template),
        ("human", "{user_message}")
    ])
    
    response = llm.invoke(
        prompt.format_messages(
            name=character["name"],
            description=character["description"],
            personality=character["personality"],
            tone=character["tone"],
            example_response=character["example_response"],
            user_message=user_message
        )
    )
    
    return {"response": response.content}

if __name__ == "__main__":
    import uvicorn
    print("Starting Roleplay AI Assistant API...")
    print(f"API Key configured: {has_api_key()}")
    uvicorn.run(
        app,
        host=os.getenv("SERVER_HOST", "0.0.0.0"),
        port=int(os.getenv("SERVER_PORT", 8000))
    )