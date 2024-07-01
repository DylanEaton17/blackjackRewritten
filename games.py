import random
import time
from colorama import Fore, Style
import typer

type = typer.Type()
ask = typer.Ask()

def red(text):
    return (Fore.RED + text + Fore.WHITE)

def green(text):
    return (Fore.GREEN + text + Fore.WHITE)
            
def magenta(text):
    return (Fore.MAGENTA + text + Fore.WHITE)

def yellow(text):
    return (Fore.YELLOW + text + Fore.WHITE)

def cyan(text):
    return (Fore.CYAN + text + Fore.WHITE)
            
def bright(text):
    return (Style.BRIGHT + text + Style.NORMAL)

def open_quote(text):
    return ("\"" + text)

def close_quote(text):
    return (text + "\"")

def quote(text):
    return ("\"" + text + "\"")

def space_quote(text):
    return ("\"" + text + "\" ")


def rock_paper_scissors():
    options = ["Rock", "Paper", "Scissors"]
    type.fast_clean("Do you choose Rock, Paper, or Scissors? ")
    player_choice = ask.choose_an_option(options)
    cpu_choice = random.choice(options)

    type.suspense_clean("Rock...Paper...Scissors...Shoot!")
    time.sleep(0.5)
    print()
    type.fast("You throw down " + bright(magenta(player_choice)))
    print()
    type.fast("The CPU throws down " + bright(magenta(cpu_choice)))

    print("\n")

    if player_choice == cpu_choice:
        type.fast(bright(cyan(player_choice + " ties " + cpu_choice + ". It's a draw!")))
        winner = "Draw"
    elif ((player_choice == "Rock" and cpu_choice == "Scissors") or
          (player_choice == "Scissors" and cpu_choice == "Paper") or
          (player_choice == "Paper") and cpu_choice == "Rock"):
        type.fast(bright(magenta(player_choice + " beats " + cpu_choice + ". You Win!")))
        winner = "Player"
    else:
        type.fast(bright(red(cpu_choice + " beats " + player_choice + ". You Lose!")))
        winner = "CPU"
    print("\n")
    return winner

def main():
    player_wins = 0
    cpu_wins = 0
    win_count=2

    while True:
        winner = rock_paper_scissors()
        if winner == "Player":
            player_wins += 1
        elif winner == "CPU":
            cpu_wins += 1

        score = str(player_wins) + "-" + str(cpu_wins)
        type.type("Best of " + str((win_count*2)-1) + ": ")
        if player_wins == win_count:
            type.type(bright(yellow("You Win " + score)))
            print("")
            break
        if cpu_wins == win_count:
            type.type(bright(red("The CPU Wins " + score)))
            print("")
            break
        elif player_wins > cpu_wins:
            type.type(bright(magenta("You are winning " + score)))
        elif player_wins < cpu_wins:
            type.type(bright(red("You are losing " + score)))
        elif player_wins == cpu_wins:
            type.type(bright(cyan("Tied " + score)))

        print("\n")
        type.fast("Let's play another round!")
        print()

    if player_wins == win_count:
        type.type(bright(yellow("You have won!")))
    else:
        type.type(bright(red("The CPU has won!")))

if __name__ == "__main__":
    main()