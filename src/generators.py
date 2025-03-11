import os
from dotenv import load_dotenv
from llama_index.llms.gemini import Gemini


# Load environment variables from .env
load_dotenv()

# Get the API key
api_key = os.getenv("GEMINI_API_KEY")

class Generators:

    def __init__(self, model="models/gemini-2.0-flash"):
        """
        Initializes the Generators class with a specified language model.

        Args:
            model (str): The name of the model to use. Defaults to "models/gemini-2.0-flash.
        """
        self.llm = Gemini(
            model=model,
            api_key=api_key
        )

    def get_llm(self):
        """
        Returns the currently initialized language model (LLM) instance.

        :return: The language model instance used by the Generators class.
        """
        return self.llm
