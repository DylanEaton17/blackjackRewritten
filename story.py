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
    __slots__ = ["__alive", "__status_effects", "__inventory", "__balance", "__previous_balance", "__rank", "__day", "__lists"]

    def __init__(self):
        self.__alive = True
        self.__status_effects = set()
        self.__inventory = set()
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
        print("\n")
        if (self.__balance + value) <= 0:
            self.__balance = 0
            slowtype("Your new balance is " + red(bright("$0")))
        else:
            self.__balance += value
            slowtype("Your new balance is " + green(bright("$" + str(self.__balance))))
        print("\n")


    def update_rank(self):
        if(1<=self.__balance<1000):
            self.__rank = 0
        elif(1000<=self.__balance<10000):
            self.__rank = 1
        elif(10000<=self.__balance<100000):
            self.__rank = 2
        elif(100000<=self.__balance<500000):
            self.__rank = 3
        elif(500000<=self.__balance<900000):
            self.__rank = 4
        elif(900000<=self.__balance<1000000):
            self.__rank = 5
        else:
            self.status()
    
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


    # Poor Day Events (1 - 1,000)
    def seat_cash(self):
        slowtype("You wake up in the front seat, covered in sweat. ")
        slowtype("As the sun shines through the car window, you notice a bright green bill tucked between the seat cushions. Must be your lucky day. ")
        print("\n")
        i = random.randint(0, 4)
        a_list = [5, 10, 20, 50, 100]
        slowtype("That's another " + green(bright("$" + str(a_list[i]))) + " dollars")
        print()
        self.change_balance(a_list[i])

    # Cheap Day Events (1,000 - 10,000)
    def big_bird(self):
        pass
        
    # Modest Day Events (10,000 - 100,000)
        
    # Rich Day Events (100,000 - 500,000)
        
    # Doughman Day Events (500,000 - 900,000)
        
    # Nearly There Day Events (900,000 - 1,000,000)



    # Poor Night Events (1 - 1,000)

    # Cheap Day Events (1,000 - 10,000)
        
    # Modest Day Events (10,000 - 100,000)
        
    # Rich Day Events (100,000 - 500,000)
        
    # Doughman Day Events (500,000 - 900,000)
        
    # Nearly There Day Events (900,000 - 1,000,000)



    # Story Events
    def trusty_tom(self):
        slowtype("You wake up to a blaring engine, roaring down the road towards you. ")
        slowtype("As you scratch your eyes awake, you read \'Tom the Trusty Mechanic\' painted on the hood of a bright gold truck. ")
        slowtype("Waving the vehicle down, the truck slows, then halts, and an old, jolly man jumps out. ")
        print("\n")
        slowtype("\"Well, howdy! The name's Tom. It appears you've gotten yourself in a bit of a pickle, ya think?\" ")
        slowtype("Tom pulls a big red wrench out of his pocket, and walks to the hood of your beaten down wagon. ")
        i = random.randint(0, 4)
        a_list = [100, 150, 200, 250, 300]
        type("\"Yep, this things busted alright! Tell ya what, for, I don't know, " + green(bright(str(a_list[i]) + " bucks")) + ", I'll get this thing replaced for ya, good as new! Whaddya say?\" ")
        while(True):
            yes_or_no = input("").lower()
            print()
            if(yes_or_no == "n") or (yes_or_no == "no"):
                slowtype("Really? No dice, huh. Yunno, I think you're makin' a mistake, but I ain't one to judge. You have a nice day now.\" ")
                slowtype("Tom has a sad look in his eye. It's clear that he wanted to help you. ")
                slowtype("You watch as his big golden truck stutters, starts, then drives away.")
                print()
                return
            elif(((yes_or_no == "y") or (yes_or_no == "yes")) and (self.__balance < a_list[i])):
                slowtype("\"Aww man, sorry to tell you, but you just don't got enough funds for this, yunno?\" ")
                random_chance = random.randrange(2)
                # Broke, and Tom offers discount
                if random_chance == 0:
                    print("\n")
                    slowtype("\"You know what? I'm feelin' generous, and the shop's been doing well lately. ")
                    slowtype("Tell ya what, I can take the offer down " + green(bright(str(50) + " dollars")) + " just for you. ")
                    slowtype("Could ya do " + green(bright(str(a_list[i]-50) + " bucks")) + "?\" ")
                    while True:
                        yes_or_no_2 = input("").lower()
                        print()
                        # Declining Tom's second offer
                        if(yes_or_no_2 == "n") or (yes_or_no_2=="no"):
                            print()
                            slowtype("Really? No dice, huh. Even with the discount? Yunno, I think you're makin' a mistake, but I ain't one to judge. You have a nice day now.\" ")
                            slowtype("Tom has a dissapointed look in his eye. It's clear that he wanted to help you. ")
                            slowtype("You watch as his big golden truck stutters, starts, then drives away.")
                            print()
                            return
                        elif(((yes_or_no_2 == "y") or (yes_or_no_2 == "yes")) and (self.__balance < (a_list[i]-50))):
                            print()
                            slowtype("\"Still can't afford it? That's a real shame. I really wish there was something I could do. Best of luck my friend. Be seeing ya around, ya know?\" ")
                            slowtype("And with that, you watch as his big golden truck stutters, starts, then drives away.")
                            print()
                            return
                        elif (yes_or_no_2 == "y") or (yes_or_no_2 == "yes"):
                            print()
                            slowtype("\"Really? Awesome! I'll be the best dang mechanic this ol' automobile has ever seen!\" ")
                            slowtype("You watch in awe, as Tom, a man who has clearly perfected his craft, fixes up your wagon in no time. Sweet. ")
                            self.change_balance(-(a_list[i]-50))
                            self.__inventory.add("Car")
                            slowtype(magenta(bright("Your car has been fixed! You can now drive around!")))
                            print("\n")
                            slowtype("\"Well, gee, this has been fun. Be seein' you around, ya know?\" ")
                            slowtype("And with that, you watch as his big golden truck stutters, starts, then drives away.")
                            print()
                            return
                        else:
                            slowtype("\"Whaddya say?\" ")

                # Broke, and Tom can't offer discount
                elif random_chance == 1:
                    print("\n")
                    slowtype("\"I really wish there was something I could do. Best of luck my friend. Be seeing ya around, ya know?\" ")
                    slowtype("And with that, you watch as his big golden truck stutters, starts, then drives away.")
                    print()
                    return
            # Accepting Tom's first offer
            elif (yes_or_no == "y") or (yes_or_no == "yes"):
                slowtype("\"Really? Awesome! I'll be the best dang mechanic this ol' automobile has ever seen!\" ")
                slowtype("You watch in awe, as Tom, a man who has clearly perfected his craft, fixes up your wagon in no time. Sweet. ")
                self.change_balance(-a_list[i])
                self.__inventory.add("Car")
                slowtype(magenta(bright("Your car has been fixed! You can now drive around!")))
                print("\n")
                slowtype("\"Well, gee, this has been fun. Be seein' you around, ya know?\" ")
                slowtype("And with that, you watch as his big golden truck stutters, starts, then drives away.")
                print()
                return
            else:
                slowtype("\"Whaddya say?\" ")


    def day_event(self):
        if("Car" not in self.__inventory) and (self.__balance>=200):
            random_chance = random.randrange(3)
            if random_chance==0:
                self.trusty_tom()

        else:
            match self.__rank:
                case 0: dayEvent = getattr(self, self.__lists.get_poor_day_event())
                case 1: dayEvent = getattr(self, self.__lists.get_cheap_day_event())
                case 2: dayEvent = getattr(self, self.__lists.get_modest_day_event())
                case 3: dayEvent = getattr(self, self.__lists.get_rich_day_event())
                case 4: dayEvent = getattr(self, self.__lists.get_doughman_day_event())
                case 5: dayEvent = getattr(self, self.__lists.get_nearly_day_event())
            dayEvent()
        self.update_rank()

    def afternoon(self):
        if "Car" in self.__inventory:
            type("Would you like to spend your day driving somewhere? ")


    def night_event(self):
        match self.__rank:
            case 0: nightEvent = getattr(self, self.__lists.get_poor_night_event())
            case 1: nightEvent = getattr(self, self.__lists.get_cheap_night_event())
            case 2: nightEvent = getattr(self, self.__lists.get_modest_night_event())
            case 3: nightEvent = getattr(self, self.__lists.get_rich_night_event())
            case 4: nightEvent = getattr(self, self.__lists.get_doughman_night_event())
            case 5: nightEvent = getattr(self, self.__lists.get_nearly_night_event())
        nightEvent()
        self.update_rank()