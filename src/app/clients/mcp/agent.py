from typing import List
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import tools_condition, ToolNode

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from app.clients.mcp.state_entity import State


async def create_graph(tools: List):
    # LLM configuration
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0,
        google_api_key="{{GOOGLE_GEMINI_API_KEY}}",
    )
    llm_with_tools = llm.bind_tools(tools)

    # Prompt template with user/assistant chat only
    prompt_template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an expert research assistant. Your purpose is to provide comprehensive answers to user requests. "
                "You have access to a specialized set of tools for analyzing the content of images and another set for researching topics on Wikipedia. "
                "Intelligently chain these tools together to fulfill the user's request. For example, if a user asks about an image, first analyze the image to understand what it is, then use that understanding to perform research.",
            ),
            MessagesPlaceholder("messages"),
        ]
    )

    chat_llm = prompt_template | llm_with_tools

    # Define chat node
    def chat_node(state: State) -> State:
        state["messages"] = chat_llm.invoke({"messages": state["messages"]})
        return state

    # Build LangGraph with tool routing
    graph = StateGraph(State)
    graph.add_node("chat_node", chat_node)
    graph.add_node("tool_node", ToolNode(tools=tools))
    graph.add_edge(START, "chat_node")
    graph.add_conditional_edges(
        "chat_node", tools_condition, {"tools": "tool_node", "__end__": END}
    )
    graph.add_edge("tool_node", "chat_node")

    return graph.compile(checkpointer=MemorySaver())
