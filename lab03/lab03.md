# Prompt Engineering Process
Intention:
Prevent the dungeon master from being passive and asking the player to narrate the scene.

Action/Change:
I added explicit instructions to guide the player through a world of fantasy and magic and forcefully move the story along. I believed this would make the agent take responsibility for the environment and npc dialogue.

Result:
The agent successfully described atmospheric locations like the taverns of oakhaven using sensory details like woodsmoke and stale ale without asking the player for help.

Reflection/Analysis of the result:
This worked because the instructions provided a clear job description for the model. However the 270m model size still limited its vocabulary leading it to repeat specific phrases like metallic scent across different environments.

Intention:
Prevent the dungeon master from acting like an helpful companion to the player.

Action/Change:
I changed the rules to include that the dungeon master is only an observer and should only describe what the player sees and does. I also added that it should not help the player in any way.

Result:
The dungeon master built on the story based on the player prompts and proceeded to provide a decently interactive session, but still occasionally repeated a few sentences.

Reflection/Analysis of the result:
The change did its purpose and the dm objectively described every situation. However, due to the rule of "do not help the player in any way", the dm seemed to leave everything up to the player and did not describe the situation in a way where the player could infer some kind of hint to proceed.

Intention:
Ensure that combat encounters are dynamic and have a clear conclusion.

Action/Change:
I increased the temperature of the model to 1. I believed these changes would stop the agent from repeating the same battle description and allow for more creative battle scenes.

Result:
Combat became more interactive and the model recognized tactical moves like slashing at feet or dodging strikes. However the monster became immortal and continued to do things it should not have been able to do, such as staring at the player despite being beheaded.

Reflection/Analysis of the result:
The change worked for tactical variety but failed on logic. The small model has a high internal probability for combat tokens like staring or rage which seems to override the logical state of being dead or beheaded.

