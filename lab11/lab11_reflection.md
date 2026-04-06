1. Compare the MCP + LangGraph approach to Lab 05's manual tool calling. What work does LangGraph remove? What are the advantages of using a standardized protocol like MCP?

For this lab, we used LangChain. It removed the work of:
    1. Writing schemas for the tool calling. It is handled autoamtically.
    2. Calling the tools manually.
    3. Parsing the LLM response to detect tool call requests.
And the advantages for using LangChain:
    1. Tools will be automatically discovered and used so we do not need to define it on the client side.
    2. We can add, swap and modify tools without modifying the client or the agent code.
    3. It is compatible with multiple clients like Python or Java as is.

2. Describe one specific way MCP could enhance your final DnD Dungeon Master project. Be specific about which tools you would create.

I would use all the tools used in this lab, that is, roll_dice, get_character_stat and calculate_damage. I would also add more tools to update the stats of a player (update_stat), finalize the damage dealt to a player/enemy (damage_final) and also a tool to create and add an enemy to the enemy list (create_enemy), alongside some others.

3. Copy the output from the demo client showing the protocol messages.

Output:
============================================================
Lab 11: MCP + LangGraph Integration
============================================================

Connecting to MCP server: mcp_server.py
[OK] Connected to MCP server!

Found 3 tools:
  - roll_dice: Roll n_dice dice with the given number of sides, plus a modifier.

TODO:
- Roll each die using random.randint(1, sides)
- Sum the rolls and add the modifier
- Return a message like "Rolled 3d6+2: [4, 2, 5] + 2 = 13"
  - get_character_stat: Look up a character's stat from the CHARACTERS dict.

TODO:
- Normalize character and stat to lowercase
- Look up the character in CHARACTERS
- Return the stat value, e.g. "Fighter's strength is 16"
- Handle invalid character/stat names gracefully
  - calculate_damage: Calculate damage dealt based on attack roll vs armor class.

TODO:
- If attack_roll >= armor_class, the attack hits (return base_damage info)
- Otherwise, the attack misses (0 damage)
- Return a descriptive message

------------------------------------------------------------
Chat with the DnD assistant (type 'quit' to exit)
Try: 'Roll a d20 for an attack' or 'What is the fighter's strength?'
------------------------------------------------------------

You: Roll a d20 for an attack

Assistant: You rolled a 20 on your d20 attack roll. Would you like to add any additional effects, such as damage or ability checks?

You: Show the fighter's strength stat

Assistant: Is there anything else I can help you with, such as calculating damage or assisting with a specific encounter?  

You: quit
Goodbye!