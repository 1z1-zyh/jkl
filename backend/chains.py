from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from .llm_config import get_deepseek_llm
from .prompts import get_character_prompt_template
from .characters import get_character

def create_character_chain(character_id):
    character = get_character(character_id)
    if not character:
        raise ValueError(f"Character {character_id} not found")
    
    llm = get_deepseek_llm()
    prompt = get_character_prompt_template()
    
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )
    
    chain = LLMChain(
        llm=llm,
        prompt=prompt,
        memory=memory,
        verbose=True
    )
    
    return chain, character

def chat_with_character(chain, character, user_message):
    response = chain.run(
        name=character["name"],
        description=character["description"],
        personality=character["personality"],
        tone=character["tone"],
        example_response=character["example_response"],
        user_message=user_message
    )
    return response