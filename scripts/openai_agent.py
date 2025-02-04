# scripts/openai_agent.py
import autogen
from config.config import llm_config

# Define a system message to set context for the agent.
SYSTEM_MESSAGE = {
    "role": "system",
    "content": (
        "You are a helpful assistant specialized in mobile test automation. "
        "Your task is to convert Appium code snippets into concise, atomic natural language instructions. "
        "Return only the requested output with no extra commentary."
    )
}

agent = autogen.AssistantAgent(name="OpenAIAgent", llm_config=llm_config)

def code_to_nlp_tool(code_snippet: str) -> str:
    """
    Converts an Appium code snippet into a single, concise natural language instruction 
    that describes one atomic action (e.g., 'Tap on the Sign Up button.').
    """

    prompt = (
        "Convert the following Appium Python code snippet into a single, concise natural language instruction "
        "that describes one atomic action. Do not combine multiple actions in one sentence or include any additional commentary.\n\n"
        "Code snippet:\n"
        f"{code_snippet}\n\n"
        "Return only the natural language instruction."
    )
    messages = [SYSTEM_MESSAGE, {"role": "user", "content": prompt}]
    response = agent.generate_reply(messages=messages, llm_config=llm_config)
    return str(response).strip()

def ask_openai(prompt: str, conversation_history=None) -> str:
    """
    Sends a prompt to the agent using a structured conversation and returns its reply.
    """
    if conversation_history is None:
        conversation_history = []
    messages = [SYSTEM_MESSAGE] + conversation_history + [{"role": "user", "content": prompt}]
    try:
        response = agent.generate_reply(messages=messages, llm_config=llm_config)
        return str(response).strip()
    except Exception as e:
        print("Error generating reply:", e)
        return ""

if __name__ == "__main__":
    # Sample Appium code snippet.
    sample_code = "driver.find_element_by_accessibility_id('Sign Up').click()"
    
    # Convert the code snippet into a natural language instruction.
    nl_instruction = code_to_nlp_tool(sample_code)
    print("Natural Language Instruction:")
    print(nl_instruction)
