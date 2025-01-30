import autogen

from config.config import llm_config

# Initialize the agent with Gemini
agent = autogen.AssistantAgent(
    name="GeminiAgent",
    llm_config=llm_config,
)

def ask_gemini(prompt):
    """Send a prompt to Gemini and return the response."""
    response = agent.generate_reply(messages=[{"role": "user", "content": prompt}], llm_config=llm_config)
    print(response)
    return response["content"] if response else "No response from Gemini."

if __name__ == "__main__":
    test = "Click on the 'Sign up free' button."
    resource_id = "com.example.app:id/signup"
    print(ask_gemini(f"Convert this step into a valid Appium command:\n'{test}'\nusing resource_id='{resource_id}'"))
