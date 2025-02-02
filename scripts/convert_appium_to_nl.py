from openai_agent import code_to_nlp_tool

def extract_test_actions(file_path):
    """
    Extracts individual Appium actions from a test script.
    Ensures that each interaction (click, send_keys, assert) is treated as a separate atomic step.
    """
    actions = []
    with open(file_path, "r") as f:
        lines = f.readlines()

    current_step = []

    for line in lines:
        line = line.strip()

        # Identify relevant Appium actions
        if any(action in line for action in ["find_element", "click()", "send_keys", "is_displayed", "assert"]):
            if current_step:  # Store previous step as a separate entry
                actions.append("\n".join(current_step).strip())
            current_step = [line]  # Start a new step

    # Capture the last action
    if current_step:
        actions.append("\n".join(current_step).strip())

    return actions

def convert_appium_script_to_nlp(input_file, output_file):
    """
    Reads an Appium test script, extracts individual test actions, and sends them to the LLM.
    Each step is treated as an atomic action for clear NLP conversion.
    """
    test_actions = extract_test_actions(input_file)
    if not test_actions:
        print("No test steps found in the script.")
        return

    nlp_steps = []

    for i, action in enumerate(test_actions, 1):
        nl_instruction = code_to_nlp_tool(action)  # Send each atomic action separately
        nlp_steps.append(f"Step {i}: {nl_instruction}")
        print(f"Converted Step {i}: {nl_instruction}")

    # Save NLP instructions to a file
    with open(output_file, "w") as f:
        for step in nlp_steps:
            f.write(step + "\n")

    print(f"Natural language test instructions saved to {output_file}")

if __name__ == "__main__":
    input_file = "test_appium.py"  # Path to your Appium test script
    output_file = "nlp_steps.txt"  # Path for saving NLP test cases
    convert_appium_script_to_nlp(input_file, output_file)
