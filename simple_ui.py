import gradio as gr
from src.agent_controller import AgentController

agent_controller = AgentController()
agent = agent_controller.get_agent()

def detect_and_store_name(user_input: str, name_state: str):
    """
    Detects if the user input is likely a name and stores only the first name in Gradio's state.

    Args:
        user_input (str): The raw input from the user.
        name_state (str): The current stored name.

    Returns:
        tuple: A message confirming the name (if detected) or None, and the updated name state.
    """
    if name_state:  # If name is already set, do nothing
        return None, name_state

    greetings = {"hi", "hello", "hey", "greetings", "hola", "salut", "hallo"}  # Add more as needed
    words = user_input.strip().split()

    if len(words) == 1 and words[0].isalpha() and words[0].lower() not in greetings:
        new_name = words[0].capitalize()
        return f"Nice to meet you, {new_name}! How can I help you with math today?", new_name

    return None, name_state  # No valid name detected, return the same state


def respond(message, history, name_state):
    """
    Handles user input and returns a response from the agent.

    Args:
        message (str): The user's message.
        history (list): The chat history.
        name_state (str): The user's stored name.

    Returns:
        tuple: Assistant's response and the updated name state.
    """
    name_response, updated_name_state = detect_and_store_name(message, name_state)
    if name_response:
        return name_response, updated_name_state

    # Otherwise, continue normal chatbot processing
    response = agent.chat(message)
    return response.response, updated_name_state

def reset_agent():
    """Resets chat history and clears the stored user name."""
    print("Resetting agent current chat history: ", agent.chat_history)
    agent.reset()
    return "", []  # Clear name state and chat history

theme = gr.themes.Ocean(
    primary_hue="yellow",
    secondary_hue="rose",
    neutral_hue="orange",
    text_size="md",
).set(
    body_background_fill='*background_fill_secondary',
    body_text_size='*text_md',
    embed_radius='*radius_xs'
)


with gr.Blocks(theme=theme) as demo:
    gr.Markdown("## Agentic Tool-Calling Chatbot")

    chatbot = gr.Chatbot(type="messages",
                         height=450)
    gr.ChatInterface(fn=respond,
                     type="messages",
                     chatbot=chatbot,
                    #  textbox=gr.Textbox(placeholder="Share your first name or let's dive into some math fun!", container=False),
                     description="Let's crunch some numbers! I'm here for your basic math needs.",
                     )

demo.launch(share=False)
