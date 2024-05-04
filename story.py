import random
import time
import sys
from colorama import Fore, Back, Style
import lists
import msvcrt

"""
Below are all of the typing/color functions, used
for terminal outputs and making my text pretty
"""
class Typing:
    def __init__(self):
        self.__type_speed = "Default"

    def fast(self, *words):
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
            if (char == ".") or (char == "!") or (char == ":"):
                time.sleep(0.5)
            if char == ",":
                time.sleep(0.4)
            self.cleanup()

    def slow(self, *words):
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
                if ((char == ".") or (char == "!") or (char == ":") or (char == ";")):
                    time.sleep(0.7)
                if (char == ","):
                    time.sleep(0.4)
                self.cleanup()

    def type(self, *words):
        str = ''
        for item in words:
            str = str + item
            for char in str:
                if self.__type_speed == "Default":
                    time.sleep(random.choice([
                    0.06, 0.05, 0.03, 0.03,
                    0.05, 0.03, 0.04, 0.05, 0.06, 0.04
                    ]))
                if self.__type_speed == "Fast":
                    time.sleep(random.choice([
                    0.06, 0.05, 0.03, 0.03,
                    0.05, 0.03, 0.04, 0.05, 0.06, 0.04
                    ]) - 0.01)
                if self.__type_speed == "Fastest":
                    time.sleep(random.choice([
                    0.06, 0.05, 0.03, 0.03,
                    0.05, 0.03, 0.04, 0.05, 0.06, 0.04
                    ]) - 0.02)
                if self.__type_speed == "Print":
                    time.sleep(0.001)

                sys.stdout.write(char)
                sys.stdout.flush()

                if self.__type_speed =="Default" and ((char == ".") or (char == "!") or (char == ";")):
                    time.sleep(0.7)
                elif self.__type_speed =="Fast" and ((char == ".") or (char == "!") or (char == ";")):
                    time.sleep(0.5)
                elif self.__type_speed =="Fastest" and ((char == ".") or (char == "!") or (char == ";")):
                    time.sleep(0.4)

                if self.__type_speed =="Default" and (char == ","):
                    time.sleep(0.4)
                elif self.__type_speed =="Fast" and (char == ","):
                    time.sleep(0.3)
                elif self.__type_speed =="Fastest" and (char == ","):
                    time.sleep(0.2)

                if self.__type_speed =="Default" and (char == "?") or (char == ":"):
                    time.sleep(0.3)
                elif self.__type_speed =="Fast" and (char == "?") or (char == ":"):
                    time.sleep(0.2)
                elif self.__type_speed =="Fastest" and (char == "?") or (char == ":"):
                    time.sleep(0.1)
                
                self.cleanup()

    def cleanup(self):
        while msvcrt.kbhit():
            byte = msvcrt.getch()
            if byte == b',':
                self.__type_speed = "Default"
            elif byte == b'.':
                self.__type_speed = "Fast"
            elif byte == b'/':
                self.__type_speed = "Fastest"
            elif byte == b'p':
                self.__type_speed = "Print"


type = Typing()

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

def open_quote(text):
    return ("\"" + text)

def close_quote(text):
    return (text + "\"")

def quote(text):
    return ("\"" + text + "\"")

def space_quote(text):
    return ("\"" + text + "\" ")

class Player:
    __slots__ = ["__name", "__alive", "__is_sick", "__is_injured", "__flask_effects", "__status_effects", "__injuries", "__travel_restrictions", "__clear_status", "__clear_all_status", "__inventory", "__broken_inventory", "__repairing_inventory", "__dangers", "__met", "__mechanic_visits", "__health", "__balance", "__previous_balance", "__rank", "__day", "__counting_days", "__item_durability", "__flask_durability", "__round_count", "__is_religious", "__prereqs", "__prereqs_done", "__convenience_store_inventory", "__lists"]

    def __init__(self):
        self.__name = None
        self.__alive = True
        self.__is_sick = False
        self.__is_injured = False
        self.__flask_effects = set()
        self.__status_effects = set()
        self.__injuries = set()
        self.__travel_restrictions = set()
        self.__clear_status = False
        self.__clear_all_status = False
        self.__inventory = set()
        self.__broken_inventory = set()
        self.__repairing_inventory = set()
        self.__dangers = set()
        self.__met = set()
        self.__mechanic_visits = 0
        self.__health = 100
        self.__balance = 50
        self.__previous_balance = 50
        self.__rank = 0
        self.__day = 1
        self.__counting_days = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.__item_durability = [0, 0, 0, 0, 0, 0, 0] # [6, 1, 1, 1, 1, 1, 1, 1]
        self.__flask_durability = [0, 0, 0, 0, 0, 0, 0]
        self.__round_count = 3
        self.__is_religious = False
        self.__prereqs = [False, False, False, False, False]
        self.__prereqs_done = [False, False, False, False, False]
        self.__convenience_store_inventory = []
        self.__lists = lists.Lists(self)

    def kill(self):
        self.__alive = False
        self.status()

    def hurt(self, value):
        if(self.__health - value <= 0):
            self.__health = 0
            type.slow(red(bright("You have succumbed to your wounds.")))
            self.kill()
        else:
            self.__health -= value
        if self.has_item("Health Indicator"):
            type.type("The " + magenta(bright("Health Indicator")) + " on your wrist makes a loud beep.")
            print()
            type.type("You took damage!")
            print()
            self.health_indicator()

    def heal(self, value):
        if(self.__health + value >= 100):
            self.__health = 100
        else:
            self.__health += value
        if self.has_item("Health Indicator"):
            type.type("The " + magenta(bright("Health Indicator")) + " on your wrist makes a subtle vibration.")
            print()
            type.type("You regained health!")
            print()
            self.health_indicator()

    def set_health(self, value):
        self.__health = value

    def get_health(self):
        return self.__health

    def health_indicator(self):
        if self.__health > 66:
            type.type("Your current health: " + bright(green(str(self.__health) + "%")))
        elif self.__health > 33:
            type.type("Your current health: " + bright(yellow(str(self.__health) + "%")))
        else:
            type.type("Your current health: " + bright(red(str(self.__health) + "%")))
        print("\n")
        self.update_health_indicator_durability()

    def status(self):
        if not self.__alive:
            print("\n")
            type.slow("You have died!")
            print()
            if self.__day == 1: type.slow("You didn't even last " + bright(yellow(str(self.__day) + " day")) + ". That's embarrasing.")
            elif self.__day == 2: type.slow("You lasted " + bright(yellow(str(self.__day-1) + " day")) + ".")
            else: type.slow("You lasted " + bright(yellow(str(self.__day) + " days")) + "!")
            print()
            type.slow("You met your fate with a final balance of " + green(bright("${:,}".format(self.__balance))))
            print()
            type.slow("The police were able to recover your body, but nobody cared enough to show up to your funeral.")
            quit()
        elif (self.__balance == 0):
            print("\n")
            type.slow("You have run out of money!")
            print()
            if self.__day == 1: type.slow("You didn't even last " + bright(yellow(str(self.__day) + " day")) + ". That's absurdly sad.")
            elif self.__day == 2: type.slow("You lasted " + bright(yellow(str(self.__day-1) + " day")) + ".")
            else: type.slow("You lasted " + bright(yellow(str(self.__day) + " days")) + "!")
            print()
            type.slow("With no cash left to play Blackjack, your source of income has been rendered useless.")
            print()
            type.slow("You spend your remaining days going hungry, wondering what life could've been, if you didn't lose that one hand.")
            quit()
        elif (self.__balance >= 1000000):
            print("\n")
            type.slow("u win lol look at u millionaire go girl")
            quit()
    
    def get_name(self):
        return self.__name

    def is_religious(self):
        return self.__is_religious
    
    def lists(self):
        return self.__lists
    
    def add_travel_restriction(self, restriction):
        self.__travel_restrictions.add(restriction)

    def has_travel_restriction(self, restriction):
        return restriction in self.__travel_restrictions
    
    def remove_travel_restriction(self, restriction):
        self.__travel_restrictions.remove(restriction)

    def add_flask(self, flask):
        self.__flask_effects.add(flask)

    def has_flask_effect(self, flask):
        return flask in self.__flask_effects
    
    def remove_flask_effect(self, flask):
        self.__flask_effects.remove(flask)

    def len_flasks(self):
        return len(self.__flask_effects)

    def add_status(self, status):
        self.__status_effects.add(status)

    def has_status(self, status):
        return status in self.__status_effects
    
    def remove_status(self, status):
        self.__status_effects.remove(status)

    def add_injury(self, injury):
        self.__injuries.add(injury)

    def has_injury(self, injury):
        return injury in self.__injuries
    
    def heal_injury(self, injury):
        self.__injuries.remove(injury)

    def len_status(self):
        return len(self.__status_effects)
    
    def get_rounds(self):
        return self.__round_count
    
    def set_rounds(self, value):
        self.__round_count = value

    def add_item(self, item):
        self.__inventory.add(item)

    def has_item(self, item):
        return item in self.__inventory
    
    def has_broken_item(self, item):
        return item in self.__broken_inventory
    
    def is_repairing_item(self, item):
        return item in self.__repairing_inventory
    
    def repair_item(self, item):
        self.__repairing_inventory.add(item)
        self.__broken_inventory.remove(item)

    def return_item(self, item):
        self.__repairing_inventory.remove(item)
        self.__broken_inventory.add(item)
    
    def use_item(self, item):
        self.__inventory.remove(item)

    def break_item(self, item):
        self.__broken_inventory.add(item)
        self.__inventory.remove(item)

    def fix_item(self, item):
        self.__inventory.add(item)
        if self.is_repairing_item(item):
            self.__repairing_inventory.remove(item)
        if self.has_broken_item(item):
            self.__broken_inventory.remove(item)
    
    def add_danger(self, danger):
        self.__dangers.add(danger)

    def has_danger(self, danger):
        return danger in self.__dangers
    
    def lose_danger(self, danger):
        self.__dangers.remove(danger)
    
    def meet(self, person):
        self.__met.add(person)

    def has_met(self, person):
        return person in self.__met

    def get_balance(self):
        return self.__balance

    def set_balance(self, value):
        self.__balance = value

    def change_balance(self, value):
        print("\n")
        if (self.__balance + value) <= 0:
            self.__balance = 0
            type.type("Your new balance is " + red(bright("$0")))
        else:
            previous_balance = self.__balance
            self.__balance += value
            if value > 0:
                type.type("Your new balance is " + green(bright("${:,}".format(previous_balance) + " + ${:,}".format(value)) + bright(green(" = " + "${:,}".format(self.__balance)))))
            elif value < 0:
                type.type("Your new balance is " + green(bright("${:,}".format(previous_balance))) + red(bright(" - ${:,}".format(abs(value)))) + green(bright(" = ${:,}".format(self.__balance))))
        print("\n")

    def get_rank(self):
        return self.__rank

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
    
    def increment_day(self): # really just for testing
        self.__day+=1

    def end_day(self):
        if(self.has_danger("Angry Dealer")):
            self.lose_danger("Angry Dealer")
            self.end_day_angry_dealer()
        elif(self.__day==1):
            self.end_day_1()
        elif(not self.has_item("Car")):
            self.end_day_car_broken()
        else:
            self.end_day_car_fixed()

        print("\n")

        self.update_dirty_old_hat_durability()
        self.update_golden_watch_durability()

        # Starting cheer (eg. Yippee!)
        type.type(self.__lists.get_cheer())

        # Tells day count and previous day's balance
        if self.__day == 1:
            type.type(" You've survived " + yellow(bright(str(self.__day) + " day")) + "!")
            print("\n")
            type.type("You started your journey with just " + green(bright("$" + str(self.__previous_balance))) + ". ")
        else:
            type.type(" You've survived " + yellow(bright(str(self.__day) + " days")) + "!")
            print("\n")
            type.type("Yesterday, at this time, you had " + green(bright("$" + str(self.__previous_balance))) + ". ")
        # increments day
        self.__day += 1

        print("")

        # Tells you the change in your balance, and if you gained or lost money
        change_in_balance = self.__balance - self.__previous_balance
        if change_in_balance > 0: type.type("Since then, you've accumulated " + green(bright("$" + str(change_in_balance))) + ". ")
        elif change_in_balance < 0: type.type("Since then, you've managed to lose " + red(bright("$" + str(abs(change_in_balance)))) + ". ")
        else: type.type("Somehow, your net earnings today was 0. Goose egg. No money. Disappointing. ")

        # Sets previous balance to current balance, so that it's ready for next day
        self.__previous_balance = self.__balance

        print("")

        # Tells you your current balance
        type.type("That brings you to a grand total of " + green(bright("$" + str(self.__balance))) + "! ")

        match self.__rank:
            case 0: type.type("Let's not get too far ahead of ourselves though, you're still quite poor.")
            case 1: type.type("You definately have some money. The keyword is 'some'.")
            case 2: type.type("You've amassed signifigant earnings. Nicely done.")
            case 3: type.type("You must have some heavy pockets, huh.")
            case 4: type.type("Where do you even keep all that?")
            case 5: type.type("So close to being a millionaire! Can you do it?")

        print("\n")

        # Gives a little personal advice, support, etc
        type.type(self.__lists.get_advice())

        print()

        # Gives one last quote before starting the next day
        type.type(self.__lists.get_quote_setup())
        type.type(self.__lists.get_quote())

        # Heals the player before the next day
        print("\n")
        self.heal(random.choice([1, 3, 5]))

    # Opening
    def first_setup(self):
        while (True):
            type.type("Type 'y' or 'yes', not case sensitive, to say yes to a question: ")
            yes_or_no = input("").lower()
            if (yes_or_no == "y") or (yes_or_no == "yes"):
                break
            else:
                print()
        print()

        while (True):
            type.type("Type 'n' or 'no', not case sensitive, to say no to a question: ")
            yes_or_no = input("").lower()
            if (yes_or_no == "n") or (yes_or_no == "no"):
                break
            else:
                print()
        print()

        while (True):
            type.type("Type 'h' or 'hit', not case sensitive, to hit your hand: ")
            hit_or_stand = input("").lower()
            if (hit_or_stand == "h") or (hit_or_stand == "hit"):
                break
            else:
                print()
        print()

        while (True):
            type.type("Type 's' or 'stand', not case sensitive, to stand with your hand's value: ")
            hit_or_stand = input("").lower()
            if (hit_or_stand == "s") or (hit_or_stand == "stand"):
                break
            else:
                print()
        print()

    def opening_lines(self):
        type.type("\"Ugh, not again,\" you spout as the old wagon shutters, then dies. ")
        type.type("Stranded on the road again, but this time, your money has gone dry. ")
        type.type("All but your 50 dollar bill that Grandma gave you on her last Christmas. ")
        type.type("You've been saving it for when you needed it most, but surely, it won't be enough.")
        print('\n')
        type.type("The door creaks open, and you step out into the night sky, coughing up the smoke from your fried vehicle. ")
        type.type("After pushing your car off the road and between the trees, there isn't much else left for you to do, ")
        type.type("so you begin to wander down the dark, lonely street.")
        print('\n')
        type.type("But at the end of the road, where concrete turned to stone turned to dirt, you notice a light up ahead, on the top of a hill. ")
        print('\n')
        type.type("As you waltz into the old, wooden shack, your eyes begin to light up with the fire of a thousand suns. ")
        type.type("Roulette wheels! Poker tables! And in a dark corner of the abandoned casino, sits a dealer, shuffling cards for a new round of Blackjack. ")
        type.type("That 50 dollars might just come in handy after all. Thanks, Grandma!")
        print('\n')
        type.type("As you go to sit down at the table, you hear the Dealer cough, then watch as he sits up.")
        print("\n")
        type.type("In a deep, and yet strained voice, the Dealer, cloaked in darkness, poses a question to you.")
        print("\n")
        self.start_night()

    # End Days
    def end_day_1(self):
        type.type("After playing a few rounds of Blackjack, the dealer points to the door. ")
        type.type("Without questing his word, and with your winnings in hand, you scurry to the door, eager to get some sleep after such a long day. ")
        type.type("Making it back to your car, ditched on the side of the road, but no longer engulfed in smoke, you lay down, and close your eyes. It's time to rest.")

    def end_day_car_broken(self):
        type.type("After playing a few rounds of Blackjack, the dealer points to the door. ")
        type.type("Without questing his word, and with your winnings in hand, you scurry to the door, eager to get some sleep. ")
        type.type("Making it back to your car, ditched on the side of the road, you lay down, and close your eyes. It's time to rest.")

    def end_day_car_fixed(self):
        type.type("After playing a few rounds of Blackjack, the dealer points to the door. ")
        type.type("Without questing his word, and with your winnings in hand, you scurry to the door, eager to get some sleep. ")
        type.type("You make it to your car and drive away from the casino, and you park in a little alcove on the side of the road. You lay down, and close your eyes. It's time to rest.")

    def end_day_wind(self):
        self.remove_travel_restriction("Wind")
        type.type("After playing a few rounds of Blackjack, the dealer points to the door. ")
        type.type("Without questing his word, and with your winnings in hand, you scurry to the door, eager to get some sleep. ")
        type.type("Stepping outside, you notice that the wind has calmed down. That's a relief. ")
        type.type("Making it back to your car, ditched on the side of the road, you lay down, and close your eyes. It's time to rest.")


    def end_day_angry_dealer(self):
        type.type("You've never seen the dealer quite so angry. Fortunately, you make it back to your car, and immediately pass out for the night. It's time to rest.")

    def start_night(self):
        if(self.__day==1):
            self.start_night_1()
        elif self.has_travel_restriction("Wind"):
            self.end_day_wind()
        elif(not self.has_item("Car")):
            self.start_night_car()
        else:
            self.start_night_car_fixed()

    def start_night_1(self):
        type.slow(red("Would you like to play a game of Blackjack? "))
        yes_or_no = input("").lower()
        print()
        if (yes_or_no == "n") or (yes_or_no == "no"):
            type.slow(red(bright("Well that's just too bad, isn't it. ")))
            type.slow(red("The Dealer fires three shots into your chest. You bleed out, and as you fade from reality, you see the Dealer reach into your pockets, and take the last 50 dollars from your lifeless body."))
            self.kill()

    def start_night_car(self):
        type.type("As the sun begins to set, and the stars light up in the night sky, you walk to the casino, eager to play more Blackjack. ")
        print("\n")
        type.slow(red(self.__lists.get_dealer_welcome()))
        print("\n")

    def start_night_car_fixed(self):
        type.type("As the sun begins to set, and the stars light up in the night sky, you drive over to the casino, eager to play more Blackjack. ")
        print("\n")
        type.slow(red(self.__lists.get_dealer_welcome()))
        print("\n")



    # Poor Day Events (1 - 1,000)
    # Everytime
    def seat_cash(self):
        type.type("You wake up in the front seat, covered in sweat. ")
        type.type("As the sun shines through the car window, you notice a bright green bill tucked between the seat cushions. Must be your lucky day. ")
        print("\n")
        bill = random.choice([5, 10, 20, 50, 100])
        type.type("That's another " + green(bright("$" + str(bill))) + " dollars.")
        self.change_balance(bill)

    def left_window_down(self):
        type.type("You wake up in the front seat, with a chill going down your spine. ")
        type.type("Had the window really been open all night? ")
        type.type("Hopefully nothing had gotten in. ")
        type.type("You roll the window up, just to be safe. ")
        random_chance = random.randrange(5)
        if random_chance == 0:
                self.add_danger("Spider")
        elif random_chance == 1:
                self.add_danger("Cockroach")
        print("\n")

    def estranged_dog(self):
        type.type("You wake up to the sound of barking outside your car. You get up, to see a golden retriever licking your window. ")
        type.type("You open the door, and pet the doggo on the head. He seems happy. You're happy, too.")
        print("\n")
        if self.has_item("Dog Treat"):
            self.use_item("Dog Treat")
            type.type("You throw your " + bright(magenta("Dog Treat")) + " into the air, and the dog jumps up, and catches it in his mouth. He wags his tail in excitement. It's super cute.")
            print("\n")
            self.heal(random.choice([15, 20]))
        else:
            self.heal(random.choice([5, 10]))
        type.type("Before you get a chance to check the dog's collar to see where it came from, the dog bolts down the road, eager to cheer up someone else. It was a good dog.")
        print("\n")
        return
    
    def freight_truck(self):
        type.type("You are jolted away by the sound of a horn blaring outside your car. Looking out your window, you see a man, in a bright red hat, inside of a freight truck that's parked just outside of your vehicle.")
        print("\n")
        type.type(quote("Hey, you. Wake the fuck up! Hahahaha!"))
        print("\n")
        type.type("You watch as the man honks his horn one more time, laughs, and drives off into the distance. What a jerk.")
        print("\n")
        return

    # Conditional
    def sore_throat(self):
        if self.has_status("Sore Throat"):
            self.day_event()
            return
            
        type.type("You wake up, and begin to have a coughing fit. Your throat is dry, and super sore. ")
        if self.has_item("Cough Drops"):
            self.use_item("Cough Drops")
            type.type("Luckily, you have some " + magenta(bright("Cough Drops")) + " on hand, and you empty the box into your mouth. Almost like magic, your throat doesn't hurt anymore.")
            print("\n")
            return
        else:
            self.add_status("Sore Throat")
            self.mark_day("Sore Throat")
            type.type("You cough, and cough, and cough some more, but the burning itch in your throat just won't go away.")
            print("\n")
            return

    def spider_bite(self):
        if not self.has_danger("Spider") or self.has_status("Spider Bite"):
            self.day_event()
            return
        
        type.type("You wake up to a sharp pain on your arm! ")
        type.type("Swinging your arm to scratch the pain, you watch as a spider jumps to your dashboard. ")
        if self.has_item("Pest Control"):
            self.kill_pests()
            type.type("You grab your " + magenta(bright("Pest Control")) + " and spray in the direction of the spider. ")
            type.type("A cloud of white liquid covers the spider, and you watch as it slows, and dies. ")
            type.type("Hopefully, that's the end of your spider problems.")
        else:
            type.type("You attempt to swat it with your hand, but it sneaks into your heater. ")
            type.type("You start the engine and blast the heat, but you aren't sure if the spider has died, or if it has a family nearby. This sucks.")
        self.add_status("Spider Bite")
        self.mark_day("Spider Bite")
        print("\n")


    def hungry_cockroach(self):
        random_choice = random.randrange(2)
        if (random_choice != 0) or not self.has_danger("Cockroach"):
            self.day_event()
            return

        type.type("You wake up to the sound of a hiss in your pile of money. ")
        type.type("You jump up to check your cash, and you find a cockroach eating away at your cash. ")
        if self.has_item("Pest Control"):
            self.kill_pests()
            type.type("You grab your " + magenta(bright("Pest Control")) + " and spray in the direction of the cockroach. ")
            type.type("A cloud of white liquid covers the cockroach, and you watch as it slows down, twitches, and dies. ")
            type.type("Hopefully, that's the end of your cockroach problems.")
        else:
            type.type("You attempt to swat it with your hand, but it falls under your car seat. ")
            type.type("You stick your head under the seat, but you aren't sure where the cockroach went, or if it has a family nearby. This is terrible.")
        print("\n")
        type.type("The cockroach ate through some of your money. ")
        losses = int(self.get_balance() * (random.randint(10, 40)/100))
        type.type("You lost " + green(bright("${:,}".format(losses))) + ".")
        self.change_balance(-losses)

    # One-Time
    def lone_cowboy(self):
        if self.has_met("Cowboy"):
            self.day_event()
            return

        self.meet("Cowboy")
        type.type("You wake up to the sounds trotting, and distant whistling. You sit up, and through your windshield, you see a man wearing a full cowboy suit, with matching black hat and boots, and a short brown beard. ")
        type.type("He's riding a magnificent horse, muscular, but nimble, each step powerful, but precise. The man reaches your window, and in a deep southern accent, he begins to talk to you.")
        print("\n")
        type.type(open_quote("Howdy, partner! The name's Jameson. Davey Jameson. I happen to notice you were admiring my steed. He's a beauty, isn't he. You see, it's common courtesy when a cowboy rides by, "))
        type.type(close_quote("to give their mighty steed a carrot, as a way to express your gratitude for their hardwork and commitment to the job."))
        print("\n")
        type.type(quote("You my friend, you are carrotless. That's quite a disrespectful showing towards my steed. My, my, this can't do at all. What if another cowboy comes by, you're just gonna disrespect their steed, too? Tell you what, I happen to have one spare carrot in my pouch. Take this, and be ready. You never know when a cowboy's gonna come trotting by."))
        print("\n")
        self.add_item("Carrot")
        type.type("Davey Jameson hands you his " + bright(magenta("Carrot")) + ", and smiles.")
        print("\n")
        type.type(quote("See, with this carrot in your possession, you're ready for anytime a cowboy strolls on down this road. Just give their steed a carrot, and they'll be very grateful."))
        print("\n")
        type.type("And with that, Jameson reins his horse high into the air, gives you a yee-haw, then dashes off down the road.")

    def whats_my_name(self):
        if not self.__name == None:
            self.day_event()
            return
        
        type.type("You wake up to the sound of sneakers scratching against the concrete. As you sit up from your seat, you notice a little girl, with blonde hair and pigtails, jump roping towards you.")
        print("\n")
        type.type(space_quote("Howdy stranger! My name's Suzy! Do you like my name?"))
        answer = self.yes_or_no("\"What was that?\" ")
        if answer == "yes":
            type.type(quote("Thanks! My mom gave it to me, before she dissapeared. Who knows where she ran off to!"))
        elif answer == "no":
            type.type(quote("Wow! That's not very nice of you. You're rude, stranger."))

        print("\n")
        type.type(space_quote("Hey, what's your name, anyways?"))
        while True:
            name = str(input())
            type.type(space_quote("So your name is " + name + "?"))
            answer = self.yes_or_no(space_quote("What was that?"))
            if answer == "yes":
                self.__name = name
                type.type("\"" + name + "...I like that name! Hello, " + name + "!\"")
                print("\n")
                type.type(space_quote("Well, " + name + ", I've got to get going now. Wouldn't want the bears to eat me!"))
                type.type("And with that, Suzy, without missing a beat, continues to jump rope down the street.")
                print("\n")
                break
            elif answer == "no":
                type.type(quote("So you lied to me? You're a liar, stranger!"))
                print("\n")
                type.type(space_quote("Come on, tell me your real name!"))
    

    def interrogation(self):
        if self.has_met("Interrogator"):
            self.day_event()
            return
    
        self.meet("Interrogator")
        self.add_danger("Further Interrogation")
        type.type("You wake up, and through your windshield, you see a car parked right in front of you. Confused, and dazed, you sit up. As you open the door and get out of your car, you notice a man, in a bright red suit, peering into your trunk.")
        print("\n")
        type.type("The man sees you, and walks up to you.")
        print("\n")
        type.type(quote("You. You're awake. Good. You know that you aren't supposed to be here? This isn't a spot for people to live. This is a road for people to drive. I hope you know this."))
        print("\n")
        type.type(space_quote("Do you know this?"))
        answer = self.yes_or_no(space_quote("Do you? Know this?"))
        if answer == "yes":
            type.type(quote("So you do know this. Then why do you live here? You shouldn't. It's not right, man. I'd suggest you stop living here. Maybe live somewhere else instead. Just not here."))
            print()
        elif answer == "no":
            type.type(quote("You don't know this? How don't you know this? It's super obvious stuff, man. People don't live at places where they're not supposed to, and that's exactly what you're doing right now. I'd suggest you stop it, right this instant."))
            print()
        type.type("After the man tells you this, he looks up, and stares at the sun. And after about 20 seconds, he rubs his eyes, walks back to his car, and drives off.")
        print("\n")
        return

    # Cheap Day Events (1,000 - 10,000)
    # Everytime
    def sun_visor_bills(self):
        type.type("You wake up in the front seat, dripping in sweat. ")
        type.type("As the sun shines through the car window, you notice a few bright green bills above you, peeking out of the sun visor. How long have they been there? ")
        print("\n")
        bill = random.choice([3, 15, 30, 60, 150, 300])
        type.type("That's another " + green(bright("$" + str(bill))) + " dollars.")
        self.change_balance(bill)

    def strong_winds(self):
        type.type("You wake up to a loud snap above you, followed by a massive branch crashing down from the treetops and into the street. The wind echoes throughout the trees around you, and many of them look to be on the verge of falling.")
        print("\n")
        type.type("With the weater being this bad, you make the executive decision to just chill in the wagon for the day.")
        self.add_travel_restriction("Wind")
        print("\n")

    # Conditional
    def got_a_cold(self):
        if self.has_status("Cold"):
            self.day_event()
            return
        
        type.type("You wake up to a sneeze, followed by your nose running, droplets falling down from your chin and onto your shirt. Damn, must be a cold.")
        self.add_status("Cold")
        self.mark_day("Cold")
        print("\n")

    # One-Time
    def turn_to_god(self):
        if self.has_met("Ezekiel"):
            self.day_event()
            return
        
        self.meet("Ezekiel")
        type.type("You wake up to someone knocking on your window. You sit up, and see a man, holding a bible, and wearing a cross on a chain around his neck.")
        print("\n")
        type.type(quote("Hello! I'm Father Ezekiel. You seem to be in a tough spot, living in your car? I was just wondering if you wanted me to give you my copy of The Bible. It has the word of God, and I hope it could help you understand that you aren't alone on this journey of life."))
        print()
        type.type(space_quote("Do you accept my offer, and Jesus as your savior?"))
        answer = self.yes_or_no(space_quote("Do you?"))
        if answer == "yes":
            self.__is_religious = True
            type.type(space_quote("Why, that's wonderful!"))
            type.type("Father Ezekiel hands you his bible. ")
            type.type(quote("I will pray for you, and I know that Jesus will always be with you. Amen."))
        elif answer == "no":
            type.type(open_quote("Well, to each their own. I certainly cast no judgements. "))
            type.type(close_quote("I will pray for you, and I know that Jesus will always be with you. Amen."))
        print("\n")
        type.type("And with that, Father Ezekiel walks down the road, and out of sight.")
        print("\n")
        return
    
    def hungry_cow(self):
        if self.has_met("Betsy"):
            self.day_event()
            return
        
        self.meet("Betsy")
        self.add_danger("Betsy Tractor")
        type.type("You wake up to your whole car shaking. As you jump up from your seat, you see a beautiful black and white cow, staring you down through your window. ")
        type.type("The cow moos at you aggressively, and you open the door. On its back is a note, that reads 'This is Betsy. Betsy gets hungry. Please feed Betsy.'")
        print("\n")
        type.type("Betsy stares into your soul, then looks over at the seat next to you. It appears Betsy is interested in your pile of money. ")
        print()
        type.type("Do you feed Betsy? ")
        while True:
            answer = self.yes_or_no("Moo? ")
            if answer == "yes":
                type.type("You put a " + green(bright("$100")) + " dollar bill into Betsy's mouth. She chews it up, then spits it out in front of you.")
                self.change_balance(-100)
                random_chance = random.randrange(4)
                if (random_chance == 0) or (self.__balance < 500):
                    type.type("Betsy moos, then smiles. She walks down the road, happy as can be.")
                    break
                else:
                    type.type("Betsy moos, then stares you down. She doesn't seem to be done with you.")
                    print()
                    type.type("Do you feed Betsy? ")
            elif answer == "no":
                type.type("Betsy moos, then charges at you. She slams into your wagon hard, and your leg gets caught in the door. That hurt. Really, really bad.")
                print("\n")
                self.hurt(40)
                self.add_injury("Broken Leg")
                type.type("Betsy moos loudly, wags her tail, then walks down the road. Oh well.")
                break
        print("\n")

    # One-Time Conditional

    # Modest Day Events (10,000 - 100,000)
    # Everytime
    def left_door_open(self):
        type.type("You wake up in the front seat, with a chill throughout your body. ")
        type.type("Had the passenger door really been open all night? ")
        type.type("Hopefully nothing had gotten in. ")
        type.type("You reach over and close the door, just to be safe.")
        random_chance = random.randrange(6)
        if random_chance <= 3:
                self.add_danger("Spider")
        elif random_chance == 3:
                self.add_danger("Squirrel")
        print("\n")   

    # Conditional
    def another_spider_bite(self):
        if not self.has_danger("Spider") or self.has_status("Spider Bite"):
            self.day_event()
            return
        
        type.type("You wake up to a sharp pain on your neck! ")
        type.type("Swinging your arm to scratch the pain, you watch as a spider jumps to the backseat. ")
        if self.has_item("Pest Control"):
            self.kill_pests()
            type.type("You grab your " + magenta(bright("Pest Control")) + " and spray in the direction of the spider. ")
            type.type("A cloud of white liquid covers the spider, and you watch as it slows, and dies. ")
            type.type("Hopefully, that's the end of your spider problems.")
        else:
            type.type("The spider, now out of reach, crawls off the seat and onto the floor. ")
            type.type("You stick your head out back, but you aren't sure where the spider went, or if it has a family nearby. This is unfortunate.")
        self.add_status("Spider Bite")
        self.mark_day("Spider Bite")
        print("\n")

    def squirrel_invasion(self):
        if not self.has_danger("Squirrel") or self.has_status("Squirrel Bite") or self.has_status("Rabies") or self.has_item("Squirrely") or self.has_met("Squirrely"):
            self.day_event()
            return

        self.lose_danger("Squirrel")
        if self.has_item("Bag of Acorns"):
            self.use("Bag of Acorns")
            type.type("You wake up to the sound of something rummaging through your car. Looking in the backseat, you notice a little squirrel, chewing through your " + bright(magenta("Bag of Acorns")) + ". He looks pretty cute.")
            print("\n")
            if self.has_met("Dead Squirrely"):
                type.type("The squirrel notices you, and jumps from the bag, and over to your center console. He peers up at you, but your eyes are filled with tears. Nothing can ever replace Squirrely. You pick up the squirrel, open the door, and let it free.")
                print("\n")
                return
            else:
                type.type("The squirrel notices you, and jumps from the bag, and over to your center console. He peers up at you, with an acorn in hand, holding it up in your direction. You sick your hand out, and the squirrel give you the acorn. This must be a sign of peace.")
                print("\n")
                type.type("After an hour of watching the squirrel eat the acorns, climb around your car, and jump from your arm to the dashboard over and over, you decide that this squirrel is now yours. You name him 'Squirrely', in honor of him being a squirrel.")
                print("\n")
                self.add_item("Squirrely")
                self.mark_day("Squirrely Fed")
                return
        else:
            type.type("You wake up to a sharp pain on your leg! ")
            type.type("You swing the hurt leg, and you watch as a squirrel goes flying into the air. ")
            type.type("The littel rodent starts climbing around your car, scurrying around the walls, desperately trying to get out. ")
            type.type("You open the backseat windows, and the squirrel jumps out, and darts into the woods. Hopefully, that bite isn't too serious.")
            self.add_status("Squirrel Bite")
            random_chance = random.randrange(4)
            if random_chance == 1:
                self.add_status("Rabies")
                self.mark_day("Rabies")
            self.mark_day("Squirrel Bite")
            print("\n") 
            return
    # One-Time
            
    # One-Time Conditional
    def further_interrogation(self):
        if not self.has_met("Interrogator") or not self.has_danger("Further Interrogation"):
            self.day_event()
            return

        self.lose_danger("Further Interrogation")
        self.add_danger("Even Further Interrogation")
        type.type("You wake up, and through your windshield, you see a car parked right in front of you. Tired, and concerned, you sit up. As you open the door and get out of your car, you notice a man you've met before, in his bright red suit, once again peering into your trunk.")
        print("\n")
        type.type("The man sees you, and walks up to you, with a clipboard in his hand.")
        print("\n")
        type.type(space_quote("You. You're awake. Good. You see this clipboard? It says you can't be here."))
        type.type("You begin to read the paper on the clipboard. It's a message, written in Comic Sans.")
        print("\n")
        type.type("It reads 'This offical message from the government and the military and the army says that you can't be here. That's right, you, the person reading this message right now, living on this land right here. It's not for you. It won't ever be for you. So, you can't live here. You need to move right now, or I'll be very very angry.'")
        print("\n")
        type.type(space_quote("Did you read it?"))
        answer = self.yes_or_no(space_quote("Did you? Read it?"))
        if answer == "yes":
            type.type(quote("Good, so you know that all these powerful people want yo- are demanding that you move from where you're currently living, right this instant! I'd suggest you do so. I certainly wouldn't want to upset the government."))
            print()
        elif answer == "no":
            type.type(quote("You didn't read it? Come on, I worked so hard on it. You really should read a clipboard with words on it if someone asks you to. Regardless, it says that you need to move! Or the consequences will be scary!"))
            print()
        type.type("After the man tells you this, he looks up, and stares at the sun. And after about 25 seconds, he rubs his eyes, walks back to his car, and drives off.")
        print("\n")
        return
        
    # Rich Day Events (100,000 - 500,000)
    # Everytime
    def left_trunk_open(self):
        type.type("You wake up in the front seat, with a chill throughout the whole wagon. ")
        type.type("Had the trunk really been open all night? ")
        type.type("Hopefully nothing had gotten in. ")
        type.type("You get out of the car and close the trunk, just to be safe.")
        random_chance = random.randrange(6)
        if random_chance < 2:
                self.add_danger("Rat")
        elif random_chance < 4:
                self.add_danger("Termite")
        print("\n")    

    # Conditional
    def rat_bite(self):
        if self.has_status("Rabies") or not self.has_danger("Rat") or self.has_status("Rat Bite"):
            self.day_event()
            return

        type.type("You wake up to a sharp pain on your ankle! ")
        type.type("You look down to see a skinny gray rat nibling your foot. You kick at it, but the little rodent runs under the seat. ")
        print("\n")
        type.type("The rat jumps up onto your backseat, and begins to laugh at you. Now that's just cruel. This rat must be crazy.")
        print("\n")
        if self.has_item("Pest Control"):
            self.kill_pests()
            type.type("You grab your " + magenta(bright("Pest Control")) + " and spray the rat down. ")
            type.type("A cloud of white liquid covers the rat, and you watch as it spazzes out, and dies. ")
            type.type("Hopefully, that's it for your rat problems. Except for that bite. You might wanna get that checked out.")
        else:
            type.type("You jump at the seat towards the rat, but it sneaks back under the passenger seat, and you can't find it. ")
            type.type("That damn rat. Hopefully, the bite isn't too serious, but it's probably worth getting checked out.")
        self.add_status("Rat Bite")
        random_chance = random.randrange(2)
        if random_chance == 1:
            self.add_status("Rabies")
            self.mark_day("Rabies")
        self.mark_day("Rat Bite")
        print("\n") 
        return       
        

    def hungry_termites(self):
        random_choice = random.randrange(2)
        if (random_choice != 0) or not self.has_danger("Termite"):
            self.day_event()
            return

        type.type("You wake up to a clicking sound. Looking around, you notice that it's coming from your pile of money. ")
        type.type("You jump up to check your cash, and you find a termite eating away at your cash. ")
        if self.has_item("Pest Control"):
            self.kill_pests()
            type.type("You grab your " + magenta(bright("Pest Control")) + " and spray in the direction of the termite. ")
            type.type("A cloud of white liquid covers the termite, and you watch as it slows down, twitches, and dies. ")
            type.type("Hopefully, that's the end of your termite problems.")
        else:
            type.type("You attempt to swat it with your hand, but it falls under your car seat. ")
            type.type("You stick your head under the seat, but you aren't sure where the termite went, or if it has a family nearby. This is just brutal.")
        print("\n")
        type.type("The termite ate through a lot of your money. ")
        losses = int(self.get_balance() * (random.randint(20, 50)/100))
        type.type("You lost " + green(bright("${:,}".format(losses))) + ".")
        self.change_balance(-losses)

    # One-Time
            
    # One-Time Conditional
    def starving_cow(self):
        if not self.has_met("Betsy") or not self.has_danger("Betsy Tractor"):
            self.day_event()
            return

        self.add_danger("Betsy Army")
        self.lose_danger("Betsy Tractor")
        type.type("You wake up to the sound of a tractor barrling closer. As you jump up from your seat, you see the tractor getting closer to your wagon. ")
        type.type("The tractor drives beside your vehicle, and pushes right up against you, grinding the paint off your car. That's just mean. ")
        print("\n")
        type.type("You look up at the driver to see a beautiful black and white cow. Good god, it's Betsy. Why, Betsy, why. The cow moos at you aggressively, and you roll down the window. ")
        print("\n")
        type.type("Betsy stares into your soul, then looks over at the seat next to you. It appears Betsy is interested in your pile of money. ")
        print()
        type.type("Do you feed Betsy? ")
        while True:
            answer = self.yes_or_no("Moo? ")
            if answer == "yes":
                type.type("You reach out your window, and put a stack of bills, worth " + green(bright("$10,000")) + " into Betsy's mouth. She chews them up, then spits them out into your wagon.")
                self.change_balance(-10000)
                random_chance = random.randrange(4)
                if (random_chance == 0) or (self.__balance <50000):
                    type.type("Betsy moos, then smiles. She pulls away from the car, and drives the tractor down the road, happy as can be.")
                    break
                else:
                    type.type("Betsy moos, then stares you down. She doesn't seem to be done with you.")
                    print()
                    type.type("Do you feed Betsy? ")
            elif answer == "no":
                type.type("Betsy moos, then backs the tractor up. She then proceeds to step on the gas, and drives the tractor forward at your vehicle, slamming into the front of your wagon hard. She moos and moos and moos, pushing your car further back. The jolt of the vehicles smashing into each other kills, and your spine begins to fracture.")
                print("\n")
                self.hurt(80)
                self.add_injury("Fractured Spine")
                type.type("Betsy laughs a laugh, almost maniacal, before driving the tractor down the road.")
                break
        print("\n")

    # Doughman Days (500,000 - 900,000)
    # Everytime
    def thunderstorm(self):
        self.add_travel_restriction("Rain")
        type.type("You wake up to the sound of raindrops hitting the roof of your wagon. It starts with a couple, then a few, and before you even get the chance to stretch, it begins to pour. The sky is a dark, dark grey, and streams start to form along the road.")
        print("\n")
        type.type("The pitter-patter of the rain on your car lulls you back to sleep. When a strike of lightning wakes you once more, you look out the windows to see a few inches of rain covering the street. Welp, there goes your plans for the day.")
        print("\n")
        return
    
    # Conditional
            
    # One-Time
            
    # One-Time Conditional
    def even_further_interrogation(self):
        if not self.has_met("Interrogator") or not self.has_danger("Even Further Interrogation"):
            self.day_event()
            return

        self.lose_danger("Even Further Interrogation")
        self.add_danger("Final Interrogation")
        type.type("You wake up, and through your windshield, you see a car parked right in front of you. Not this again. As you open the door and get out of your car, you notice the man in his bright red suit, once again peering into your trunk.")
        print("\n")
        type.type("The man sees you, and walks up to you, with a badge in his hand.")
        print("\n")
        type.type(space_quote("You. You're awake. Good. You see this badge? It says I have the authority to make you not live here."))
        type.type("You look at the badge. It's a piece of paper, colored gold, with the letters 'FBI' and 'CIA' written in pencil.")
        print("\n")
        type.type(quote("See? I'm allowed to make you leave. And I'm invoking my right to do this right now!"))
        print("\n")
        type.type(space_quote("Are you gonna leave?"))
        answer = self.yes_or_no(space_quote("Are you? Gonna leave?"))
        if answer == "yes":
            type.type(quote("Good, you better do what I say, I'm super powerful. I hope you actually move and stop living here, because it's really getting on my nervers. I'll be back to make sure you do it, mark my words."))
            print()
        elif answer == "no":
            type.type(quote("What? But you have to! This badge says so! You better listen to me, because I'm really starting to get upset. I'll be back, and if you haven't moved yet, I'll make you, mark my words."))
            print()
        type.type("After the man tells you this, he looks up, and stares at the sun. And after about 30 seconds, he rubs his eyes, walks back to his car, and drives off.")
        print("\n")
        return
        
    # Nearly There Days (900,000+)
    # Everytime
        
    # Conditional
        
    # One-Time
        
    # One-Time Conditional
    def cow_army(self):
        if not self.has_met("Betsy") or not self.has_danger("Betsy Army"):
            self.day_event()
            return

        self.lose_danger("Betsy Army")
        type.type("You wake up to the sound of thousands of hoofsteps, getting closer to your wagon. You jump out of your seat, to see the street flooded with cows, all getting closer to your vehicle. ")
        type.type("At the front of the crowd, is a cow, distinct from the rest. It's Betsy. Of course, it's Betsy. God fucking dammit.")
        print("\n")
        type.type("Betsy leads the herd to your wagon, and as you roll the window down, all you can hear are the hundreds upon hundreds of moos, from each of the angry cows. ")
        print("\n")
        type.type("Betsy, and the rest of the cows, all stare into your soul, then look over at the seat next to you. It appears Betsy and her friends are interested in your pile of money. ")
        print()
        type.type("Do you feed Betsy and her friends? ")
        while True:
            answer = self.yes_or_no("Moo? ")
            if answer == "yes":
                type.type("You throw a bunch of bills into the crowd of cows, worth " + green(bright("$100,000")) + ". Betsy catches a bill, chews it up, then spits it out into your face.")
                self.change_balance(-100000)
                random_chance = random.randrange(4)
                if (random_chance == 0) or (self.__balance <100001):
                    type.type("Betsy moos, then smiles. The rest of the cows moo in harmony, and the crowd begins to march down the road, happy as can be.")
                    break
                else:
                    type.type("Betsy moos, then stares you down. The rest of the cows begin to moo. They don't seem to be done with you.")
                    print()
                    type.type("Do you feed Betsy? ")
            elif answer == "no":
                type.type("Betsy moos, then charges your vehicle. The rest of the cows start attacking your wagon, shattering the windows, knocking off the tires, and pummeling the doors.")
                print("\n")
                type.slow(red(bright("A pane of glass explodes next to you, sending shards into your face. One catches your eye, and you scream in pain. The cows continue to attack you, and your money is spiring all around you. Unable to see, and covered in blood, you close your eyes, and let yourself succumb to the army of cows. You won, Betsy, you won.")))
                self.kill()
                break
        print("\n")

    def final_interrogation(self):
        if not self.has_met("Interrogator") or not self.has_danger("Final Interrogation"):
            self.day_event()
            return

        self.lose_danger("Final Interrogation")
        type.type("You wake up, and through your windshield, you see a car parked right in front of you. You can feel your blood start to boil. What's this guys problem? As you open the door and get out of your car, you notice the man in his bright red suit, once again peering into your trunk.")
        print("\n")
        type.type("The man sees you, and walks up to you, with a pistol holstered to his waist.")
        print("\n")
        type.type(space_quote("You. I'm done playing around. It's time to move. I mean it."))
        type.type("You look down at the gun on his waist. It looks fancy, and certainly deadly.")
        print("\n")
        type.type(quote("I wouldn't test me if I were you. It's time to go, now."))
        print("\n")
        type.type(space_quote("Will you leave?"))
        answer = self.yes_or_no(space_quote("Answer me. "))
        if answer == "yes":
            type.type(quote("That's great. Fantastic. But I don't believe a word that comes out of your filty mouth. Prove it. Leave. Go away. GET OUT."))
            print("\n")
            type.type("You are fueled with anger. Who is this guy, and what gives him the right to harass you? All for being homeless? No longer. You reach for the gun on his waist.")
            print("\n")
            random_chance = random.randrange(4)
            if random_chance == 0:
                type.slow(red("Before you get the chance to grab it, the man steps back, unholsters the pistol, then fires three shots into your chest. The glass behind you shatters, and you fall to your knees in the street."))
                print("\n")
                type.slow(red(quote("You should've just listened to me man! All you had to do was listen! Move, live somewhere else. Find a home, anything. But no! You just had to live in your car, like the homeless piece of shit that you are!")))
                print("\n")
                type.slow(red(bright("The man kicks you down, and steps on your chest, causing the bullet holes to leak blood onto the concrete below you. As you feel yourself beginning to fade away, you watch the man lift his pistol to your head, and pull the trigger.")))
                self.kill()
            else:
                type.type("You snatch the gun from his holster, and he tackles you to the ground. You fight and struggle, each of you with both hands on the pistol. In the distance, you hear the horn of a freight truck beginning to drive closer. The man punches you in the arm, and it stings. Without thinking twice, you give the man a headbutt, and he falls backwards into the road. You point the gun at the man, and he begins to cry.")
                print("\n")
                type.type(quote("Please, I'm sorry. I didn't mean to cause any of this. I just, I hate seeing people living on the streets, all alone. I was just trying to help you. Just, please, for the love of god, don't hurt me."))
                print("\n")
                type.type("As the man begs for his life, the freight truck continues to draw closer, and the horn gets louder. You point at the truck in the distance, but the man can't see through the tears in his eyes.")
                print("\n")
                type.type(space_quote("Please, I have a family. I have children. My name is Phil. I don't wanna die. I'm too young. I can't die. I can't die. I ca-"))
                type.type("You watch as the freight truck crushes Phil, and continues down the road. Nothing remained but the splotches of blood that splattered the road where he once stood.")
                print("\n")
                type.type("After sitting a while, and recollecting your thoughts, you bring the pistol over to Phil's car, and throw it onto the passengers seat. Looking inside, the car has dice hanging on the mirror, and is filled to the brim with red suits. On the dashboard sits a photo, of Phil, his wife, and his three kids, all wearing bright red suits. Phil might've been crazy, but at least he was consistent.")
                print("\n")
                type.type("You get in the car, and drive it down the road, before turning into the woods. You drive a mile in, before parking the car before the lake. You get out, and push the car into the water, watching as it submerges.")
                print("\n")
                return
        elif answer == "no":
            type.type(quote("Really? You really want to do that? I warned you, man."))
            print("\n")
            type.type("The man pulls out his pistol, and points it at you. You lift your hands above your head, before quickly reaching for the pistol.")
            print("\n")
            random_chance = random.randrange(3)
            if random_chance == 0:
                type.slow(red("Before you get the chance to grab it, the man steps back, then fires three shots into your chest. The glass behind you shatters, and you fall to your knees in the street."))
                print("\n")
                type.slow(red(quote("Nice try, man! You should've just listened to me! All you had to do was listen! Move, live somewhere else. Find a home, anything. But no! You just had to live in your car, like the homeless piece of shit that you are!")))
                print("\n")
                type.slow(red(bright("The man kicks you down, and steps on your chest, causing the bullet holes to leak blood onto the concrete below you. As you feel yourself beginning to fade away, you watch the man lift his pistol to your hand, and pull the trigger.")))
                self.kill()
            else:
                type.type("You snatch the gun from his hands, and he tackles you to the ground. You fight and struggle, each of you with both hands on the pistol. The man punches you in the arm, and it stings. Without thinking twice, you give the man a headbutt, and he falls backwards into the road. You point the gun at the man, and he begins to cry.")
                print("\n")
                type.type(quote("Please, I'm sorry. I didn't mean to cause any of this. I just, I hate seeing people living on the streets, all alone. I was just trying to help you. Just, please, for the love of god, don't hurt me."))
                print("\n")
                type.type("As the man begs for his life, you cock the gun. You point pistol at the man, and he continues to cry.")
                print("\n")
                type.type(space_quote("Please, I have a family. I have children. My name is Phil. I don't wanna die. I'm too young. I can't die. I can't die. I ca-"))
                type.type("You pull the trigger, and Phil becomes quiet. His blood covers the street, but at least his red suit still looks good as new.")
                print("\n")
                type.type("After sitting a while, and recollecting your thoughts, you drag Phil over to his car. You stuff him into the trunk, and throw his pistol onto the passengers seat. Looking inside, the car has dice hanging on the mirror, and is filled to the brim with red suits. On the dashboard sits a photo, of Phil, his wife, and his three kids, all wearing bright red suits. Phil might've been crazy, but at least he was consistent.")
                print("\n")
                type.type("You get in the car, and drive it down the road, before turning into the woods. You drive a mile in, before parking the car before the lake. You get out, and push the car into the water, watching as it submerges.")
                print("\n")
                return


    # Poor Nights (1 - 1,000)
    # Everytime
    def ditched_wallet(self):
        type.type("Bored out of your mind, you decide to wander along the side of the road, just to get a change of scenery from the dusty leather seats of your wagon. ")
        type.type("As you take step after step over the asphalt, you notice a ditched wallet, just laying there. I guess it's yours now. ")
        print("\n")
        random_chance = random.randrange(2)
        if random_chance == 0:
            worth = random.randint(65, 120)
        else:
            worth = random.randint(7, 50)
        type.type("Inside the wallet, you find " + green(bright("$" + str(worth))) + " dollars.")
        self.change_balance(worth)

    def went_jogging(self):
        type.type("After spending an hour sitting in your car doing nothing, you feel like you should get some exersize. You get out of the wagon, and begin to jog down the road.")
        print("\n")
        type.type("A couple hours go by, and while jogging back, you see the wagon in the distance. ")
        random_chance = random.randrange(3)
        if random_chance == 0:
            type.type("But, right as you get to your car, you trip over a stone on the ground, and scrape your knee hard. Blood begins to drip down your leg. That's a bummer.")
            print("\n")
            self.hurt(random.choice([5, 10, 15]))
            self.add_injury("Scraped Knee")
            return
        else:
            type.type("You get back to the car, and get in, out of breath from your trip. You start the wagon and run the AC, and you feel good inside.")
            print("\n")
            self.heal(random.choice([5, 10, 15]))
            return

    def woodlands_path(self):
        type.type("After wandering from your vehicle, you find yourself deep in the woods. Squirrels run by and up into the trees. The sun hits every branch and casts a shadow below. And you wander on a natural path, journeying into the unknown.")
        print("\n")
        random_chance = random.randrange(3)
        if random_chance == 0:
            type.type("As you walk along the path, you find a mother deer, with two children, walking the path towards you. As you get closer, the mother appears cautious, but then runs in your direction, before stopping before you. ")
            type.type("Her two children follow behind, and before you know it, the three of them wait in front of you.")
            print("\n")
            type.type("You put your hand out, and pet the mother deer. She makes a happy squeak noise, and wags her tail. She touches her head to yours, then continues down the path, with her two children following.")
            print("\n")
            type.type("Eventually, you get to the end of the path, and find the main road. You follow it back to your wagon, and take a seat, to rest for a moment.")
            print("\n")
            return
        elif random_chance == 1:
            type.type("As you walk along the path, you notice someone laying against a tree in front of you. As you get closer, you notice that the person's face is blue, their eyes are bloodshot, and they don't appear to be breathing.")
            print("\n")
            type.type("You begin to panic, before thinking through the situation. They're already dead, so there's nothing you can do to help them. Maybe they had some money on them? I mean, they're not gonna use it. Why shouldn't you?")
            print()
            type.type("Do you search the body? ")
            answer = self.yes_or_no()
            if answer == "yes":
                type.type("You rummage through the pockets, trying to find anything worthwhile. ")
                random_chance = random.randrange(4)
                if random_chance == 0:
                    self.add_status("Hepatitus")
                    type.type("As you do so, you notice the body begin to move. It looks up at you, screams, then coughs blood all over you. You freak out, before running back down the path the way you came.")
                    print("\n")
                    type.type("You make it back to your car, and find some old clothes to wipe the blood off your face. Great, just great. You already start to feel under the weather.")
                    print("\n")
                    return
                else:
                    type.type("After a minute of digging, you manage to find a wallet. Score!")
                    print("\n")
                    worth = random.randint(100, 150)
                    type.type("Inside the wallet, you find " + green(bright("$" + str(worth))) + " dollars.")
                    self.change_balance(worth)
                    type.type("You leave the dead body, and continue down the path, until the forest opens up to the main road. You follow the road back to your wagon, with your winnings in hand.")
                    print("\n")
                    return
            elif answer == "no":
                type.type("While this body might be the body of a rich man, judging by the situation, it's very unlikely. Plus, dead bodies tend to be unsanitary. No, this body was simply not worth searching.")
                print("\n")
                type.type("You continue down the path, before the forest opens up to the main road. You follow the road back to your wagon, and sit. You rest for a while.")
                print("\n")
                return
        else:
            type.type("You walk, and walk, and walk further down the path, before the forest opens up to the main road. You follow the road back to your wagon, wondering if there was anything you missed. At least you made it back safe and sound.")
            print("\n")
            return
                

    # Cheap Nights (1,000 - 10,000)
    # Everytime
    def woodlands_river(self):
        type.type("After wandering from your vehicle, you find yourself deep in the woods. Deer dart by you. Trees branches sway back and forth. And you wander along a river, journeying into the unknown.")
        print("\n")
        random_chance = random.randrange(3)
        if random_chance == 0:
            type.type("As you walk further, you stumble across a large brown bear, bathing in the river. ")
            if self.has_item("Quiet Sneakers"):
                print("\n")
                type.type("Thank goodness you're wearing your " + magenta(bright("Quiet Sneakers")) + "!")
                print("\n")
                type.type("You turn and run back up the riverbank, never looking back. Eventually, you make it out of the woods, and return to your car, safe and sound.")
                print("\n")
                self.update_quiet_sneakers_durability()
                return
            else:
                type.type("Right as you're about to turn around, you step on a branch, which makes a loud crunching noise. ")
                print("\n")
                random_chance_2 = random.randrange(2)
                if random_chance_2 == 0:
                    type.type("The bear sits up from the water, and glares at you. Before you get a chance to react, the bear charges at you. He swipes at your leg. He bites your arm. He punches your neck. My, what a beating he gave you.")
                    print("\n")
                    self.hurt(75)
                    type.type("Thankfully, you're able to play dead, just long enough for the bear to walk away without killing you. Somehow, you get up, and limp your way back to your wagon.")
                    print("\n")
                    type.type("The damage inflicted from the bear is serious and severe. It's probably a good idea to see the doctor tomorrow, when they're open again. In the meantime, you wrap yourself up with spare clothes, and go on with your life.")
                    self.add_injury("Severed Skin")
                    print("\n")
                    return
                elif random_chance_2 == 1:
                    type.type("Thankfully, it seems that the bear doesn't notice you. You quietly step away, before running back up the riverbank. Eventually, you make it out of the woods, and back to your wagon, safe and sound. That could've gone a lot worse!")
                    print("\n")
                    return
        elif (random_chance == 1) and not (self.has_item("Map")):
            type.type("As you walk further, you stumble across an old treasure chest, sitting in the river, the water flowing around it. ")
            type.type("Walking closer, you wade the water to get to the chest, and open up the lid. Inside, you find a large paper drawing. Opening it up, you realize that it's a map that resembles the town you're parked just outside of. Down one of the side roads, there's an old bridge with a star underneath it. The caption reads 'To those who wish to visit Marvin, just go to the bridge, and follow the stars.'")
            print("\n")
            self.add_item("Map")
            type.type("You got the " + magenta(bright("Map")) + "! You can now drive to Marvin's Mystical Merchandise!")
            type.type("Without a second thought, you pocket the map, and turn back, following the riverbank home.")
            print("\n")
            return
        else:
            type.type("You keep walking, and keep walking, and keep walking, and eventually, the woods clear up, and you're back on the main road. You follow it back to your car, wondering if there was anything else to see. Well, at least you're home, safe and sound.")
            print("\n")
            return
   
    # Modest Nights (10,000 - 100,000)
        
    # Rich Nights (100,000 - 500,000)
        
    # Doughman Nights (500,000 - 900,000)
        
    # Nearly There Nights (900,000+)

    def yes_or_no(self, reiterate = "What? "):
        while True:
            yes_or_no = input("").lower()
            if (yes_or_no == "y") or (yes_or_no == "yes"):
                print()
                return "yes"
            elif (yes_or_no == "n") or (yes_or_no == "no"):
                print()
                return "no"
            else:
                type.type(reiterate)

    def empty_event(self):
        type.type("This day's events are empty. Therefore, this played. Thank you.")
        print("\n")

    # Story Events
    def trusty_tom(self):
        self.meet("Tom Event")
        type.type("You wake up to a blaring engine, roaring down the road towards you. ")
        type.type("As you scratch your eyes awake, you read \'Tom's Trusty Trucks and Tires\' painted on the hood of a bright gold truck. ")
        type.type("Waving the vehicle down, the truck slows, then halts, and an old, jolly man jumps out. ")
        print("\n")
        type.type("\"Well, howdy! The name's Tom. It appears you've gotten yourself in a bit of a pickle, ya think?\" ")
        type.type("Tom pulls a big red wrench out of his pocket, and walks to the hood of your beaten down wagon. ")
        repair_price = random.choice([150, 200, 250, 300, 350])
        type.type("\"Yep, this thing's busted alright! Tell ya what, for, I don't know, " + green(bright(str(repair_price) + " bucks")) + ", I'll get this thing replaced for ya, good as new! Whaddya say?\" ")
        while(True):
            yes_or_no = input("").lower()
            print()
            if(yes_or_no == "n") or (yes_or_no == "no"):
                type.type("\"Really? No dice, huh. Yunno, I think you're makin' a mistake, but I ain't one to judge. You have a nice day now.\" ")
                type.type("Tom has a sad look in his eye. It's clear that he wanted to help you. ")
                type.type("You watch as his big golden truck stutters, starts, then drives away.")
                print("\n")
                return
            elif((yes_or_no == "y") or (yes_or_no == "yes")):
                if self.__balance >= repair_price:
                    self.meet("Tom")
                    type.type("\"Really? Awesome! I'll be the best dang mechanic this ol' automobile has ever seen!\" ")
                    type.type("You watch in awe, as Tom, a man who has clearly perfected his craft, fixes up your wagon in no time. Sweet. ")
                    self.change_balance(-repair_price)
                    self.add_item("Car")
                    type.type(magenta(bright("Your car has been fixed! You can now drive around!")))
                    print("\n")
                    type.type("\"Well, gee, this has been fun. Be seein' you around, ya know?\" ")
                    type.type("And with that, you watch as his big golden truck stutters, starts, then drives away.")
                    print("\n")
                    return
                else:
                    type.type("\"Aww man, sorry to tell you, but you just don't got enough funds for this, yunno?\" ")
                    random_chance = random.randrange(2)
                    # Broke, and Tom offers discount
                    if random_chance == 0:
                        print("\n")
                        type.type("\"You know what? I'm feelin' generous, and the shop's been doing well lately. ")
                        type.type("Tell ya what, I can take the offer down " + green(bright(str(50) + " dollars")) + " just for you. ")
                        type.type("Could ya do " + green(bright(str(repair_price-50) + " bucks")) + "?\" ")
                        while True:
                            yes_or_no_2 = input("").lower()
                            print()
                            # Declining Tom's second offer
                            if(yes_or_no_2 == "n") or (yes_or_no_2=="no"):
                                print()
                                type.type("\"Really? No dice, huh. Even with the discount? Yunno, I think you're makin' a mistake, but I ain't one to judge. You have a nice day now.\" ")
                                type.type("Tom has a dissapointed look in his eye. It's clear that he wanted to help you. ")
                                type.type("You watch as his big golden truck stutters, starts, then drives away.")
                                print("\n")
                                return
                            elif((yes_or_no_2 == "y") or (yes_or_no_2 == "yes")):
                                if self.__balance >= (repair_price-50):
                                    self.meet("Tom")
                                    type.type("\"Really? Awesome! I'll be the best dang mechanic this ol' automobile has ever seen!\" ")
                                    type.type("You watch in awe, as Tom, a man who has clearly perfected his craft, fixes up your wagon in no time. Sweet. ")
                                    self.change_balance(-(repair_price-50))
                                    self.add_item("Car")
                                    type.type(magenta(bright("Your car has been fixed! You can now drive around!")))
                                    print("\n")
                                    type.type("\"Well, gee, this has been fun. Be seein' you around, ya know?\" ")
                                    type.type("And with that, you watch as his big golden truck stutters, starts, then drives away.")
                                    print("\n")
                                    return
                                else:
                                    type.type("\"Still can't afford it? That's a real shame. I really wish there was something I could do. Best of luck my friend. Be seeing ya around, ya know?\" ")
                                    type.type("And with that, you watch as his big golden truck stutters, starts, then drives away.")
                                    print("\n")
                                return
                            else:
                                type.type("\"Whaddya say?\" ")

                    # Broke, and Tom can't offer discount
                    elif random_chance == 1:
                        print("\n")
                        type.type("\"I really wish there was something I could do. Best of luck my friend. Be seeing ya around, ya know?\" ")
                        type.type("And with that, you watch as his big golden truck stutters, starts, then drives away.")
                        print("\n")
                        return
            else:
                type.type("\"Whaddya say?\" ")



    def filthy_frank(self):
        self.meet("Frank Event")
        type.type("You wake up to a roaring engine, blasting into your eardrums. ")
        type.type("As you jump up out of the front seat, you read \'Filthy Frank's Flawless Fixtures\' painted on the hood of a...well...a beater. ")
        type.type("Waving the vehicle down, the beater slows, then appears to break down, and an old man with tattoo sleeves and long black hair steps out. He kicks his car, and the engine starts blaring once more. ")
        print("\n")
        type.type("\"Hello, the name's Frank. Now I've got a baseball game to catch, but it looks like you could use some help.\" ")
        type.type("Frank pulls a shiny silver hammer out of his pocket, and walks to the hood of your beaten down wagon. ")
        repair_price = random.choice([50, 75, 100])
        type.type("\"My god. This is just awful. Tell you what, I can fix this up for like " + green(bright(str(repair_price) + " bucks")) + ", and your engine will be runnin' just as good as mine. You game?\" ")
        while(True):
            yes_or_no = input("").lower()
            print()
            if(yes_or_no == "n") or (yes_or_no == "no"):
                type.type("\"What?! How could you not accept my service? I'm the cheapest damn autoshop worker on this here planet! But NOOOO, NOT FRANK! Never Frank. He Voted For Trump! Let's all ridicule frank for his political party. You god damn liberals.\" ")
                type.type("Frank spits in your face, and get back in his truck. ")
                print("\n")
                type.type("You watch as he revs his engine, gets out of his truck, kicks his beater, gets back in, revs his engine, and speeds off into the horizon. ")
                print("\n")
                return
            elif((yes_or_no == "y") or (yes_or_no == "yes")):
                if self.__balance >= repair_price:
                    type.type("\"Darn tootin! Lemme just do my thing.\" ")
                    type.type("You watch in terror as Frank takes the hammer, and begins to beat the living daylight out of your wagon's engine. Each swing causes you to wince more and more. ")
                    self.change_balance(-repair_price)
                    random_chance = random.randrange(5)
                    if random_chance < 2:
                        self.meet("Frank")
                        self.add_item("Car")
                        type.type(magenta(bright("Your car has been fixed! You can now drive around!")))
                        print("\n")
                        type.type("\"Ah, I love fixin people's cars. You sure do drive a shitty vehicle, but I'm just glad I can help get you back up and going to your job every day. Gotta do something to help in this economy, you know?\" ")
                        print("\n")
                        type.type("And with that, you watch as he revs his engine, gets out of his truck, kicks his beater, gets back in, revs his engine, and speeds off into the horizon.")
                        print("\n")
                        return
                    else: 
                        type.type("You notice Frank beginning to sweat while trying to fix your car. Each swing of his hammer is getting louder and louder, and Frank is clearly beginning to panic. Frank turns towards you, with tears streaming down his face. Or maybe it's just sweat.")
                        print("\n")
                        type.type("\"Oh man, listen, I'm so sorry about this, you know? I really thought if I just gave it the old hammer whirl that would do the trick. Hold on, maybe I have something in my truck. Stay right here!\"")
                        print("\n")
                        type.type("You watch Frank runs over to his truck, kicks the side of it, gets in, revs his engine, and speeds off into the horizon. God Dammit.")
                        print("\n")
                        return
                else:
                    self.add_danger("Frank")
                    type.type("\"Are you tryna rip me off? Clearly you don't have enough money to afford my services, which is honestly pathetic, since I have the cheapest services around! I don't get what it is with you young folk and not working, just staying home and smoking weed. It's miserable. You're miserable. Dontchu know I know people on the inside! I'll remember this one.\"")
                    print("\n")
                    type.type("You watch as he revs his engine, gets out of his truck, kicks his beater, gets back in, revs his engine, and speeds off into the horizon.")
                    print("\n")
                    return
            else:
                type.type("\"Speak up! You're mumbling. \" ")



    def optimal_oswald(self):
        self.meet("Oswald Event")
        type.type("You wake up to the sight of a glossy black limousine, quietly approaching your wagon. ")
        type.type("As you sit up from your slumber, you read \'Oswald's Optimal Outoparts\' cursively engraved in gold letters on the side of the limo. ")
        type.type("Waving the vehicle down, the limo slows, then stops before you. The door opens vertically, and a large red carpet is rolled out onto the street. You watch in awe as a man, with a combover and a tuxedo, walks out before you. He coughs, then speaks.")
        print("\n")
        type.type("\"Why hello there! The name's Oswald, as you can see by my nametag. Do you like my bowtie? Well of course you do! It appears your limousine has broken down.\" ")
        type.type("Oswald pulls a gold whistle out of his pocket, and blows into it deeply. ")
        type.type("\"Oh Stuart!\" You watch as a bald man in a tailcoat suit, no taller than 4 feet, hobbles over to Oswald's side.")
        print("\n")
        type.type("\"This is Stuart! He will fix your limousine up for a fair price. Let's say, I don't know, I suppose a fair price is " + green(bright("500,000 dollars")) + ". ")
        repair_price = random.choice([800, 850, 900])
        type.type("Okay, the look on your face says that I'm making a big mistake. Let's try " + green(bright("$" + str(repair_price))) + ", and Stuart here will get you back on the road! Do you accept?\" ")
        while(True):
            yes_or_no = input("").lower()
            print()
            if(yes_or_no == "n") or (yes_or_no == "no"):
                type.type("\"Really? You don't want my services? I'm so sorry Stuart, But it appears they don't want our services.\" ")
                type.type("Stuart begins to break down into tears, and he runs quickly back into the limo. ")
                type.type("\"Shame on you! Shame on you! I hope to never see the likes of you again.\"")
                print("\n")
                type.type("You watch as Oswald rolls up the red carpet, gets back in the limo, and drives off into the distance.")
                print("\n")
                return
            elif((yes_or_no == "y") or (yes_or_no == "yes")):
                if self.__balance >= repair_price:
                    self.meet("Oswald")
                    type.type("\"Jolly good! Stuart!\" ")
                    type.type("You watch as the little man walks to the front of your wagon, opens the hood, and jumps in. You can't really see what's going on, but after a couple of minutes, Stuart jumps back out, covered in oil.")
                    self.change_balance(-repair_price)
                    self.add_item("Car")
                    type.type(magenta(bright("Your car has been fixed! You can now drive around!")))
                    print("\n")
                    type.type("\"Oh my Stuart! Someone got a little too excited, didn't you? Yep, you're getting a bath as soon as we get back to the shop. Thanks again, stranger, it's been a pleasure doing business with you. I recall it's good custom to tip after events like this, yes? Here, take this.\" ")
                    tip = random.choice([50, 100])
                    type.type("Oswald hands you a bright green bill, worth " + green(bright("$" + str(tip))) + ".")
                    self.change_balance(tip)
                    type.type("And with that, you watch as Stuart rolls up the red carpet. Oswald and Stuart get back in the limo, and drive off into the distance.")
                    print("\n")
                    return
                else:
                    type.type("\"Why, it appears you're far too poor to attain my services. I'm truly sorry about this. Tell you what, here's a little something to get you back on your feet.\" ")
                    tip = random.choice([50, 100])
                    type.type("Oswald hands you a bright green bill, worth " + green(bright("$" + str(tip))) + ".")
                    self.change_balance(tip)
                    type.type("And with that, you watch as Stuart rolls up the red carpet. Oswald and Stuart get back in the limo, and drive off into the distance. ")
                    if self.__balance > repair_price:
                        type.type("Looking down, you see that after Oswald's tip, you had enough money to pay for the repair service after all, but it was too late. Oh well.")
                    print("\n")
                    return
            else:
                type.type("\"Come again?\" ")


    def update_story_event_prereqs(self):
        if(self.__balance>=200):
            self.__prereqs[0] = True
        if self.has_item("Car"):
            self.__prereqs_done[0] = True

    def start_day(self):
        self.update_rank()
        self.update_story_event_prereqs()
        ranStoryEvent = False

        if((self.__prereqs[0]) and not (self.__prereqs_done[0])):
            random_chance = random.randrange(3)
            if random_chance == 0:
                while((not self.has_met("Tom Event")) or (not self.has_met("Frank Event")) or (not self.has_met("Oswald Event"))):
                    random_chance = random.randrange(3)
                    if (random_chance == 0) and (not self.has_met("Tom Event")):
                        self.trusty_tom()
                        ranStoryEvent = True
                        break
                    elif (random_chance == 1) and (not self.has_met("Frank Event")):
                        self.filthy_frank()
                        ranStoryEvent = True
                        break
                    elif (random_chance == 2) and (not self.has_met("Oswald Event")):
                        self.optimal_oswald()
                        ranStoryEvent = True
                        break

        if ranStoryEvent == False:
            self.day_event()

        self.update_rank()


    def has_pests(self):
        if self.has_danger("Spider"):
            return True
        elif self.has_danger("Cockroach"):
            return True
        else:
            return False

    def kill_pests(self):
        self.use_item("Pest Control")
        if self.has_danger("Spider"):
            self.lose_danger("Spider")
        if self.has_danger("Cockroach"):
            self.lose_danger("Cockroach")
        if self.has_danger("Rat"):
            self.lose_danger("Rat")
        if self.has_danger("Termite"):
            self.lose_danger("Termite")

    def get_mark_index(self, mark):
        match mark:
            case "Spider Bite":
                return 0
            case "Hepatitis":
                return 1
            case "Squirrel Bite":
                return 2
            case "Squirrely Fed":
                return 3
            case "Rabies":
                return 4
            case "Rat Bite":
                return 5
            case "Snake Bite":
                return 6
            case "Sore Throat":
                return 7
            case "Cold":
                return 8
            case "Mechanic":
                return 9

    def mark_day(self, mark, time="day"):
        i = self.get_mark_index(mark)
        if time == "day":
            self.__counting_days[i] = self.__day
        if time == "night":
            self.__counting_days[i] = self.__day-1

    def get_days_elapsed(self, mark):
        i = self.get_mark_index(mark)
        return self.__day - self.__counting_days[i]
    
    
    def update_silver_value(self):
        if self.has_item("Enchanting Silver Bar"):
            return 1000

    def update_status(self):
        damage = 0
        if self.__clear_all_status == True:
            type.type("Whatever the Witch Doctor gave you yesterday, it worked wonders on you. You feel amazing, as though your body had been completely cleansed.")
            print("\n")
            self.__status_effects = set()
            self.__injuries = set()
            self.__is_sick = False
            self.__is_injured = False
            self.__clear_all_status = False

        # Physical Threats
        # Spider Bite
        if self.has_status("Spider Bite"):
            days_elapsed = self.get_days_elapsed("Spider Bite")
            if(self.__clear_status):
                self.remove_status("Spider Bite")
                type.type("Your spider bite is starting to heal. ")
            elif days_elapsed == 0:
                damage += random.choice([1, 2])
                type.type("The fangmarks of your spider bite are faint but visible. ")
            elif days_elapsed == 1:
                damage += random.choice([3, 4, 5, 6])
                type.type("Your spider bite is sore and swolen. ")
            elif days_elapsed == 2:
                damage += random.choice([4, 5, 6, 7, 8, 9])
                type.type("Your spider bite is really painful. You don't feel good. ")
            elif days_elapsed >= 3:
                random_chance = random.randrange(4)
                if (random_chance == 0):
                    self.remove_status("Spider Bite")
                    type.type("Your spider bite is starting to heal. ")
                else:
                    damage += random.choice([7, 9, 11, 13, 15])
                    type.type("Your spider bite is purple and pussing. A trip to the doctors might be a good idea. ")
            print("\n")

            if damage >= self.__health:
                self.hurt(damage)

        # Snake Bite
        if self.has_status("Snake Bite"):
            days_elapsed = self.get_days_elapsed("Snake Bite")
            if(self.__clear_status):
                self.remove_status("Snake Bite")
                type.type("Your snake bite is starting to heal. ")
            elif days_elapsed == 0:
                damage += random.choice([2, 4])
                type.type("The fangmarks of your snake bite are faint but visible. There's some swelling. ")
            elif days_elapsed == 1:
                damage += random.choice([6, 8, 10, 12])
                type.type("Your snake bite is swolen, and very painful. ")
            elif days_elapsed == 2:
                damage += random.choice([8, 10, 12, 14, 16, 18])
                type.type("Your snake bite is really painful. You feel really nauseous. ")
            elif days_elapsed >= 3:
                damage += random.choice([7, 14, 18, 22, 26, 30])
                type.type("Your snake bite is turning black. A trip to the doctors is probably the right choice. ")
            print("\n")

            if damage >= self.__health:
                self.hurt(damage)

        # Squirrel Bite
        if self.has_status("Squirrel Bite"):
            days_elapsed = self.get_days_elapsed("Squirrel Bite")
            if(self.__clear_status):
                self.remove_status("Squirrel Bite")
                type.type("Your squirrel bite is starting to heal. ")
            elif days_elapsed == 0:
                type.type("You look at the bite mark the squirrel left on your leg, but it's hard to tell if it's infected. A trip to the doctor's would solve all your worries.")
            elif ((days_elapsed >= 1) and self.has_status("Rabies")) or (days_elapsed < 5):
                type.type("Your squirrel bite looks the same as it did yesterday.")
            elif (days_elapsed == 5):
                self.remove_status("Squirrel Bite")
                type.type("Your squirrel bite is starting to heal. ")
            print("\n")

        # Rat Bite
        if self.has_status("Rat Bite"):
            days_elapsed = self.get_days_elapsed("Rat Bite")
            if(self.__clear_status):
                self.remove_status("Rat Bite")
                type.type("Your rat bite is starting to heal. ")
            elif days_elapsed == 0:
                type.type("You look at the bite mark the rat left on your ankle. It hurts like a motherfucker, but it's hard to tell if the bite infected. A trip to the doctor's is what a smart person would do.")
            elif ((days_elapsed >= 1) and self.has_status("Rabies")) or (days_elapsed < 5):
                type.type("Your rat bite looks the same as it did yesterday. It might hurt worse, but it's hard to tell.")
            elif (days_elapsed == 5):
                self.remove_status("Rat Bite")
                type.type("Your rat bite is starting to heal. ")
            print("\n")

        # Rabies
        if self.has_status("Rabies"):
            days_elapsed = self.get_days_elapsed("Rabies")
            if(self.__clear_status) and (days_elapsed<=3):
                self.remove_status("Rabies")
            elif days_elapsed==3:
                type.type(red("Your mouth has begun to foam. It seems you've contracted rabies. Death is inevitable, and it's hurdling towards you."))
                damage += random.choice([10, 30, 50, 70])
                print("\n")
            elif days_elapsed==4:
                type.type(red("The foaming has gotten worse, to the point where you begin to choke on it. You have a seizure in your car. Life is coming to an end."))
                damage += random.choice([50, 70, 90])
                print("\n")
            elif days_elapsed==5:
                type.slow(red(bright("Your mind has gone completely insane. You start tearing at your face, ripping away chunks of skin. The foam in your mouth turns red, and you feel yourself begin to fade from existance. You pull your eyes from their sockets, and scream in agony, as you die a painful death.")))
                self.kill()

            if damage >= self.__health:
                self.hurt(damage)


        # Sicknesses
        # Cold
        if self.has_status("Cold"):
            self.__is_sick = True
            days_elapsed = self.get_days_elapsed("Cold")
            if(self.__clear_status):
                self.remove_status("Cold")
            elif days_elapsed == 0:
                damage += random.choice([2, 3, 6])
            elif days_elapsed == 1:
                damage += random.choice([2, 5, 7])
            elif days_elapsed > 3:
                random_chance = random.randrange(2)
                if random_chance == 0:
                    self.remove_status("Cold")
                else:
                    damage += random.choice([3, 4, 5, 6, 7, 8, 9])

        # Sore Throat
        if self.has_status("Sore Throat"):
            self.__is_sick = True
            days_elapsed = self.get_days_elapsed("Sore Throat")
            if(self.__clear_status):
                self.remove_status("Sore Throat")
            elif self.has_item("Cough Drops"):
                type.type("With your " + bright(magenta("Cough Drops")) + " in hand, you begin to suck each drop, one by one, until the box is empty, and your throat feels nice and cool.")
            elif days_elapsed == 0:
                damage += random.choice([1, 3, 5])
            elif days_elapsed == 1:
                damage += random.choice([2, 4, 5])
            elif days_elapsed > 3:
                random_chance = random.randrange(2)
                if random_chance == 0:
                    self.remove_status("Sore Throat")
                else:
                    damage += random.choice([5, 6])

        # Hepatitis
        if self.has_status("Hepatitis"):
            self.__is_sick = True
            days_elapsed = self.get_days_elapsed("Hepatitis")
            if(self.__clear_status):
                self.remove_status("Hepatitis")
            elif days_elapsed == 0:
                damage += random.choice([1, 3, 5])
            elif days_elapsed == 1:
                damage += random.choice([5, 6, 7])
            elif days_elapsed == 2:
                damage += random.choice([2, 7, 10, 12])
            elif days_elapsed == 3:
                damage += random.choice([2, 8, 15, 17, 20])
            elif days_elapsed == 4:
                damage += random.choice([3, 9, 18, 20, 25])
            elif days_elapsed > 4:
                random_chance = random.randrange(4)
                if random_chance == 0:
                    self.remove_status("Hepatitis")
                else:
                    damage += random.choice([5, 10, 15, 20, 25, 30])


        # Sets is_sick to False if you don't have any sicknesses, an prints a health update
        if (self.__is_sick) and not (self.has_status("Hepatitis") and not self.has_status("Sore Throat") or self.has_status("Cold")):
            if self.has_status("Rabies"):
                type.type("With rabies in your system, you're lucky to be alive.")
            elif self.has_status("Snake Bite") or self.has_status("Spider Bite"):
                type.type("You may not be 100%, but at least you don't feel under the weather anymore.")
            else:
                type.type("You feel much less sick than you did yesterday, which is always good.")
            self.__is_sick = False
            print("\n")

        # if player is sick, prints a sickness update
        if self.__is_sick:
            type.type(self.__lists.get_sickness_update())
            print("\n")

        # If sickness kills the player, this does it.
        if damage >= self.__health:
                type.slow(bright(red(self.__lists.get_sickness_death())))
                self.kill()

        # Sets is_injured to True if you have 1 or more injuries
        if len(self.__injuries)>0:
            self.__is_injured = True

        # Sets is_injured to False if you have 0 injuries, and prints a healed update
        if (self.__is_injured) and len(self.__injuries)==0:
            type.type("The injuries on your body are doing much better.")
            print("\n")
            self.__is_injured = False
        
        # If you're injured, prints an injury update, and adds damage
        if self.__is_injured:
            damage += len(self.__injuries)
            type.type(self.__lists.get_injury_update())
            print("\n")

        # If you took damage, this does it.
        if damage > 0:
            self.hurt(damage)

        self.__clear_status = False

        # Sprays your car with Pest Control if you have a pest
        if self.has_pests() and self.has_item("Pest Control") and (not self.has_travel_restriction("Rain")) and (not self.has_travel_restriction("Wind")):
            type.type("Believing that there may be an unwanted pest somewhere in your car, you spray your " + magenta(bright("Pest Control")) + " throughout the vehicle, hoping that it'll solve your pest issues. ")
            self.kill_pests()
            type.type("After giving the wagon a minute to air out, you get back inside.")
            print("\n")

        # Feeds Squirrely if you have Acorns
        if self.has_item("Bag of Acorns") and self.has_item("Squirrely"):
            type.type("You give Squirrely your " + magenta(bright("Bag of Acorns")) + ", and he goes to town, munching down all of them. What a good squirrel.")
            print("\n")

        # Gives Squirrely Status Update
        if self.has_item("Squirrely"):
            days_elapsed = self.get_days_elapsed("Squirrely Fed")
            if self.has_travel_restriction("rain") or self.has_travel_restriction("Wind"):
                type.type(self.__lists.get_worried_squirrely_update())
            if days_elapsed == 0:
                type.type("Squirrely is well-fed, and happy as can be.")
            elif days_elapsed <= 4:
                type.type(self.__lists.get_fed_squirrely_update())
            elif days_elapsed < 6:
                type.type(self.__lists.get_hungry_squirrely_update())
            elif days_elapsed >= 6:
                random_chance = random.randrange(5)
                if random_chance == 0:
                    type.type("Looking around, you can't find Squirrely anywhere. No, seriously, you can't find him anywhere. Beginning to panic, you start to tear the car apart, hoping that you'll find him somewhere. You call out his name, 'Squirrely', 'Squirrely', but you get no response. Tears start falling from your eyes. Is this really it? Is this really goodbye? Poor Squrrely, all alone. You may never see your little Squirrely ever again.")
                    self.use_item("Squirrely")
                    self.meet("Squirrely")
                elif random_chance == 1:
                    type.type("Looking around, you can't find Squirrely anywhere. No, seriously, you can't find him anywhere. And that smell, it reeks! You begin to fear for the worst. Tearing the car apart, you find him, laying lifeless under the passenger seat. Poor Squirrely.")
                    print("\n")
                    type.type("Using an old shirt, you pick Squirrely off the floor of the wagon. Carrying him into the woods, you set him down, and dig a hole. You place Squirrely inside, cover him up with dirt, and place a flower over the grave. Goodbye, Squirrely. I loved you.")
                    self.use_item("Squirrely")
                    self.meet("Dead Squirrely")
                else:
                    type.type(self.__lists.get_hungry_squirrely_update())
            print("\n")


    def afternoon(self):
        self.update_status()
        self.update_rank()
        self.update_convenience_store_inventory()
        if self.has_travel_restriction("Wind"):
            random_chance = random.randrange(3)
            if random_chance == 0:
                type.type("You watch the wind pull twigs and branches from the trees all afternoon.")
            elif random_chance == 1:
                type.type("One branch falls, and lands on the hood of your wagon. Had it been any bigger, that could've been bad.")
            elif random_chance == 2:
                type.type("You hear a loud crash in the distance. A tree must've fallen nearby.")
            else:
                type.type("The wind pushes the light gray clouds across the sky, and you watch them all afternoon.")
            
            print("\n")
            
            type.type("As the sun begins to fall, you collect your money, and leave the warmth of your wagon. You barrel out into the wind, trudging your way to the casino.")

            print("\n")
            random_chance = random.randrange(3)
            if random_chance == 1:
                type.slow(red("It's a windy one today. Now, let us gamble."))
            elif random_chance == 2:
                type.slow(red("Suprised you made it here in one piece, given the weather. It's time to bet."))
            elif random_chance == 3:
                type.slow(red("It's nice to see you tonight. Shows commitment. You ready?"))
            else:
                type.slow(red("Wind didn't blow any of your money away, did it? Anyways, let's play."))
            print("\n")

        elif self.has_travel_restriction("Rain"):
            type.type("You watch, as the rain pours, and pours, and pours. By nightfall, the rain hasn't let up, and flooding in the streets has only gotten worse. Unfortunately, you're gonna have to skip out on Blackjack for the night.")
            print("\n")
            type.type("You get cozy in your car, and begin to doze off. ")
            print("\n")
            type.type()

        elif self.has_travel_restriction("Battery"):
            pass

        elif self.has_travel_restriction("Engine"):
            pass
            
        elif self.has_item("Car"):
            choice = None
            shops = self.__lists.make_shop_list()
            type.type("Would you like to spend your day driving somewhere? ")
            print()
            for i in range(len(shops)+1):
                if(i<len(shops)):
                    type.type(str(i+1) + ". " + shops[i])
                    time.sleep(0.5)
                    print()
                else:
                    type.type(str(i+1) + ". Stay Home")
                    time.sleep(0.5)
                    print()
            type.type("Choose a number: ")
            while True:
                while choice is None:
                    try:
                        choice = int(input())
                    except ValueError:
                        type.type("Choose a number: ")
                if(1<=choice<=len(shops)):
                    shop = shops[choice-1]
                    break
                elif choice==len(shops)+1:
                    shop = "Home"
                    break
                else:
                    choice = None
                    type.type("That number's not a choice!")
                    print()
                    type.type("Choose a number: ")
            print()

            if shop == "Doctor's Office": self.visit_doctor()
            elif shop == "Witch Doctor's Tower": self.visit_witch_doctor()
            elif shop == "Trusty Tom's Trucks and Tires": self.visit_tom()
            elif shop == "Filthy Frank's Flawless Fixtures": self.visit_frank()
            elif shop == "Oswald's Optimal Outoparts": self.visit_oswald()
            elif shop == "Convenience Store": self.visit_convenience_store()
            elif shop == "Marvin's Mystical Merchandise": self.visit_marvin()
            else: self.night_event()
            
        else:
            self.night_event()

    #Doctor's Office Interaction    
    def visit_doctor(self):
        type.type("You get in your car and drive to the Doctor's Office. ")
        if not self.has_met("Doctor's Office"):
            self.meet("Doctor's Office")
            type.type("As you pull up closer to the bright blue building, you notice that the parking lot is concerningly empty. You park your wagon right up front next to the entrance, and step out towards the doors. ")
            type.type("When you enter into the lobby, you're immediately hit with the strong smell of hand sanitizer in the air. The carpets are dull and brown, the light above you is flickering, and the walls are filled with posters telling you to 'Floss More Often!' and 'Wash Your Hands Before You Eat!' ")
            type.type("If you didn't know any better, you would have guessed you were on a movie set.")
            print("\n")
            type.type("Walking towards the front desk, you see a cheery old lady, who looks up from her computer to smile at you. Her gray hair covers her glasses, and her hand trembles as she hands you a pen and a clipboard with some paperwork. Of course it's paperwork.")
            print("\n")
            type.type("After filling out your information, you walk back to the front desk, and hand the lady the clipboard. She smiles, and begins to speak to you.")
        print("\n")
        type.type("I see you're here for a checkup. The Doctor will see you now.")
        print("\n")
        type.type("Hey there champ! How are you? Doing all right? Let's check you out and make sure you're all up to snuff.")
        print()
        if (self.len_status() == 0) and (self.__health == 100):
            type.type("Why, you look just as healthy as the day I met you, fresh from your mother's womb! Let me just give you this lollipop and you'll be free to go.")
        elif (self.len_status() == 0):
            type.type("Why, you don't seem to really need my help. You appear a little worse for wear, but this medicine should do the trick.")
            print("\n")
        else:
            self.__clear_status = True
            if self.has_status("Spider Bite"):
                type.type("I see you have a nasty spider bite. That thing looks gross. Let me get that cleaned up for you.")
                print()
            print()
            type.type("Well, that seems to be everything. You still appear a little worse for wear, but this medicine should do the trick.")
        print("\n")
        self.heal(100)
        type.type("You walk back to the front desk to checkout.")
        print("\n")
        cost = int((random.randint(65, 90)/100)*self.__balance)
        type.type("That will be " + bright(green("${:,}".format(cost))))
        if self.has_item("Faulty Insurance"):
            print("\n")
            type.type("You show off your " + bright(magenta("Faulty Insurance")) + " to the lady, and put a convincing smile on your face. ")
            random_chance = random.randrange(10)
            if random_chance < 2:
                self.add_danger("Doctor Ban")
                print("\n")
                self.use_item("Faulty Insurance")
                type.type("Is this supposed to fool me? A fake insurance card? That's it, I'm calling the cops!")
                print("\n")
                type.type("Without hesitation, you turn, and run far, far away from the hospital, knowing that your face can't be seen there again.")
                print("\n")
                self.start_night()
                return
            else:
                print("\n")
                type.type("I see, you have insurance. Well, that should give you quite the discount.")
                print()
                cost = int((random.randint(10, 35)/100)*self.__balance)
                type.type("That will be " + bright(green("${:,}".format(cost))))
                self.change_balance(-cost)
                self.update_faulty_insurance_durability()
                self.start_night()
                return
        else:
            self.change_balance(-cost)
            self.start_night()
            return


    # Witch Doctor's shop and interactions
    def visit_witch_doctor(self):
        potions = self.__lists.make_witch_inventory()
        type.type("You get in your car and drive to the Witch Doctor's Tower. ")
        print("\n")
        type.type("Muahahahahaha, hahahahahaha, HAHAHAHAHA!")
        print()
        type.type("Would you like me to HEAL you, HUMAN? ")
        while(True):
            yes_or_no = input("").lower()
            print()
            if((yes_or_no == "y") or (yes_or_no == "yes")):
                type.type("Now THATS what I LIKE to hear!")
                print("\n")
                type.type("You watch as the Witch goes from shelf to shelf, grabbing frog legs and horse hairs and bee carcasses, throwing them all into the black boiling pot. It begins to glow green, and the Witch looks pleased. ")
                print("\n")
                type.type("HAHAHAHAHA! DRINK this, my DEAR!")
                print("\n")
                type.type("You drink the strange concoction, and it burns in your stomach. Hopefully, it makes you feel better.")
                
                print("\n")

                random_chance = random.randrange(10)
                if random_chance < 5:
                    self.__clear_status = True
                elif random_chance == 5:
                    self.__clear_all_status = True

                random_chance = random.randrange(3)
                if random_chance == 0:
                    self.heal(100)
                
                cost = int((random.randint(5, 25)/100)*self.__balance)
                type.type("YOU owe ME some of your green BILLS! I THINK that " + bright(green("${:,}".format(cost))) + " would SUFFICE!")
                self.change_balance(-cost)
                if len(potions)==0:
                    type.type("SORRY FOR YOU, but I'm simply out of FLASKS. No FLASKS means no POTIONS. Maybe try COMING BACK another DAY!")
                    print("\n")
                    self.start_night()
                    return
                else:
                    type.type("NOW, while I have YOU here, care to PURCHASE any of my POWERFUL POTIONS?")
                break
            elif((yes_or_no == "n") or (yes_or_no == "no")):
                type.type("HAHAH-oh what? You don't want MY help? That's QUITE UNFORTUNATE!")
                print("\n")
                if len(potions)==0:
                    type.type("SORRY FOR YOU, but I'm simply out of FLASKS. No FLASKS means no POTIONS. Maybe try COMING BACK another DAY!")
                    print("\n")
                    self.start_night()
                    return
                else:
                    type.type("WELL, are YOU in the MOOD to spend some MONEY on my MAGIC POTIONS?")
                    break
            else:
                type.type("WHAT did you SAY? ")

        print()

        no_bust_price = 0
        imminent_blackjack_price = 0
        dealers_whispers_price = 0
        bonus_fortune_price = 0
        antivenom_price = 0
        antivirus_price = 0
        fortunate_day_price = 0
        fortunate_night_price = 0
        while(True):
            for i in range(len(potions)+1):
                if(i<len(potions)):
                    type.type(str(i+1) + ". Flask of " + potions[i])
                    time.sleep(0.5)
                    print()
                else:
                    type.type(str(i+1) + ". I'm not buying anything")
                    time.sleep(0.5)
                    print()

            if(self.len_flasks()==1):
                type.type("NOW, I'm not ONE to JUDGE, but MIXING potions can be RISKY BUSINESS. Don't BLAME ME if you feel SICK.")
                print()
            elif(self.len_flasks()==2):
                type.type("SO, you're TEETERING on DANGEROUS levels of potion in your BLOOD. Proceed with CAUTON.")
                print()
            elif(self.len_flasks()>=3):
                type.type("ANY additional POTIONS in YOUR SYSTEM is ENTIRELY YOUR DECISION, and A BAD ONE AT THAT BUT I'M NOT YOU. Just please don't DIE on my CARPETS.")
                print()
            type.type("CHOOSE a number: ")
            while True:
                choice = None
                while choice is None:
                    try:
                        choice = int(input())
                    except ValueError:
                        type.type("Choose A number: ")
                if(1<=choice<=len(potions)):
                    potion = potions[choice-1]
                    break
                elif choice==len(potions)+1:
                    potion = "Home"
                    break
                else:
                    choice = None
                    type.type("I DONT have that NUMBER!")
                    print()
                    type.type("Choose a NUMBER: ")

            print()

            if potion == "No Bust":
                type.type("AHHH, so YOU WANT the Flask of No Bust?")
                if no_bust_price == 0:
                    no_bust_price = random.choice([25000, 27000, 30000])
                price = no_bust_price
            elif potion == "Imminent Blackjack":
                type.type("I SEE, so YOU WANT the Flask of Imminent Blackjack?")
                if imminent_blackjack_price == 0:
                    imminent_blackjack_price = random.choice([40000, 45000, 50000])
            elif potion == "Dealer's Whispers":
                type.type("HAHAHA, so YOU WANT the Flask of Dealer's Whispers?")
                if dealers_whispers_price == 0:
                    dealers_whispers_price = random.choice([23000, 27000, 32000])
                price = dealers_whispers_price
            elif potion == "Bonus Fortune":
                type.type("OOOOOOOOHHH, so YOU WANT the Flask of Bonus Fortune?")
                if bonus_fortune_price == 0:
                    bonus_fortune_price = random.choice([35000, 42000, 45000])
                price = bonus_fortune_price
            elif potion == "Anti-Venom":
                type.type("OF COURSEEEE, YOU WANT the Flask of Anti-Venom?")
                if antivenom_price == 0:
                    antivenom_price = random.choice([25000, 26000, 27000])
                price = antivenom_price
            elif potion == "Anti-Virus":
                type.type("AH-HA, YOU WANT the Flask of Anti-Virus?")
                if antivirus_price == 0:
                    antivirus_price = random.choice([26000, 27000, 28000])
                price = antivirus_price
            elif potion == "Fortunate Day":
                type.type("HEHEHAHAIHEHIA, so YOU WANT the Flask of Fortunate Day?")
                if fortunate_day_price == 0:
                    fortunate_day_price = random.choice([12000, 13000, 18000])
                price = fortunate_day_price
            elif potion == "Fortunate Night":
                type.type("MUAHAHAHAHA, so YOU WANT the Flask of Fortunate Night?")
                if fortunate_night_price == 0:
                    fortunate_night_price = random.choice([12000, 15000, 20000])
                price = fortunate_night_price
            else: 
                type.type("Then OUR BUSINESS has been SETTLED. Be GONE. GOODBYE! COME AGAIN!")
                print("\n")
                self.start_night()
                return

            print()

            type.type("I SUPPOSE I can PART WAYS with THIS for " + green(bright("${:,}".format(price))) + ". What do YOU think? ")
            
            while True:
                yes_or_no = input("").lower()
                if ((yes_or_no == "y") or (yes_or_no == "yes")) and (self.__balance<price):
                    print()
                    type.type("YOUR WALLETS are far too SMALL for this TRANSACTION.")
                    print("\n")
                    type.type("PERHAPS one of the OTHER potions?")
                    break
                elif (yes_or_no == "y") or (yes_or_no == "yes"):
                    print()
                    type.type("HAHAHAHAHAHAHAHAHA! YES! YES!")
                    self.change_balance(-price)
                    self.add_flask(potion)
                    potions.pop(choice-1)
                    type.type("You got the " + magenta(bright("Flask of " + potion)) + "!")
                    print()
                    type.type("Description: " + self.get_item_desc(potion))
                    print("\n")
                    if(self.len_flasks()==1):
                        type.type("You chug the potion, and begin to feel warm inside.")
                        print("\n")
                    elif(self.len_flasks()==2):
                        type.type("You chug the potion, and feel a bit dizzy. Maybe no more potions.")
                        print("\n")
                    elif(self.len_flasks()>=3):
                        type.type("You chug the potion, and feel really, really awful.")
                        random_chance = random.randrange(2)
                        if random_chance == 0:
                            self.__flask_effects = set()
                            print("\n")
                            type.type("You stumble back and forth, on the verge of fainting. You puke all over the floor.")
                            print("\n")
                            type.type("NOOOO, NOT ON THE CARPETS! WHAT did I SAY! NO MORE. NO MORE. YOU are DONE for TODAY. OUT, NOW.")
                            print("\n")
                            type.type("As you walk out, you feel your body begin to weaken. After all that, it seems the potions you had injested are now laying in a puddle on the floor of the Witch Doctor's tower. ")
                            print("\n")
                            self.start_night()
                            return
                        
                        damage = random.choice([10, 12, 15, 20, 30, 40])
                        if damage >= self.__health:
                            print("\n")
                            type.slow(red("Your vision starts turning red, then green, then purple. "))
                            type.slow(red("Panicking, you run around the room, desperate to find an antidote. "))
                            type.slow(red("You begin drinking potion, after potion, to no avail. "))
                            type.slow(red("You can hear the Witch cackling in the background of your ringing ears, and slowly, you fall to the ground. "))
                            type.slow(red("Your face rests on the soft carpet. It's so cozy. Too cosy. "))
                            type.slow(red("Is that God? Yes, I think I can hear him! God! God! "))
                            type.slow(red("My goodness, he's real! God begins to decend from the roof hundreds of feet above you, and as he slowly glides down the tower, "))
                            type.slow(red("you get a closer look at his figure. A golden ring surrounds his body, and his white cloak is long and elegant. "))
                            print("\n")
                            type.slow(red(bright("As God decends, he looks you in the eyes, and you watch his face melt in front of you, his skin dripping onto your skin. ")))
                            type.slow(red(bright("It burns, and all you can do is sit with the pain and agony as your body slowly shuts down.")))
                            self.kill()
                        else:
                            print("\n")
                            self.hurt(damage)

                    if len(potions)==0:
                        type.type("YOU bought EVERYTHING! How EXCITING! I suppose we're DONE exchanging GOODS! GOODBYE NOW!")
                        print("\n")
                        self.start_night()
                        return
                    else:
                        type.type("OOOOH YES! Capitalism is FUN! I WANT MORE! MORE!")
                        print()
                    break
                elif (yes_or_no == "n") or (yes_or_no == "no"):
                    print()
                    type.type("OK OK I see how IT IS! ")
                    print("\n")
                    type.type("PERHAPS a DIFFERENT potion?")
                    print()
                    break
                else:
                    print()
                    type.type("GIVE me an ANSWER! ")


    # Tom's shop and interactions
    def tom_dialogue(self):
        if self.__mechanic_visits == 0:
            type.type("Heyo! That's it. Heyo.")

    def visit_tom(self):
        days_elapsed = self.get_days_elapsed("Mechanic")
        self.mark_day("Mechanic")
        type.type("You get in your car and drive to Tom's Trusty Trucks and Tires. ")
        print("\n")
        self.tom_dialogue()
        print("\n")
        repairing_items_len = len(self.__repairing_inventory)
        if(repairing_items_len>0):
            if days_elapsed == 3:
                type.type("You've been gone a while. Honestly, I forgot about ya stuff. Just come back soon, and I'll get to it.")
                print("\n")
            else:
                type.type("You left me some items to fix up since I last saw you. Here's the rundown:")
                print("\n")
                repairing_items = self.__lists.make_repairing_items_list()
                for item in repairing_items:
                    if item == "Delight Indicator":
                        random_chance = random.randrange(2)
                        if random_chance == 0:
                            type.type("I managed to get this Delight Indicator up and running for ya. Just took a few new wires.")
                            self.fix_item(item)
                            print("\n")
                            type.type("Your " + magenta(bright(item)) + " has been fixed!")
                            print("\n")
                    elif item == "Health Indicator":
                        random_chance = random.randrange(2)
                        if random_chance == 0:
                            type.type("I somehow managed to get this Health Indicator workin'. Just took a few new screws.")
                            self.fix_item(item)
                            print("\n")
                            type.type("Your " + magenta(bright(item)) + " has been fixed!")
                            print("\n")
                    elif item == "Dirty Old Hat":
                        random_chance = random.randrange(2)
                        if random_chance == 0:
                            type.type("This Dirty Old Hat has never looked cleaner! If that's what you want, at least.")
                            self.fix_item(item)
                            print("\n")
                            type.type("Your " + magenta(bright(item)) + " has been fixed!")
                            print("\n")
                    elif item == "Golden Watch":
                        random_chance = random.randrange(2)
                        if random_chance == 0:
                            type.type("I put new gears in your Golden Watch. Should tell the time now.")
                            self.fix_item(item)
                            print("\n")
                            type.type("Your " + magenta(bright(item)) + " has been fixed!")
                            print("\n")
                    elif item == "Faulty Insurance":
                        random_chance = random.randrange(2)
                        if random_chance == 0:
                            type.type("Against my better judgement, I touched up your Faulty Insurance card. If it'll work, well, my guess is as good as yours.")
                            self.fix_item(item)
                            print("\n")
                            type.type("Your " + magenta(bright(item)) + " has been fixed!")
                            print("\n")
                    elif item == "Sneaky Peeky Shades":
                        random_chance = random.randrange(2)
                        if random_chance == 0:
                            type.type("I replaced the frame in your Sneaky Peeky Shades, so now you can see out of them.")
                            self.fix_item(item)
                            print("\n")
                            type.type("Your " + magenta(bright(item)) + " have been fixed!")
                            print("\n")
                    elif item == "Quiet Sneakers":
                        random_chance = random.randrange(2)
                        if random_chance == 0:
                            type.type("I relaced these Quiet Sneakers, so you can run again.")
                            self.fix_item(item)
                            print("\n")
                            type.type("Your " + magenta(bright(item)) + " have been fixed!")
                            print("\n")

                if len(self.__repairing_inventory) == repairing_items_len:
                    type.type("Yesterday was a long one, and I retired to home early to see my wife and the girlies. Didn't get much progress on your things, but I assure you, they'll be fixed before you know it.")
                elif len(self.__repairing_inventory) > 1:
                    type.type("I've still got " + str(len(self.__repairing_inventory)) + " items of yours that I'm still looking at. Just swing by tomorrow, and hopefully I'll have them done.")
                elif len(self.__repairing_inventory) == 1:
                    type.type("I've still got " + str(len(self.__repairing_inventory)) + " item of yours that I'm still looking at. Just swing by tomorrow, and hopefully I'll have it done.")
                elif len(self.__repairing_inventory) == 0:
                    type.type("That should be everything you left with me. Hopefully everything's up to snuff and good as new, ya know!")
                print("\n")

        if(len(self.__broken_inventory)>0):
            broken_items = self.__lists.make_broken_items_list()
            delight_indicator_price = 0
            health_indicator_price = 0
            dirty_old_hat_price = 0
            golden_watch_price = 0
            faulty_insurance_price = 0
            sneaky_peeky_glasses_price = 0
            quiet_sneakers_price = 0
            type.type("I see you came in here with some broken valuables. Mind if I take a look at em?")
            print()
            while(True):
                for i in range(len(broken_items)+1):
                    if(i<len(broken_items)):
                        type.type(str(i+1) + ". " + broken_items[i])
                        time.sleep(0.5)
                        print()
                    else:
                        type.type(str(i+1) + ". I'm all set")
                        time.sleep(0.5)
                        print()
                type.type("Choose a number: ")
                while True:
                    choice = None
                    while choice is None:
                        try:
                            choice = int(input())
                        except ValueError:
                            type.type("Choose a number: ")
                    if(1<=choice<=len(broken_items)):
                        item = broken_items[choice-1]
                        break
                    elif choice==len(broken_items)+1:
                        item = "Home"
                        break
                    else:
                        choice = None
                        type.type("You don't have an item with that number!")
                        print()
                        type.type("Choose a number: ")

                print()

                if item == "Delight Indicator":
                    type.type("You want me to fix that Delight Indicator of yours?")
                    if delight_indicator_price == 0:
                        delight_indicator_price = random.choice([4500, 5500, 6000])
                    price = delight_indicator_price
                elif item == "Health Indicator":
                    type.type("You want me to fix that Health Indicator for ya?")
                    if health_indicator_price == 0:
                        health_indicator_price = random.choice([4000, 4500, 5500])
                    price = health_indicator_price
                elif item == "Dirty Old Hat":
                    type.type("You want me to fix that Dirty Old Hat you got there?")
                    if dirty_old_hat_price == 0:
                        dirty_old_hat_price = random.choice([12500, 14000, 15000])
                    price = dirty_old_hat_price
                elif item == "Golden Watch":
                    type.type("You want me to fix that Golden Watch you're wearin'?")
                    if golden_watch_price == 0:
                        golden_watch_price = random.choice([15000, 16000, 17500])
                    price = golden_watch_price
                elif item == "Faulty Insurance":
                    type.type("Uhm, you want me to fix your Faulty Insurance card?")
                    if faulty_insurance_price == 0:
                        faulty_insurance_price = random.choice([5000, 5500, 6000])
                    price = faulty_insurance_price
                elif item == "Sneaky Peeky Shades":
                    type.type("You want me to fix those Sneaky Peeky Shades on your head?")
                    if sneaky_peeky_glasses_price == 0:
                        sneaky_peeky_glasses_price = random.choice([17000, 18000, 20000])
                    price = sneaky_peeky_glasses_price
                elif item == "Quiet Sneakers":
                    type.type("You want me to fix them there Quiet Sneakers you're rockin'?")
                    if quiet_sneakers_price == 0:
                       quiet_sneakers_price = random.choice([7500, 9000, 10000])
                    price = quiet_sneakers_price
                else: 
                    type.type("Well then, I hope you have a great rest of your night. Stay safe now.")
                    print("\n")
                    self.start_night()
                    return

                print()

                type.type("It'll take me a couple days, but I can do that for ya for " + green(bright("${:,}".format(price))) + ". Whaddya say? ")
                
                while True:
                    yes_or_no = input("").lower()
                    if ((yes_or_no == "y") or (yes_or_no == "yes")) and (self.__balance<price):
                        print()
                        type.type("Aww man, sorry to tell you, but you just don't got enough funds for this, yunno?")
                        print("\n")
                        random_chance = random.randrange(2)
                        if random_chance == 0:
                            type.type("Ugh, man, I just hate seein' people in need of help and not gettin' it, ya hear? ")
                            type.type("Tell ya what, limited time offer, I'm giving out a special discount, just for you. ")
                            discount = random.choice([20, 25, 30, 35])
                            price = int(price - (price*(discount/100)))
                            type.type("Say yes right now, and I'll take " + str(discount) + "%" + " off your order.")
                            print("\n")
                            type.type("That means you're only payin' " + green(bright("${:,}".format(price))) + ". Could ya do that? ")

                            while True:
                                yes_or_no_2 = input("").lower()
                                if ((yes_or_no_2 == "y") or (yes_or_no_2 == "yes")) and (self.__balance<price):
                                    print()
                                    type.type("Still can't afford it? That's tough luck, man. I really wish there was more I could do, ya know?")
                                    print("\n")
                                    type.type("Maybe you can fix up something else.")
                                    print()
                                    break
                                elif (yes_or_no == "y") or (yes_or_no == "yes"):
                                    print()
                                    type.type("Really? Awesome. Just leave this here with me, and let me wrench that baby back to life for ya.")
                                    self.change_balance(-price)
                                    self.repair_item(item)
                                    broken_items.pop(choice-1)
                                    type.type("Your " + magenta(bright(item)) + " is safe with Tom. Come back later to see if it's fixed!")
                                    print("\n")
                                    if len(broken_items)==0:
                                        type.type("Well, that appears to be everything, doesn't it? Thanks for letting me help ya out. Have a nice day, now.")
                                        print("\n")
                                        self.start_night()
                                        return
                                    else:
                                        type.type("Got anything else for me?")
                                        print()
                                        break
                                elif (yes_or_no_2 == "n") or (yes_or_no_2 == "no"):
                                    type.type("Really? Even with the discount? You do you, I suppose.")
                                    print("\n")
                                    type.type("Is there anything else I can fix for ya?")
                                    print()
                                    break
                                else:
                                    print()
                                    type.type("Couldn't hear ya. Whaddya say? ")
                            break
                        else:
                            broken_items.pop(choice-1)
                            type.type("Maybe you can afford to fix up somethin' else?")
                            print()
                        break
                    elif (yes_or_no == "y") or (yes_or_no == "yes"):
                        print()
                        type.type("Really? Awesome. Just leave this here with me, and let me wrench that baby back to life for ya.")
                        self.change_balance(-price)
                        self.repair_item(item)
                        broken_items.pop(choice-1)
                        type.type("Your " + magenta(bright(item)) + " is safe with Tom. Come back later to see if it's fixed!")
                        print("\n")
                        if len(broken_items)==0:
                            type.type("Well, that appears to be everything, doesn't it? Thanks for letting me help ya out. Have a nice day, now.")
                            print("\n")
                            self.start_night()
                            return
                        else:
                            type.type("Got anything else for me?")
                            print()
                        break
                    elif (yes_or_no == "n") or (yes_or_no == "no"):
                        print()
                        type.type("No dice? ")
                        random_chance = random.randrange(10)
                        if random_chance == 0:
                            type.type("You don't say. I mean, my prices are unbeatable. You know what, I'll prove it!")
                            print("\n")
                            type.type("Tell ya what, limited time offer, I'm giving out a special discount, just for you. ")
                            discount = random.choice([15, 20, 25])
                            price = int(price - (price*(discount/100)))
                            type.type("Say yes right now, and I'll take " + str(discount) + "%" + " off your order.")
                            print("\n")
                            type.type("That means you're only payin' " + green(bright("${:,}".format(price))) + ". You interested? ")
                            while True:
                                yes_or_no_2 = input("").lower()
                                if ((yes_or_no_2 == "y") or (yes_or_no_2 == "yes")) and (self.__balance<price):
                                    print()
                                    type.type("You can't afford it? Really? That's tough luck, man. I really wish there was more I could do, ya know?")
                                    print("\n")
                                    type.type("Maybe you can fix up something else.")
                                    print()
                                    break
                                elif (yes_or_no_2 == "y") or (yes_or_no_2 == "yes"):
                                    print()
                                    type.type("Really? Awesome. Just leave this here with me, and let me wrench that baby back to life for ya.")
                                    self.change_balance(-price)
                                    self.repair_item(item)
                                    broken_items.pop(choice-1)
                                    type.type("Your " + magenta(bright(item)) + " is safe with Tom. Come back later to see if it's fixed!")
                                    print("\n")
                                    if len(broken_items)==0:
                                        type.type("Well, that appears to be everything, doesn't it? Thanks for letting me help ya out. Have a nice day, now.")
                                        print("\n")
                                        self.start_night()
                                        return
                                    else:
                                        type.type("Got anything else for me?")
                                        print()
                                        break
                                elif (yes_or_no_2 == "n") or (yes_or_no_2 == "no"):
                                    type.type("Really? No interest, whatsoever? Even with the discount? You do you, I suppose.")
                                    print("\n")
                                    type.type("Want me to fix anything else?")
                                    print()
                                    break
                                else:
                                    print()
                                    type.type("Couldn't hear ya. Whaddya say? ")
                            break
                        else:
                            type.type("That's alright, now.")
                            print("\n")
                            type.type("What about your other wares?")
                            print()
                            break
                    else:
                        print()
                        type.type("Couldn't hear ya. Whaddya say? ")

        self.start_night()
        return



    # Frank's shop and interactions
    def frank_dialogue(self):
        if self.__mechanic_visits == 0:
            type.type("Franko! That's it. Franko. Because I'm Frank.")

    def visit_frank(self):
        days_elapsed = self.get_days_elapsed("Mechanic")
        self.mark_day("Mechanic")
        type.type("You get in your car and drive to Filthy Frank's Flawless Fixtures. ")
        print("\n")
        self.frank_dialogue()
        print("\n")
        repairing_items_len = len(self.__repairing_inventory)
        if(repairing_items_len>0):
            if days_elapsed == 2:
                type.type("You didn't show up yesterday. That means I haven't looked at your stuff. Come back soon, and maybe I will have made some progress, yeah?")
                print("\n")
            else:
                type.type("You left me some of your trinkets. This is what I've got for you:")
                print("\n")
                repairing_items = self.__lists.make_repairing_items_list()
                for item in repairing_items:
                    if item == "Delight Indicator":
                        random_chance = random.randrange(5)
                        if random_chance < 3:
                            type.type("With a couple new wires I got your Delight Indicator working.")
                            self.fix_item(item)
                            print("\n")
                            type.type("Your " + magenta(bright(item)) + " has been fixed!")
                            print("\n")
                        elif random_chance == 3:
                            type.type("Honestly, after one look at this Delight Indicator thingy, I gave up entirely. Take it back. No refunds.")
                            self.return_item(item)
                            print("\n")
                            type.type(red("Your broken " + (item) + " has been returned."))
                            print("\n")
                    elif item == "Health Indicator":
                        random_chance = random.randrange(5)
                        if random_chance < 3:
                            type.type("Tighted some screws and the Health Indicator started up again. Seems good? Just take it.")
                            self.fix_item(item)
                            print("\n")
                            type.type("Your " + magenta(bright(item)) + " has been fixed!")
                            print("\n")
                        elif random_chance == 3:
                            type.type("Get that the fuck out my face with that fancy wizard crap. This Health Indicator thing is too complicated. No refunds.")
                            self.return_item(item)
                            print("\n")
                            type.type(red("Your broken " + (item) + " has been returned."))
                            print("\n")
                    elif item == "Dirty Old Hat":
                        random_chance = random.randrange(5)
                        if random_chance < 3:
                            type.type("I gave this Dirty Old Hat to my wife, and after enough convincing, she sewed it back up.")
                            self.fix_item(item)
                            print("\n")
                            type.type("Your " + magenta(bright(item)) + " has been fixed!")
                            print("\n")
                        elif random_chance == 3:
                            type.type("You gave me a Dirty Old Hat and asked me to fix it. What did you expect? No refunds.")
                            self.return_item(item)
                            print("\n")
                            type.type(red("Your broken " + (item) + " has been returned."))
                            print("\n")
                    elif item == "Golden Watch":
                        random_chance = random.randrange(5)
                        if random_chance < 3:
                            type.type("All I had to do was tap the watch face with my finger and it started ticking again, so I'd say that's a job well done.")
                            self.fix_item(item)
                            print("\n")
                            type.type("Your " + magenta(bright(item)) + " has been fixed!")
                            print("\n")
                        elif random_chance == 3:
                            type.type("I looked at the watch, spun all the gears and clicked all the buttons, but nothing worked. Sorry dude. No refunds.")
                            self.return_item(item)
                            print("\n")
                            type.type(red("Your broken " + (item) + " has been returned."))
                            print("\n")
                    elif item == "Faulty Insurance":
                        random_chance = random.randrange(5)
                        if random_chance < 3:
                            type.type("My guy was around last night, and he looked at your Faulty Insurance card. Should work again.")
                            self.fix_item(item)
                            print("\n")
                            type.type("Your " + magenta(bright(item)) + " has been fixed!")
                            print("\n")
                        elif random_chance == 3:
                            type.type("I've been calling my guy, but he won't answer. I can't fix your Faulty Insurance card. Take it back. No refunds.")
                            self.return_item(item)
                            print("\n")
                            type.type(red("Your broken " + (item) + " has been returned."))
                            print("\n")
                    elif item == "Sneaky Peeky Shades":
                        random_chance = random.randrange(5)
                        if random_chance < 3:
                            type.type("A little mouth water vapor and my shirt was more than enough to polish up the Sneaky Peeky Shades you gave me.")
                            self.fix_item(item)
                            print("\n")
                            type.type("Your " + magenta(bright(item)) + " have been fixed!")
                            print("\n")
                        elif random_chance == 3:
                            type.type("I ain't no opotometigist. These Sneaky Peeky Shades, well, they are glasses. I fix cars. No refunds.")
                            self.return_item(item)
                            print("\n")
                            type.type(("Your broken " + red(bright(item)) + " have been returned."))
                            print("\n")
                    elif item == "Quiet Sneakers":
                        random_chance = random.randrange(5)
                        if random_chance < 3:
                            type.type("I gave your Quiet Sneakers to my son Kyle, and ran around the yard all day yesterday. Should've broken them in for ya.")
                            self.fix_item(item)
                            print("\n")
                            type.type("Your " + magenta(bright(item)) + " have been fixed!")
                            print("\n")
                        elif random_chance == 3:
                            type.type("These Quiet Sneakers reek like hell. Please take them. No refunds.")
                            self.return_item(item)
                            print("\n")
                            type.type(red("Your broken " + (item) + " have been returned."))
                            print("\n")

                if len(self.__repairing_inventory) == repairing_items_len:
                    type.type("I didn't fix a damn thing of yours, and I ain't afraid to show it. Look at this box. It has all the stuff you gave me. It hasn't moved since you gave me it. Now scram, hard work takes time.")
                elif len(self.__repairing_inventory) > 1:
                    type.type("That leaves " + str(len(self.__repairing_inventory)) + " items of yours still in my posession. Just swing by tomorrow, and I'll do my best to finish them up.")
                elif len(self.__repairing_inventory) == 1:
                    type.type("That leaves " + str(len(self.__repairing_inventory)) + " item of yours still in my posession. Just swing by tomorrow, and I'll do my best to finish it up.")
                elif len(self.__repairing_inventory) == 0:
                    type.type("That's all your junk, fixed better than the best. Enjoy it while it lasts.")
                print("\n")

        if(len(self.__broken_inventory)>0):
            broken_items = self.__lists.make_broken_items_list()
            delight_indicator_price = 0
            health_indicator_price = 0
            dirty_old_hat_price = 0
            golden_watch_price = 0
            faulty_insurance_price = 0
            sneaky_peeky_glasses_price = 0
            quiet_sneakers_price = 0
            type.type("You have some broken things for me. Come on, don't be shy. Let me take a whack at them.")
            print()
            while(True):
                for i in range(len(broken_items)+1):
                    if(i<len(broken_items)):
                        type.type(str(i+1) + ". " + broken_items[i])
                        time.sleep(0.5)
                        print()
                    else:
                        type.type(str(i+1) + ". I'm all set")
                        time.sleep(0.5)
                        print()
                type.type("Choose a number: ")
                while True:
                    choice = None
                    while choice is None:
                        try:
                            choice = int(input())
                        except ValueError:
                            type.type("Choose a number: ")
                    if(1<=choice<=len(broken_items)):
                        item = broken_items[choice-1]
                        break
                    elif choice==len(broken_items)+1:
                        item = "Home"
                        break
                    else:
                        choice = None
                        type.type("Did I stutter?")
                        print()
                        type.type("Choose a number: ")

                print()

                if item == "Delight Indicator":
                    type.type("You need me to repair your Delight Indicator?")
                    if delight_indicator_price == 0:
                        delight_indicator_price = random.choice([4000, 4250, 4500, 5500, 6000, 9000])
                    price = delight_indicator_price
                elif item == "Health Indicator":
                    type.type("You need me to repair that Health Indicator?")
                    if health_indicator_price == 0:
                        health_indicator_price = random.choice([3000, 3200, 4000, 4500, 5500, 7000])
                    price = health_indicator_price
                elif item == "Dirty Old Hat":
                    type.type("You need me to repair the Dirty Old Hat you have?")
                    if dirty_old_hat_price == 0:
                        dirty_old_hat_price = random.choice([10000, 10500, 12500, 14000, 15000, 17000])
                    price = dirty_old_hat_price
                elif item == "Golden Watch":
                    type.type("You need me to repair that Golden Watch on your wrist?")
                    if golden_watch_price == 0:
                        golden_watch_price = random.choice([13000, 14000, 15000, 16000, 17500, 19500])
                    price = golden_watch_price
                elif item == "Faulty Insurance":
                    type.type("You need me to touch up your Faulty Insurance card?")
                    if faulty_insurance_price == 0:
                        faulty_insurance_price = random.choice([3500, 4000, 5000, 5500, 6000, 7000])
                    price = faulty_insurance_price
                elif item == "Sneaky Peeky Shades":
                    type.type("You need me to repair those Sneaky Peeky Shades over your eyes?")
                    if sneaky_peeky_glasses_price == 0:
                        sneaky_peeky_glasses_price = random.choice([15500, 16500, 17000, 18000, 20000, 25000])
                    price = sneaky_peeky_glasses_price
                elif item == "Quiet Sneakers":
                    type.type("You need me to repair those Quiet Sneakers you're wearing?")
                    if quiet_sneakers_price == 0:
                       quiet_sneakers_price = random.choice([6000, 6500, 7500, 9000, 10000, 12000])
                    price = quiet_sneakers_price
                else: 
                    type.type("Well then I've done all I can do. Stay out of trouble, now.")
                    print("\n")
                    self.start_night()
                    return
                
                print()

                type.type("I can fix this up for like " + green(bright("${:,}".format(price))) + ". You game? ")
                
                while True:
                    yes_or_no = input("").lower()
                    if ((yes_or_no == "y") or (yes_or_no == "yes")) and (self.__balance<price):
                        print()
                        type.type("Are you tryna rip me off? Nah man, I'm just kidding. But seriously, don't mess with me like that.")
                        print("\n")
                        broken_items.pop(choice-1)
                        type.type("Am I repairing something for you or what?")
                        break
                    elif (yes_or_no == "y") or (yes_or_no == "yes"):
                        print()
                        type.type("Darn tootin! Lemme just take this from you, and sooner or later I'll wield my hammer and do my thing.")
                        self.change_balance(-price)
                        self.repair_item(item)
                        broken_items.pop(choice-1)
                        type.type("Your " + magenta(bright(item)) + " is in Frank's possession. Come back tomorrow to see if it's fixed!")
                        print("\n")
                        if len(broken_items)==0:
                            type.type("Well I'd say that's all you've got that I could fix. Just check in tomorrow and hopefully it'll be to your liking.")
                            print("\n")
                            self.start_night()
                            return
                        else:
                            type.type("Got anything else I can repair?")
                            print()
                        break
                    elif (yes_or_no == "n") or (yes_or_no == "no"):
                        print()
                        type.type("What?! Why'd you ask, then. God, that's just annoying. You bug me sometimes, man.")
                        print("\n")
                        type.type("Anything you actually want me to repair?")
                        print()
                        break
                    else:
                        print()
                        type.type("Speak up! You're mumbling. ")
        self.start_night()
        return



    # Oswald's shop and interactions NOT IMPLEMENTED
    def oswald_dialogue(self):
        if self.__mechanic_visits == 0:
            type.type("Heyoswald! That's it. Heyoswald.")

    def visit_oswald(self):
        type.type("You get in your car and drive to Oswald's Optimal Outoparts. ")
        print("\n")
        self.oswald_dialogue()
        print("\n")

        if(len(self.__broken_inventory)>0):
            broken_items = self.__lists.make_broken_items_list()
            tips = 0
            free_money = 0
            delight_indicator_price = 0
            health_indicator_price = 0
            dirty_old_hat_price = 0
            golden_watch_price = 0
            faulty_insurance_price = 0
            sneaky_peeky_glasses_price = 0
            quiet_sneakers_price = 0
            type.type("It appears that you possess some valuables in need of attention. Oh Stuart!")
            print("\n")
            type.type("Is there anything you would like Stuart to fix?")
            print()
            while(True):
                for i in range(len(broken_items)+1):
                    if(i<len(broken_items)):
                        type.type(str(i+1) + ". " + broken_items[i])
                        time.sleep(0.5)
                        print()
                    else:
                        type.type(str(i+1) + ". I'm all set")
                        time.sleep(0.5)
                        print()
                type.type("Choose a number: ")
                while True:
                    choice = None
                    while choice is None:
                        try:
                            choice = int(input())
                        except ValueError:
                            type.type("Choose a number: ")
                    if(1<=choice<=len(broken_items)):
                        item = broken_items[choice-1]
                        break
                    elif choice==len(broken_items)+1:
                        item = "Home"
                        break
                    else:
                        choice = None
                        type.type("Did you comprehend that?")
                        print()
                        type.type("Choose a number: ")

                print()

                if item == "Delight Indicator":
                    type.type("You'd like Stuart to repair your Delight Indicator?")
                    if delight_indicator_price == 0:
                        delight_indicator_price = random.choice([5500, 6000, 9000, 10000])
                    price = delight_indicator_price
                elif item == "Health Indicator":
                    type.type("You'd like Stuart to repair your Health Indicator?")
                    if health_indicator_price == 0:
                        health_indicator_price = random.choice([4500, 5500, 7000, 9000, 11000])
                    price = health_indicator_price
                elif item == "Dirty Old Hat":
                    type.type("You'd like Stuart to repair the cloth on your Dirty Old Hat?")
                    if dirty_old_hat_price == 0:
                        dirty_old_hat_price = random.choice([14000, 15000, 17000, 20000])
                    price = dirty_old_hat_price
                elif item == "Golden Watch":
                    type.type("You'd like Stuart to repair that Golden Watch you possess?")
                    if golden_watch_price == 0:
                        golden_watch_price = random.choice([16000, 17500, 18000, 20000, 30000])
                    price = golden_watch_price
                elif item == "Faulty Insurance":
                    type.type("You'd like Stuart to restore your Faulty Insurance card?")
                    if faulty_insurance_price == 0:
                        faulty_insurance_price = random.choice([5500, 6000, 7000, 9000, 10000])
                    price = faulty_insurance_price
                elif item == "Sneaky Peeky Shades":
                    type.type("You'd like Stuart to fix up those Sneaky Peeky Shades on top of your eyelids?")
                    if sneaky_peeky_glasses_price == 0:
                        sneaky_peeky_glasses_price = random.choice([18000, 20000, 25000, 30000])
                    price = sneaky_peeky_glasses_price
                elif item == "Quiet Sneakers":
                    type.type("You'd like Stuart to sew up those Quiet Sneakers on your feet?")
                    if quiet_sneakers_price == 0:
                       quiet_sneakers_price = random.choice([9000, 10000, 12000])
                    price = quiet_sneakers_price
                else: 
                    type.type("Welp, then I've done all I can possibly do. Good day, my friend.")
                    print("\n")
                    self.start_night()
                    return
                
                print()

                type.type("Stuart will be able to fix this, for say, " + green(bright("${:,}".format(price))) + ". Do you accept? ")
                
                while True:
                    yes_or_no = input("").lower()
                    if ((yes_or_no == "y") or (yes_or_no == "yes")) and (self.__balance<price):
                        print()
                        type.type("Oh dear! I'm afraid you can't afford this purchase.")
                        if tips <= 2:
                            random_chance = random.randrange(2)
                            print("\n")
                            if random_chance <= 1:
                                type.type("Here, take this as a pick me up, hopefully it helps. Try again?")
                                self.change_balance(random.choice([50, 100, 200, 300, 400, 500]))
                                tips += 1
                            else:
                                broken_items.pop(choice-1)
                                type.type("Maybe give me something else to fix.")
                        else:
                            broken_items.pop(choice-1)  
                            print("\n")
                            type.type("Shall Stuart repair something else?")
                        break
                    elif (yes_or_no == "y") or (yes_or_no == "yes"):
                        print()
                        type.type("Jolly good! Stuart!")
                        random_chance = random.randrange(2)
                        if random_chance == 0:
                            print("\n")
                            type.type("Yes! Yes! Work your magic, you little man.")
                            self.change_balance(-price)
                            self.fix_item(item)
                            broken_items.pop(choice-1)
                            if item=="Sneaky Peeky Shades" or item=="Quiet Sneakers":
                                type.type("Your " + magenta(bright(item)) + " have been fixed!")
                            else:
                                type.type("Your " + magenta(bright(item)) + " has been fixed!")
                            print("\n")
                        else:
                            print("\n")
                            type.type("Okay, Stuart. What are you doing? It appears that Stuart has gotten stuck whilst trying to fix your thingy. No matter! Stuart, will you please stop? Here, friend, I am giving you your item back. I won't even charge you.")
                            print("\n")
                            broken_items.pop(choice-1)
                            if free_money < 2:
                                random_chance = random.randrange(2)
                                if random_chance == 0:
                                    type.type("In fact, here, just take it, this is yours now.")
                                    self.change_balance(random.choice([50, 100, 200, 500, 1000]))
                                    free_money += 1
                                else:
                                    type.type("I'm so sorry that Stuart was unable to help. My deepest condolences.")
                                    print("\n")
                            else:
                                type.type("Honestly, Stuart is trying his best, and you shouldn't get mad at him.")
                                print("\n")

                            
                        if len(broken_items)==0:
                            type.type("My my, that's everything! Please come again soon, and we can continue performing business!")
                            print("\n")
                            self.start_night()
                            return
                        else:
                            type.type("Is there anything else Stuart can help you with?")
                            print()
                        break
                    elif (yes_or_no == "n") or (yes_or_no == "no"):
                        print()
                        type.type("Really? Nevermind Stuart, you aren't going to fix this. I apologise, but they simply don't want you to. Blame them.")
                        print("\n")
                        type.type("Are you done teasing Stuart? Have anything else for him?")
                        print()
                        break
                    else:
                        print()
                        type.type("Come again? ")
        self.start_night()
        return

    # Convenience Store
    def update_convenience_store_inventory(self):
        if self.__day == 2: self.__convenience_store_inventory = self.__lists.make_convenience_store_inventory()
        if (self.__day % 7) == 0:
            self.__convenience_store_inventory = self.__lists.make_convenience_store_inventory()

    def visit_convenience_store(self):
        type.type("You get in your car and drive to the Convenience Store. ")
        if not self.has_met("Convenience Store"):
            self.meet("Convenience Store")
            type.type("When pulling into the parking lot, you have to grip the wheel tightly to keep control of the wagon, as the concrete beneath you is littered with potholes. As you drive closer to bright red brick building, you begin to read the sign 'Convenience Store' written in bold. ")
            type.type("Really? This place really called 'Convenience Store'? They couldn't have come up with anything more creative? You park nearby, and get out, being sure not to trip on the loose chunks of road. ")
            type.type("Walking closer to the store, you notice there's a poster with a smiling dude on it, holding his thumbs up, with the caption 'We Love our Customers! That's why we're limiting each customer to one item per visit. That means there's more for everyone! Sharing is caring!' ")
            type.type("Looking through the window, the store is barren, with only a few items on the shelf. If not for someone standing at the register, you would have thought the place to be abandoned.")
            print("\n")
            type.type("When you open the glass door, you notice a bell above you ring. There's a teenager on his phone, sitting with his feet up on the counter. His face is covered with pimples, and he's in the middle of blowing a bubble with the gum in his mouth.")
            print("\n")
            type.type("You get closer to the boy, and he finally notices you, and puts his phone down.")
        print("\n")
        if(len(self.__convenience_store_inventory)==0):
            type.type("As you walk up to the store, you see a white sign hanging on the front door. They're closed. Bummer.")
            print("\n")
            self.start_night()
            return
        type.type("Sup. Name's Kyle. Got a one-item limit. Managers orders. I don't make the rules. ")
        print("\n")
        items_bought = 0
        while True:
            choice = None
            items = self.__convenience_store_inventory
            if items_bought == 0:
                type.type("What do you want?")
            else:
                type.type("What else you want?")
            print()
            for i in range(len(items)+1):
                if(i<len(items)):
                    type.type(str(i+1) + ". " + items[i][0] + " - " + green(bright("${:,}".format(items[i][1]))))
                    print()
                else:
                    type.type(str(i+1) + ". I'm not buying anything")
                    time.sleep(0.5)
                    print()
            type.type("Choose a number: ")
            while True:
                while choice is None:
                    try:
                        choice = int(input())
                    except ValueError:
                        type.type("C'mon I don't have all day just pick something: ")
                if(1<=choice<=len(items)):
                    item = items[choice-1][0]
                    price = items[choice-1][1]
                    if(price<=self.__balance):
                        break
                    else:
                        type.type("Dude, you obviously can't afford that. Try again, buddy: ")
                elif choice==len(items)+1:
                    item = "Home"
                    break
                else:
                    choice = None
                    type.type("We clearly don't have that in right now.")
                    print()
                    type.type("It's not hard, just choose a number: ")
            print()

            if choice!=len(items)+1:
                items.pop(choice-1)

            if item == "Candy Bar":
                type.type("You got a " + bright(magenta("Candy Bar!")))
                print()
                type.type("You chomp down the candy bar. It's sweet chocolate and caramel fill your stomach, and you feel a little better.")
            elif item == "Bag of Chips":
                type.type("You got a " + bright(magenta("Bag of Chips!")))
                print()
                type.type("You chomp down the bag of chips. It's salty potato goodness fill your stomach, and you feel better.")
            elif item == "Turkey Sandwich":
                type.type("You got a " + bright(magenta("Turkey Sandwich!")))
                print()
                type.type("You chomp down the turkey sandwich. It's savory turkey and provolone fill your stomach, and you feel much better.")
            elif item == "Deck of Cards":
                type.type(bright(magenta("Deck of Cards!")))
                self.add_item("Deck of Cards")
            elif item == "Pest Control":
                type.type("You got " + bright(magenta("Pest Control!")))
                self.add_item("Pest Control")
            elif item == "LifeAlert":
                type.type(bright(magenta("You got LifeAlert!")))
            elif item == "Necronomicon":
                type.type(bright(magenta("You got a ") + red("Necronomicon!")))
            elif item == "Bag of Acorns":
                type.type(bright(magenta("You got a Bag of Acorns!")))
            elif item == "Home":
                type.type("Suit yourself.")
                print("\n")
                self.start_night()
                return
            
            items_bought+=1
            print("\n")

            if items_bought == 1:
                random_chance = random.randrange(5)
                if random_chance < 2:
                    type.type("You know what? Rules are made to be broken. I mean, screw em! I hate my manager anyways. ")
                    type.type("You can have one more item, just don't tell anyone I let you do this.")
                    print("\n")
                else:
                    type.type("Welp. There you go. That's your item. Weird thing to buy, if you ask me. Now get lost, I'm going on break.")
                    print("\n")
                    self.start_night()
                    return
            else:
                type.type("Welp. There you go. Two whole items. Wow. Now get lost. I've got a girl to text. She's super hot.")
                print("\n")
                self.start_night()
                return


    # Marvin's Shop and interactions
    def visit_marvin(self):
        type.type("You get in your car and drive to Marvin's Mystical Merchandise. ")
        print("\n")
        inventory = self.__lists.make_marvin_inventory()
        if len(inventory) == 0:
            type.type("Sorry man, I've got no product for you tonight. Maybe try coming back another day. ")
            return
        else:
            type.type("Welcome, welcome. I've got some very valuable stuff in stock, just for a fine gambler like you.")
            print("\n")
            type.type("While I won't get bogged down in the details of how I got my hands on it, I think you'll wanna check these out:")
            print("\n")

        for item_number in range(len(inventory)):
            item = inventory[item_number]
            if (item_number==0) and (len(inventory)==1):
                type.type("The only item I've got right now is the " + self.__lists.get_marvin_adjective() + " " + magenta(bright(item)))
            elif (item_number==0):
                type.type("The first item I've got is the " + self.__lists.get_marvin_adjective() + " " + magenta(bright(item)))
            elif item_number==len(inventory)-1:
                type.type("The last item I've got is the " + self.__lists.get_marvin_adjective() + " " + magenta(bright(item)))
            else:
                type.type("The next item I've got is the " + self.__lists.get_marvin_adjective() + " " + magenta(bright(item)))

            print()

            if item == "Delight Indicator":
                type.type("With this little device, you can read how happy anyone is, just by pointing it at them! Could get you out of a lot of trouble.")
                price = random.choice([8500, 9500, 10000])
            elif item == "Health Indicator":
                type.type("This gadget lets you see how healthy you are at any given moment. It's great for knowing how imminent a trip to the ER is.")
                price = random.choice([8000, 8500, 9500])
            elif item == "Dirty Old Hat":
                type.type("By wearing this, you're telling the whole world \"I'm poor and I'm not afraid to show it!\" It's a foolproof way for people to take pity on you.")
                price = random.choice([25000, 28000, 30000])
            elif item == "Golden Watch":
                type.type("This watch was my grandfathers at one point. It's a beauty. If you're a gambling man, anyone in their right mind would wanna see you betting on their table.")
                price = random.choice([29000, 32000, 35000])
            elif item == "Faulty Insurance":
                type.type("I got this thing forged by a buddy of mine. It's a fake insurance card. I've used it to get out of so many hospital bills, and you could too!")
                price = random.choice([10000, 11000, 12000])
            elif item == "Enchanting Silver Bar":
                type.type("Listen, I know this silver bar looks a bit useless, but I swear, it's awesome. Look at the stock market, this thing is only gonna get more and more expensive. And if I sell it to you, you can sell it off later and make some money.")
                price = 10000
            elif item == "Sneaky Peeky Shades":
                type.type("These aren't your ordinary pair of glasses. Put them on, and you'll catch glimpses that others can't see. But use them wisely; you only get one peek per night.")
                price = random.choice([35000, 38000, 40000])
            elif item == "Quiet Sneakers":
                type.type("Sometimes, the best move is to walk away. Use this when you feel trouble brewing, and avoid the day's misfortunes.")
                price = random.choice([15000, 18000, 20000])

            print()

            type.type("For " + green(bright("${:,}".format(price))) + ", it can be all yours. You buying? ")
            while True:
                yes_or_no = input("").lower()
                if ((yes_or_no == "y") or (yes_or_no == "yes")) and (self.__balance<price):
                    print()
                    type.type("Cmon man, you can't afford this.")
                    print("\n")
                    break
                if (yes_or_no == "y") or (yes_or_no == "yes"):
                    print()
                    type.type("Great! It's all yours.")
                    self.change_balance(-price)
                    self.add_item(item)
                    type.type("You got the " + magenta(bright(item)) + "!")
                    print()
                    type.type("Description: " + self.get_item_desc(item))
                    print("\n")
                    break
                elif (yes_or_no == "n") or (yes_or_no == "no"):
                    print()
                    type.type("Not your thing, huh? Well that's ok. ")
                    break
                else:
                    print()
                    type.type("What was that? ")

        type.type("That's all I've got to sell you tonight. Maybe try coming back another day. ")
        self.start_night()

    def update_no_bust_durability(self, invincible=False):
        if (self.has_flask_effect("No Bust")):
            if invincible:
                self.__flask_durability[0] = -1
                
            if (self.__flask_durability[0] > 0):
                self.__flask_durability[0] -= random.choice([1, 2])
                if self.__flask_durability[0] <= 0:
                    self.__flask_durability[0] = 0
                    self.remove_flask_effect("No Bust")
                    print("\n")
                    type.slow(red(bright("Your Flask of No Bust effect ran out!")))

            # Sets durability when you get the item, or if the item is fixed
            if (self.__flask_durability[0] == 0):
                self.__flask_durability[0] = 4

    def update_delight_indicator_durability(self, invincible=False):
        if self.has_item("Delight Indicator"):
            if invincible:
                self.__item_durability[0] = -1
                
            if (self.__item_durability[0] > 0):
                self.__item_durability[0] -= random.choice([1, 2, 3, 5])
                if self.__item_durability[0] <= 0:
                    self.__item_durability[0] = 0
                    self.break_item("Delight Indicator")
                    print("\n")
                    type.slow(red(bright("Your Delight Indicator broke!")))

            # Sets durability when you get the item, or if the item is fixed
            if (self.__item_durability[0] == 0):
                self.__item_durability[0] = 45


    def update_health_indicator_durability(self, invincible=False):
        if self.has_item("Health Indicator"):
            if invincible:
                self.__item_durability[1] = -1
                
            if (self.__item_durability[1] > 0):
                self.__item_durability[1] -= random.choice([1, 2, 3, 5])
                if self.__item_durability[1] <= 0:
                    self.__item_durability[1] = 0
                    self.break_item("Health Indicator")
                    type.slow(red(bright("Your Health Indicator broke!")))
                    print("\n")

            # Sets durability when you get the item, or if the item is fixed
            if (self.__item_durability[1] == 0):
                self.__item_durability[1] = 30


    def update_dirty_old_hat_durability(self, invincible=False):
        if self.has_item("Dirty Old Hat"):
            if invincible:
                self.__item_durability[2] = -1
                
            if (self.__item_durability[2] > 0):
                self.__item_durability[2] -= random.choice([1, 2, 3, 5])
                if self.__item_durability[2] <= 0:
                    self.__item_durability[2] = 0
                    self.break_item("Dirty Old Hat")
                    type.slow(red(bright("Your Dirty Old Hat broke!")))
                    print("\n")

            # Sets durability when you get the item, or if the item is fixed
            if (self.__item_durability[2] == 0):
                self.__item_durability[2] = 25


    def update_golden_watch_durability(self, invincible=False):
        if self.has_item("Golden Watch"):
            if invincible:
                self.__item_durability[3] = -1
                
            if (self.__item_durability[3] > 0):
                self.__item_durability[3] -= random.choice([1, 2, 3, 5])
                if self.__item_durability[3] <= 0:
                    self.__item_durability[3] = 0
                    self.break_item("Golden Watch")
                    type.slow(red(bright("Your Golden Watch broke!")))
                    print("\n")

            # Sets durability when you get the item, or if the item is fixed
            if (self.__item_durability[3] == 0):
                self.__item_durability[3] = 20


    def update_sneaky_peeky_glasses_durability(self, invincible=False):
        if self.has_item("Sneaky Peeky Shades"):
            if invincible:
                self.__item_durability[5] = -1

            if (self.__item_durability[5] > 0):
                self.__item_durability[5] -= random.choice([1, 2, 3, 5])
                if self.__item_durability[5] <= 0:
                    self.__item_durability[5] = 0
                    self.break_item("Sneaky Peeky Shades")
                    type.slow(red(bright("Your Sneaky Peeky Shades broke!")))
                    print("\n")

            # Sets durability when you get the item, or if the item is fixed
            if (self.__item_durability[5] == 0):
                self.__item_durability[5] = 15


    def update_quiet_sneakers_durability(self, invincible=False):
        if self.has_item("Quiet Sneakers"):
            if invincible:
                self.__item_durability[6] = -1

            if (self.__item_durability[6] > 0):
                self.__item_durability[6] -= random.choice([1, 2, 3, 5])
                if self.__item_durability[6] <= 0:
                    self.__item_durability[6] = 0
                    self.break_item("Quiet Sneakers")
                    type.slow(red(bright("Your Quiet Sneakers broke!")))
                    print("\n")

            # Sets durability when you get the item, or if the item is fixed
            if (self.__item_durability[6] == 0):
                self.__item_durability[6] = 15


    def update_faulty_insurance_durability(self, invincible=False):
        if self.has_item("Faulty Insurance"):
            if invincible:
                self.__item_durability[7] = -1
                
            if (self.__item_durability[7] > 0):
                self.__item_durability[7] -= random.choice([1, 2, 3, 5])
                if self.__item_durability[7] <= 0:
                    self.__item_durability[7] = 0
                    self.break_item("Faulty Insurance")
                    type.slow(red(bright("Your Faulty Insurance broke!")))
                    print("\n")

            # Sets durability when you get the item, or if the item is fixed
            if (self.__item_durability[7] == 0):
                self.__item_durability[7] = 15
        

    def get_item_desc(self, item):
        if item == "Delight Indicator": return "A small gadget, with wires tangled around it, and a small meter that displays the Dealer's happiness before every round of Blackjack."
        elif item == "Health Indicator": return "A small gadget, with wires construed around it, and a small gauge that displays changes in your health. Your current health is " + bright(magenta(str(self.__health) + "%")) + "."
        elif item == "Dirty Old Hat": return "A dark brown leather hat, covered in dirt and tears. It makes you look poor, and lowers the Dealer's minimum bet."
        elif item == "Golden Watch": return "A bright gold watch that glistens in any light. It makes you look rich, and increases the number of Blackjack rounds the Dealer lets you play."
        elif item == "Enchanting Silver Bar": return "A silver bar that slowly increases in worth every day. Sell this after 3 days to make a profit."
        elif item == "Sneaky Peeky Shades": return "A pair of glasses that allow you to sneak a peek at the next card in the deck once per night."
        elif item == "Quiet Sneakers": return "A pair of shoes that allows you to skip an unfavorable event during the day."
        elif item == "Faulty Insurance": return "A plastic card, with the company \'Super Real Insurance\' written on it. This card can be brought to the doctor's office for a chance of lowering bill fees."

        elif item == "Delight Manipulator": return "A small gadget, embedded in your right arm, with wires sticking into your veins. Attached is a small antenna that elicits complete and absolute happiness in anyone around you."
        elif item == "Health Manipulator": return "A small gadget, embedded in your left arm, with wires construed throughout your veins and into your heart. The device pumps artificial blood with a syntetic heartbeat throught your body, ensuring that you're always perfectly healthy."
        elif item == "Unwashed Hair": return "An implant into your scalp, giving you a fake hairdo covered in grime and grease. It makes you look abysmally poor, and sets the Dealer's minimum bet to one measly dollar"
        elif item == "Sapphire Watch": return "A sparkling sapphire watch that lights up any room. It makes you look richer than everyone else in the room, and greatly increases the number of Blackjack rounds the Dealer lets you play."
        elif item == "Enchanting Gold Bar": return "A gold bar that quickly increases in worth every day. Sell this after 3 days to make a profit."
        elif item == "Sneaky Peeky Goggles": return "A pair of goggles that allow you to sneak a peek at the next card in the deck once per round."
        elif item == "Quiet Bunny Slippers": return "A pair of slippers that allows you to skip all unfavorable events during the day."
        elif item == "Real Insurance": return "A plastic card, with the company \'Super Duper Real Insurance\' written on it. This card can be brought to the doctor's office to cover all bill fees."

        elif item == "No Bust": return "A flask holding a dark green potion. It's infused with the power to veto a hand that busts. It lasts a few days."
        elif item == "Imminent Blackjack": return "A flask holding a neon yellow potion. It's infused with the power to instantly give you a Blackjack after hitting your hand. It wears off after one use."
        elif item == "Dealer's Whispers": return "A flask holding a navy blue potion. It's infused with the power to reveal the Dealer's hidden card. It lasts a few days."
        elif item == "Bonus Fortune": return "A flask holding a shiny gold potion. It's infused with the power to let you double down after being dealt a hand. It lasts a few days."
        elif item == "Anti-Venom": return "A flask holding a sparkly orange potion. It's infused with the power to heal you when attacked by a venemous creature. It lasts until used."
        elif item == "Anti-Virus": return "A flask holding a flowing gray potion. It's infused with the power to heal you when affected by a disease. It lasts until used."
        elif item == "Fortunate Day": return "A flask holding a bright orange potion. It's infused with the luck of the sun, and makes your next morning lucky. It wears off after one use."
        elif item == "Fortunate Night": return "A flask holding a pretty magenta potion. It's infused with the luck of the stars, and makes your next evening lucky. It wears off after one use, and has no impact on gambling."

        elif item == "Never Bust": return "A flask holding a glowing green potion. It's infused with the power to veto a hand that busts."
        elif item == "Guaranteed Blackjack": return "A flask holding a glowing yellow potion. It's infused with the power to instantly give you a Blackjack after hitting your hand."
        elif item == "Dealer's Thoughts": return "A flask holding a glowing blue potion. It's infused with the power to always reveal the Dealer's hidden card."
        elif item == "Endless Fortune": return "A flask holding a glowing gold potion. It's infused with the power randomly double your bet for free after being dealt a hand."
        elif item == "Anti-Pathogen": return "A flask holding a glowing orange potion. It's infused with the power to heal you from any status effect."
        elif item == "Fortunate Life": return "A flask holding a glowing red potion. It's infused with the luck of the sun and the moon, and fills your life with good fortune."

    def day_event(self):
        self.update_rank()
        dayEvent = getattr(self, self.__lists.get_day_event())
        dayEvent()
        return

    def night_event(self):
        self.update_rank()
        nightEvent = getattr(self, self.__lists.get_night_event())
        nightEvent()
        self.update_rank()
        self.start_night()