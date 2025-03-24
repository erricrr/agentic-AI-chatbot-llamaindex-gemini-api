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
    print("Added user message to memory:", message)

    try:
        # Get response from agent
        agent_response = agent.chat(message)

        # Check if response or response.response is None
        if agent_response is None:
            content = "I apologize, but I couldn't process that math problem correctly. Please try rephrasing your question."
        elif hasattr(agent_response, 'response') and agent_response.response is None:
            content = "I apologize, but I couldn't process that math problem correctly. Please try rephrasing your question."
        elif hasattr(agent_response, 'response'):
            # Normal case - we have a valid response
            content = agent_response.response
            # Check if content is 'None' string or empty
            if content is None or content.strip() == "" or content.strip().lower() == "none":
                content = "I apologize, but I couldn't process that math problem correctly. Please try rephrasing your question."
        else:
            # Fallback if response has unexpected structure
            content = str(agent_response)
            if content is None or content.strip() == "" or content.strip().lower() == "none":
                content = "I apologize, but I couldn't process that math problem correctly. Please try rephrasing your question."

        print("=== LLM Response ===")
        print(content)

        return {"role": "assistant", "content": content}
    except Exception as e:
        print(f"Error processing message: {e}")
        return {"role": "assistant", "content": "I encountered an error while processing your request. Please try again with a different question."}

def reset_agent():
    """
    Resets the agent's current chat history.

    This function prints the current chat history of the agent for logging purposes and
    resets it to clear any past interactions. This is useful for starting a new conversation
    session without any prior context.
    """
    print("resetting agent current chat history: ", agent.chat_history)
    agent.reset()

theme = gr.themes.Soft(primary_hue='emerald')

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
