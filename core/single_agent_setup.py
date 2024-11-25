from core.llm_setup import get_llama3_2_3b_instruct_bedrock_llm
from core.tools_setup import get_tools
from agents.travel_agent import TravelAgent

def get_agent():
    llm = get_llama3_2_3b_instruct_bedrock_llm()
    tools = get_tools()
    print(f"Number of tools: {len(tools)}")
    if not tools:
        raise ValueError("No tools were initialized")
    print(f"Tools: {[tool.name for tool in tools]}")
    
    travel_agent = TravelAgent(
        llm=llm,
        tools=tools
    )
    
    return travel_agent