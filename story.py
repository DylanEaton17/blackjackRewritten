import random
import time
import sys
from colorama import Fore, Back, Style
import lists

"""
Below are all of the typing/color functions, used
for terminal outputs and making my text pretty
"""
def type(*words):
    str = ''
    for item in words:
        str = str + item
    # str += "\n"
    for char in str:
        time.sleep(random.choice([
          0.03, 0.05, 0.04, 0.02,
          0.05, 0.03, 0.02, 0.05, 0.04, 0.01
        ]))
        sys.stdout.write(char)
        sys.stdout.flush()

def slowtype(*words):
    str = ''
    for item in words:
        str = str + item
    # str += "\n"
    for char in str:
        time.sleep(random.choice([
        0.06, 0.05, 0.03, 0.03,
        0.05, 0.03, 0.04, 0.05, 0.06, 0.04
        ]))
        sys.stdout.write(char)
        sys.stdout.flush()
        if (char == ".") or (char == "!") or (char == ":") or (char == ";") or (char == "?"):
            time.sleep(0.7)
        if char == ",":
            time.sleep(0.4)

# all the pretty colors
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

class Player:
    __slots__ = ["__alive", "__status_effects", "__balance", "__previous_balance", "__rank", "__day", "__lists"]

    def __init__(self):
        self.__alive = True
        self.__status_effects = set()
        self.__balance = 50
        self.__previous_balance = 50
        self.__rank = 0
        self.__day = 1
        self.__lists = lists.Lists(self)

    def kill(self):
        self.__alive = False
        self.status()

    def status(self):
        if not self.__alive:
            print("\n")
            slowtype("You have died!")
            print()
            if self.__day == 1: slowtype("You lasted " + bright(yellow(str(self.__day) + " day")))
            else: slowtype("You lasted " + bright(yellow(str(self.__day) + " days")))
            print()
            slowtype("You met your fate with a final balance of " + green(bright("$" + str(self.__balance))))
            print()
            slowtype("The police were able to recover your body, but nobody cared enough to show up to your funeral.")
            quit()
        elif (self.__balance == 0):
            print("\n")
            slowtype("You have run out of money!")
            print()
            if self.__day == 1: slowtype("You lasted " + bright(yellow(str(self.__day) + " day")))
            else: slowtype("You lasted " + bright(yellow(str(self.__day) + " days")))
            print()
            slowtype("With no cash left to play Blackjack, your source of income has been rendered useless.")
            print()
            slowtype("You spend your remaining days going hungry, wondering what life could've been, if you didn't lose that one hand.")
            quit()
        elif (self.__balance >= 1000000):
            print("\n")
            slowtype("u win lol look at u millionaire go girl")
            quit()
    
    def get_balance(self):
        return self.__balance

    def set_balance(self, value):
        self.__balance = value

    def change_balance(self, value):
        if (self.__balance + value) == 0:
            self.__balance = 0
            slowtype("Your new balance is " + red(bright("$0")))
        else:
            self.__balance += value
            slowtype("Your new balance is " + green(bright("$" + str(self.__balance))))
    
    def end_day(self):
        if(self.__day==1):
            self.end_day_1()
        else:
            self.end_day_car()

        print("\n")

        # Starting cheer (eg. Yippee!)
        slowtype(self.__lists.get_cheer())

        # Tells day count and previous day's balance
        if self.__day == 1:
            slowtype(" You've survived " + yellow(bright(str(self.__day) + " day")) + "!")
            print("\n")
            slowtype("You started your journey with just " + green(bright("$" + str(self.__previous_balance))) + ". ")
        else:
            slowtype(" You've survived " + yellow(bright(str(self.__day) + " days")) + "!")
            print("\n")
            slowtype("Yesterday, at this time, you had " + green(bright("$" + str(self.__previous_balance))) + ". ")
        # increments day
        self.__day += 1

        print("")

        # Tells you the change in your balance, and if you gained or lost money
        change_in_balance = self.__balance - self.__previous_balance
        if change_in_balance > 0: slowtype("Since then, you've accumulated " + green(bright("$" + str(change_in_balance))) + ". ")
        elif change_in_balance < 0: slowtype("Since then, you've managed to lose " + red(bright("$" + str(abs(change_in_balance)))) + ". ")
        else: slowtype("Somehow, your net earnings today was 0. Goose egg. No money. Disappointing. ")

        # Sets previous balance to current balance, so that it's ready for next day
        self.__previous_balance = self.__balance

        print("")

        # Tells you your current balance
        slowtype("That brings you to a grand total of " + green(bright("$" + str(self.__balance))) + "! ")

        match self.__rank:
            case 0: slowtype("Let's not get too far ahead of ourselves though, you're still quite poor.")
            case 1: slowtype("You definately have some money. The keyword is 'some'.")
            case 2: slowtype("You've amassed signifigant earnings. Nicely done.")
            case 3: slowtype("You must have some heavy pockets, huh.")
            case 4: slowtype("Where do you even keep all that?")
            case 5: slowtype("So close to being a millionaire! Can you do it?")

        print("\n")

        # Gives a little personal advice, support, etc
        slowtype(self.__lists.get_advice())

        print()

        # Gives one last quote before starting the next day
        slowtype(self.__lists.get_quote_setup())
        slowtype(self.__lists.get_quote())

        print("\n")

    # Opening
    def first_setup(self):
        while (True):
            type("Type 'y' or 'yes', not case sensitive, to say yes to a question: ")
            yes_or_no = input("").lower()
            if (yes_or_no == "y") or (yes_or_no == "yes"):
                break
            else:
                print()
        print()

        while (True):
            type("Type 'n' or 'no', not case sensitive, to say no to a question: ")
            yes_or_no = input("").lower()
            if (yes_or_no == "n") or (yes_or_no == "no"):
                break
            else:
                print()
        print()

        while (True):
            type("Type 'h' or 'hit', not case sensitive, to hit your hand: ")
            hit_or_stand = input("").lower()
            if (hit_or_stand == "h") or (hit_or_stand == "hit"):
                break
            else:
                print()
        print()

        while (True):
            type("Type 's' or 'stand', not case sensitive, to stand with your hand's value: ")
            hit_or_stand = input("").lower()
            if (hit_or_stand == "s") or (hit_or_stand == "stand"):
                break
            else:
                print()
        print()

    def opening_lines(self):
        slowtype("\"Ugh, not again,\" you spout as the old wagon shutters, then dies. ")
        slowtype("Stranded on the road again, but this time, your money has gone dry. ")
        slowtype("All but your 50 dollar bill that Grandma gave you on her last Christmas. ")
        slowtype("You've been saving it for when you needed it most. ")
        slowtype("But surely, it won't be enough.")
        print('\n')
        slowtype("The door creaks open, and you step out into the night sky, coughing up the smoke from your fried vehicle. ")
        slowtype("After pushing your car off the road and between the trees, there isn't much else left for you to do, ")
        slowtype("so you begin to wander down the dark, lonely street.")
        print('\n')
        slowtype("But at the end of the road, where concrete turned to stone turned to dirt, you notice a light up ahead, on the top of a hill. ")
        print('\n')
        slowtype("As you waltz into the old, wooden shack, your eyes begin to light up with the fire of a thousand suns. ")
        slowtype("Roulette wheels! Poker tables! And in a dark corner of the abandoned casino, sits a dealer, shuffling cards for a new round of Blackjack. ")
        slowtype("That 50 dollars might just come in handy after all. Thanks, Grandma!")
        print('\n')
        slowtype("As you go to sit down at the table, you hear the dealer cough, then watch as he sits up.")
        print("\n")
        slowtype("In a deep, and yet strained voice, the dealer, cloaked in darkness, poses a question to you.")
        print("\n")


    # End Days
    def end_day_1(self):
        slowtype("After playing a few rounds of Blackjack, the dealer points to the door. ")
        slowtype("Without questing his word, and with your winnings in hand, you scurry to the door, eager to get some sleep after such a long day. ")
        slowtype("Making it back to your car, ditched on the side of the road, but no longer engulfed in smoke, you lay down, and close your eyes. It's time to rest. ")

    def end_day_car(self):
        slowtype("After playing a few rounds of Blackjack, the dealer points to the door. ")
        slowtype("Without questing his word, and with your winnings in hand, you scurry to the door, eager to get some sleep. ")
        slowtype("Making it back to your car, ditched on the side of the road, you lay down, and close your eyes. It's time to rest.")


    # Poor Day Events (0 - 1,000)
    def seat_cash(self):
        slowtype("As the sun shines through the car window, you notice a bright green bill tucked between the seat cushions. Must be your lucky day. ")
        print("\n")
        x = random.randint(0, 4)
        a_list = [5, 10, 20, 50, 100]
        slowtype("That's another " + green(bright("$" + str(a_list[x]))) + " dollars")
        print()
        self.change_balance(a_list[x])

    # Cheap Day Events (1,000 - 10,000)
        
    # Modest Day Events (10,000 - 100,000)
        
    # Rich Day Events (100,000 - 500,000)
        
    # Doughman Day Events (500,000 - 900,000)
        
    # Nearly There Day Events (900,000 - 1,000,000)


    def day_event(self):
        if self.__rank==0:
            dayEvent = getattr(self, self.__lists.get_poor_day_event())
        elif self.__rank==1:
            dayEvent = getattr(self, self.__lists.get_)
        dayEvent()