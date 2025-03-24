from llama_index.core.agent import FunctionCallingAgent
from llama_index.core.tools import FunctionTool
from src.generators import Generators
from src.tools import *
from src.utils.app_logger import GenericLogger

logger = GenericLogger().get_logger()


add_tool = FunctionTool.from_defaults(fn=add)
multiply_tool = FunctionTool.from_defaults(fn=multiply)
miscellaneous_tool = FunctionTool.from_defaults(fn=miscellaneous)
sin_tool = FunctionTool.from_defaults(fn=calculate_sin)
cos_tool = FunctionTool.from_defaults(fn=calculate_cos)
log_tool = FunctionTool.from_defaults(fn=calculate_log)
exp_tool = FunctionTool.from_defaults(fn=calculate_power)
real_number_tool = FunctionTool.from_defaults(fn=only_real_numbers)
convert_to_real_number_tool = FunctionTool.from_defaults(fn=convert_to_real_number)
divide_tool = FunctionTool.from_defaults(fn=divide)
subtract_tool = FunctionTool.from_defaults(fn=subtract)


class AgentController:
    def __init__(self):
        """
        Initializes the AgentController class.

        This method creates an instance of the AgentController class with the Gemini API model and the system prompt.

        The system prompt is a string that is provided to the Gemini API model to generate responses.
        """

        logger.info("creating AgentController")
        self.llm = Generators().get_llm()
        self.system_prompt = """
                                INSTRUCTIONS: You are a math tools expert. You are capable of having chain of thoughts and you will only use the tools available to you. You must wait for each function's output before proceeding to the next step.

                                CRITICAL: Word problems are ALWAYS math problems. ANY problem that involves numbers, quantities, rates, time, money, or measurements IS a math problem and should NEVER use the miscellaneous tool.

                                IMPORTANT: The miscellaneous tool should ONLY be used when the query has absolutely nothing to do with mathematics (e.g., questions about politics, history, entertainment, etc.).

                                IMPORTANT FOR WORD PROBLEMS:
                                1. Math word problems (even complex ones involving scenarios, rates, time, etc.) should NEVER use the miscellaneous tool.
                                2. Always use the appropriate math tools to solve word problems step by step.
                                3. For word problems, first identify the key variables and relationships, then use the appropriate tools.
                                4. Always double-check your calculations and reasoning.

                                FUNCTION CALLING RULES:
                                1. Always pass simple numeric values directly to functions, not nested function calls.
                                2. Avoid nesting function calls like this: subtract({"a": {"function": "subtract", "args": [...]}}, ...)
                                3. Instead, calculate intermediate values first, then use those in subsequent function calls.
                                4. Always use the simplest approach to solve the problem.

                                NOTE: You will ALWAYS evaluate the user's query and provide three things:
                                answer, tool_used, reasoning.

                                like this:

                                Answer: answer
                                - Tool Used: tool_name
                                - Reasoning: reasoning for using the tool


                                An example:

                                Answer: 21.0
                                - Tool Used: multiply
                                - Reasoning: The tool was used to calculate the product of two numbers.

                                Example for math word problem:
                                "A farming field can be ploughed by 6 tractors in 4 days. When 6 tractors work together, each of them ploughs 120 hectares a day. If two of the tractors were moved to another field, then the remaining 4 tractors could plough the same field in 5 days. How many hectares a day would one tractor plough then?"

                                For this problem, you would use the appropriate math tools (multiply, divide, etc.) to solve it step by step, NOT the miscellaneous tool.

                                Example for non-math query (like asking about politics, history, etc.):
                                Answer: Hi there, I can't help you with that, if you have any other math questions please ask them
                                - Tool Used: miscellaneous
                                - Reasoning: The query was not related to mathematics or calculations.

                                Solve the queries STEP by STEP and feel free to use the tools available to you and do not hallucinate or make assumptions.
                                """
        self.agent = self.get_agent()
        logger.info("AgentController created")
    def get_agent(self):

        """
        Creates and returns a FunctionCallingAgent initialized with a set of tools and the specified language model.

        The agent is configured to use a variety of mathematical and utility tools,
        and is provided with a system prompt for operation. It logs the creation process.

        :return: An initialized FunctionCallingAgent instance.
        """
        logger.info("creating Agent")

        # Reorder tools to prioritize basic math operations first, then complex ones, and miscellaneous last
        # This ordering can help the model make better decisions about which tool to use
        agent = FunctionCallingAgent.from_tools([
                # Basic math operations first
                add_tool,
                subtract_tool,
                multiply_tool,
                divide_tool,

                # More complex operations
                exp_tool,
                sin_tool,
                cos_tool,
                log_tool,

                # Utility tools
                real_number_tool,
                convert_to_real_number_tool,

                # Miscellaneous tool last (least priority)
                miscellaneous_tool
            ],
            llm=self.llm,
            verbose=True,
            system_prompt=self.system_prompt
        )

        logger.info("Agent created")
        return agent


    def chat(self, query: str):
        """
        Processes a chat query using the initialized agent and returns the response.

        This method sends a user query to the agent, which processes it using the available tools
        and language model, and returns the generated response.

        Args:
            query (str): The query string to be processed by the agent.

        Returns:
            The agent's response to the provided query.
        """
        try:
            # Try to get a response from the agent
            response = self.agent.chat(query)

            # Check if response is None or empty
            if response is None or str(response).strip() == "" or str(response).strip().lower() == "none":
                # This is likely a math word problem that failed to process correctly
                # Create a fallback response that encourages the user to try again
                logger.warning("Received None or empty response for query: %s", query)

                # Check if it's likely a word problem (contains numbers and narrative elements)
                if any(char.isdigit() for char in query) and len(query.split()) > 10:
                    return "I apologize, but I couldn't process that math word problem correctly. Please try rephrasing your question or breaking it down into smaller steps."
                else:
                    return "I apologize, but I couldn't process that request. Could you please rephrase your question?"

            return response

        except Exception as e:
            # Log the error and return a friendly message
            logger.error("Error processing query: %s. Error: %s", query, str(e))
            return "I encountered an error while processing your request. Please try again with a different question."
