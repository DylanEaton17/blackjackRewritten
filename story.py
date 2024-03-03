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
        self.__enter = False

    def holding_enter(self):
        return self.__enter

    def type(self, *words):
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

    def slowtype(self, *words):
        str = ''
        for item in words:
            str = str + item
        # str += "\n"
            for char in str:
                if self.holding_enter() == True:
                    time.sleep(0.01)
                else:
                    time.sleep(random.choice([
                    0.06, 0.05, 0.03, 0.03,
                    0.05, 0.03, 0.04, 0.05, 0.06, 0.04
                    ]))
                sys.stdout.write(char)
                sys.stdout.flush()
                if not self.holding_enter() and ((char == ".") or (char == "!") or (char == ":") or (char == ";") or (char == "?")):
                    time.sleep(0.7)
                if not self.holding_enter() and (char == ","):
                    time.sleep(0.4)
                
                self.cleanup()

    def cleanup(self):
        while msvcrt.kbhit():
            byte = msvcrt.getch()
            if byte == b'\r':
                self.__enter = True
            else:
                self.__enter = False


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
    __slots__ = ["__alive", "__status_effects", "__inventory", "__dangers", "__met", "__health", "__balance", "__previous_balance", "__rank", "__day", "__counting_days", "__lists"]

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
        self.__lists = lists.Lists(self)

    def kill(self):
        self.__alive = False
        self.status()

    def hurt(self, value):
        if(self.__health - value <= 0):
            self.__health = 0
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
            type.slowtype("You have died!")
            print()
            if self.__day == 1: type.slowtype("You didn't even last " + bright(yellow(str(self.__day) + " day") + ". That's embarrasing."))
            if self.__day == 2: type.slowtype("You lasted " + bright(yellow(str(self.__day-1) + " day")))
            else: type.slowtype("You lasted " + bright(yellow(str(self.__day) + " days")))
            print()
            type.slowtype("You met your fate with a final balance of " + green(bright("$" + str(self.__balance))))
            print()
            type.slowtype("The police were able to recover your body, but nobody cared enough to show up to your funeral.")
            quit()
        elif (self.__balance == 0):
            print("\n")
            type.slowtype("You have run out of money!")
            print()
            if self.__day == 1: type.slowtype("You lasted " + bright(yellow(str(self.__day) + " day")))
            else: type.slowtype("You lasted " + bright(yellow(str(self.__day) + " days")))
            print()
            type.slowtype("With no cash left to play Blackjack, your source of income has been rendered useless.")
            print()
            type.slowtype("You spend your remaining days going hungry, wondering what life could've been, if you didn't lose that one hand.")
            quit()
        elif (self.__balance >= 1000000):
            print("\n")
            type.slowtype("u win lol look at u millionaire go girl")
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
            type.slowtype("Your new balance is " + red(bright("$0")))
        else:
            self.__balance += value
            type.slowtype("Your new balance is " + green(bright("${:,}".format(self.__balance))))
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
        type.slowtype(self.__lists.get_cheer())

        # Tells day count and previous day's balance
        if self.__day == 1:
            type.slowtype(" You've survived " + yellow(bright(str(self.__day) + " day")) + "!")
            print("\n")
            type.slowtype("You started your journey with just " + green(bright("$" + str(self.__previous_balance))) + ". ")
        else:
            type.slowtype(" You've survived " + yellow(bright(str(self.__day) + " days")) + "!")
            print("\n")
            type.slowtype("Yesterday, at this time, you had " + green(bright("$" + str(self.__previous_balance))) + ". ")
        # increments day
        self.__day += 1

        print("")

        # Tells you the change in your balance, and if you gained or lost money
        change_in_balance = self.__balance - self.__previous_balance
        if change_in_balance > 0: type.slowtype("Since then, you've accumulated " + green(bright("$" + str(change_in_balance))) + ". ")
        elif change_in_balance < 0: type.slowtype("Since then, you've managed to lose " + red(bright("$" + str(abs(change_in_balance)))) + ". ")
        else: type.slowtype("Somehow, your net earnings today was 0. Goose egg. No money. Disappointing. ")

        # Sets previous balance to current balance, so that it's ready for next day
        self.__previous_balance = self.__balance

        print("")

        # Tells you your current balance
        type.slowtype("That brings you to a grand total of " + green(bright("$" + str(self.__balance))) + "! ")

        match self.__rank:
            case 0: type.slowtype("Let's not get too far ahead of ourselves though, you're still quite poor.")
            case 1: type.slowtype("You definately have some money. The keyword is 'some'.")
            case 2: type.slowtype("You've amassed signifigant earnings. Nicely done.")
            case 3: type.slowtype("You must have some heavy pockets, huh.")
            case 4: type.slowtype("Where do you even keep all that?")
            case 5: type.slowtype("So close to being a millionaire! Can you do it?")

        print("\n")

        # Gives a little personal advice, support, etc
        type.slowtype(self.__lists.get_advice())

        print()

        # Gives one last quote before starting the next day
        type.slowtype(self.__lists.get_quote_setup())
        type.slowtype(self.__lists.get_quote())

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
        type.slowtype("\"Ugh, not again,\" you spout as the old wagon shutters, then dies. ")
        type.slowtype("Stranded on the road again, but this time, your money has gone dry. ")
        type.slowtype("All but your 50 dollar bill that Grandma gave you on her last Christmas. ")
        type.slowtype("You've been saving it for when you needed it most, but surely, it won't be enough.")
        print('\n')
        type.slowtype("The door creaks open, and you step out into the night sky, coughing up the smoke from your fried vehicle. ")
        type.slowtype("After pushing your car off the road and between the trees, there isn't much else left for you to do, ")
        type.slowtype("so you begin to wander down the dark, lonely street.")
        print('\n')
        type.slowtype("But at the end of the road, where concrete turned to stone turned to dirt, you notice a light up ahead, on the top of a hill. ")
        print('\n')
        type.slowtype("As you waltz into the old, wooden shack, your eyes begin to light up with the fire of a thousand suns. ")
        type.slowtype("Roulette wheels! Poker tables! And in a dark corner of the abandoned casino, sits a dealer, shuffling cards for a new round of Blackjack. ")
        type.slowtype("That 50 dollars might just come in handy after all. Thanks, Grandma!")
        print('\n')
        type.slowtype("As you go to sit down at the table, you hear the dealer cough, then watch as he sits up.")
        print("\n")
        type.slowtype("In a deep, and yet strained voice, the dealer, cloaked in darkness, poses a question to you.")
        print("\n")


    # End Days
    def end_day_1(self):
        type.slowtype("After playing a few rounds of Blackjack, the dealer points to the door. ")
        type.slowtype("Without questing his word, and with your winnings in hand, you scurry to the door, eager to get some sleep after such a long day. ")
        type.slowtype("Making it back to your car, ditched on the side of the road, but no longer engulfed in smoke, you lay down, and close your eyes. It's time to rest. ")

    def end_day_car(self):
        type.slowtype("After playing a few rounds of Blackjack, the dealer points to the door. ")
        type.slowtype("Without questing his word, and with your winnings in hand, you scurry to the door, eager to get some sleep. ")
        type.slowtype("Making it back to your car, ditched on the side of the road, you lay down, and close your eyes. It's time to rest.")

    def mark_spider_bite_day(self, day):
        self.__counting_days[0] = day

    def get_spider_bite_day(self):
        return self.__day - self.__counting_days[0]
    
    def update_status(self):
        if self.has_status("Spider Bite"):
            days_elapsed = self.get_spider_bite_day()
            if days_elapsed == 0:
                self.hurt(random.choice([1, 2]))
                type.slowtype("The fangmarks of your spider bite are faint but visible. ")
            elif days_elapsed == 1:
                self.hurt(random.choice([3, 4, 5, 6]))
                type.slowtype("Your spider bite is sore and swolen. ")
            elif days_elapsed == 2:
                self.hurt(random.choice([4, 5, 6, 7, 8, 9]))
                type.slowtype("Your spider bite is really painful. You don't feel good. ")
            elif days_elapsed >= 3:
                random_chance = random.randrange(4)
                if random_chance == 0:
                    self.remove_status("Spider Bite")
                    type.slowtype("Your spider bite is starting to heal. ")
                else:
                    self.hurt(random.choice([2, 7, 9, 11, 13, 15]))
                    type.slowtype("Your spider bite is purple and pussing. A trip to the doctors might be a good idea. ")
            print("\n")

                



    # Poor Day Events (1 - 1,000)
    def seat_cash(self):
        type.slowtype("You wake up in the front seat, covered in sweat. ")
        type.slowtype("As the sun shines through the car window, you notice a bright green bill tucked between the seat cushions. Must be your lucky day. ")
        print("\n")
        bill = random.choice([5, 10, 20, 50, 100])
        type.slowtype("That's another " + green(bright("$" + str(bill))) + " dollars")
        self.change_balance(bill)

    def left_window_down(self):
        type.slowtype("You wake up in the front seat, with a chill going down your spine. ")
        type.slowtype("Had the window really been open all night? ")
        type.slowtype("Hopefully nothing had gotten in. ")
        type.slowtype("You roll the window up, just to be safe. ")
        random_chance = random.randrange(5)
        if random_chance == 0:
                self.add_danger("Spider")
        elif random_chance == 1:
                self.add_danger("Cockroach")
        print("\n")

    def spider_bite(self):
        if self.has_danger("Spider"):
            type.slowtype("You wake up to a sharp pain on your arm! ")
            type.slowtype("Swinging your arm to scratch the pain, you watch as a spider jumps to your dashboard. ")
            if self.has_item("Pest Control"):
                self.use_item("Pest Control")
                self.lose_danger("Spider")
                type.slowtype("You grab your " + magenta(bright("Pest Control")) + " and spray in the direction of the spider. ")
                type.slowtype("A cloud of white liquid covers the spider, and you watch as it slows, and dies. ")
                type.slowtype("Hopefully, that's the end of your spider problems. ")
            else:
                type.slowtype("You attempt to swat it with your hand, but it sneaks into your heater. ")
                type.slowtype("You start the engine and blast the heat, but you aren't sure if the spider has died, or if it has a family nearby. This sucks. ")
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
                type.slowtype("You wake up to the sound of a hiss in your pile of money. ")
                type.slowtype("You jump up to check your cash, and you find a cockroach eating away at your cash. ")
                if self.has_item("Pest Control"):
                    self.use_item("Pest Control")
                    self.lose_danger("Cockroach")
                    type.slowtype("You grab your " + magenta(bright("Pest Control")) + " and spray in the direction of the cockroach. ")
                    type.slowtype("A cloud of white liquid covers the cockroach, and you watch as it slows down, twitches, and dies. ")
                    type.slowtype("Hopefully, that's the end of your cockroach problems. ")
                else:
                    type.slowtype("You attempt to swat it with your hand, but it falls under your car seat ")
                    type.slowtype("You stick your head under the seat, but you aren't sure where the cockroach went, or if it has a family nearby. This is terrible. ")
                print("\n")
                type.slowtype("The cockroach ate through some of your money. ")
                losses = int(self.get_balance() * (random.randint(10, 40)/100))
                type.slowtype("You lost " + green(bright("${:,}".format(losses))) + ".")
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

    # Cheap Day Events (1,000 - 10,000)
        
    # Modest Day Events (10,000 - 100,000)
        
    # Rich Day Events (100,000 - 500,000)
        
    # Doughman Day Events (500,000 - 900,000)
        
    # Nearly There Day Events (900,000 - 1,000,000)



    # Story Events
    def trusty_tom(self):
        type.slowtype("You wake up to a blaring engine, roaring down the road towards you. ")
        type.slowtype("As you scratch your eyes awake, you read \'Tom the Trusty Mechanic\' painted on the hood of a bright gold truck. ")
        type.slowtype("Waving the vehicle down, the truck slows, then halts, and an old, jolly man jumps out. ")
        print("\n")
        type.slowtype("\"Well, howdy! The name's Tom. It appears you've gotten yourself in a bit of a pickle, ya think?\" ")
        type.slowtype("Tom pulls a big red wrench out of his pocket, and walks to the hood of your beaten down wagon. ")
        repair_price = random.choice([100, 150, 200, 250, 300])
        type("\"Yep, this things busted alright! Tell ya what, for, I don't know, " + green(bright(str(repair_price) + " bucks")) + ", I'll get this thing replaced for ya, good as new! Whaddya say?\" ")
        while(True):
            yes_or_no = input("").lower()
            print()
            if(yes_or_no == "n") or (yes_or_no == "no"):
                type.slowtype("Really? No dice, huh. Yunno, I think you're makin' a mistake, but I ain't one to judge. You have a nice day now.\" ")
                type.slowtype("Tom has a sad look in his eye. It's clear that he wanted to help you. ")
                type.slowtype("You watch as his big golden truck stutters, starts, then drives away.")
                print("\n")
                return
            elif((yes_or_no == "y") or (yes_or_no == "yes")):
                if self.__balance >= repair_price:
                    type.slowtype("\"Really? Awesome! I'll be the best dang mechanic this ol' automobile has ever seen!\" ")
                    type.slowtype("You watch in awe, as Tom, a man who has clearly perfected his craft, fixes up your wagon in no time. Sweet. ")
                    self.change_balance(-repair_price)
                    self.add_item("Car")
                    type.slowtype(magenta(bright("Your car has been fixed! You can now drive around!")))
                    print("\n")
                    type.slowtype("\"Well, gee, this has been fun. Be seein' you around, ya know?\" ")
                    type.slowtype("And with that, you watch as his big golden truck stutters, starts, then drives away.")
                    print("\n")
                    return
                else:
                    type.slowtype("\"Aww man, sorry to tell you, but you just don't got enough funds for this, yunno?\" ")
                    random_chance = random.randrange(2)
                    # Broke, and Tom offers discount
                    if random_chance == 0:
                        print("\n")
                        type.slowtype("\"You know what? I'm feelin' generous, and the shop's been doing well lately. ")
                        type.slowtype("Tell ya what, I can take the offer down " + green(bright(str(50) + " dollars")) + " just for you. ")
                        type.slowtype("Could ya do " + green(bright(str(repair_price-50) + " bucks")) + "?\" ")
                        while True:
                            yes_or_no_2 = input("").lower()
                            print()
                            # Declining Tom's second offer
                            if(yes_or_no_2 == "n") or (yes_or_no_2=="no"):
                                print()
                                type.slowtype("Really? No dice, huh. Even with the discount? Yunno, I think you're makin' a mistake, but I ain't one to judge. You have a nice day now.\" ")
                                type.slowtype("Tom has a dissapointed look in his eye. It's clear that he wanted to help you. ")
                                type.slowtype("You watch as his big golden truck stutters, starts, then drives away.")
                                print("\n")
                                return
                            elif((yes_or_no_2 == "y") or (yes_or_no_2 == "yes")):
                                if self.__balance >= (repair_price-50):
                                    type.slowtype("\"Really? Awesome! I'll be the best dang mechanic this ol' automobile has ever seen!\" ")
                                    type.slowtype("You watch in awe, as Tom, a man who has clearly perfected his craft, fixes up your wagon in no time. Sweet. ")
                                    self.change_balance(-(repair_price-50))
                                    self.add_item("Car")
                                    type.slowtype(magenta(bright("Your car has been fixed! You can now drive around!")))
                                    print("\n")
                                    type.slowtype("\"Well, gee, this has been fun. Be seein' you around, ya know?\" ")
                                    type.slowtype("And with that, you watch as his big golden truck stutters, starts, then drives away.")
                                    print("\n")
                                    return
                                else:
                                    type.slowtype("\"Still can't afford it? That's a real shame. I really wish there was something I could do. Best of luck my friend. Be seeing ya around, ya know?\" ")
                                    type.slowtype("And with that, you watch as his big golden truck stutters, starts, then drives away.")
                                    print("\n")
                                return
                            else:
                                type.slowtype("\"Whaddya say?\" ")

                    # Broke, and Tom can't offer discount
                    elif random_chance == 1:
                        print("\n")
                        type.slowtype("\"I really wish there was something I could do. Best of luck my friend. Be seeing ya around, ya know?\" ")
                        type.slowtype("And with that, you watch as his big golden truck stutters, starts, then drives away.")
                        print("\n")
                        return
            else:
                type.slowtype("\"Whaddya say?\" ")


    def day_event(self):
        self.update_rank()
        ranStoryEvent = False

        if(not self.has_item("Car")) and (self.__balance>=200):
            random_chance = random.randrange(3)
            if random_chance==0:
                self.trusty_tom()
                ranStoryEvent = True
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

        if self.has_item("Car"):
            choice = None
            shops = self.__lists.make_shop_list()
            type.slowtype("Would you like to spend your day driving somewhere? ")
            print()
            for i in range(len(shops)+1):
                if(i<len(shops)):
                    type.slowtype(str(i+1) + ". " + shops[i])
                    time.sleep(0.5)
                    print()
                else:
                    type.slowtype(str(i+1) + ". Stay Home")
                    time.sleep(0.5)
                    print()
            type.slowtype("Choose a number: ")
            while True:
                while choice is None:
                    try:
                        choice = int(input())
                    except ValueError:
                        type.slowtype("Choose a number: ")
                if(1<=choice<=len(shops)):
                    shop = shops[choice-1]
                    break
                elif choice==len(shops)+1:
                    shop = "Home"
                    break
                else:
                    choice = None
                    type.slowtype("That number's not a choice! ")
                    print()
                    type.slowtype("Choose a number: ")
            print()

            if shop == "Doctor's Office":
                self.visit_doctor()
                return
            elif shop == "Witch Doctor's Tower":
                self.visit_witch_doctor()
                return
            elif shop == "Convenience Store":
                self.visit_convenience_store()
                return
            elif shop == "Marvin's Mystical Merchandise":
                self.visit_marvin()
                return
            else:
                self.night_event()
                return
            
        else:
            self.night_event()

            
    def visit_doctor(self):
        type.slowtype("You get in your car and drive to the Doctor's Office. ")
        print("\n")
        type.slowtype("I see you're here for a checkup. The Doctor will see you now.")
        print("\n")
        type.slowtype("Hey there champ! How are you? Doing all right? Let's check you out and make sure you're all up to snuff. ")
        print()
        if (self.len_status() == 0) and (self.__health == 100):
            type.slowtype("Why, you look just as healthy as the day I met you, fresh from your mother's womb! Let me just give you this lollipop and you'll be free to go. ")
        elif (self.len_status() == 0):
            type.slowtype("Why, you don't seem to really need my help. You appear a little worse for wear, but this medicine should do the trick. ")
            print("\n")
            self.heal(100)
        else:
            if self.has_status("Spider Bite"):
                type.slowtype("I see you have a nasty spider bite. That thing looks gross. Let me get that cleaned up for you.")
                print()
            print()
            type.slowtype("Well, that seems to be everything. You still appear a little worse for wear, but this medicine should do the trick. ")
            self.heal(100)
            
        print("\n")
        type.slowtype("You walk back to the front desk to checkout. ")
        print("\n")
        cost = int((random.randint(65, 90)/100)*self.__balance)
        type.slowtype("That will be " + bright(green("${:,}".format(cost))))
        if self.has_item("Faulty Insurance"):
            type.slowtype("You show off your " + bright(magenta("Faulty Insurance")) + " to the lady, and put a convincing smile on your face. ")
            random_chance = random.randrange(10)
            if random_chance < 2:
                self.add_danger("Doctor Ban")
                self.use_item("Faulty Insurance")
                type.slowtype("Is this supposed to fool me? A fake insurance card? That's it, I'm calling the cops! ")
                print("\n")
                type.slowtype("Without hesitation, you turn, and run far, far away from the hospital, knowing that your face can't be seen there again. ")
                return
            else:
                type.slowtype("I see, you have insurance. Well, that should give you quite the discount. ")
                print()
                cost = int((random.randint(10, 35)/100)*self.__balance)
                type.slowtype("That will be " + bright(green("${:,}".format(cost))))
                self.change_balance(-cost)
        else:
            self.change_balance(-cost)
            return


    def visit_witch_doctor(self):
        type.slowtype("You get in your car and drive to the Witch Doctor's Tower. ")

    def visit_convenience_store(self):
        type.slowtype("You get in your car and drive to the Convenience Store. ")

    def visit_marvin(self):
        type.slowtype("You get in your car and drive to Marvin's Mystical Merchandise. ")
        print("\n")
        inventory = self.__lists.make_marvin_inventory()
        if len(inventory) == 0:
            type.slowtype("Sorry man, I've got no product for you tonight. Maybe try coming back another day. ")
            return

        for item_number in range(len(inventory)):
            item = inventory[item_number]
            if (item_number==0) and (len(inventory)==1):
                type.slowtype("The only item I've got right now is: " + magenta(bright(item)))
            elif (item_number==0):
                type.slowtype("The first item I've got is: " + magenta(bright(item)))
            elif item_number==len(inventory)-1:
                type.slowtype("The last item I've got is: " + magenta(bright(item)))
            else:
                type.slowtype("The next item I've got is: " + magenta(bright(item)))

            print()

            if item == "Delight Indicator":
                type.slowtype("With this little device, you can read how happy anyone is, just by pointing it at them! Could get you out of a lot of trouble.")
                price = random.choice([8500, 9500, 10000])
            elif item == "Health Indicator":
                type.slowtype("This gadget lets you see how healthy you are at any given moment. It's great for knowing how imminent a trip to the ER is.")
                price = random.choice([8000, 8500, 9500])
            elif item == "Dirty Old Hat":
                type.slowtype("By wearing this, you're telling the whole world \"I'm poor and I'm not afraid to show it!\" It's a foolproof way for people to take pity on you.")
                price = random.choice([25000, 28000, 30000])
            elif item == "Golden Watch":
                type.slowtype("This watch was my grandfathers at one point. It's a beauty. If you're a gambling man, anyone in their right mind would wanna see you betting on their table.")
                price = random.choice([29000, 32000, 35000])
            elif item == "Faulty Insurance":
                type.slowtype("I got this thing forged by a buddy of mine. It's a fake insurance card. I've used it to get out of so many hospital bills, and you could too!")
                price = random.choice([10000, 11000, 12000])
            elif item == "Enchanting Silver Bar":
                type.slowtype("Listen, I know this silver bar looks a bit useless, but I swear, it's awesome. Look at the stock market, this thing is only gonna get more and more expensive. And if I sell it to you, you can sell it off later and make some money.")
                price = 10000
            elif item == "Sneaky Peeky Glasses":
                type.slowtype("These aren't your ordinary pair of glasses. Put them on, and you'll catch glimpses that others can't see. But use them wisely; you only get one peek per night.")
                price = random.choice([35000, 38000, 40000])
            elif item == "Quiet Sneakers":
                type.slowtype("Sometimes, the best move is to walk away. Use this when you feel trouble brewing, and avoid the day's misfortunes.")
                price = random.choice([15000, 18000, 20000])

            print()

            type.slowtype("For " + green(bright("${:,}".format(price))) + ", it can be all yours. You buying? ")
            while True:
                yes_or_no = input("").lower()
                if ((yes_or_no == "y") or (yes_or_no == "yes")) and (self.__balance<price):
                    print()
                    type.slowtype("Cmon man, you can't afford this.")
                    print("\n")
                    break
                if (yes_or_no == "y") or (yes_or_no == "yes"):
                    print()
                    type.slowtype("Great! It's all yours.")
                    self.change_balance(-price)
                    self.add_item(item)
                    type.slowtype("You got " + magenta(bright(item)) + "!")
                    print()
                    type.slowtype("Description: " + self.get_item_desc(item))
                    print("\n")
                    break
                elif (yes_or_no == "n") or (yes_or_no == "no"):
                    print()
                    type.slowtype("Not your thing, huh? Well that's ok. ")
                    break
                else:
                    print()
                    type.slowtype("What was that? ")

        type.slowtype("That's all I've got to sell you tonight. Maybe try coming back another day. ")

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