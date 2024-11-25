import sys
import os
# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tools.flight_price_agent_tool import FlightPriceAgentTool
from dotenv import load_dotenv
load_dotenv()
def test_flight_price_agent():
    serpapi_key = os.getenv("SERPAPI_API_KEY")
    flight_tool = FlightPriceAgentTool(serpapi_key=serpapi_key)
    query = "Vuelo desde cancun a madrid para el 27 de noviembre solo ida"
    response = flight_tool._run(query)
    print(response)

if __name__ == "__main__":
    test_flight_price_agent()
