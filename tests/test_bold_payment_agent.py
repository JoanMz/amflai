import sys
import os
# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tools.bold_payment_agent_tool import BoldPaymentAgentTool
import os
from dotenv import load_dotenv

def test_bold_payment_agent():
    load_dotenv()
    api_key = os.getenv("BOLD_API_KEY")  # Asegúrate de tener esta variable en tu archivo .env
    payment_tool = BoldPaymentAgentTool(api_key=api_key)
    
    # Prueba con un monto de 1100 COP
    amount = 3000
    response = payment_tool._run(amount)
    print(response)

if __name__ == "__main__":
    test_bold_payment_agent() 