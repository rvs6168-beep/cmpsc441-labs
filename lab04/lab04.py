from pathlib import Path
import sys
import os

sys.path.append(str(Path(__file__).parents[1]))

from util.llm_utils import AgentTemplate

# Add code here
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_path)
DM_TEMPLATE_NAME = "lab04_dm.json"
NPC_TEMPLATE_NAME = "lab04_npc.json"
ENEMY_TEMPLATE_NAME = "lab04_enemy.json"
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
            user_input_text = input('You: ')
            response = chat.send(user_input_text) 
            if '_routing_state' not in chat.parameters:
                chat.parameters['_routing_state'] = {
                    'is_routed': False,
                    'current_role_name': agent_name,
                    'encounter_summary': "The adventure has just begun with the Dungeon Master.",
                    'dm_initial_context': ""
                }
            
            routing_state = chat.parameters['_routing_state']

            if not routing_state.get('_dm_context_captured', False):
                routing_state['dm_initial_context'] = "Initial DM scene not explicitly captured in this loop pass due to constraint." # Placeholder
                routing_state['_dm_context_captured'] = True 

            if not routing_state['is_routed']:
                dm_response_for_routing = response 

                next_template_file = ""
                
                if "ENEMY" in dm_response_for_routing.upper():
                    next_template_file = ENEMY_TEMPLATE_NAME
                    new_agent_display_name = "Enemy"
                    print("\n>>> System: DM indicated ENEMY. Switching to combat agent...\n")
                else:
                    next_template_file = NPC_TEMPLATE_NAME
                    new_agent_display_name = "NPC"
                    print("\n>>> System: DM indicated NPC. Switching to social agent...\n")

                next_template_path = os.path.join(root_path, "lab04", next_template_file)
                
                new_encounter_agent = AgentTemplate.from_file(
                    next_template_path, 
                    context=dm_response_for_routing,
                    summary=routing_state['encounter_summary']
                )
                
                chat = new_encounter_agent 
                
                routing_state['is_routed'] = True 
                routing_state['current_role_name'] = new_agent_display_name

                response = chat.start_chat() 

                print(f"--- Encounter with {new_agent_display_name} Started! ---")
                print(f"{new_agent_display_name}: {response}\n") 
                
            else:
                routing_state['encounter_summary'] = \
                    f"Player's last action: '{user_input_text}'. {routing_state['current_role_name']}'s previous response was: '{response[:50]}...'"

                response = chat.send(user_input_text)
            # But before here.
        except StopIteration as e:
            break

if __name__ ==  '__main__':
    # Add code here to start DM chat
    dm_json_path = os.path.join(root_path, "lab04", DM_TEMPLATE_NAME)
    
    if not os.path.exists(dm_json_path):
        print(f"Error: DM template not found at {os.path.abspath(dm_json_path)}")
        sys.exit(1)

    adventure_options_for_dm = "a social meeting with a friendly merchant (NPC) or an ambush by a bridge troll (ENEMY)"
    run_console_chat(dm_json_path, agent_name='Dungeon Master', encounters=adventure_options_for_dm)

    # But before here.
    pass