import os
import sys

root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_path)

from util.llm_utils import AgentTemplate

# Add code here.
from ollama import chat
from util.llm_utils import pretty_stringify_chat, ollama_seed as seed

# Model and name information
sign_your_name = 'Raghav Sandeep Sharavanan'
model = 'gemma3:270m'
dm_template_file = 'lab04/demo_template.json'

# System prompt to define the agent's behavior as a Dungeon Master
messages = [
    {'role': 'system', 'content': template_file=dm_template_file, recruit_difficulty='not easy', reward='a sword'}
]

# Hyperparameters: High temperature with high token
options = {'temperature': 1, 'max_tokens': 300}

messages.append({'role':'user', 'content':''}) # An empty user message to prompt the model to start responding.

options |= {'seed': seed(sign_your_name)}

# But before here.

def run_console_chat(template_file, agent_name='Agent', **kwargs):
    '''
    Run a console chat with the given template file and agent name.
    Args:
        template_file: The path to the template file.
        agent_name: The name of the agent to display in the console.
        **kwargs: Additional arguments to pass to the AgentTemplate.from_file method.
    '''
    chat = AgentTemplate.from_file(template_file, **kwargs)
    response = chat.start_chat()
    while True:
        user_input = input("You: ")
        
        if user_input.lower() in ["exit", "/exit", "quit"]:
            break
            
        new_summary = f"The player chose to: {user_input}. Previously, you said: {agent_message[:50]}..."
        encounter_agent.parameters['summary'] = new_summary

        agent_message = encounter_agent.send(user_input)
        print(f"\nAgent: {agent_message}\n")

if __name__ == "__main__":
    dm_json_path = os.path.join(root_path, "lab04", "lab04_dm.json")
    
    if not os.path.exists(dm_json_path):
        print(f"Error: Could not find {dm_json_path}")
        sys.exit(1)

    adventure_options = "a social meeting with a merchant (NPC) or an ambush by a monster (ENEMY)"
    
    dm_agent = AgentTemplate.from_file(dm_json_path, encounters=adventure_options)

    run_console_chat(dm_agent)