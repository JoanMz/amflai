from langchain.agents import Tool
from tools.flight_price_agent_tool import FlightPriceAgentTool
from tools.package_price_agent_tool import PackagePriceAgentTool
from tools.bold_payment_agent_tool import BoldPaymentAgentTool
from config.settings import settings

def get_tools():
    try:
        print("Initializing tools...")

        flight_tool = FlightPriceAgentTool(serpapi_key=settings.serpapi_api_key)
        print(f"Flight tool initialized: {flight_tool.name}")

        package_tool = PackagePriceAgentTool(excel_path=settings.excel_file_path)
        print(f"Package tool initialized: {package_tool.name}")

        payment_tool = BoldPaymentAgentTool(api_key=settings.bold_api_key)
        print(f"Payment tool initialized: {payment_tool.name}")

        tools = [
            Tool(
                name="FlightPriceAgent",
                func=flight_tool._run,
                description=flight_tool.description
            ),
            Tool(
                name="PackagePriceAgent",
                func=package_tool.run,
                description=package_tool.description
            ),
            Tool(
                name="BoldPaymentAgent",
                func=payment_tool._run,
                description=payment_tool.description
            )
        ]

        print(f"Total tools created: {len(tools)}")
        print(f"Tools names: {[tool.name for tool in tools]}")
        return tools
    except Exception as e:
        print(f"Error in get_tools: {str(e)}")
        raise
