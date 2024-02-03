from os import name

import random
import json


Your_Pv = 150
Your_attack = 5
Your_defense = 4
Your_level = 1
Your_xp = 0
Your_attack_range = 12
xp_to_next_level = 40


Monster_Pv = 50
Monster_attack = 4
Monster_defense = 3
Monster_level = 1


inventory = {
    'Potion' : 3,
    'Attack_Boost' : 2,
    'Defense_Boost' : 2
}

Attack_Boost_Duration = 0
Defense_Boost_Duration = 0

Name = ""

def Create_New_Game():
    global Your_Pv, Your_level, Your_attack, Your_defense, Your_xp, Name
    global Monster_Pv, Monster_attack, Monster_defense, Monster_level
    print("\nStart new game...")

    Name = str(input('Please enter your name: '))
    print(f'Welcome {Name}.')

    print("\nAfter a long year of work, you finally took a break and decided to go on a field trip near the forest.")

    print("\nOut of curiousity, you went to explore the forest which had a few monsters and unfortunately got lost with your backpack containing a few items")
    save_game(Name)
    Monster_level = 1
    Monster_Pv = 50
    Monster_attack = 4
    Monster_defense = 3
    choose_direction()

Monster_defeated = 0
level_5_unlocked = False
level_6_unlocked = False

class Colors:
  RESET = "\033[0m"
  RED = "\033[91m"
  GREEN = "\033[92m"
  YELLOW = "\033[93m"
  BLUE = "\033[94m"
  MAGENTA = "\033[95m"
  CYAN = "\033[96m"
  INDIGO = "\033[97m"
  PURPLE = "\033[98m"

def print_colored(text, color):
    print(f"{color}{text}{Colors.RESET}")

def choose_direction():
    while True:
        print_colored('\nChoose a direction to move to', Colors.BLUE)
        print_colored('1. Go North\n2. Go South\n3. Go East\n4. Go West', Colors.GREEN)
        choice = input('Please choose your direction:  ')

        if choice in {'1', '2', '3', '4'}:
          print(f'\nGo {["North", "South", "East", "West"][int(choice) - 1]}')
          print(f"You moved deeper {['North', 'South', 'East', 'West'][int(choice) - 1]} in the forest")
          enemy_encountered()
        else:
            print("\nError. Option not available")


def enemy_encountered():
    global Monster_Pv, Monster_attack, Monster_defense, Monster_level
    global Monster_defeated, level_5_unlocked, level_6_unlocked
    attacked = random.choice([True, False])

    if attacked:
        Monster_level += 1
        if Monster_level > 6:
          Monster_level = 6
        Monster_Pv = max(50, 50 + (Monster_level - 1) * 50)
        print(f'\nYou have encountered a level {Monster_level} monster!')
        print('Press any key to start the battle...')

        if Monster_level == 6:
          print("\n This is the boss level!")
          input()
          combat_mode()
        else:
          input()
          combat_mode()

        Monster_defeated += 1
        if Monster_defeated == 4 and Monster_level == 5:
          level_5_unlocked = True
          print("\n You sense a stronger presence in the forest. Level 5 monsters are now appearing!")

        elif Monster_defeated == 1 and Monster_level == 6 and level_5_unlocked:
          level_6_unlocked = True
          print("\n A powerful aura surrounded the forest. The level 6 monsters are now appearing!")

    else:
        print('\nYou are safe! Do you want to explore deeper?')

exit_game = False

def save_game_and_exit():
    global Your_Pv, Monster_Pv, exit_game
    print("\nGame saved. Do you want to exit the game?")
    user_input = input("Type 'yes' to exit or any other key to return to the main menu: ")

    if user_input.lower() == 'yes':
        print("Returning to the main menu.")
        save_game(Name)
        exit_game = False
        main()

    elif user_input.lower() == 'no':
      print("\n Continuing the game!")
      return
    else:
        print("Error. Returning to the main menu.")
        main()


def combat_mode():
    global exit_game, Attack_Boost_Duration, Defense_Boost_Duration
    global Your_attack, Your_defense, Your_level, Your_Pv, Your_xp
    global Monster_attack, Monster_defense, Monster_level, Monster_Pv
    global inventory, xp_to_next_level

    original_defense = Your_defense

    print_colored(f"\nYou start the batle with a level {Monster_level} monster", Colors.PURPLE)

    while Your_Pv > 0 and Monster_Pv > 0 and not exit_game:
      Your_attack = random.randint(1, 12)
      Monster_attack = random.randint(1, 10)
      print_colored(f"\n Your level: {Your_level}  | Your xp: {Your_xp}/{xp_to_next_level}  | Your Pv:  {Your_Pv}", Colors.GREEN)
      print_colored(f"Monster PV: {Monster_Pv} |  Monster level: {Monster_level}  ", Colors.RED)

      if Attack_Boost_Duration > 0:
        Your_attack += 10
        Attack_Boost_Duration -= 1

      if Defense_Boost_Duration > 0:
        Your_defense += 10
        Defense_Boost_Duration -= 1


      print_colored('\nWhat do you want to do', Colors.MAGENTA)
      print('1. Attack with Chucks Nunchucks')
      print('2. Attack with Nokia 3310')
      print('3. Use an object from inventory')
      print('4. Run')
      print('5. Save and exit')

      choice = input('\n Choose what you want to do: ')

      if choice == '1' or choice == '2':
          player_attack_result = attack(min(Your_attack, 10 + (Your_level - 1) * 10), Monster_defense)
          if player_attack_result > 0:
                  print_colored(f"You dealt {player_attack_result} damage to the monster!", Colors.RED)
                  Monster_Pv -= player_attack_result
      elif choice == '3':
                print_colored('\nChoose what you want from your inventory', Colors.INDIGO)
                item()
      elif choice == '4':
                print('\nYou chose to run. Good decision!')
                choose_direction()

      elif choice == '5':
         save_game_and_exit()
      else:
                print_colored('\nError. Option not found', Colors.RED)



      monster_attack_result = attack(min(Monster_attack, 10 + (Monster_level - 1) * 10), Your_defense)
      if monster_attack_result > 0:
                print_colored(f"The monster dealt {monster_attack_result} damage to you!", Colors.PURPLE)
                Your_Pv -= monster_attack_result
      else:
                print_colored("The monster's attack missed!", Colors.PURPLE)

    Your_defense = original_defense

    if  Your_Pv<= 0:
          print_colored("You were defeated. Game over.", Colors.RED)
          main()
          Exit()
          exit_game = True
    elif not exit_game:
          print_colored(f"You defeated the level {Monster_level} monster!", Colors.CYAN)
          gain_xp(20)
          check_level_up()
          choose_direction()

def attack(attackers_attack, defenders_defense):

  damage = max(0, attackers_attack - defenders_defense + random.randint(1, 20))
  return damage

def item():
    global Your_Pv, Your_attack, Your_defense, inventory, Attack_Boost_Duration, Defense_Boost_Duration
    print_colored("\n Inventory:", Colors.MAGENTA)
    print_colored(f" 1. Potion ({inventory.get('Potion', 0)})", Colors.GREEN)
    print_colored(f" 2. Attack Boost ({inventory.get('Attack_Boost', 0)})", Colors.GREEN)
    print_colored(f" 3. Defense Boost ({inventory.get('Defense_Boost', 0)})", Colors.GREEN)
    print_colored(" 4. Go back", Colors.GREEN)

    Option = input("Choose an option:")

    if Option == '1':
        if 'Potion' in inventory and inventory['Potion'] > 0:
            Your_Pv += 30
            inventory['Potion'] -= 1
            print_colored("\nYou decided to drink the potion to increase your HP by 30", Colors.BLUE)
            print_colored(f"Now you have {inventory.get('Potion', 0)} Potion(s) left.", Colors.BLUE)
        else:
            print_colored("\nYou don't have any potion", Colors.RED)

    elif Option == '2':
        if 'Attack_Boost' in inventory and inventory['Attack_Boost'] > 0:
            Your_attack += 20
            Attack_Boost_Duration = 2
            inventory['Attack_Boost'] -= 1
            print("\nYou chose to use an attack boost")
            print(f"Now you have {inventory.get('Attack_Boost', 0)} Attack Boost(s) left.")
        else:
            print("\nYou don't have any attack boost left")

    elif Option == '3':
        if 'Defense_Boost' in inventory and inventory['Defense_Boost'] > 0:
            Your_defense += 5
            Defense_Boost_Duration = 2
            inventory['Defense_Boost'] -= 1
            print("\nYou chose to use a defense boost")
            print(f"Now you have {inventory.get('Defense_Boost', 0)} Defense Boost(s) left.")
        else:
            print("\nYou don't have any defense boost left")

    elif Option == '4':
        print("\nYou chose to go back")
        return

    else:
        print_colored("\nError. Try a different option", Colors.RED)


def gain_xp(xp_amount):
    global Your_xp, xp_to_next_level
    Your_xp += xp_amount
    print(f"\n You gained {xp_amount} xp")


def check_level_up():
    global Your_Pv, Your_level, Your_attack, Your_defense, xp_to_next_level, Your_attack_range
    if Your_xp >= xp_to_next_level:
      Your_level += 1
      Your_Pv += 20
      Your_attack +=5
      Your_defense += 3
      xp_to_next_level += 80
      Your_attack_range += 12
      print(f"\n Congratulation! You reached level {Your_level}")
      print(f"\n You now have a Pv of {Your_Pv}, and an attack of {Your_attack}, and a defense of {Your_defense}")
      print(f"\n Your attack range is now {Your_attack_range}")
      print(f"\n You still need {xp_to_next_level - Your_xp}xp to reach the next level")

def save_game(Player_name):
      global Your_Pv, Monster_Pv,Monster_level, Your_level, Your_xp, xp_to_next_level

      file_name = f"{Player_name}_save_game.json"
      game_data = {
        "Your_Pv": Your_Pv,
        "Monster_Pv": Monster_Pv,
        "Monster_level": Monster_level,
        "Your_level": Your_level,
        "Your_xp": Your_xp,
        "xp_to_next_level": xp_to_next_level
    }

      with open(file_name, 'w') as file:
        json.dump(game_data, file)

      print(f"\nGame saved as {file_name}")

def load_game(file_name):
    global Your_Pv, Monster_Pv, Monster_level, Your_level, Your_xp, xp_to_next_level

    try:
        with open(file_name, 'r') as file:
            game_data = json.load(file)

            Your_Pv = game_data["Your_Pv"]
            Monster_Pv = game_data["Monster_Pv"]
            Monster_level = game_data["Monster_level"]
            Your_level = game_data["Your_level"]
            Your_xp = game_data["Your_xp"]
            xp_to_next_level = game_data["xp_to_next_level"]

            print("Game loaded successfully!")

    except FileNotFoundError:
        print("Save file not found. Unable to load game.")
    except Exception as e:
        print(f"An error occurred while loading the game: {str(e)}")
    combat_mode()

def Load_Saved_Game():
    print("\nLoading saved game...")
    player_name = str(input('Please enter your name: '))
    saved_file_name = f"{player_name}_save_game.json"

    try:
        load_game(saved_file_name)
        print(f'Welcome back, {player_name}!')
        return
    except:
        pass

    print("\nStart new game...")
    print(f'Welcome {player_name}.')
    combat_mode()


def About():
    print_colored("\nAbout the Game:", Colors.RED)
    print_colored("Welcome to the Forest Adventure!", Colors.BLUE)
    print_colored("In this text-based game, you embark on a journey through a mysterious forest filled with monsters.", Colors.BLUE)
    print_colored("Your goal is to navigate through the forest, defeat monsters, and level up to become a true adventurer.", Colors.BLUE)
    print_colored("Beware of powerful bosses and unexpected challenges as you progress!", Colors.BLUE)

    print_colored("\nSpecial Features:", Colors.BLUE)
    print_colored("- Engage in turn-based combat with various monsters.", Colors.BLUE)
    print_colored("- Discover and use items from your inventory to boost your stats.", Colors.BLUE)
    print_colored("- Unlock new levels and face stronger foes as you progress.", Colors.BLUE)
    print_colored("- Save your game at any time and continue your adventure later.", Colors.BLUE)

    print_colored("\nInstructions:", Colors.RED)
    print_colored("1. Choose directions to move through the forest.", Colors.BLUE)
    print_colored("2. Encounter monsters and engage in combat.", Colors.BLUE)
    print_colored("3. Use items wisely and strategize to defeat tough opponents.", Colors.BLUE)
    print_colored("4. Save your game with 'Save and Exit' to continue later.", Colors.BLUE)
    print_colored("5. Have fun and become the ultimate forest adventurer!", Colors.BLUE)

    print_colored("\nAcknowledgments:", Colors.RED)
    print_colored("This game was developed by NGANKAM NANCY ETHAN, BEN CHEIKH Mehdi and DEVADEVAN Ashwin.", Colors.RED)

def main():
    global exit_game
    while not exit_game:
        print("Main menu:")
        print("1. Create New Game")
        print("2. Load Saved Game")
        print("3. About")
        print("4. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            Create_New_Game()
        elif choice == '2':
            Load_Saved_Game()
        elif choice == '3':
            About()
        elif choice == '4':
            Exit()
        else:
            print("Error. Option not found")
def Exit():
    global exit_game
    print("Thank you for playing!")
    exit_game = True



if __name__ == "__main__":
    main()