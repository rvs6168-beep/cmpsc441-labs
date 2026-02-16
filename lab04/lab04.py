import os
import sys

root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_path)

from util.llm_utils import AgentTemplate


# --- Model and name information ---
sign_your_name = 'Raghav Sandeep Sharavanaan'
model = 'gemma3:270m'


def run_console_chat(dm_agent):
    """
    Orchestrates the DnD experience:
    1. Starts the DM chat to set the scene.
    2. Branches to a new agent based on DM response.
    3. Manages the encounter loop.
    """
    print("\n>>> [System] Contacting the Dungeon Master...\n")
    
    dm_response = dm_agent.start_chat() 
    print(f"[Dungeon Master]: {dm_response}\n")

    # Routing logic: Branch based on keywords in the DM response
    if "ENEMY" in dm_response.upper():
        next_template_name = "lab04_enemy.json"
        print(">>> System: Branching to ENEMY encounter...\n")
    else:
        # Defaulting to NPC for social or ambiguous responses
        next_template_name = "lab04_npc.json"
        print(">>> System: Branching to NPC encounter...\n")


    next_path = os.path.join(root_path, "lab04", next_template_name) 
    encounter_agent = AgentTemplate.from_file(next_path, context=dm_response)

    # Start the encounter chat
    agent_message = encounter_agent.start_chat()
    print(f"--- Encounter Started ---")
    print(f"Agent: {agent_message}\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "/exit", "quit"]:
            break

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