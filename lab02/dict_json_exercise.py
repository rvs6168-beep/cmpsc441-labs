"""
Python Dictionary & JSON Exercise
=================================

This exercise helps you understand complex (nested) dictionaries in Python,
which mirror the structure of JSON data - a common format for APIs and config files.

Learning Objectives:
- Navigate nested dictionaries
- Access and modify values at different levels
- Use dictionary methods (.get(), .keys(), .values(), .items())
- Convert between dictionaries and JSON strings
"""

import json

# ============================================================================
# PART 1: Understanding the Data Structure
# ============================================================================

# Here's a complex dictionary representing a game character inventory system.
# This structure is identical to what you'd see in a JSON file.

game_data = {
    "player": {
        "name": "Aldric",
        "level": 15,
        "class": "Wizard",
        "stats": {
            "health": 85,
            "mana": 150,
            "strength": 12,
            "intelligence": 25
        }
    },
    "inventory": {
        "weapons": [
            {"name": "Staff of Fire", "damage": 45, "element": "fire"},
            {"name": "Crystal Dagger", "damage": 20, "element": "ice"}
        ],
        "potions": [
            {"name": "Health Potion", "effect": "heal", "amount": 50, "quantity": 3},
            {"name": "Mana Potion", "effect": "restore_mana", "amount": 75, "quantity": 5}
        ],
        "gold": 1250
    },
    "quests": {
        "active": [
            {"id": 101, "title": "Defeat the Dragon", "reward": 500},
            {"id": 102, "title": "Find the Lost Tome", "reward": 200}
        ],
        "completed": ["Rescue the Villagers", "Gather Herbs"]
    }
}


# ============================================================================
# PART 2: Accessing Nested Data (Examples)
# ============================================================================

# Example 1: Access a simple nested value
player_name = game_data["player"]["name"]
print(f"Player name: {player_name}")

# Example 2: Access deeply nested value
player_health = game_data["player"]["stats"]["health"]
print(f"Player health: {player_health}")

# Example 3: Access an item in a list within the dictionary
first_weapon = game_data["inventory"]["weapons"][0]
print(f"First weapon: {first_weapon['name']} (Damage: {first_weapon['damage']})")

# Example 4: Using .get() for safe access (returns None if key doesn't exist)
armor = game_data["inventory"].get("armor", "No armor equipped")
print(f"Armor: {armor}")


# ============================================================================
# PART 3: YOUR EXERCISES
# ============================================================================

# TODO Task 1: Get the player's intelligence stat
# Expected output: 25
def get_player_intelligence(data):
    """Return the player's intelligence stat."""
    player_intelligence = data["player"]["stats"]["intelligence"]
    return player_intelligence
    # print(f"Player intelligence: {player_intelligence}")
    pass


# TODO Task 2: Get the total number of health potions
# Expected output: 3
def get_health_potion_count(data):
    """Return the quantity of health potions in inventory."""
    health_potion_count = data["inventory"]["potions"][0]["quantity"]
    return health_potion_count
    # print(f"Health Potions: {health_potion_count}")
    pass


# TODO Task 3: Get a list of all active quest titles
# Expected output: ["Defeat the Dragon", "Find the Lost Tome"]
def get_active_quest_titles(data):
    """Return a list of titles from active quests."""
    active_quests = data["quests"]["active"]
    size = len(active_quests)
    return active_quests
    pass


# TODO Task 4: Calculate total damage from all weapons
# Expected output: 65 (45 + 20)
def calculate_total_weapon_damage(data):
    """Return the sum of damage from all weapons."""
    weapon_list = data["inventory"]["weapons"]
    size = len(weapon_list)
    tracker = 0
    total_weapon_damage = 0
    while (tracker != size):
        total_weapon_damage = total_weapon_damage + weapon_list[tracker]['damage']
        tracker += 1
    return total_weapon_damage
    pass


# TODO Task 5: Add a new potion to the inventory
# Add: {"name": "Stamina Elixir", "effect": "boost_stamina", "amount": 30, "quantity": 2}
def add_potion(data, potion):
    """Add a new potion dictionary to the inventory's potions list."""
    potion_list = data["inventory"]["potions"]
    potion_list.append(potion)
    pass


# TODO Task 6: Update the player's gold after completing a quest
# Increase gold by the reward amount of quest with id 101
def complete_quest_and_get_reward(data, quest_id):
    """
    Find the quest with the given id, add its reward to player's gold,
    and return the new gold total.
    """
    active_quest_list = data["quests"].get("active", "No active quests")
    size = len(active_quest_list)
    tracker = 0
    while (tracker != size):
        if (active_quest_list[tracker]["id"] == quest_id):
            reward_gold = active_quest_list[tracker]["reward"]
            data["inventory"]["gold"] += reward_gold
            return data["inventory"]["gold"]
        tracker += 1
    pass


# ============================================================================
# PART 4: JSON Conversion
# ============================================================================

# Convert dictionary to JSON string (pretty printed)
json_string = json.dumps(game_data, indent=2)
print("\n--- Dictionary as JSON string (first 500 chars) ---")
print(json_string[:500] + "...")

# Convert JSON string back to dictionary
parsed_data = json.loads(json_string)
print(f"\nParsed back - Player name: {parsed_data['player']['name']}")


# TODO Task 7: Write a function that takes a dictionary and returns
# a "pretty" JSON string with 4-space indentation
def to_pretty_json(data):
    """Convert a dictionary to a pretty-printed JSON string with 4-space indent."""
    json_string = json.dumps(data, indent=4)
    return json_string
    pass


# ============================================================================
# PART 5: Run the Examples
# ============================================================================

if __name__ == "__main__":
    print("\nRun tests with: pytest tests/test_dict_json_exercise.py -v")
