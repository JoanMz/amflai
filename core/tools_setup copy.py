import os
from langchain.agents import Tool
from tools.package_price_agent_tool import PackagePriceAgentTool
from tools.flight_price_agent_tool import FlightPriceAgentTool
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def get_tools():
    # Inicializar las herramientas
    package_tool = PackagePriceAgentTool(excel_path='./data/vivecolombia.xlsx')  # Asegúrate de que la ruta sea correcta
    flight_tool = FlightPriceAgentTool(serpapi_key=os.getenv('SERPAPI_API_KEY'))
    
    # Definir las herramientas para LangChain
    tools = [
        Tool(
            name=package_tool.name,
            func=package_tool.run,
            description=package_tool.description
        ),
        Tool(
            name=flight_tool.name,
            func=flight_tool._run,
            description=flight_tool.description
        )
    ]
    
    return tools
