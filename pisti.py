from time import sleep
import os

print(r"""
.------..------..------..------..------.
|P.--. ||I.--. ||S.--. ||T.--. ||I.--. |
| :/\: || (\/) || :/\: || :/\: || (\/) |
| (__) || :\/: || :\/: || (__) || :\/: |
| '--'P|| '--'I|| '--'S|| '--'T|| '--'I|
`------'`------'`------'`------'`------'
""")

print("-------------------Welcome to the Pisti Point Calculator-------------------\n")

def get_input(prompt):
    val = input(prompt)
    if val.lower() == 'b':
        raise RestartRoundException()
    return int(val)

class RestartRoundException(Exception):
    pass

while True:
    try:
        num_players = int(input("How many players? (2 or 4): "))
        if num_players in [2, 4]:
            break
        print("Please enter 2 or 4.")
    except ValueError:
        print("Invalid number.")

is_team = False
if num_players == 4:
    while True:
        mode = input("Game Mode: (1) Individual, (2) Team: ")
        if mode == '1':
            break
        elif mode == '2':
            is_team = True
            break
        print("Invalid choice.")

max_points = 0
while max_points <= 0:
    try:
        max_points = int(input("Enter max points (e.g., 51, 81, 101): "))
    except ValueError:
        print("Enter a number.")

names = []
points = []
for i in range(num_players):
    names.append(input(f"Enter name for Player {i+1}: "))
    points.append(0)

round_num = 1
while True:
    try:
        print(f"\n--- Round {round_num} ---")
        
        round_jokers = 0
        round_aces = 0
        
        current_round_points = [0] * num_players
        for i in range(num_players):
            print(f"\nStats for {names[i]}:")
            
            while True:
                try:
                    j = get_input("  Jokers collected (0-4): ")
                    if 0 <= j <= 4:
                        if round_jokers + j > 4:
                             print("  Error: Total jokers cannot exceed 4.")
                        else:
                            current_round_points[i] += j
                            round_jokers += j
                            break
                    else:
                        print("  0-4 only.")
                except ValueError:
                    print("  Enter a number.")
            
            while True:
                try:
                    a = get_input("  Aces collected (0-4): ")
                    if 0 <= a <= 4:
                        if round_aces + a > 4:
                            print("  Error: Total aces cannot exceed 4.")
                        else:
                            current_round_points[i] += a
                            round_aces += a
                            break
                    else:
                         print("  0-4 only.")
                except ValueError:
                     print("  Enter a number.")
            
            while True:
                try:
                    p = get_input("  Pistis made: ")
                    if p >= 0:
                        current_round_points[i] += p * 10
                        break
                    print("  Cannot be negative.")
                except ValueError:
                    print("  Enter a number.")

        if round_jokers != 4 or round_aces != 4:
            print("\nWARNING: Total Jokers or Aces != 4.")

        for extra_name, extra_points in [("2 of Clubs", 2), ("10 of Diamonds", 3), ("the most cards", 3)]:
            print(f"Who has {extra_name}?")
            for idx, name in enumerate(names):
                print(f"{idx+1}. {name}")
            while True:
                try:
                    c = get_input("Choice: ")
                    if 1 <= c <= num_players:
                        current_round_points[c-1] += extra_points
                        break
                    print("Invalid choice.")
                except ValueError:
                    print("Enter a number.")

        for i in range(num_players):
            points[i] += current_round_points[i]

        sleep(1)
        print("\n--- Scores ---")
        sleep(1)
        if is_team:
            team1_score = points[0] + points[2]
            team2_score = points[1] + points[3]
            print(f"Team 1 ({names[0]} & {names[2]}): {team1_score}")
            sleep(1)
            print(f"Team 2 ({names[1]} & {names[3]}): {team2_score}")
            
            if team1_score >= max_points and team2_score >= max_points:
                 if team1_score > team2_score:
                     print("Team 1 Wins!")
                     sleep(1)
                     break
                 elif team2_score > team1_score:
                     print("Team 2 Wins!")
                     sleep(1)
                     break
                 else:
                     print("Draw! Go on...")
            elif team1_score >= max_points:
                 print("Team 1 Wins!")
                 sleep(1)
                 break
            elif team2_score >= max_points:
                 print("Team 2 Wins!")
                 sleep(1)
                 break
        else:
            for i in range(num_players):
                print(f"{names[i]}: {points[i]}")
                sleep(0.5)
            
            leaders = []
            for i in range(num_players):
                if points[i] >= max_points:
                    leaders.append((points[i], names[i]))
            
            if leaders:
                leaders.sort(reverse=True)
                if len(leaders) > 1 and leaders[0][0] == leaders[1][0]:
                    print("Draw! Go on...")
                else:
                    print(f"{leaders[0][1]} Wins!")
                    sleep(1)
                    break
        
        print("\nNext Round...")
        round_num += 1

    except RestartRoundException:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Restaring current round...")
        continue