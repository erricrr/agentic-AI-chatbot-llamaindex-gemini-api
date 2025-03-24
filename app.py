import gradio as gr
from src.agent_controller import AgentController

agent_controller = AgentController()
agent = agent_controller.get_agent()


def respond(message, history):
    # {"role": "user", "content": "message"}
    """
    Function to handle user input and return a response from the agent.

    Args:
        message (str): The user's message.
        history (list): The chat history.

    Returns:
        dict: A dictionary with the keys "role" and "content", where "role" is "assistant" and "content" is the response message.
    """
    response = agent.chat(message)
    response = {"role": "assistant", "content": response.response}
    return response

def reset_agent():
    """
    Resets the agent's current chat history.

    This function prints the current chat history of the agent for logging purposes and
    resets it to clear any past interactions. This is useful for starting a new conversation
    session without any prior context.
    """
    print("resetting agent current chat history: ", agent.chat_history)
    agent.reset()

theme = gr.themes.Citrus()

with gr.Blocks(theme=theme) as demo:
    gr.Markdown("## Agentic Tool-Calling Chatbot")
    gr.Markdown("### The Power of Basic Math Tools")

    chatbot = gr.Chatbot(type="messages",
                         height=450)
    gr.ChatInterface(fn=respond,
                     type="messages",
                     chatbot=chatbot,
                     description="Type a math problem to solve:",
                    #  textbox=gr.Textbox(placeholder="Ready to solve some math? Type your problem here!", container=False),
                     )

demo.launch(share=False)
