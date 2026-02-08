from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parents[1]))

from ollama import chat
from util.llm_utils import pretty_stringify_chat, ollama_seed as seed

# Model and name information
sign_your_name = 'Raghav Sandeep Sharavanan'
model = 'gemma3:270m'

# System prompt to define the agent's behavior as a Dungeon Master
messages = [
    {'role': 'system', 'content': "You are a Dnd Dungeon Master. You MUST follow these rules: "
                                  "You act as an observer and describe what the player sees and does. "
                                  "Do not help or guide the player. "
                                  "Describe any situation within 3 sentences. "
                                  "Always introduce a new situation to the player. "
                                  "If the player attacks, and there is something nearby, immediately name what it is and what damage was dealt. "
                                  "Never repeat the same thing twice. "
                                  "Every response must end with a specific question for the player. "
                                  "Tell the player what kind of character they are playing as at the start. "
                                 }
]

# Hyperparameters: High temperature with high token
options = {'temperature': 1, 'max_tokens': 300}

messages.append({'role':'user', 'content':''}) # An empty user message to prompt the model to start responding.

options |= {'seed': seed(sign_your_name)}

# Chat loop
while True:
  # Get the model's response (The DM starts the conversation)
  response = chat(model=model, messages=messages, stream=False, options=options)
  
  # DM response code
  dm_response = response.message.content
  print(f'\nDM: {dm_response}\n')
  
  # Store the DM's response in history
  messages.append({'role': 'assistant', 'content': dm_response})

  # Get the player's input
  user_input = input('You: ')
  
  # Store user input in history
  messages.append({'role': 'user', 'content': user_input})

  # Exit logic
  if messages[-1]['content'] == '/exit':
    print("Exiting game and saving log...")
    break

# Save chat
# Ensure the folder lab03 exists or change the path accordingly
attempts_path = Path('lab03/attempts.txt')
attempts_path.parent.mkdir(parents=True, exist_ok=True)

with open(attempts_path, 'a') as f:
  file_string  = ''
  file_string +=       '-------------------------NEW ATTEMPT-------------------------\n\n\n'
  file_string += f'Model: {model}\n'
  file_string += f'Options: {options}\n'
  file_string += pretty_stringify_chat(messages)
  file_string += '\n\n\n------------------------END OF ATTEMPT------------------------\n\n\n'
  f.write(file_string)