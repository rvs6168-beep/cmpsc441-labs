import os
import sys

root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_path)

from util.llm_utils import AgentTemplate

def run_console_chat(dm_agent):
    print("\n>>> [System] Contacting the Dungeon Master...\n")
    
    dm_response = dm_agent.start_chat() 
    print(f"[Dungeon Master]: {dm_response}\n")

    if "ENEMY" in dm_response.upper() or "FIGHT" in dm_response.upper():
        next_template = "lab04_enemy.json"
        print(">>> System: Routing to ENEMY encounter...\n")
    else:
        next_template = "lab04_npc.json"
        print(">>> System: Routing to NPC encounter...\n")

    next_path = os.path.join(root_path, "lab04", next_template)
    
    current_summary = "The encounter has just begun."
    encounter_agent = AgentTemplate.from_file(
        next_path, 
        context=dm_response, 
        summary=current_summary
    )

    agent_message = encounter_agent.start_chat()
    print(f"--- Encounter Started ---")
    print(f"Agent: {agent_message}\n")

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