from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parents[1]))

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
        print(f'{agent_name}: {response}')
        try:
            response = chat.send(input('You: '))
            # Add code here to check which agent chat should be started


            # But before here.
        except StopIteration as e:
            break

if __name__ ==  '__main__':
    # Add code here to start DM chat


    # But before here.
    pass