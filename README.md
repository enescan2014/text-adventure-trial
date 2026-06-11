# text-adventure-trial
Text dungeon game
I made a text input adventure game where you can explore a haunted castle, fight enemies, collect items and try find an Ancient Crown - like a treasure hunt :). Everything happens in the terminal, couldnt add graphics yet, you need to use your imagination. Can be boring but I was inspired by really really old dungeon games.

What is it about?

- You move through 5 rooms which are : Entrance, Courtyard, Dungeon, Garden and Throne Room
-Each room may have an " item that you can pick up" like potions, a magic sword, a key etc.
-2 rooms contain enemy so you fight them in turns
-Your goal is to reach the Throne Room, defeat the Dark King and take the Ancient Crown
-There is a score, not perfect but it is tracked based on rooms explored, items taken and enemies beaten

YOU SHOULD RUN IT IN TERMINAL
  like Jupyter Notebook, type %run lost_kingdom.py and run the cell or VS Code better.

COMMANDS (means text you type, and what it does): 
1. go north - Move north or south or east or west
2. take - Pick up the item from the room you are in
3. use potion - Drink a health potion from your bag
4. inventory - You can take a look what you have
5. help - to show tihs command list
6. quit - to exit

CODING RELATED:
I used Dictionaries. The entire game world lives in ROOMS, a dictionary where each key is a room name and the value is another dictionary with its description, exits, item, and enemy. I think this is clean code.
All the code is tied to a while loop - health should be > 0. You win / die, loop stops.
I used Functions, each part of the game has its own function, do_combat(), explore_room(), show_status() etc. 
I used some AI help on string methods like action.startswith("go ") - need some more practice.

CORRECTIONS MADE:
At first I had a separate defeated_enemies list, but after you kill enemies and when you leave the room and comeback, enemies were still there - so I stored the enemies inside the room Dictionary (this is why Dictionary is good). I set ROOMS[room]["enemy"]=NONE. so it stays defeated if you come back. 

dict(room["enemy"]) creates a copy of the enemy dictionary if I didn't copy it, the health I reduced during combat would be saved permanently and the enemy would always start with 0 HP on entering again.
