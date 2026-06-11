"""
The Lost Kingdom - A Text Adventure Game
Run with: python lost_kingdom.py
"""

import time
import os

# The entire game world stored in one dictionary
ROOMS = {
    "entrance": {
        "description": "You stand at the entrance of an old castle. Torches flicker on stone walls.",
        "exits": {"north": "courtyard", "east": "dungeon"},
        "item": "key",
        "enemy": None,
    },
    "courtyard": {
        "description": "A wide open courtyard. A dry, cracked fountain sits in the middle. Ravens flying above.",
        "exits": {"south": "entrance", "north": "throne_room", "east": "garden"},
        "item": "health_potion",
        "enemy": None,
    },
    "dungeon": {
        "description": "Dark and damp. Something moves in the shadows. The smell of old stuff fills the air.",
        "exits": {"west": "entrance"},
        "item": "magic_sword",
        "enemy": {"name": "Skeleton Guard", "health": 30, "attack": 10},
    },
    "garden": {
        "description": "An overgrown garden. Strange blue mushroom things glow between the weeds.",
        "exits": {"west": "courtyard"},
        "item": "glowing_mushroom",
        "enemy": None,
    },
    "throne_room": {
        "description": "The grand throne room. Gold paint peels from the walls. A dark figure sits on the throne.",
        "exits": {"south": "courtyard"},
        "item": "ancient_crown",
        "enemy": {"name": "Dark King", "health": 60, "attack": 20},
    },
}

ITEMS = {
    "key": {"name": "Rusty Key",       "type": "key",     "value": 0},
    "health_potion": {"name": "Health Potion",   "type": "heal",    "value": 30},
    "magic_sword": {"name": "Magic Sword",     "type": "weapon",  "attack": 25},
    "glowing_mushroom":{"name": "Glowing Mushroom","type": "heal",    "value": 15},
    "ancient_crown":   {"name": "Ancient Crown",   "type": "treasure","value": 200},
}


def clear_screen():
    os.system("cls" if os.name == "nt" 
              else "clear")


def divider():
    print("-" * 52)


def create_player(name):
    return {
        "name": name,
        "health": 100,
        "max_health": 100,
        "attack": 15,
        "inventory": [],
        "current_room": "entrance",
        "score": 0,
    }


def show_status(player):
    divider()
    hp_bar = ("█" * (player["health"] // 10)).ljust(10)
    print(f"  {player['name']}  |  HP [{hp_bar}] {player['health']}/100  |  Score: {player['score']}")
    if player["inventory"]:
        names = [ITEMS[i]["name"] for i in player["inventory"]]
        print(f"  Bag: {', '.join(names)}")
    divider()


def do_combat(player, enemy):
    """This is the combat loop per turn. Returns True (win), False (fled), None (died)."""
    print(f"\n  A {enemy['name']} blocks your way!")
    enemy_hp = enemy["health"]

    while player["health"] > 0 and enemy_hp > 0:
        """Printing the HP of player"""
        print(f"\n  {enemy['name']} HP: {enemy_hp}  |  Your HP: {player['health']}")
         """Options to input in terminal"""
        print("  1) Attack   2) Use Potion   3) Run away")
        choice = input("  > ").strip()

        if choice == "1":
            dmg = ITEMS["magic_sword"]["attack"] if "magic_sword" in player["inventory"] else player["attack"]
            enemy_hp -= dmg
            print(f"  You deal {dmg} damage!")
            if enemy_hp > 0:
                player["health"] -= enemy["attack"]
                print(f"  {enemy['name']} hits you for {enemy['attack']}! HP: {player['health']}")

        elif choice == "2":
             """Drink potion or mushroom to recover if have them"""
            if "health_potion" in player["inventory"]:
                heal = ITEMS["health_potion"]["value"]
                player["health"] = min(player["max_health"], player["health"] + heal)
                player["inventory"].remove("health_potion")
                  print(f"  You drink a potion and recover {heal} HP! HP: {player['health']}")
            elif "glowing_mushroom" in player["inventory"]:
                heal = ITEMS["glowing_mushroom"]["value"]
                player["health"] = min(player["max_health"], player["health"] + heal)
                player["inventory"].remove("glowing_mushroom")
                print(f"  You eat the mushroom and recover {heal} HP!")
            else:
                print("  You have no healing items!")

        elif choice == "3":
            print("  You run away!")
            return False
        else:
            print("  Unknown command.")

    if player["health"] <= 0:
        return None  # player died

    print(f"\n  You defeated the {enemy['name']}! (+50 points)")
    player["score"] += 50
    return True

 """ROOMS Dictionary"""
def explore_room(player):
    room = ROOMS[player["current_room"]]
    room_name = player["current_room"].replace("_", " ").title()
    print(f"\n  Location: {room_name}")
    print(f"  {room['description']}")

    if room["item"]:
        print(f"\n  You notice a {ITEMS[room['item']]['name']} on the ground.")

    exits = list(room["exits"].keys())
    print(f"  Exits: {', '.join(exits)}")
    return room


def game_loop():
    print("=" * 52)
    print("        THE LOST KINGDOM")
    print("        A Text Adventure Game")
    print("=" * 52)
    print("\n  The Ancient Crown has been stolen by the Dark King.")
    print("  Only a brave adventurer can reclaim it...\n")

    name = input("  Enter your name, adventurer: ").strip() or "Hero"
    player = create_player(name)

    print(f"\n  Welcome, {name}! Find the Ancient Crown to win!")
    print("  Type 'help' for a list of commands.\n")
    time.sleep(1)

    running = True
    while running and player["health"] > 0:
        show_status(player)
        room = explore_room(player)

        # Handle enemy encounter
        if room["enemy"]:
            result = do_combat(player, dict(room["enemy"]))  # copy so HP resets on re-enter
            if result is None:
                print("\n  You have fallen in battle... GAME OVER.")
                print(f"  Final score: {player['score']}")
                return
            elif result is True:
                ROOMS[player["current_room"]]["enemy"] = None  # enemy stays defeated

        if player["health"] <= 0:
            print("\n  You have fallen in battle... GAME OVER.")
            break

        # Player turn
        print()
        action = input("  What do you do? > ").strip().lower()

        if action == "help":
            print("\n  Commands:")
            print("    go [north/south/east/west]  — move to another room")
            print("    take                        — pick up the item in this room")
            print("    use [potion/mushroom]       — use a healing item")
            print("    inventory                   — check your bag")
            print("    quit                        — exit the game")

        elif action.startswith("go "):
            direction = action[3:].strip()
            if direction in room["exits"]:
                player["current_room"] = room["exits"][direction]
                player["score"] += 5
                print(f"  You head {direction}...")
            else:
                print("  You can't go that way!")

        elif action == "take":
            if room["item"]:
                key = room["item"]
                player["inventory"].append(key)
                print(f"  You picked up the {ITEMS[key]['name']}! (+10 points)")
                player["score"] += 10
                ROOMS[player["current_room"]]["item"] = None

                if key == "ancient_crown":
                    print("\n  *** YOU FOUND THE ANCIENT CROWN! ***")
                    print(f"  *** YOU WIN! Final Score: {player['score']} ***")
                    running = False
            else:
                print("  There is nothing to take here.")

        elif action.startswith("use "):
            target = action[4:].strip()
            used = False
            for inv_item in list(player["inventory"]):
                if target in inv_item:
                    if ITEMS[inv_item]["type"] == "heal":
                        heal = ITEMS[inv_item]["value"]
                        player["health"] = min(player["max_health"], player["health"] + heal)
                        player["inventory"].remove(inv_item)
                        print(f"  You used {ITEMS[inv_item]['name']} and recovered {heal} HP!")
                        used = True
                    else:
                        print(f"  You can't use the {ITEMS[inv_item]['name']} here.")
                        used = True
                    break
            if not used:
                print("  You don't have that item.")

        elif action == "inventory":
            if player["inventory"]:
                print("  Your bag contains:")
                for i in player["inventory"]:
                    print(f"    - {ITEMS[i]['name']}")
            else:
                print("  Your bag is empty.")

        elif action == "quit":
            print(f"  Thanks for playing! Score: {player['score']}")
            running = False

        else:
            print("  I don't understand that. Type 'help' for commands.")


if __name__ == "__main__":
    game_loop()
