# A MCP Client to connect to MCP servers and create agents with memory support.

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
import os
import asyncio

# Load environment variables for API keys
load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# weather mathconfig JSON
weather_math_config = {
    "weather": {
        "url": "http://localhost:8000/mcp",  # Update with your weather server URL
        "transport": "streamable_http",
    },
    "math": {
        "command": "python",
        "args": ["math_server.py"],
        "transport": "stdio",
    },
}

async def main():
    """Main function to run the MCP client and agent."""

    print("Initializing MCP Client...")

    # Create MCP client from config file
    client = MultiServerMCPClient(weather_math_config)

    # Initialize the language model
    llm = ChatGroq(model="qwen/qwen3-32b")

    # Get tools
    tools = await client.get_tools()

    # Create a ReAct agent with memory enabled
    agent = create_react_agent(
        llm,
        tools
    )

    print("\n===== Interactive MCP Chat =====")
    print("Type 'exit' or 'quit' to end the conversation")
    print("==================================\n")

    try:
        # Main chat loop
        while True:
            # Get user input
            user_input = input("\nYou: ")

            # Check for exit command
            if user_input.lower() in ["exit", "quit"]:
                print("Ending conversation...")
                break

            # Get response from agent
            print("\nAssistant: ", end="", flush=True)

            try:
                # Run the agent with the user input (memory handling is automatic)
                response = await agent.ainvoke(
                    {"messages": [{"role": "user", "content": user_input}]}
                )
                print(response["messages"][-1].content)
            except Exception as e:
                print(f"\n[Error] {e}")

    except KeyboardInterrupt:
        print("\nConversation interrupted. Exiting...")

asyncio.run(main())