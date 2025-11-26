import asyncio
from app.clients.mcp.agent import create_graph

from langchain_mcp_adapters.client import MultiServerMCPClient

# --- Multi-server configuration dictionary ---
# This dictionary defines all the servers the client will connect to
server_configs = {
    "vision": {
        "command": "python",
        "args": ["app/servers/vision/server.py"],
        "transport": "stdio",
    },
    "wikipedia": {
        "command": "python",
        "args": ["app/servers/wikipedia/server.py"],
        "transport": "stdio",
    },
}


# Entry point
async def main():
    # The client will manage the server subprocesses internally
    client = MultiServerMCPClient(server_configs)

    # get a unified list of tools from all connected servers
    all_tools = await client.get_tools()

    agent = create_graph(all_tools)

    while True:
        # This variable will hold the final message to be sent to the agent
        message_to_agent = ""

        user_input = input("\nYou: ").strip()
        if user_input.lower() in {"exit", "quit", "q"}:
            break

        # Final agent invocation
        # All paths (regular chat or successful prompt) now lead to this single block
        if message_to_agent:
            try:
                # LangGraph expects a list of messages
                response = await agent.ainvoke(
                    {"messages": [("user", message_to_agent)]},
                    config={"configurable": {"thread_id": "multi-server-session"}},
                )
                print("AI:", response["messages"][-1].content)
            except Exception as e:
                print("Error:", e)


if __name__ == "__main__":
    asyncio.run(main())
