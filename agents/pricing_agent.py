from tools.flight_price_agent_tool import FlightPriceAgentTool
from tools.package_price_agent_tool import PackagePriceAgentTool
import logging

logger = logging.getLogger(__name__)

class PricingAgent:
    def __init__(self, flight_tool: FlightPriceAgentTool, package_tool: PackagePriceAgentTool):
        self.flight_tool = flight_tool
        self.package_tool = package_tool

    def get_total_price(self, flight_query: str, package_params: dict) -> str:
        try:
            print(f"flight_query: {flight_query}")
            flight_price_response = self.flight_tool.run(flight_query)
            print(f"flight_price_response: {flight_price_response}")
            package_price_response = self.package_tool.run(**package_params)
            print(f"package_price_response: {package_price_response}")
            
            # Extraer precios numéricos de las respuestas
            flight_amount = self.extract_price(flight_price_response)
            package_amount = self.extract_price(package_price_response)
            print(f"flight_amount: {flight_amount}")
            print(f"package_amount: {package_amount}")
            total = flight_amount + package_amount
            logger.info(f"Total price calculated: {total}")
            return f"El precio total del viaje es: ${total}."
        except Exception as e:
            logger.error(f"Error al calcular el precio total: {e}")
            return f"Error al calcular el precio total: {e}"

    def extract_price(self, response: str) -> float:
        import re
        match = re.search(r'\$(\d+)', response)
        return float(match.group(1)) if match else 0.0
