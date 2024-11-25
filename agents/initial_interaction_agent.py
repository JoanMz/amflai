# agents/initial_interaction_agent.py
from langchain.agents import initialize_agent, AgentType
from langchain_community.chat_models import ChatOpenAI
from langchain.agents import Tool
from pydantic import Field
import logging

logger = logging.getLogger(__name__)

class InitialInteractionAgent:
    def __init__(self, llm, tools: list):
        self.llm = llm
        self.tools = tools
        self.agent = self.initialize_agent()

    def initialize_agent(self):
        agent = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True  # Cambia a False en producción
        )
        return agent

    def handle_initial_interaction(self, user_input: str) -> str:
        try:
            response = self.agent.invoke(user_input)
            return response
        except Exception as e:
            logger.error(f"Error en la interacción inicial: {e}")
            return f"Error en la interacción inicial: {e}"
