from langchain_openai import ChatOpenAI
from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent
from langchain.prompts import StringPromptTemplate
from langchain.chains.llm import LLMChain
from langchain.schema import AgentAction, AgentFinish
from typing import List, Union, Dict, ClassVar
from bold_payment_agent import BoldPaymentAgentTool
import os
from dotenv import load_dotenv

# Template para el agente
TEMPLATE_SPANISH = """Eres un asistente amable que ayuda con pagos. Puedes:
1. Negociar precios (dentro de un 10% de descuento máximo)
2. Generar enlaces de pago
3. Despedirte cuando el cliente quiera salir

Precio actual: {current_amount} COP

Historial de la conversación:
{chat_history}

Entrada del usuario: {input}

Debes responder en español y ser amable.
Para generar un pago, usa la herramienta de Bold.
Para salir, simplemente despídete.

Formato de respuesta:
Action: la acción a tomar (generate_payment/think)
Action Input: el monto para el pago o tu respuesta
"""

class NegotiationPrompt(StringPromptTemplate):
    template: ClassVar[str] = TEMPLATE_SPANISH
    input_variables: ClassVar[List[str]] = ["input", "current_amount", "chat_history"]

    def format(self, **kwargs) -> str:
        # Implementación del método abstracto format
        return self.template.format(**kwargs)

class PaymentNegotiationAgent:
    def __init__(self):
        load_dotenv()
        
        # Inicializar herramienta de Bold
        self.bold_tool = BoldPaymentAgentTool(api_key=os.getenv("BOLD_API_KEY"))
        
        # Configurar LLM
        self.llm = ChatOpenAI(temperature=0.7, model="gpt-3.5-turbo")
        
        # Herramientas disponibles
        self.tools = [
            Tool(
                name="generate_payment",
                func=self.bold_tool._run,
                description="Genera un enlace de pago por el monto especificado"
            )
        ]
        
        self.prompt = NegotiationPrompt()
        
        # Configurar el agente
        self.llm_chain = LLMChain(llm=self.llm, prompt=self.prompt)
        
        self.agent = LLMSingleActionAgent(
            llm_chain=self.llm_chain,
            output_parser=self._parse_output,
            stop=["\nObservation:"],
            allowed_tools=["generate_payment", "think"]
        )
        
        self.agent_executor = AgentExecutor.from_agent_and_tools(
            agent=self.agent,
            tools=self.tools,
            verbose=True
        )
        
        self.chat_history = []
        self.current_amount = 3000  # Monto inicial

    def _parse_output(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
        # Parsear la salida del LLM
        if "Action:" not in llm_output:
            return AgentFinish(
                return_values={"output": llm_output},
                log=llm_output,
            )
            
        action_match = llm_output.split("Action:")[1].strip()
        action_input_match = llm_output.split("Action Input:")[1].strip()
        
        action = action_match.split("\n")[0].strip()
        action_input = action_input_match.split("\n")[0].strip()
        
        return AgentAction(tool=action, tool_input=action_input, log=llm_output)

    async def process_message(self, user_input: str) -> str:
        # Procesar el mensaje del usuario
        response = await self.agent_executor.arun(
            input=user_input,
            current_amount=self.current_amount,
            chat_history="\n".join(self.chat_history)
        )
        
        self.chat_history.append(f"Usuario: {user_input}")
        self.chat_history.append(f"Asistente: {response}")
        
        return response 