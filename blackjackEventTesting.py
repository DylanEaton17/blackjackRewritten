import story
import random
from colorama import Fore, Back, Style


# Coloring text
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


# Makes the player
def make_player(balance=50, health=100, items=[], statuses=[], dangers=[]):
    player = story.Player()
    player.set_balance(balance)
    player.set_health(health)
    for item in items:
        player.add_item(item)
    for danger in dangers:
        player.add_danger(danger)
    for status in statuses:
        player.add_status(status)
    return player

# Poor Day Tests
def test_seat_cash():
    print(bright(magenta("TESTING SEAT_CASH")))
    player = make_player()
    starting_balance = player.get_balance()
    print(cyan(bright("STARTING CONDITIONS")))
    print(cyan(bright("Balance? " + str(player.get_balance()))))

    print(bright(yellow("EVENT STARTS HERE")))
    player.seat_cash()
    print(bright(yellow("EVENT ENDS HERE")))

    print(cyan(bright("ENDING CONDITIONS")))
    print(cyan(bright("Balance? " + str(player.get_balance()))))
    properties = player.get_balance() > starting_balance
    if properties:
        print(green(bright("EVENT PROPERTIES SATISFIED")))
    else:
        print(red(bright("EVENT PROPERTIES NOT SATISFIED")))
    print("\n")

def test_left_window_down_no_infestation():
    print(bright(magenta("TESTING LEFT_WINDOW_DOWN NO INFESTATION")))
    player = make_player()
    random.seed(2)
    print(cyan(bright("STARTING CONDITIONS")))
    print(cyan(bright("Spider Infestation? " + str(player.has_danger("Spider")))))
    print(cyan(bright("Cockroach Infestation? " + str(player.has_danger("Cockroach")))))

    print(bright(yellow("EVENT STARTS HERE")))
    player.left_window_down()
    print(bright(yellow("EVENT ENDS HERE")))

    print(cyan(bright("ENDING CONDITIONS")))
    print(cyan(bright("Spider Infestation? " + str(player.has_danger("Spider")))))
    print(cyan(bright("Cockroach Infestation? " + str(player.has_danger("Cockroach")))))
    properties = (not player.has_danger("Spider") and not player.has_danger("Cockroach"))
    if properties:
        print(green(bright("EVENT PROPERTIES SATISFIED")))
    else:
        print(red(bright("EVENT PROPERTIES NOT SATISFIED")))
    print("\n")


def test_left_window_down_cockroach_infestation():
    print(bright(magenta("TESTING LEFT_WINDOW_DOWN COCKROACH INFESTATION")))
    player = make_player()
    random.seed(1)
    print(cyan(bright("STARTING CONDITIONS")))
    print(cyan(bright("Spider Infestation? " + str(player.has_danger("Spider")))))
    print(cyan(bright("Cockroach Infestation? " + str(player.has_danger("Cockroach")))))

    print(bright(yellow("EVENT STARTS HERE")))
    player.left_window_down()
    print(bright(yellow("EVENT ENDS HERE")))

    print(cyan(bright("ENDING CONDITIONS")))
    print(cyan(bright("Spider Infestation? " + str(player.has_danger("Spider")))))
    print(cyan(bright("Cockroach Infestation? " + str(player.has_danger("Cockroach")))))
    properties = (not player.has_danger("Spider") and player.has_danger("Cockroach"))
    if properties:
        print(green(bright("EVENT PROPERTIES SATISFIED")))
    else:
        print(red(bright("EVENT PROPERTIES NOT SATISFIED")))
    print("\n")


def test_left_window_down_spider_infestation():
    print(bright(magenta("TESTING LEFT_WINDOW_DOWN SPIDER INFESTATION")))
    player = make_player()
    random.seed(14)
    print(cyan(bright("STARTING CONDITIONS")))
    print(cyan(bright("Spider Infestation? " + str(player.has_danger("Spider")))))
    print(cyan(bright("Cockroach Infestation? " + str(player.has_danger("Cockroach")))))

    print(bright(yellow("EVENT STARTS HERE")))
    player.left_window_down()
    print(bright(yellow("EVENT ENDS HERE")))

    print(cyan(bright("ENDING CONDITIONS")))
    print(cyan(bright("Spider Infestation? " + str(player.has_danger("Spider")))))
    print(cyan(bright("Cockroach Infestation? " + str(player.has_danger("Cockroach")))))
    properties = (player.has_danger("Spider") and not player.has_danger("Cockroach"))
    if properties:
        print(green(bright("EVENT PROPERTIES SATISFIED")))
    else:
        print(red(bright("EVENT PROPERTIES NOT SATISFIED")))
    print("\n")


def test_estranged_dog():
    print(bright(magenta("TESTING ESTRANGED DOG")))
    player = make_player(health=50)
    starting_health = player.get_health()
    print(cyan(bright("STARTING CONDITIONS")))
    print(cyan(bright("Health? " + str(player.get_health()))))

    print(bright(yellow("EVENT STARTS HERE")))
    player.estranged_dog()
    print(bright(yellow("EVENT ENDS HERE")))

    print(cyan(bright("ENDING CONDITIONS")))
    print(cyan(bright("Health? " + str(player.get_health()))))
    properties = player.get_health() > starting_health
    if properties:
        print(green(bright("EVENT PROPERTIES SATISFIED")))
    else:
        print(red(bright("EVENT PROPERTIES NOT SATISFIED")))
    print("\n")


def test_spider_bite():
    print(bright(magenta("TESTING SPIDER BITE")))
    player = make_player(dangers=["Spider"])
    print(cyan(bright("STARTING CONDITIONS")))
    print(cyan(bright("Spider Infestation? " + str(player.has_danger("Spider")))))
    print(cyan(bright("Spider Bite? " + str(player.has_status("Spider Bite")))))

    print(bright(yellow("EVENT STARTS HERE")))
    player.spider_bite()
    print(bright(yellow("EVENT ENDS HERE")))

    print(cyan(bright("ENDING CONDITIONS")))
    print(cyan(bright("Spider Infestation? " + str(player.has_danger("Spider")))))
    print(cyan(bright("Spider Bite? " + str(player.has_status("Spider Bite")))))
    properties = player.has_danger("Spider") and player.has_status("Spider Bite")
    if properties:
        print(green(bright("EVENT PROPERTIES SATISFIED")))
    else:
        print(red(bright("EVENT PROPERTIES NOT SATISFIED")))
    print("\n")

def test_spider_bite_pest_control():
    print(bright(magenta("TESTING SPIDER BITE WITH PEST CONTROL")))
    player = make_player(dangers=["Spider"], items=["Pest Control"])
    print(cyan(bright("STARTING CONDITIONS")))
    print(cyan(bright("Spider Infestation? " + str(player.has_danger("Spider")))))
    print(cyan(bright("Spider Bite? " + str(player.has_status("Spider Bite")))))
    print(cyan(bright("Pest Control? " + str(player.has_item("Pest Control")))))

    print(bright(yellow("EVENT STARTS HERE")))
    player.spider_bite()
    print(bright(yellow("EVENT ENDS HERE")))

    print(cyan(bright("ENDING CONDITIONS")))
    print(cyan(bright("Spider Infestation? " + str(player.has_danger("Spider")))))
    print(cyan(bright("Spider Bite? " + str(player.has_status("Spider Bite")))))
    print(cyan(bright("Pest Control? " + str(player.has_item("Pest Control")))))
    properties = not player.has_danger("Spider") and player.has_status("Spider Bite") and not player.has_item("Pest Control")
    if properties:
        print(green(bright("EVENT PROPERTIES SATISFIED")))
    else:
        print(red(bright("EVENT PROPERTIES NOT SATISFIED")))
    print("\n")


def test_hungry_cockroach():
    print(bright(magenta("TESTING HUNGRY COCKROACH")))
    player = make_player(balance=100, dangers=["Cockroach"])
    starting_balance = 100
    print(cyan(bright("STARTING CONDITIONS")))
    print(cyan(bright("Cockroach Infestation? " + str(player.has_danger("Cockroach")))))
    print(cyan(bright("Balance? " + str(player.get_balance()))))

    print(bright(yellow("EVENT STARTS HERE")))
    player.hungry_cockroach()
    print(bright(yellow("EVENT ENDS HERE")))

    print(cyan(bright("ENDING CONDITIONS")))
    print(cyan(bright("Cockroach Infestation? " + str(player.has_danger("Cockroach")))))
    print(cyan(bright("Balance? " + str(player.get_balance()))))
    properties = player.has_danger("Cockroach") and player.get_balance() < starting_balance
    if properties:
        print(green(bright("EVENT PROPERTIES SATISFIED")))
    else:
        print(red(bright("EVENT PROPERTIES NOT SATISFIED")))
    print("\n")

def test_hungry_cockroach_pest_control():
    print(bright(magenta("TESTING HUNGRY COCKROACH PEST CONTROL")))
    player = make_player(balance=100, dangers=["Cockroach"], items=["Pest Control"])
    starting_balance = 100
    print(cyan(bright("STARTING CONDITIONS")))
    print(cyan(bright("Cockroach Infestation? " + str(player.has_danger("Cockroach")))))
    print(cyan(bright("Balance? " + str(player.get_balance()))))
    print(cyan(bright("Pest Control? " + str(player.has_item("Pest Control")))))


    print(bright(yellow("EVENT STARTS HERE")))
    player.hungry_cockroach()
    print(bright(yellow("EVENT ENDS HERE")))

    print(cyan(bright("ENDING CONDITIONS")))
    print(cyan(bright("Cockroach Infestation? " + str(player.has_danger("Cockroach")))))
    print(cyan(bright("Balance? " + str(player.get_balance()))))
    print(cyan(bright("Pest Control? " + str(player.has_item("Pest Control")))))
    properties = not player.has_danger("Cockroach") and not player.has_item("Pest Control") and (player.get_balance() < starting_balance)
    if properties:
        print(green(bright("EVENT PROPERTIES SATISFIED")))
    else:
        print(red(bright("EVENT PROPERTIES NOT SATISFIED")))
    print("\n")


def test_whats_my_name():
    print("TESTING WHATS_MY_NAME")
    player = make_player()
    print(cyan(bright("STARTING CONDITIONS")))
    print(cyan(bright("Name? " + str(player.get_name()))))

    print(bright(yellow("EVENT STARTS HERE")))
    player.whats_my_name()
    print(bright(yellow("EVENT ENDS HERE")))

    print(cyan(bright("ENDING CONDITIONS")))
    print(cyan(bright("Name? " + str(player.get_name()))))
    properties = player.get_name()!=None
    if properties:
        print(green(bright("EVENT PROPERTIES SATISFIED")))
    else:
        print(red(bright("EVENT PROPERTIES NOT SATISFIED")))
    print("\n")


def test_interrogation():
    print("TESTING INTERROGATION")
    player = make_player()
    print(cyan(bright("STARTING CONDITIONS")))
    print(cyan(bright("Met Interrogator? " + str(player.has_met("Interrogator")))))

    print(bright(yellow("EVENT STARTS HERE")))
    player.interrogation()
    print(bright(yellow("EVENT ENDS HERE")))

    print(cyan(bright("ENDING CONDITIONS")))
    print(cyan(bright("Met Interrogator? " + str(player.has_met("Interrogator")))))
    properties = player.has_met("Interrogator")
    if properties:
        print(green(bright("EVENT PROPERTIES SATISFIED")))
    else:
        print(red(bright("EVENT PROPERTIES NOT SATISFIED")))
    print("\n")

# Poor Night
def test_ditched_wallet():
    print(bright(magenta("TESTING DITCHED_WALLET")))
    player = make_player()
    starting_balance = player.get_balance()
    print(cyan(bright("STARTING CONDITIONS")))
    print(cyan(bright("Balance? " + str(player.get_balance()))))

    print(bright(yellow("EVENT STARTS HERE")))
    player.ditched_wallet()
    print(bright(yellow("EVENT ENDS HERE")))

    print(cyan(bright("ENDING CONDITIONS")))
    print(cyan(bright("Balance? " + str(player.get_balance()))))
    properties = player.get_balance() > starting_balance
    if properties:
        print(green(bright("EVENT PROPERTIES SATISFIED")))
    else:
        print(red(bright("EVENT PROPERTIES NOT SATISFIED")))
    print("\n")


def test_went_jogging():
    random.seed(1)
    print(bright(magenta("TESTING WENT JOGGING")))
    player = make_player(health=50)
    starting_health = player.get_health()
    print(cyan(bright("STARTING CONDITIONS")))
    print(cyan(bright("Health? " + str(player.get_health()))))

    print(bright(yellow("EVENT STARTS HERE")))
    player.went_jogging()
    print(bright(yellow("EVENT ENDS HERE")))

    print(cyan(bright("ENDING CONDITIONS")))
    print(cyan(bright("Health? " + str(player.get_health()))))
    properties = player.get_health() > starting_health
    if properties:
        print(green(bright("EVENT PROPERTIES SATISFIED")))
    else:
        print(red(bright("EVENT PROPERTIES NOT SATISFIED")))
    print("\n")


def test_went_jogging_fell():
    random.seed(0)
    print(bright(magenta("TESTING WENT JOGGING FELL")))
    player = make_player()
    starting_health = player.get_health()
    print(cyan(bright("STARTING CONDITIONS")))
    print(cyan(bright("Health? " + str(player.get_health()))))

    print(bright(yellow("EVENT STARTS HERE")))
    player.went_jogging()
    print(bright(yellow("EVENT ENDS HERE")))

    print(cyan(bright("ENDING CONDITIONS")))
    print(cyan(bright("Health? " + str(player.get_health()))))
    properties = player.get_health() < starting_health
    if properties:
        print(green(bright("EVENT PROPERTIES SATISFIED")))
    else:
        print(red(bright("EVENT PROPERTIES NOT SATISFIED")))
    print("\n")

def test_woodlands_path_deer():
    print(bright(magenta("TESTING WOODLANDS_PATH DEER")))
    player = make_player()
    random.seed(1)
    print(cyan(bright("STARTING CONDITIONS: NONE")))

    print(bright(yellow("EVENT STARTS HERE")))
    player.woodlands_path()
    print(bright(yellow("EVENT ENDS HERE")))

    print(cyan(bright("ENDING CONDITIONS: NONE")))
    properties = True
    if properties:
        print(green(bright("EVENT PROPERTIES SATISFIED")))
    else:
        print(red(bright("EVENT PROPERTIES NOT SATISFIED")))
    print("\n")

def test_woodlands_path_body_no():
    print(bright(magenta("TESTING WOODLANDS_PATH BODY NOT SEARCHED")))
    player = make_player()
    starting_balance = player.get_balance()
    random.seed(6)
    print(cyan(bright("STARTING CONDITIONS")))
    print(cyan(bright("Balance? " + str(player.get_balance()))))
    print(cyan(bright("Hepatitus? " + str(player.has_status("Hepatitus")))))

    print(bright(yellow("EVENT STARTS HERE")))
    player.woodlands_path()
    print(bright(yellow("EVENT ENDS HERE")))

    print(cyan(bright("ENDING CONDITIONS")))
    print(cyan(bright("Balance? " + str(player.get_balance()))))
    print(cyan(bright("Hepatitus? " + str(player.has_status("Hepatitus")))))
    properties = (player.get_balance() == starting_balance) and (not player.has_status("Hepatitus"))
    if properties:
        print(green(bright("EVENT PROPERTIES SATISFIED")))
    else:
        print(red(bright("EVENT PROPERTIES NOT SATISFIED")))
    print("\n")

def test_woodlands_path_body_success():
    print(bright(magenta("TESTING WOODLANDS_PATH BODY SUCCESSFUL SEARCH")))
    player = make_player()
    random.seed(6)
    starting_balance = player.get_balance()
    print(cyan(bright("STARTING CONDITIONS")))
    print(cyan(bright("Balance? " + str(player.get_balance()))))

    print(bright(yellow("EVENT STARTS HERE")))
    player.woodlands_path()
    print(bright(yellow("EVENT ENDS HERE")))

    print(cyan(bright("ENDING CONDITIONS")))
    print(cyan(bright("Balance? " + str(player.get_balance()))))
    properties = player.get_balance() > starting_balance
    if properties:
        print(green(bright("EVENT PROPERTIES SATISFIED")))
    else:
        print(red(bright("EVENT PROPERTIES NOT SATISFIED")))
    print("\n")

def test_woodlands_path_body_fail():
    print(bright(magenta("TESTING WOODLANDS_PATH BODY FAILED SEARCH")))
    player = make_player()
    random.seed(8)
    starting_balance = player.get_balance()
    print(cyan(bright("STARTING CONDITIONS")))
    print(cyan(bright("Balance? " + str(player.get_balance()))))
    print(cyan(bright("Hepatitus? " + str(player.has_status("Hepatitus")))))

    print(bright(yellow("EVENT STARTS HERE")))
    player.woodlands_path()
    print(bright(yellow("EVENT ENDS HERE")))

    print(cyan(bright("ENDING CONDITIONS")))
    print(cyan(bright("Balance? " + str(player.get_balance()))))
    print(cyan(bright("Hepatitus? " + str(player.has_status("Hepatitus")))))
    properties = (player.get_balance() == starting_balance) and (player.has_status("Hepatitus"))
    if properties:
        print(green(bright("EVENT PROPERTIES SATISFIED")))
    else:
        print(red(bright("EVENT PROPERTIES NOT SATISFIED")))
    print("\n")

def test_woodlands_path_none():
    print(bright(magenta("TESTING WOODLANDS_PATH NONE")))
    player = make_player()
    random.seed(4)
    print(cyan(bright("STARTING CONDITIONS: NONE")))

    print(bright(yellow("EVENT STARTS HERE")))
    player.woodlands_path()
    print(bright(yellow("EVENT ENDS HERE")))

    print(cyan(bright("ENDING CONDITIONS: NONE")))
    properties = True
    if properties:
        print(green(bright("EVENT PROPERTIES SATISFIED")))
    else:
        print(red(bright("EVENT PROPERTIES NOT SATISFIED")))
    print("\n")


def test_woodlands_river_bear_escape_quiet_sneakers():
    print(bright(magenta("TESTING WOODLANDS_RIVER BEAR ESCAPE QUIET SNEAKERS")))
    player = make_player()
    random.seed(1)
    print(cyan(bright("STARTING CONDITIONS")))
    print(cyan(bright("Quiet Sneakers? " + str(player.has_item("Quiet Sneakers")))))

    print(bright(yellow("EVENT STARTS HERE")))
    player.woodlands_river()
    print(bright(yellow("EVENT ENDS HERE")))

    print(cyan(bright("ENDING CONDITIONS")))
    print(cyan(bright("Quiet Sneakers? " + str(player.has_item("Quiet Sneakers")))))
    properties = True
    if properties:
        print(green(bright("EVENT PROPERTIES SATISFIED")))
    else:
        print(red(bright("EVENT PROPERTIES NOT SATISFIED")))
    print("\n")

def test_woodlands_river_bear_escape():
    print(bright(magenta("TESTING WOODLANDS_RIVER BEAR ESCAPE")))
    player = make_player()
    random.seed(1)
    print(cyan(bright("STARTING CONDITIONS: NONE")))

    print(bright(yellow("EVENT STARTS HERE")))
    player.woodlands_river()
    print(bright(yellow("EVENT ENDS HERE")))

    print(cyan(bright("ENDING CONDITIONS: NONE")))
    properties = True
    if properties:
        print(green(bright("EVENT PROPERTIES SATISFIED")))
    else:
        print(red(bright("EVENT PROPERTIES NOT SATISFIED")))
    print("\n")

def test_woodlands_river_bear_attack():
    print(bright(magenta("TESTING WOODLANDS_RIVER BEAR ATTACK")))
    player = make_player()
    random.seed(2)
    starting_health = player.get_health()
    print(cyan(bright("STARTING CONDITIONS")))
    print(cyan(bright("Health? " + str(player.get_health()))))

    print(bright(yellow("EVENT STARTS HERE")))
    player.woodlands_river()
    print(bright(yellow("EVENT ENDS HERE")))

    print(cyan(bright("ENDING CONDITIONS")))
    print(cyan(bright("Health? " + str(player.get_health()))))
    properties = player.get_health() < starting_health
    if properties:
        print(green(bright("EVENT PROPERTIES SATISFIED")))
    else:
        print(red(bright("EVENT PROPERTIES NOT SATISFIED")))
    print("\n")

def test_woodlands_river_none():
    print(bright(magenta("TESTING WOODLANDS_RIVER NONE")))
    player = make_player()
    random.seed(3)
    print(cyan(bright("STARTING CONDITIONS: NONE")))

    print(bright(yellow("EVENT STARTS HERE")))
    player.woodlands_river()
    print(bright(yellow("EVENT ENDS HERE")))

    print(cyan(bright("ENDING CONDITIONS: NONE")))
    properties = True
    if properties:
        print(green(bright("EVENT PROPERTIES SATISFIED")))
    else:
        print(red(bright("EVENT PROPERTIES NOT SATISFIED")))
    print("\n")

def template():
    print("TESTING (event)")
    player = make_player()
    # random.seed(0)
    print(cyan(bright("STARTING CONDITIONS")))
    print(cyan(bright("(condition)? " + str(player.has_item()))))

    print(bright(yellow("EVENT STARTS HERE")))
    # Event
    print(bright(yellow("EVENT ENDS HERE")))

    print(cyan(bright("ENDING CONDITIONS")))
    print(cyan(bright("(condition)? " + str("player.has_item()"))))
    properties = True
    if properties:
        print(green(bright("EVENT PROPERTIES SATISFIED")))
    else:
        print(red(bright("EVENT PROPERTIES NOT SATISFIED")))
    print("\n")


def main():
    """
    Poor Day
    """
    # # Test seat_cash
    # test_seat_cash()

    # # Test left_window_down
    # test_left_window_down_no_infestation()
    # test_left_window_down_spider_infestation()
    # test_left_window_down_cockroach_infestation()

    # # Test estranged_dog
    # test_estranged_dog()

    # # Test spider_bite
    # test_spider_bite()
    # test_spider_bite_pest_control()

    # # Test hungry_cockroach
    # test_hungry_cockroach()
    # test_hungry_cockroach_pest_control()

    # # Test whats_my_name
    # test_whats_my_name() # (say yes)
    # test_whats_my_name() # (say no)

    # # Test interrogation
    # test_interrogation() # (say yes)
    # test_interrogation() # (say no)

    """
    Poor Night
    """
    # # Test ditched_wallet
    # test_ditched_wallet()

    # # Test went_jogging
    # test_went_jogging()
    # test_went_jogging_fell()

    # Test woodlands_path
    test_woodlands_path_deer()
    test_woodlands_path_body_fail() # Say No
    test_woodlands_path_body_fail() # Say Yes
    test_woodlands_path_body_success() # Say Yes
    test_woodlands_path_none()

    pass

main()