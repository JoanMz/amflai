from langchain.agents import initialize_agent, AgentType
from core.llm_setup import get_llama3_2_3b_instruct_bedrock_llm
from core.tools_setup import get_tools

def get_agent():
    llm = get_llama3_2_3b_instruct_bedrock_llm()
    tools = get_tools()
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )
    
    return agent

"""
def process_query_and_calculate_total(query: str) -> str:
    # Use the LLM to process the query and extract necessary information
    llm = get_llama3_2_3b_instruct_bedrock_llm()
    processed_data = llm.invoke(f"Extrae la siguiente información en formato JSON con las claves 'origin', 'destination', 'date' y 'trip_type': {query}")
    print(f"type(processed_data): {(processed_data)}")
    
    # Check if processed_data is not empty and is a valid JSON string
    if processed_data:
        try:
            import json
            processed_data = json.loads(processed_data)
        except json.JSONDecodeError:
            # Fallback in case response is not valid JSON
            processed_data = {
                'origin': None,
                'destination': None, 
                'date': None,
                'trip_type': None
            }
    else:
        # Handle the case where processed_data is empty
        processed_data = {
            'origin': None,
            'destination': None, 
            'date': None,
            'trip_type': None
        }

    print(f"processed_data: {processed_data}")
    # Extract variables from processed data
    origin = processed_data.get('origin')
    destination = processed_data.get('destination') 
    date = processed_data.get('date')
    trip_type = processed_data.get('trip_type')

    print(f"origin: {origin}, destination: {destination}, date: {date}, trip_type: {trip_type}")
    # Initialize tools
    tools = get_tools()
    flight_tool = tools[1]  # Assuming the second tool is FlightPriceAgentTool
    package_tool = tools[0]  # Assuming the first tool is PackagePriceAgentTool

    # Get flight price
    flight_info = flight_tool.func(f"vuelo desde {origin} a {destination} para el {date} {trip_type}")
    flight_price = flight_info['price'] if flight_info else 0

    # Get package price
    package_info = package_tool.func(destination, destination, "pesos")
    package_price = float(package_info.split("Precio: $")[1].split(" ")[0]) if package_info else 0

    # Calculate total price
    total_price = flight_price + package_price

    return f"El precio total es: ${total_price} pesos"

# Example usage
query = "Vuelo desde Cali a Cartagena para el 29 de noviembre solo ida"
total_price = process_query_and_calculate_total(query)
print(total_price)

"""