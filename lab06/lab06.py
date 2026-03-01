"""
Lab 06: Structured Output with Pydantic and Ollama

This lab demonstrates how to use Pydantic models with Ollama's `format`
parameter to get structured, validated JSON output from an LLM.
"""

from typing import List

import ollama
from pydantic import BaseModel, Field


MODEL = "llama3.2:latest"


# ============================================================================
# Pydantic Models (provided -- do not modify)
# ============================================================================

class AbilityScores(BaseModel):
    strength: int = Field(..., ge=1, le=20, description="Strength score")
    dexterity: int = Field(..., ge=1, le=20, description="Dexterity score")
    constitution: int = Field(..., ge=1, le=20, description="Constitution score")
    intelligence: int = Field(..., ge=1, le=20, description="Intelligence score")
    wisdom: int = Field(..., ge=1, le=20, description="Wisdom score")
    charisma: int = Field(..., ge=1, le=20, description="Charisma score")


class CharacterSheet(BaseModel):
    name: str = Field(..., min_length=1, description="Character name")
    race: str = Field(..., min_length=1, description="Character race, e.g. Elf, Dwarf, Human")
    char_class: str = Field(..., min_length=1, description="Character class, e.g. Wizard, Fighter, Rogue")
    level: int = Field(..., ge=1, le=20, description="Character level")
    ability_scores: AbilityScores
    hit_points: int = Field(..., ge=1, description="Maximum hit points")
    backstory: str = Field(..., min_length=1, description="Brief character backstory")


class MonsterStats(BaseModel):
    name: str = Field(..., min_length=1, description="Monster name")
    monster_type: str = Field(..., min_length=1, description="Monster type, e.g. Undead, Beast, Dragon")
    challenge_rating: float = Field(..., ge=0, le=30, description="Challenge rating")
    hit_points: int = Field(..., ge=1, description="Hit points")
    armor_class: int = Field(..., ge=1, le=30, description="Armor class")
    abilities: List[str] = Field(..., min_length=1, description="List of special abilities")
    description: str = Field(..., min_length=1, description="Physical description of the monster")


class Encounter(BaseModel):
    title: str = Field(..., min_length=1, description="Encounter title")
    setting: str = Field(..., min_length=1, description="Description of where the encounter takes place")
    monsters: List[MonsterStats] = Field(..., min_length=1, description="Monsters in this encounter")
    difficulty: str = Field(..., description="Encounter difficulty: Easy, Medium, Hard, or Deadly")
    treasure: List[str] = Field(default_factory=list, description="Possible treasure rewards")
    narrative_hook: str = Field(..., min_length=1, description="Story hook that leads into this encounter")


# ============================================================================
# Functions to implement
# ============================================================================

def generate_character(description: str) -> CharacterSheet:
    """
    Generate a D&D character sheet from a natural language description.

    Use ollama.chat() with the `format` parameter to get structured output.
    The format parameter should be set to CharacterSheet.model_json_schema().

    Steps:
        1. Call ollama.chat() with:
           - model: MODEL
           - messages: a system message instructing the LLM to create a D&D
             character, and a user message containing the description
           - format: the JSON schema from CharacterSheet
        2. Parse the response with CharacterSheet.model_validate_json()
        3. Return the CharacterSheet instance

    Refer to the Ollama Python API for more information:
    https://github.com/ollama/ollama-python

    Args:
        description: A natural language description of the desired character,
                     e.g. "A wise old elven wizard who studied at the Arcane Academy"

    Returns:
        A validated CharacterSheet instance
    """
    character_response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "Create a DND character using the user description provided. This DND character will be used the the player (user). Generate different name and background everytime to keep things unique."
             },
             {
                 "role": "user",
                 "content": description
             }
             ],
        format=CharacterSheet.model_json_schema()
    )
    character_result = CharacterSheet.model_validate_json(character_response.message.content)
    return character_result
    pass


def generate_monster(concept: str) -> MonsterStats:
    """
    Generate D&D monster stats from a concept description.

    Use the same structured output pattern as generate_character,
    but with the MonsterStats schema.

    Args:
        concept: A concept for the monster,
                 e.g. "A fire-breathing turtle that lives in volcanic caves"

    Returns:
        A validated MonsterStats instance
    """
    monster_response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "Create a DND monster based on the concept provided. This monster will fight the player (user). Generate different name and background everytime to keep things unique."
             },
             {
                 "role": "user",
                 "content": concept
             }
             ],
        format=MonsterStats.model_json_schema()
    )
    monster_result = MonsterStats.model_validate_json(monster_response.message.content)
    return monster_result
    pass


def generate_encounter(party_level: int, num_monsters: int, theme: str) -> Encounter:
    """
    Generate a complete D&D encounter with nested structured output.

    This function demonstrates nested Pydantic models -- the Encounter model
    contains a list of MonsterStats. The LLM must produce valid JSON for
    the entire nested structure.

    The prompt should instruct the LLM to:
    - Create an encounter appropriate for the given party level
    - Include the requested number of monsters
    - Follow the given theme
    - Set difficulty to exactly one of: Easy, Medium, Hard, or Deadly

    Args:
        party_level: The level of the player party (1-20)
        num_monsters: How many monsters to include in the encounter
        theme: A thematic description, e.g. "undead dungeon", "forest ambush"

    Returns:
        A validated Encounter instance
    """
    encounter_response = ollama.chat(
        model="llama3.2:latest",
        messages=[
            {
                "role": "system",
                "content": f"Create an encounter that is appropriate for a player level of {party_level}, while having exactly {num_monsters} monsters and following the environmental theme of {theme}"
             },
             {
                 "role": "user",
                 "content": f"player level: {party_level}, number of monsters: {num_monsters}, theme: {theme}"
             }
             ],
        format=Encounter.model_json_schema()
    )
    
    encounter_result = Encounter.model_validate_json(encounter_response.message.content)
    return encounter_result


# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    print("=== Generating Character ===")
    character = generate_character("A brave halfling rogue who grew up on the streets")
    print(character.model_dump_json(indent=2))

    print("\n=== Generating Monster ===")
    monster = generate_monster("A shadow wolf that phases through walls")
    print(monster.model_dump_json(indent=2))

    print("\n=== Generating Encounter ===")
    encounter = generate_encounter(party_level=3, num_monsters=2, theme="haunted forest")
    print(encounter.model_dump_json(indent=2))
