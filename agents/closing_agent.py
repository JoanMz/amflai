# agents/closing_agent.py
from tools.bold_payment_agent_tool import BoldPaymentAgentTool
import logging

logger = logging.getLogger(__name__)

class ClosingAgent:
    def __init__(self, payment_tool: BoldPaymentAgentTool):
        self.payment_tool = payment_tool

    def close_sale(self, amount: float) -> str:
        try:
            payment_link_response = self.payment_tool.run(amount=amount)
            logger.info("Cierre de venta exitoso.")
            return payment_link_response
        except Exception as e:
            logger.error(f"Error al cerrar la venta: {e}")
            return f"Error al cerrar la venta: {e}"
