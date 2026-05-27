import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from typing import List, Optional, Any
from pydantic import Field

load_dotenv()

CHARACTER_RESPONSES = {
    "xiaoming": [
        "哇，这个问题好有趣呀！让我想想...",
        "我觉得是这样的，你看对不对？",
        "这个我知道！我们老师刚讲过呢！",
        "哈哈，这个问题难不倒我！",
        "让我告诉你一个小秘密...",
        "我们一起学习吧！",
        "我最喜欢回答问题啦！"
    ],
    "teacher": [
        "这位同学提出的问题很好，我们一起来分析一下。",
        "很好的思考！让我们从几个方面来理解。",
        "你的观察很敏锐，这正是我们需要讨论的重点。",
        "请坐好，让我详细为你讲解这个知识点。",
        "这个问题涉及到我们之前学过的内容，谁能回忆一下？",
        "思考是学习的第一步，继续保持这种探索精神。",
        "从这个问题中，我们可以引申出几个重要的概念。"
    ],
    "customer_service": [
        "您好！很高兴为您服务。",
        "请不要着急，我会尽力帮助您解决问题。",
        "感谢您的耐心等待，让我为您处理这个问题。",
        "请问还有什么可以帮助您的吗？",
        "非常抱歉给您带来不便，我们会尽快处理。",
        "您的反馈对我们非常重要，感谢您的支持。",
        "好的，我已经为您记录了这个问题。"
    ],
    "doctor": [
        "您好，请详细描述一下您的症状。",
        "这种情况出现多久了？还有其他不舒服吗？",
        "请放松，我来帮您分析一下情况。",
        "根据您的描述，可能是以下几种情况。",
        "我建议您注意休息，保持良好的生活习惯。",
        "如果症状持续，请及时来医院检查。",
        "请放心，我会为您制定最合适的治疗方案。"
    ],
    "friend": [
        "嘿！最近怎么样啊？",
        "哈哈，这个我太懂了！跟我说说。",
        "我觉得你说得对，支持你！",
        "有什么烦心事吗？我听你倾诉。",
        "这个想法太棒了！一定要试试！",
        "别担心，一切都会好起来的！",
        "走，我们去喝杯咖啡聊聊！"
    ],
    "business_consultant": [
        "很高兴为您提供商业咨询服务。",
        "从商业角度来看，这个问题需要综合考虑。",
        "根据我的分析，有以下几个关键因素。",
        "我建议采取以下策略来应对。",
        "这个市场机会值得深入研究。",
        "我们需要制定一个详细的执行计划。",
        "从投资回报率来看，这个方案是可行的。"
    ]
}

class RoleBasedMockLLM(BaseChatModel):
    """基于角色的模拟LLM"""
    
    role_id: str = Field(default="friend")
    
    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[Any] = None,
        **kwargs: Any
    ) -> ChatResult:
        user_message = ""
        
        for msg in messages:
            if isinstance(msg, HumanMessage):
                user_message = msg.content
        
        responses = CHARACTER_RESPONSES.get(self.role_id, CHARACTER_RESPONSES["friend"])
        response_text = responses[len(user_message) % len(responses)]
        
        return ChatResult(
            generations=[ChatGeneration(message=AIMessage(content=response_text))]
        )
    
    @property
    def _llm_type(self) -> str:
        return "mock"

def get_deepseek_llm(role_id: str = None):
    api_key = os.getenv("DEEPSEEK_API_KEY")
    mock_mode = os.getenv("MOCK_MODE", "false").lower() == "true"
    
    if mock_mode:
        return RoleBasedMockLLM(role_id=role_id or "friend")
    
    if not api_key or api_key.strip() == "":
        return None
    
    return ChatOpenAI(
        model=os.getenv("MODEL_NAME", "deepseek-chat"),
        temperature=float(os.getenv("MODEL_TEMPERATURE", 0.7)),
        max_tokens=int(os.getenv("MODEL_MAX_TOKENS", 2048)),
        api_key=api_key,
        base_url=os.getenv("DEEPSEEK_API_BASE", "https://api.deepseek.com/v1")
    )

def has_api_key():
    api_key = os.getenv("DEEPSEEK_API_KEY")
    mock_mode = os.getenv("MOCK_MODE", "false").lower() == "true"
    return mock_mode or (api_key and api_key.strip() != "")