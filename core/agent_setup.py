from core.llm_setup import get_llama3_2_3b_instruct_bedrock_llm# core/agent_setup.py
from agents.pricing_agent import PricingAgent
from agents.closing_agent import ClosingAgent
from agents.conversational_agent import ConversationalAgent
from agents.initial_interaction_agent import InitialInteractionAgent
from core.tools_setup import get_tools
from config.settings import settings
import logging

logger = logging.getLogger(__name__)

def get_agents():
    # Inicializar LLM
    llm = get_llama3_2_3b_instruct_bedrock_llm()

    # Inicializar herramientas
    tools = get_tools()

    # Inicializar Agentes
    pricing_agent = PricingAgent(
        flight_tool=tools[0],  # Pass the tool instance
        package_tool=tools[1]  # Pass the tool instance
    )

    closing_agent = ClosingAgent(
        payment_tool=tools[2]  # Pass the tool instance
    )

    conversational_agent = ConversationalAgent(
        llm=llm,
        tools=tools
    )

    initial_interaction_agent = InitialInteractionAgent(
        llm=llm,
        tools=tools
    )

    return {
        "pricing_agent": pricing_agent,
        "closing_agent": closing_agent,
        "conversational_agent": conversational_agent,
        "initial_interaction_agent": initial_interaction_agent
    }
