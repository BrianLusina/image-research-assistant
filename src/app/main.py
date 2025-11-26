import os
import sys

# Ensure the project `src` directory is on sys.path so `from app...` imports
# work when running this file directly (for example: `python src/app/main.py`).
# This is a minimal, local fix to make the package importable without requiring
# the user to set PYTHONPATH or install the package.
_SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _SRC_DIR not in sys.path:
    sys.path.insert(0, _SRC_DIR)

import asyncio
import gradio as gr
from langchain_mcp_adapters.client import MultiServerMCPClient

from app.clients import create_graph

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


# --- Main function with Gradio UI ---
async def main():
    # This setup runs only ONCE when the application starts
    client = MultiServerMCPClient(server_configs)
    all_tools = await client.get_tools()
    agent = await create_graph(all_tools)

    print("The Image Research Assistant is ready and launching on a web UI.")

    # --- Gradio UI Implementation ---
    with gr.Blocks(theme=gr.themes.Default(primary_hue="blue")) as gradio_ui:
        gr.Markdown("# Image Research Assistant")
        chatbot = gr.Chatbot(label="Conversation", height=500)

        with gr.Row():
            # The gr.Image component will handle the upload
            # Setting type="filepath" is crucial, as it gives our tool a path to work with
            image_box = gr.Image(type="filepath", label="Upload an Image")

            # The textbox is for the user's text query
            text_box = gr.Textbox(
                label="Ask a question about the image or a general research question.",
                scale=2  # Makes the textbox wider than the image box
            )

        submit_btn = gr.Button("Submit", variant="primary")

        # This function handles the agent's response
        # It now accepts an image_path from the gr.Image component
        async def get_agent_response(user_text, image_path, chat_history):
            # If an image is provided, combine it with the text to form the message
            if image_path:
                # The agent will see both the text and the path and chain the tools
                full_message = f"{user_text} {image_path}"
                # Add the user's turn to the chat history immediately for a better UI experience
                chat_history.append(((image_path,), None))
                chat_history.append((user_text, None))
            else:
                # If no image, just use the text
                full_message = user_text
                chat_history.append((user_text, None))

            # The agent.ainvoke call remains the same, but now with the potentially combined message
            response = await agent.ainvoke(
                {"messages": [("user", full_message)]},
                config={"configurable": {"thread_id": "gradio-session"}}
            )

            # The agent's final response is added to the history
            bot_message = response["messages"][-1].content
            chat_history.append((None, bot_message))

            return "", chat_history, None  # Clear textbox, return updated history, clear image box

        # Wire up the submit button to the handler function
        submit_btn.click(
            get_agent_response,
            [text_box, image_box, chatbot],
            [text_box, chatbot, image_box]
        )

    # Launch the Gradio web server
    gradio_ui.launch(server_name="0.0.0.0")

if __name__ == "__main__":
    asyncio.run(main())
