from langchain.agents import create_react_agent, AgentExecutor
from langchain.prompts import PromptTemplate

class TravelAgent:
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = tools
        self.agent_executor = self.initialize_agent()

    def initialize_agent(self):
        print("Initializing Travel Agent...")
        try:
            prompt = PromptTemplate(
    template="""
You are a professional and friendly travel agent. Your goal is to help clients plan their trips using the available tools.

**Available Tools:**
{tool_names}
{tools}

1. **FlightPriceAgent**: Use this tool to search and quote flights. Provide specific details of the flight the client desires.

2. **PackagePriceAgent**: Use this tool to get prices for tour packages that include accommodation and activities.

3. **BoldPaymentAgent**: Use this tool to process payments. You must provide the amount to charge just numbers.

**Interaction Format:**

The agent should follow this format:

1. **Thought**: Reflect on what needs to be done to address the client's request.
2. **Action**: The exact name of the tool to use, chosen from [FlightPriceAgent, PackagePriceAgent, BoldPaymentAgent].
3. **Action Input**:  Provide the necessary input for the chosen action.
4. **Observation**: The output provided by the tool. Record the result of the action.
5. **(Repeat Thought/Action/Action Input/Observation as needed)**
6. **Final Answer**: Provide the final response to the client, summarizing the information obtained. and using the tool for generate the link

**Important Guidelines:**

- **Action** and **Action Input** must be on separate lines.
- Do not include any extra text or explanations in **Action** or **Action Input**.
- Do not include the **Final Answer** immediately after the **Observation**. Think again before providing it.
- The **Final Answer** should only be given after all necessary actions are completed.
- Only perform one action at a time.
 After receiving an **Observation**, think again to decide if another action is needed.
 - Only provide the **Final Answer** after all necessary information has been gathered.

*Assuming the tool returns the observation:*
*The agent continues:*

*Assuming the tool dont return the observation:*
*The agent speak with the client*

*Assuming the tool returns the observation:*

*The agent continues:*


*The agent concludes:*




**Example:**
*After the tool provides the observation, the agent continues:*
**Client Inquiry:** {input}

{agent_scratchpad}
""",
    input_variables=["input", "tool_names", "tools", "agent_scratchpad"]
)



# Create the agent
            agent = create_react_agent(
                llm=self.llm,
                tools=self.tools,
                prompt=prompt
            )

            # Create executor with parsing error handling
            agent_executor = AgentExecutor.from_agent_and_tools(
                agent=agent,
                tools=self.tools,
                verbose=True,
                handle_parsing_errors=True  # Error handling
            )
            print("Agent initialized successfully.")
            return agent_executor
        except Exception as e:
            print(f"Error initializing agent: {str(e)}")
            raise

    def run(self, query: str):
        print(f"Processing query: {query}")
        try:
            if not query:
                raise ValueError("The query cannot be empty.")
            response = self.agent_executor.invoke({"input": query})
            print(f"Agent response: {response}")
            # Return only the 'output' field
            return response['output']
        except Exception as e:
            print(f"Error during query execution: {str(e)}")
            raise