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
                    time.sleep(0.1)
                elif self.__type_speed =="Fast" and (char == "?") or (char == ":"):
                    time.sleep(0.1)
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

class Player:
    __slots__ = ["__alive", "__status_effects", "__inventory", "__dangers", "__met", "__health", "__balance", "__previous_balance", "__rank", "__day", "__counting_days", "__prereqs", "__prereqs_done", "__convenience_store_inventory", "__lists"]

    def __init__(self):
        self.__alive = True
        self.__status_effects = set()
        self.__inventory = set()
        self.__dangers = set()
        self.__met = set()
        self.__health = 100
        self.__balance = 50
        self.__previous_balance = 50
        self.__rank = 0
        self.__day = 1
        self.__counting_days = [0, 0, 0, 0, 0, 0, 0]
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

    def heal(self, value):
        if(self.__health + value >= 100):
            self.__health = 100
        else:
            self.__health += value

    def status(self):
        if not self.__alive:
            print("\n")
            type.slow("You have died!")
            print()
            if self.__day == 1: type.slow("You didn't even last " + bright(yellow(str(self.__day) + " day")) + ". That's embarrasing.")
            elif self.__day == 2: type.slow("You lasted " + bright(yellow(str(self.__day-1) + " day")) + ".")
            else: type.slow("You lasted " + bright(yellow(str(self.__day) + " days")) + "!")
            print()
            type.slow("You met your fate with a final balance of " + green(bright("$" + str(self.__balance))))
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
    
    def add_status(self, status):
        self.__status_effects.add(status)

    def has_status(self, status):
        return status in self.__status_effects
    
    def remove_status(self, status):
        self.__status_effects.remove(status)

    def len_status(self):
        return len(self.__status_effects)

    def add_item(self, item):
        self.__inventory.add(item)

    def has_item(self, item):
        return item in self.__inventory
    
    def use_item(self, item):
        self.__inventory.remove(item)
    
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
            self.__balance += value
            type.type("Your new balance is " + green(bright("${:,}".format(self.__balance))))
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
        if(self.__day==1):
            self.end_day_1()
        elif(not self.has_item("Car")):
            self.end_day_car()
        else:
            self.end_day_car_fixed()

        print("\n")

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
        self.heal(random.choice([1, 3, 5]))
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
        type.type("As you go to sit down at the table, you hear the dealer cough, then watch as he sits up.")
        print("\n")
        type.type("In a deep, and yet strained voice, the dealer, cloaked in darkness, poses a question to you.")
        print("\n")
        self.start_night()



    # End Days
    def end_day_1(self):
        type.type("After playing a few rounds of Blackjack, the dealer points to the door. ")
        type.type("Without questing his word, and with your winnings in hand, you scurry to the door, eager to get some sleep after such a long day. ")
        type.type("Making it back to your car, ditched on the side of the road, but no longer engulfed in smoke, you lay down, and close your eyes. It's time to rest.")

    def end_day_car(self):
        type.type("After playing a few rounds of Blackjack, the dealer points to the door. ")
        type.type("Without questing his word, and with your winnings in hand, you scurry to the door, eager to get some sleep. ")
        type.type("Making it back to your car, ditched on the side of the road, you lay down, and close your eyes. It's time to rest.")

    def end_day_car_fixed(self):
        type.type("After playing a few rounds of Blackjack, the dealer points to the door. ")
        type.type("Without questing his word, and with your winnings in hand, you scurry to the door, eager to get some sleep. ")
        type.type("You make it to your car and drive away from the casino, and you park in a little alcove on the side of the road. You lay down, and close your eyes. It's time to rest.")

    def start_night(self):
        if(self.__day==1):
            self.start_night_1()
        elif(not self.has_item("Car")):
            self.start_night_car()
        else:
            self.start_night_car_fixed()

    def start_night_1(self):
        type.slow(red("Would you like to play a game of Blackjack? "))
        yes_or_no = input("").lower()
        print()
        if (yes_or_no == "n") or (yes_or_no == "no"):
            type.slow(red(bright("Well that's just too bad isn't it. ")))
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

    def mark_spider_bite_day(self, day):
        self.__counting_days[0] = day

    def get_spider_bite_day(self):
        return self.__day - self.__counting_days[0]
    
    def update_status(self):
        if self.has_status("Spider Bite"):
            days_elapsed = self.get_spider_bite_day()
            if days_elapsed == 0:
                self.hurt(random.choice([1, 2]))
                type.type("The fangmarks of your spider bite are faint but visible. ")
            elif days_elapsed == 1:
                self.hurt(random.choice([3, 4, 5, 6]))
                type.type("Your spider bite is sore and swolen. ")
            elif days_elapsed == 2:
                self.hurt(random.choice([4, 5, 6, 7, 8, 9]))
                type.type("Your spider bite is really painful. You don't feel good. ")
            elif days_elapsed >= 3:
                random_chance = random.randrange(4)
                if random_chance == 0:
                    self.remove_status("Spider Bite")
                    type.type("Your spider bite is starting to heal. ")
                else:
                    self.hurt(random.choice([7, 9, 11, 13, 15]))
                    type.type("Your spider bite is purple and pussing. A trip to the doctors might be a good idea. ")
            print("\n")

                
    # Poor Day Events (1 - 1,000)
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

    def spider_bite(self):
        if self.has_danger("Spider") and not self.has_status("Spider Bite"):
            type.type("You wake up to a sharp pain on your arm! ")
            type.type("Swinging your arm to scratch the pain, you watch as a spider jumps to your dashboard. ")
            if self.has_item("Pest Control"):
                self.use_item("Pest Control")
                self.lose_danger("Spider")
                type.type("You grab your " + magenta(bright("Pest Control")) + " and spray in the direction of the spider. ")
                type.type("A cloud of white liquid covers the spider, and you watch as it slows, and dies. ")
                type.type("Hopefully, that's the end of your spider problems. ")
            else:
                type.type("You attempt to swat it with your hand, but it sneaks into your heater. ")
                type.type("You start the engine and blast the heat, but you aren't sure if the spider has died, or if it has a family nearby. This sucks. ")
            self.add_status("Spider Bite")
            self.mark_spider_bite_day(self.__day)
            print("\n")
        else: 
            dayEvent = getattr(self, self.__lists.get_poor_day_event())
            dayEvent()

    def hungry_cockroach(self):
        random_choice = random.randrange(2)
        if random_choice == 0:
            if self.has_danger("Cockroach"):
                type.type("You wake up to the sound of a hiss in your pile of money. ")
                type.type("You jump up to check your cash, and you find a cockroach eating away at your cash. ")
                if self.has_item("Pest Control"):
                    self.use_item("Pest Control")
                    self.lose_danger("Cockroach")
                    type.type("You grab your " + magenta(bright("Pest Control")) + " and spray in the direction of the cockroach. ")
                    type.type("A cloud of white liquid covers the cockroach, and you watch as it slows down, twitches, and dies. ")
                    type.type("Hopefully, that's the end of your cockroach problems. ")
                else:
                    type.type("You attempt to swat it with your hand, but it falls under your car seat. ")
                    type.type("You stick your head under the seat, but you aren't sure where the cockroach went, or if it has a family nearby. This is terrible. ")
                print("\n")
                type.type("The cockroach ate through some of your money. ")
                losses = int(self.get_balance() * (random.randint(10, 40)/100))
                type.type("You lost " + green(bright("${:,}".format(losses))) + ".")
                self.change_balance(-losses)
            else: 
                dayEvent = getattr(self, self.__lists.get_poor_day_event())
                dayEvent()
        else: 
            dayEvent = getattr(self, self.__lists.get_poor_day_event())
            dayEvent()


    # Cheap Day Events (1,000 - 10,000)
    def big_bird(self):
        pass
        
    # Modest Day Events (10,000 - 100,000)
        
    # Rich Day Events (100,000 - 500,000)
        
    # Doughman Day Events (500,000 - 900,000)
        
    # Nearly There Day Events (900,000 - 1,000,000)



    # Poor Night Events (1 - 1,000)
    def ditched_wallet(self):
        type.type("Bored out of your mind, you decide to wander along the side of the road, just to get a change of scenery from the dusty leather seats of your wagon. ")
        type.type("As you take step after step over the asphalt, you notice a ditched wallet, just laying there. I guess it's yours now. ")
        print("\n")
        random_chance = random.randrange(2)
        if random_chance == 0:
            worth = random.randint(65, 120)
        else:
            worth = random.randint(7, 50)
        type.type("That's another " + green(bright("$" + str(worth))) + " dollars.")
        self.change_balance(worth)

    # Cheap Day Events (1,000 - 10,000)
        
    # Modest Day Events (10,000 - 100,000)
        
    # Rich Day Events (100,000 - 500,000)
        
    # Doughman Day Events (500,000 - 900,000)
        
    # Nearly There Day Events (900,000 - 1,000,000)



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
        type.type("\"Yep, this things busted alright! Tell ya what, for, I don't know, " + green(bright(str(repair_price) + " bucks")) + ", I'll get this thing replaced for ya, good as new! Whaddya say?\" ")
        while(True):
            yes_or_no = input("").lower()
            print()
            if(yes_or_no == "n") or (yes_or_no == "no"):
                type.type("Really? No dice, huh. Yunno, I think you're makin' a mistake, but I ain't one to judge. You have a nice day now.\" ")
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
                                type.type("Really? No dice, huh. Even with the discount? Yunno, I think you're makin' a mistake, but I ain't one to judge. You have a nice day now.\" ")
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
                type.type("What?! How could you not accept my service? I'm the cheapest damn autoshop worker on this here planet! But NOOOO, NOT FRANK! Never Frank. He Voted For Trump! Let's all ridicule frank for his political party. You god damn liberals.\" ")
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
                        type.type("And with that, you watch as he revs his engine, gets out of his truck, kicks his beater, gets back in, revs his engine, and speeds off into the horizon. ")
                        print("\n")
                        return
                    else: 
                        type.type("You notice Frank beginning to sweat while trying to fix your car. Each swing of his hammer is getting louder and louder, and Frank is clearly beginning to panic. Frank turns towards you, with tears streaming down his face. Or maybe it's just sweat.")
                        print("\n")
                        type.type("\"Oh man, listen, I'm so sorry about this, you know? I really thought if I just gave it the old hammer whirl that would do the trick. Hold on, maybe I have something in my truck. Stay right here!\" ")
                        print("\n")
                        type.type("You watch Frank runs over to his truck, kicks the side of it, gets in, revs his engine, and speeds off into the horizon. God Dammit.")
                        print("\n")
                        return
                else:
                    self.add_danger("Frank")
                    type.type("\"Are you tryna rip me off? Cleary you don't have enough money to afford my services, which is honestly pathetic, since I have the cheapest services around! I don't get what it is with you young folk and not working, just staying home and smoking weed. It's miserable. You're miserable. Dontchu know I know people on the inside! I'll remeber this one.\" ")
                    print("\n")
                    type.type("You watch as he revs his engine, gets out of his truck, kicks his beater, gets back in, revs his engine, and speeds off into the horizon. ")
                    print("\n")
                    return
            else:
                type.type("\"Speak up! You're mumbling. \" ")



    def optimal_oswald(self):
        self.meet("Oswald Event")
        type.type("You wake up to the sight of a glossy black limousine, quietly approaching your wagon. ")
        type.type("As you sit up from your slumber, you read \'Oswald's Optimal Outoparts\' cursively engraved in gold letters on the side of the limo. ")
        type.type("Waving the vehicle down, the limo slows, then stops before you. The door opens vertically, and a large red carpet is rolled out onto the street. You watch in awe as a man, with a combover and a tuxedo, walks out before you. He coughs, then speaks.  ")
        print("\n")
        type.type("\"Why hello there! The name's Oswald, as you can see by my nametag. Do you like my bowtie? Well of course you do! It appears your limousine has broken down.\" ")
        type.type("Oswald pulls a gold whistle out of his pocket, and blows into it deeply. ")
        type.type("\"Oh Stuart!\" You watch as a bald man in a tailcoat suit, no taller than 4 feet, hobbles over to Oswald's side. ")
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
                type.type("\"Shame on you! Shame on you! I hope to never see the likes of you again.\" ")
                print("\n")
                type.type("You watch as Oswald rolls up the red carpet, gets back in the limo, and drives off into the distance. ")
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
                    type.type("\"Oh my Stuart! Someone got a little too excited, didn't you? Yep, you're getting a bath as soon as we get back to the shop. Thanks again, stranger, its been a pleasure doing business with you. I recall it's good custom to tip after events like this, yes? Here, take this.\" ")
                    tip = random.choice([50, 100])
                    type.type("Oswald hands you a bright green bill, worth " + green(bright("$" + str(tip))) + ".")
                    self.change_balance(tip)
                    type.type("And with that, you watch as Stuart rolls up the red carpet. Oswald and Stuart get back in the limo, and drive off into the distance. ")
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
                type.type("\"Come again? \" ")


    def update_story_event_prereqs(self):
        if(self.__balance>=200):
            self.__prereqs[0] = True
        if self.has_item("Car"):
            self.__prereqs_done[0] = True

    def day_event(self):
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
        self.update_status()
        self.update_rank()
        self.update_convenience_store_inventory()
        if self.has_item("Car"):
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
                    type.type("That number's not a choice! ")
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
        print("\n")
        type.type("I see you're here for a checkup. The Doctor will see you now.")
        print("\n")
        type.type("Hey there champ! How are you? Doing all right? Let's check you out and make sure you're all up to snuff. ")
        print()
        if (self.len_status() == 0) and (self.__health == 100):
            type.type("Why, you look just as healthy as the day I met you, fresh from your mother's womb! Let me just give you this lollipop and you'll be free to go. ")
        elif (self.len_status() == 0):
            type.type("Why, you don't seem to really need my help. You appear a little worse for wear, but this medicine should do the trick. ")
            print("\n")
            self.heal(100)
        else:
            if self.has_status("Spider Bite"):
                type.type("I see you have a nasty spider bite. That thing looks gross. Let me get that cleaned up for you.")
                print()
            print()
            type.type("Well, that seems to be everything. You still appear a little worse for wear, but this medicine should do the trick. ")
            self.heal(100)
            
        print("\n")
        type.type("You walk back to the front desk to checkout. ")
        print("\n")
        cost = int((random.randint(65, 90)/100)*self.__balance)
        type.type("That will be " + bright(green("${:,}".format(cost))))
        if self.has_item("Faulty Insurance"):
            print()
            type.type("You show off your " + bright(magenta("Faulty Insurance")) + " to the lady, and put a convincing smile on your face. ")
            random_chance = random.randrange(10)
            if random_chance < 2:
                self.add_danger("Doctor Ban")
                print()
                self.use_item("Faulty Insurance")
                type.type("Is this supposed to fool me? A fake insurance card? That's it, I'm calling the cops! ")
                print("\n")
                type.type("Without hesitation, you turn, and run far, far away from the hospital, knowing that your face can't be seen there again. ")
                self.start_night()
                return
            else:
                print()
                type.type("I see, you have insurance. Well, that should give you quite the discount. ")
                print()
                cost = int((random.randint(10, 35)/100)*self.__balance)
                type.type("That will be " + bright(green("${:,}".format(cost))))
                self.change_balance(-cost)
                self.start_night()
                return
        else:
            self.change_balance(-cost)
            self.start_night()
            return


    # Witch Doctor's shop and interactions
    def visit_witch_doctor(self):
        type.type("You get in your car and drive to the Witch Doctor's Tower. ")
        self.start_night()

    # Tom's shop and interactions
    def visit_tom(self):
        type.type("You get in your car and drive to Tom's Trusty Trucks and Tires. ")
        self.start_night()

    # Frank's shop and interactions
    def visit_frank(self):
        type.type("You get in your car and drive to Filthy Frank's Flawless Fixtures. ")
        self.start_night()

    # Oswald's shop and interactions
    def visit_oswald(self):
        type.type("You get in your car and drive to Oswald's Optimal Outoparts. ")
        self.start_night()

    def update_convenience_store_inventory(self):
        if self.__day == 2: self.__convenience_store_inventory = self.__lists.make_convenience_store_inventory()
        if (self.__day % 7) == 0:
            self.__convenience_store_inventory = self.__lists.make_convenience_store_inventory()

    # Convenience Store
    def visit_convenience_store(self):
        type.type("You get in your car and drive to the Convenience Store. ")
        print("\n")
        if(len(self.__convenience_store_inventory)==0):
            type.type("As you walk up to the store, you see a white sign hanging on the front door. They're closed. Bummer. ")
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
                type.type("What do you want? ")
            else:
                type.type("What else you want? ")
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
                    type.type("We clearly don't have that in right now. ")
                    print()
                    type.type("It's not hard, just choose a number: ")
            print()

            if choice!=len(items)+1:
                items.pop(choice-1)

            if item == "Candy Bar":
                self.add_item("Candy Bar")
                type.type(bright(magenta("You got a Candy Bar!")))
            elif item == "Bag of Chips":
                self.add_item("")
                type.type(bright(magenta("You got a Bag of Chips!")))
            elif item == "Turkey Sandwich":
                self.add_item("")
                type.type(bright(magenta("You got a Turkey Sandwich!")))
            elif item == "Deck of Cards":
                self.add_item("Deck of Cards")
                type.type(bright(magenta("You got a Deck of Cards!")))
            elif item == "Pest Control":
                self.add_item("Pest Control")
                type.type(bright(magenta("You got Pest Control!")))
            elif item == "LifeAlert":
                type.type(bright(magenta("You got LifeAlert!")))
            elif item == "Necronomicon":
                type.type(bright(magenta("You got a ") + red("Necronomicon!")))
            elif item == "Bag of Acorns":
                type.type(bright(magenta("You got a Bag of Acorns!")))
            elif item == "Home":
                type.type("Suit yourself.")
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

        for item_number in range(len(inventory)):
            item = inventory[item_number]
            if (item_number==0) and (len(inventory)==1):
                type.type("The only item I've got right now is: " + magenta(bright(item)))
            elif (item_number==0):
                type.type("The first item I've got is: " + magenta(bright(item)))
            elif item_number==len(inventory)-1:
                type.type("The last item I've got is: " + magenta(bright(item)))
            else:
                type.type("The next item I've got is: " + magenta(bright(item)))

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
            elif item == "Sneaky Peeky Glasses":
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
                    type.type("You got " + magenta(bright(item)) + "!")
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

    def get_item_desc(self, item):
        if item == "Delight Indicator": return "A small gadget, with wires tangled around it, and a small meter that displays the Dealer's happiness before every round of Blackjack."
        elif item == "Health Indicator": return "A small gadget, with wires construed around it, and a small gauge that displays changes in your health. Your current health is " + str(self.__health) + "."
        elif item == "Dirty Old Hat": return "A dark brown leather hat, covered in dirt and tears. It makes you look poor, and lowers the Dealer's minimum bet."
        elif item == "Golden Watch": return "A bright gold watch that glistens in any light. It makes you look rich, and increases the number of Blackjack rounds the Dealer lets you play."
        elif item == "Enchanting Silver Bar": return "A silver bar that slowly increases in worth every day. Sell this after 3 days to make a profit. Its current value is (value)."
        elif item == "Sneaky Peeky Glasses": return "A pair of glasses that allow you to sneak a peek at the next card in the deck once per night."
        elif item == "Quiet Sneakers": return "A pair of shoes that allows you to skip an unfavorable event during the day."
        elif item == "Faulty Insurance": return "A plastic card, with the company \'Super Real Insurance\' written on it. This card can be brought to the doctor's office for a chance of lowering bill fees."

    def update_silver_value(self):
        if self.has_item("Enchanting Silver Bar"):
            return 1000


    def night_event(self):
        self.update_rank()
        match self.__rank:
            case 0: nightEvent = getattr(self, self.__lists.get_poor_night_event())
            case 1: nightEvent = getattr(self, self.__lists.get_cheap_night_event())
            case 2: nightEvent = getattr(self, self.__lists.get_modest_night_event())
            case 3: nightEvent = getattr(self, self.__lists.get_rich_night_event())
            case 4: nightEvent = getattr(self, self.__lists.get_doughman_night_event())
            case 5: nightEvent = getattr(self, self.__lists.get_nearly_night_event())
        nightEvent()
        self.update_rank()
        self.start_night()