import random
import deckOfCards
from colorama import Fore, Back, Style
import time
import random
import sys
import msvcrt

PAUSE = .25

"""
Below are all of the typing/color functions, used
for terminal outputs and making my text pretty
"""
class Typing:
    def __init__(self):
        self.__enter = False

    def holding_enter(self):
        return self.__enter

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
                if ((char == ".") or (char == "!") or (char == ":") or (char == ";") or (char == "?")):
                    time.sleep(0.7)
                if (char == ","):
                    time.sleep(0.4)
                self.cleanup()

    def cleanup(self):
        while msvcrt.kbhit():
            byte = msvcrt.getch()


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



class Blackjack:
    __slots__=["__balance", "__bet", "__min_bet", "__dealer_happiness", "__deck", "__hand", "__dealer_hand", "__player", "__used_peak", "__dealer_warning", "__free_hand"]

    def __init__(self, player):
        self.__balance = 50
        self.__bet = 0
        self.__min_bet = 1
        self.__dealer_happiness = 45
        self.__deck = deckOfCards.Deck()
        self.__hand = Hand("Player")
        self.__dealer_hand = Hand("Dealer")
        self.__player = player
        self.__used_peak = False
        self.__dealer_warning = False
        self.__free_hand = False

    def update_player(self):
        self.__balance = self.__player.get_balance()
        self.__player.update_rank()
        if self.__player.has_item("Golden Watch"):
            self.__player.set_rounds(4)
        self.__used_peak = False

    def play_round(self, count=None):
        # Updates the player
        self.update_player()

        # Sets number of rounds played, if not specified. Mainly for testing
        if count==None:
            count = self.__player.get_rounds()

        # Resets the deck
        self.hard_reset()

        # Tells player that their golden watch is noticed by the Dealer
        if self.__player.has_item("Golden Watch"):
            type.fast("Your " + bright(magenta("Golden Watch")) + " glistens in the light hanging above the betting table. The Dealer will let you play an extra round.")
            print("\n")

        if self.__player.has_item("Dirty Old Hat"):
            type.fast("The " + bright(magenta("Dirty Old Hat")) + " on your head sends dust in the air, and reeks of poverty. Minimum bets are lowered.")
            print("\n")

        # Makes the dealer a bit happier, as a new day has started
        self.calm_dealer(random.choice([5, 7, 10]), False)
        if self.__player.has_item("Delight Indicator"):
            type.fast("Your " + bright(magenta("Delight Indicator")) + " begins to flash.")
            print()
            type.fast("The Dealer has calmed down since you've last seen him!")
            print()
            self.delight_indicator()
            print("\n")

        # Tells the player their balance.
        type.fast("You have " + green(bright("${:,}".format(self.__balance))))
        print()

        for _ in range(count):
            while(True):
                self.__player.status()
                print()

                # Checks the dealer's happiness, which could lead to effects
                self.dealer_status()

                if(self.__player.has_item("Dirty Old Hat")):
                    self.set_min_bet(int(self.__balance/4))
                else:
                    self.set_min_bet(self.__balance)

                if(not self.__free_hand):
                    player_betting = False
                    while(not player_betting):
                        player_betting = self.bet()

                self.first_deal()

                # Checks if either player was dealt blackjack
                if(self.is_game_over(False)):
                    break

                # Main loop for player hitting their hand
                # will continue until they choose to stand or is_game_over detects their hand's value >= 21
                player_standing = False
                while(not player_standing):
                    player_standing = self.hit_or_stand()
                    breakloop = self.is_game_over(False)
                    if breakloop:
                        break

                # Breaks main loop if smaller loop broke from the game ending
                if breakloop:
                    break

                print("\n")

                self.print_draw("Dealer", "second", self.__dealer_hand.get_card(1))
                print()

                type.fast(str(self.__dealer_hand))
                print()

                # The loop that has the dealer hit until their value is >= 17
                # At that point, they stand, or the game ends
                # regardless, is_game_over will be true after this loop
                dealer_standing = False
                while(not dealer_standing):
                    dealer_standing = self.dealer_hit()
                    breakloop = self.is_game_over(dealer_standing)
                    if breakloop:
                        break

                # Breaks main loop if smaller loop broke from the game ending
                if breakloop:
                    break

            self.reset()

        # Prints a line after all rounds of blackjack have finished
        print()

    def anger_dealer(self, value, message=True):
        if(self.__dealer_happiness - value <= 0):
            self.__dealer_happiness = 0
        else:
            self.__dealer_happiness -= value
        if self.__player.has_item("Delight Indicator") and message == True:
            print("\n")
            type.fast("The Dealer has been angered!")
            print()
            self.delight_indicator()

    def calm_dealer(self, value, message=True):
        if(self.__dealer_happiness + value >= 100):
            self.__dealer_happiness = 100
        else:
            self.__dealer_happiness += value
        if self.__player.has_item("Delight Indicator") and message==True:
            print("\n")
            type.fast("The Dealer has calmed down!")
            print()
            self.delight_indicator()


    def dealer_status(self):
                # Dealer happiness effects
                self.__free_hand = False
                if self.__dealer_happiness == 100:
                    random_chance = random.randrange(3)
                    if random_chance == 0:
                        self.__bet = random.randrange(int(self.__balance/18), int(self.__balance/8))
                        type.slow(bright(yellow("The Dealer's in a good mood. Here's a ") + green("${:,}".format(self.__bet)) + yellow(" hand, on the house!")))
                        print("\n")
                        self.__free_hand = True
                elif self.__dealer_happiness > 95:
                    random_chance = random.randrange(10)
                    if random_chance == 0:
                        self.__bet = random.randrange(int(self.__balance/20), int(self.__balance/10))
                        type.slow(bright(yellow("The Dealer's in a good mood. Here's a ") + green("${:,}".format(self.__bet)) + yellow(" hand, on the house!")))
                        print("\n")
                        self.__free_hand = True
                elif self.__dealer_happiness > 90:
                    random_chance = random.randrange(10)
                    if random_chance == 0:
                        self.__bet = random.randrange(int(self.__balance/25), int(self.__balance/15))
                        type.slow(bright(yellow("The Dealer's in a good mood. Here's a ") + green("${:,}".format(self.__bet)) + yellow(" hand, on the house!")))
                        print("\n")
                        self.__free_hand = True

                # Dealer anger effects
                if self.__dealer_happiness > 30:
                    self.__dealer_warning = False

                if self.__dealer_happiness == 0:
                    random_chance = random.randrange(2)
                    if random_chance == 0:
                        type.slow(red(bright("The Dealer's had it with you. He gets up from his chair, and fires three shots into your chest. You bleed out, and as you fade from reality, you see the Dealer reach into your pockets, and take every last penny from your lifeless body.")))
                        self.__player.kill()
                    else:
                        type.slow(red(bright("The Dealer's had it with you. He points aggressively towards the door. Scared to question his authority, you scurry out. It seems you just dodged a bullet.")))
                        self.__player.add_danger("Angry Dealer")
                        print("\n")
                        return
                elif self.__dealer_happiness < 5:
                    random_chance = random.randrange(5)
                    if random_chance == 0:
                        type.slow(red(bright("The Dealer's had it with you. He gets up from his chair, and fires three shots into your chest. You bleed out, and as you fade from reality, you see the Dealer reach into your pockets, and take every last penny from your lifeless body.")))
                        self.__player.kill()
                    elif random_chance == 1:
                        type.slow(red(bright("The Dealer's had it with you. He points aggressively towards the door. Scared to question his authority, you scurry out. It seems you just dodged a bullet.")))
                        self.__player.add_danger("Angry Dealer")
                        print("\n")
                        return
                elif self.__dealer_happiness < 10:
                    random_chance = random.randrange(10)
                    if random_chance == 0:
                        type.slow(red(bright("The Dealer's had it with you. He gets up from his chair, and fires three shots into your chest. You bleed out, and as you fade from reality, you see the Dealer reach into your pockets, and take every last penny from your lifeless body.")))
                        self.__player.kill()
                    elif random_chance < 3:
                        type.slow(red(bright("The Dealer's had it with you. He points aggressively towards the door. Scared to question his authority, you scurry out. It seems you just dodged a bullet.")))
                        self.__player.add_danger("Angry Dealer")
                        print("\n")
                        return
                if self.__dealer_happiness < 20 and not self.__dealer_warning:
                    self.__dealer_warning = True
                    type.slow(red(bright("The Dealer is visibly pissed. Perhaps you've been getting too lucky.")))


    def delight_indicator(self):
        if self.__dealer_happiness > 66:
            type.fast("Dealer's current happiness: " + bright(green(str(self.__dealer_happiness) + "%")))
        elif self.__dealer_happiness > 33:
            type.fast("Dealer's current happiness: " + bright(yellow(str(self.__dealer_happiness) + "%")))
        else:
            type.fast("Dealer's current happiness: " + bright(green(str(self.__dealer_happiness) + "%")))
        self.__player.update_delight_indicator_durability()



    def set_min_bet(self, balance):
        balance_str = str(balance)
        balance_len = len(balance_str)
        if balance_len == 1:
            self.__min_bet = 1
        elif balance_len  == 2:
            self.__min_bet = int(balance_str[0])
        else:
            new_balance_str = balance_str[0] + balance_str[1]
            for _ in range(balance_len-3):
                new_balance_str += "0"
            self.__min_bet = int(new_balance_str)

    def bet(self):
        bet = None
        while bet is None:
            type.fast("The Dealer expects you to bet at least " + green(bright("${:,}".format(self.__min_bet))))
            print("")
            type.fast("How much would you like to bet? ")
            try:
                bet = int(input(""))
            except ValueError:
                print("")
                type.fast(red("The Dealer looks at you confused. Perhaps he didn't hear you."))
                print("\n")

        print("")

        if(self.__min_bet<=int(bet)<=self.__balance):
            self.__bet = bet
            return True
        elif((int(bet) < self.__min_bet)):
            if self.__dealer_happiness >= 30: type.slow(red("The Dealer doesn't like that bet."))
            elif self.__dealer_happiness >= 25: type.slow.type(red("The Dealer looks at you with an aggressive eye. Maybe try betting more cash!"))
            elif self.__dealer_happiness >= 20: type.slow(red("The Dealer is infuriated. You've insulted him. You should bet more cash."))
            elif self.__dealer_happiness >= 15: type.slow(red("The Dealer gets up from his chair and charges his relover. Bet more cash. You'll regret it if you don't."))
            elif self.__dealer_happiness >= 0: 
                type.slow(red(bright("THAT'S NOT ENOUGH MONEY. ")))
                type.slow(red("The Dealer fires three shots into your chest. You bleed out, and as you fade from reality, you see the Dealer reach into your pockets, and take every last penny from your lifeless body."))
                self.__player.kill()
            self.anger_dealer(5)
            print("\n")

        else:
            type.fast(red("The dealer looks at you confused. You don't have that much money."))
            print("\n")


    def first_deal(self):
        # Deal first card to Player
        card = self.draw(self.__hand)
        self.print_draw("Player", "first", card)
        print()

        # Deal first card to Dealer
        card = self.draw(self.__dealer_hand)
        self.print_draw("Dealer", "first", card)
        print("\n")

        # Saves dealer hand value, as it's the only card the player sees
        known_value = self.__dealer_hand.value()

        # Deal second card to Player
        card = self.draw(self.__hand)
        self.print_draw("Player", "second", card)
        print()

        # Deal second card to Dealer, which might be face down, if value<21
        card = self.draw(self.__dealer_hand)
        if(self.__dealer_hand.value()==21):
            self.print_draw("Dealer", "second", card)
        else:
            type.fast(red("The Dealer's second card is face down"))
            time.sleep(PAUSE)
        print("\n")

        # Prints Dealer's starting hand value. This is a special case (known value or 21 with a wink).
        if((self.__dealer_hand.value()!=21) & (known_value==1)):
            type.fast(red("As of now, the Dealer's hand has a known value of " + bright(str(1)) + ", or " + bright(str(11)) + ", since they have an ace"))
            time.sleep(PAUSE)
        elif(self.__dealer_hand.value()==21):
            type.fast(red("The Dealer's hand has a value of " + bright(str(21)) + " ;)"))
        else:
            type.fast(red("As of now, the Dealer's hand has a known value of " + bright(str(known_value))))

        print()

        # Prints player's starting hand value.
        type.fast(str(self.__hand))
        if len(self.__hand)>1:
            time.sleep(PAUSE)
        print()

    def hit_or_stand(self):
        if self.__player.has_item("Sneaky Peeky Glasses") and not self.__used_peak:
            type.fast("Would you like to hit, stand, or peek? ")
        else:
            type.fast("Would you like to hit or stand? ")
        hit_or_stand = input().lower()
        if((hit_or_stand=="h")or(hit_or_stand=="hit")):
            self.hit()
            return False
        elif ((hit_or_stand=="s")or(hit_or_stand=="stand")):
            self.__hand.get_final_value()
            print()
            type.fast("You decided to stand at a value of " + green(bright(str(self.__hand.value()))))
            return True
        elif self.__player.has_item("Sneaky Peeky Glasses") and not self.__used_peak and ((hit_or_stand=="p")or(hit_or_stand=="peek")):
            self.__used_peak = True
            next_card = self.__deck.peek()
            print()
            if (next_card.value()==1) or (next_card.value()==8):
                type.fast("Using your " + magenta(bright("Sneaky Peeky Glasses")) + ", you notice that the top card is an " + bright(magenta(str(next_card))))
            else:
                type.fast("Using your " + magenta(bright("Sneaky Peeky Glasses")) + ", you notice that the top card is a " + bright(magenta(str(next_card))))
            print("\n")
            self.__player.update_sneaky_peeky_glasses_durability()
        else:
            print()
            type.fast(red("I didn't quite catch that."))
            time.sleep(PAUSE)
            print("\n")

    def hit(self):
        # Hits a player's hand, then types their hand's value
        print()
        card = self.draw(self.__hand)
        self.print_draw("Player", "next", card)
        if len(self.__hand)>1:
            time.sleep(PAUSE)
        print()
        type.fast(str(self.__hand))
        print()

    def dealer_hit(self):
        # Checks if the dealer has a hand that can be hit (value less than 17)
        # if it can, the hand will be hit, and the value will be typed
        if(self.__dealer_hand.value()>=17):
            self.__dealer_hand.get_final_value()
            print()
            type.fast(red("The Dealer stands at " + bright(str(self.__dealer_hand.value()))))
            print()
            return True
        elif(self.__dealer_hand.possible_hands()==2):
            if(self.__dealer_hand.ace_value()>=17):
                self.__dealer_hand.get_final_value()
                print()
                type.fast(red("The Dealer stands at " + bright(str(self.__dealer_hand.value()))))
                print()
                return True
        print()
        if(len(self.__dealer_hand)>2):
            type.fast(red("The Dealer hits"))
            time.sleep(PAUSE)
        else:
            type.fast(red("The Dealer's hand has a value under 17 so they hit"))
            time.sleep(PAUSE)
        card = self.draw(self.__dealer_hand)
        print()
        self.print_draw("Dealer", "next", card)
        if len(self.__dealer_hand)>1:
            time.sleep(PAUSE)
        print()
        type.fast(str(self.__dealer_hand))
        print()
        return False

    def is_game_over(self, dealer_standing):
        # Checks if the game is over
        # If true, passes a string to end_round explaining the method of victory/defeat
        player_value = self.__hand.value()
        if(self.__hand.possible_hands==2):
            player_value = self.__hand.ace_value()

        dealer_value = self.__dealer_hand.value()
        if(self.__hand.possible_hands==2):
            dealer_value = self.__dealer_hand.ace_value()

        if(player_value>21):
            return self.end_round("Player Bust")
        elif(dealer_value>21):
            return self.end_round("Dealer Bust")
        elif(player_value==21)&(dealer_value==21):
            return self.end_round("Tie Blackjack")
        elif(player_value==21):
            return self.end_round("Player Blackjack")
        elif(dealer_value==21):
            return self.end_round("Dealer Blackjack")
        elif(player_value>dealer_value)&(dealer_standing):
            return self.end_round("Player Wins")
        elif(player_value==dealer_value)&(dealer_standing):
            return self.end_round("Tie")
        elif(player_value<dealer_value)&(dealer_standing):
            return self.end_round("Dealer Wins")
        else:
            return False
        
    def end_round(self, status):
        print()
        message = random.randrange(5)

        match status:
            case "Player Blackjack": 
                if message==0: type.fast(yellow(bright("You got a Blackjack! You Win! Yay!")))
                if message==1: type.fast(yellow(bright("Blackjack! What a moment! Mom, get the camera!")))
                if message==2: type.fast(yellow(bright("WOOOOOOO!!! Blackjack!!! WOOOOOOOO!!!")))
                if message==3: type.fast(yellow(bright("You hit Blackjack! What's cooking, good looking?")))
                if message==4: type.fast(yellow(bright("Oh lord have mercy, you got a Blackjack!")))
                print()
                if self.__free_hand:
                    type.fast(yellow(bright("You had " + green("${:,}".format(self.__balance)) + magenta(", and with a free bet of ") + green("${:,}".format(self.__bet)) + magenta(", you've tripled it!"))))
                else:
                    type.fast(yellow(bright("You had " + green("${:,}".format(self.__balance)) + magenta(", and with a bet of ") + green("${:,}".format(self.__bet)) + magenta(", you've tripled it!"))))
                print("\n")
                type.fast(yellow(bright("Your new balance is " + green("${:,}".format(self.__balance) + " + ${:,}".format(self.__bet*2) + " = ${:,}".format(self.__balance+self.__bet*2)))))
                self.__balance += 2*self.__bet

            case "Player Wins":
                if message==0: type.fast(magenta(bright("Congrats! You Win! Get REKT, Dealer!")))
                if message==1: type.fast(magenta(bright("You topple the Dealer! Are we witnessing a heist?")))
                if message==2: type.fast(magenta(bright("You outplayed the Dealer to victory! Nice moves.")))
                if message==3: type.fast(magenta(bright("You win...this time.")))
                if message==4: type.fast(magenta(bright("Winner winner chicken dinner! Must be tasty.")))
                print()
                if self.__free_hand:
                    type.fast(magenta(bright("You had " + green("${:,}".format(self.__balance)) + magenta(", and with a free bet of ") + green("${:,}".format(self.__bet)) + magenta(", you've doubled it!"))))
                else:
                    type.fast(magenta(bright("You had " + green("${:,}".format(self.__balance)) + magenta(", and with a bet of ") + green("${:,}".format(self.__bet)) + magenta(", you've doubled it!"))))
                print("\n")
                type.fast(magenta(bright("Your new balance is " + green("${:,}".format(self.__balance) + " + ${:,}".format(self.__bet) + " = ${:,}".format(self.__balance+self.__bet)))))
                self.__balance += self.__bet

            case "Dealer Bust":
                if message==0: type.fast(magenta(bright("The Dealer went over 21! Bust! You Win!")))
                if message==1: type.fast(magenta(bright("Dealer's hand busts! Victory is yours!")))
                if message==2: type.fast(magenta(bright("Dealer goes kaboom! Were they trying to bake a number cake?")))
                if message==3: type.fast(magenta(bright("Dealer hand goes bust! You're one lucky lucy.")))
                if message==4: type.fast(magenta(bright("The Dealer's over 21, which means you are the winner! Dope.")))
                print()
                if self.__free_hand:
                    type.fast(magenta(bright("You had " + green("${:,}".format(self.__balance)) + magenta(", and with a free bet of ") + green("${:,}".format(self.__bet)) + magenta(", you've doubled it!"))))
                else:
                    type.fast(magenta(bright("You had " + green("${:,}".format(self.__balance)) + magenta(", and with a bet of ") + green("${:,}".format(self.__bet)) + magenta(", you've doubled it!"))))
                print("\n")
                type.fast(magenta(bright("Your new balance is " + green("${:,}".format(self.__balance) + " + ${:,}".format(self.__bet) + " = ${:,}".format(self.__balance+self.__bet)))))
                self.__balance += self.__bet

            case "Dealer Blackjack":
                if message==0: type.fast(red(bright("The Dealer gets a Blackjack and wins! Too bad! So sad! Get good, kiddo!")))
                if message==1: type.fast(red(bright("Dealer secures Blackjack! Game over for you, loser!")))
                if message==2: type.fast(red(bright("Dealer's Blackjack! Well, butter my biscuit, what a surprise!")))
                if message==3: type.fast(red(bright("HAHA you suck buddy. Living infinite money glitch.")))
                if message==4: type.fast(red(bright("You just witnessed greatness. You only wish you were this good.")))
                print()
                if self.__free_hand:
                    type.fast(red(bright("You had " + green("${:,}".format(self.__balance)) + red(" and lost your free bet of ") + green("${:,}".format(self.__bet)))))
                    print("\n")
                    type.fast(red(bright("Your balance is still " + green("${:,}".format(self.__balance)))))
                else:
                    type.fast(red(bright("You had " + green("${:,}".format(self.__balance)) + red(" and lost your bet of ") + green("${:,}".format(self.__bet)))))
                    print("\n")
                    type.fast(red(bright("Your new balance is " + green("${:,}".format(self.__balance) + red(" - ${:,}".format(self.__bet)) + green(" = ${:,}".format(self.__balance-self.__bet))))))
                    self.__balance -= self.__bet

            case "Dealer Wins":
                if message==0: type.fast(red(bright("The Dealer wins! Too bad! So sad! Stay mad!")))
                if message==1: type.fast(red(bright("Dealer wins with the higher hand! Not your day, huh?")))
                if message==2: type.fast(red(bright("You simply got outplayed on this one.")))
                if message==3: type.fast(red(bright("Your hand is inferrior to the Dealer's. Which means you lose.")))
                if message==4: type.fast(red(bright("Dealer's number is higher, so I guess you lost. Unfortunate.")))
                print()
                if self.__free_hand:
                    type.fast(red(bright("You had " + green("${:,}".format(self.__balance)) + red(" and lost your free bet of ") + green("${:,}".format(self.__bet)))))
                    print("\n")
                    type.fast(red(bright("Your balance is still " + green("${:,}".format(self.__balance)))))
                else:
                    type.fast(red(bright("You had " + green("${:,}".format(self.__balance)) + red(" and lost your bet of ") + green("${:,}".format(self.__bet)))))
                    print("\n")
                    type.fast(red(bright("Your new balance is " + green("${:,}".format(self.__balance) + red(" - ${:,}".format(self.__bet)) + green(" = ${:,}".format(self.__balance-self.__bet))))))
                    self.__balance -= self.__bet

            case "Player Bust":
                if message==0: type.fast(red(bright("Bust! The Dealer wins! Too bad! So sad! You suuuuck!")))
                if message==1: type.fast(red(bright("Bust city! Did your cards get too excited?")))
                if message==2: type.fast(red(bright("Busted! Did you think this was a game of 'who can count the highest'?")))
                if message==3: type.fast(red(bright("Bust! Should've stopped while you were ahead.")))
                if message==4: type.fast(red(bright("You busted! How'd it feel?")))
                print()

                if self.__free_hand:
                    type.fast(red(bright("You had " + green("${:,}".format(self.__balance)) + red(" and lost your free bet of ") + green("${:,}".format(self.__bet)))))
                    print("\n")
                    type.fast(red(bright("Your balance is still " + green("${:,}".format(self.__balance)))))
                else:
                    type.fast(red(bright("You had " + green("${:,}".format(self.__balance)) + red(" and lost your bet of ") + green("${:,}".format(self.__bet)))))
                    print("\n")
                    type.fast(red(bright("Your new balance is " + green("${:,}".format(self.__balance) + red(" - ${:,}".format(self.__bet)) + green(" = ${:,}".format(self.__balance-self.__bet))))))
                    self.__balance -= self.__bet

            case "Tie":
                if message==0: type.fast(cyan(bright("You and the Dealer have the same value. It's a draw. So, so very lame.")))
                if message==1: type.fast(cyan(bright("Standoff! Equal hands, no winner!")))
                if message==2: type.fast(cyan(bright("Twinsies! You and the Dealer are matchy-matchy!")))
                if message==3: type.fast(cyan(bright("Welp. Those numbers are the same. So much for that round.")))
                if message==4: type.fast(cyan(bright("The lamest outcome possible, and yet here we are.")))
                print()
                if self.__free_hand:
                    type.fast(cyan(bright("You had " + green("${:,}".format(self.__balance)) + cyan(", and since this hand was free, your balance hasn't changed"))))
                else:
                    type.fast(cyan(bright("You had " + green("${:,}".format(self.__balance)) + cyan(", and you win back your bet of ") + green("${:,}".format(self.__bet)))))
                print("\n")
                type.fast(cyan(bright("Your balance is still " + green("${:,}".format(self.__balance)))))

            case "Tie Blackjack":
                if message==0: type.fast(cyan(bright("You and the Dealer both got a Blackjack. How boring.")))
                if message==1: type.fast(cyan(bright("Stalemate with matching Blackjacks! Who coulda guessed?")))
                if message==2: type.fast(cyan(bright("Double Blackjacks! What are the odds? (Don't answer that.)")))
                if message==3: type.fast(cyan(bright("It's a Blackjack draw! Did you both use your one-time miracle for this?")))
                if message==4: type.fast(cyan(bright("21 = 21. Sorry.")))
                print()
                if self.__free_hand:
                    type.fast(cyan(bright("You had " + green("${:,}".format(self.__balance)) + cyan(", and since this hand was free, your balance hasn't changed"))))
                else:
                    type.fast(cyan(bright("You had " + green("${:,}".format(self.__balance)) + cyan(", and you win back your bet of ") + green("${:,}".format(self.__bet)))))
                print("\n")
                type.fast(cyan(bright("Your balance is still " + green("${:,}".format(self.__balance)))))


        self.__player.set_balance(self.__balance)
        self.__player.status()
        self.end_round_dealer_happiness(status)

        print()
        return True

    def end_round_dealer_happiness(self, status):
        bet_ratio = self.__bet/self.__balance

        match status:
            case "Player Blackjack": 
                if bet_ratio >= 0.9:
                    self.anger_dealer(20)
                elif bet_ratio >= 0.6:
                    self.anger_dealer(10)
                elif bet_ratio >= 0.3:
                    self.anger_dealer(7)
                else:
                    self.anger_dealer(5)

            case "Player Wins":
                if bet_ratio >= 0.9:
                    self.anger_dealer(10)
                elif bet_ratio >= 0.6:
                    self.anger_dealer(7)
                elif bet_ratio >= 0.3:
                    self.anger_dealer(4)
                else:
                    self.anger_dealer(2)

            case "Dealer Bust":
                if bet_ratio >= 0.9:
                    self.anger_dealer(12)
                elif bet_ratio >= 0.6:
                    self.anger_dealer(8)
                elif bet_ratio >= 0.3:
                    self.anger_dealer(4)
                else:
                    self.anger_dealer(2)

            case "Dealer Blackjack":
                if bet_ratio >= 0.9:
                    self.calm_dealer(25)
                elif bet_ratio >= 0.6:
                    self.calm_dealer(15)
                elif bet_ratio >= 0.3:
                    self.calm_dealer(7)
                else:
                    self.calm_dealer(5)

            case "Dealer Wins":
                if bet_ratio >= 0.9:
                    self.calm_dealer(10)
                elif bet_ratio >= 0.6:
                    self.calm_dealer(6)
                elif bet_ratio >= 0.3:
                    self.calm_dealer(3)
                else:
                    self.calm_dealer(2)

            case "Player Bust":
                if bet_ratio >= 0.9:
                    self.calm_dealer(12)
                elif bet_ratio >= 0.6:
                    self.calm_dealer(7)
                elif bet_ratio >= 0.3:
                    self.calm_dealer(3)
                else:
                    self.calm_dealer(2)

            case "Tie":
                if bet_ratio >= 0.9:
                    self.anger_dealer(3)
                elif bet_ratio >= 0.6:
                    self.anger_dealer(2)
                elif bet_ratio >= 0.3:
                    self.anger_dealer(1)
                else:
                    self.anger_dealer(1)

            case "Tie Blackjack":
                if bet_ratio >= 0.9:
                    self.anger_dealer(4)
                elif bet_ratio >= 0.6:
                    self.anger_dealer(3)
                elif bet_ratio >= 0.3:
                    self.anger_dealer(1)
                else:
                    self.anger_dealer(1)


    def draw(self, hand):
        card = self.__deck.draw()
        hand.add(card)
        return card
    
    def print_draw(self, name, position, card):
        # Prints the drawn card, for either the player or dealer
        # Can specify first, second, or next card drawn (could be any word)
        if name == "Player":
            if((card.value()==1) or card.value()==8):
                type.fast("Your " + position + " card is an " + bright(magenta(str(card))))
            else:
                type.fast("Your " + position + " card is a " + bright(magenta(str(card))))

        elif name == "Dealer":
            if((card.value()==1) or card.value()==8):
                type.fast(red("The Dealer's " + position + " card is an " + bright(str(card))))
            else:
                type.fast(red("The Dealer's " + position + " card is a " + bright(str(card))))
    
    def reset(self):
        # Resets hands
        self.__hand = Hand("Player")
        self.__dealer_hand = Hand("Dealer")

    def hard_reset(self):
        # Resets hands, deck, and possibly anything else I can think of
        self.reset()
        self.__deck.reset()



class Hand:
    __slots__ = ["__cards", "__value", "__name"]

    def __init__(self, name):
        self.__name = name
        self.__cards = []
        self.__value = [0]

    def __repr__(self):
        # Prints for dealer's hand without an ace
        if ((len(self.__value)==1) & (self.__name == "Dealer")):
            hand_string = red(
                "The Dealer's hand has a value of " + bright(str(self.__value[0]))
                )
        
        # Prints for dealer's hand with an ace
        elif ((len(self.__value)==2) & (self.__name == "Dealer")):
            hand_string = red(
                "The Dealer's hand has a value of " + bright(str((self.__value[0]))) + 
                ", or " + bright(str(self.__value[1])) + " since they have an ace"
                )
            
        # Prints for player's hand without an ace
        elif ((len(self.__value)==1) & (self.__name == "Player")):
            hand_string = "Your hand has a value of " + green(bright(str(self.__value[0])))

        elif ((len(self.__value)==2) & (self.__name == "Player")):
            hand_string = ("Your hand has a value of " + green(bright(str(self.__value[0]))) + 
                           ", or " + green(bright(str(self.__value[1]))) + " since you have an ace")

        # for potential debugging purposes. 
        # This intentionally leaves room for additional players
        else:
            hand_string = "This player does not exist. How are you real?"

        return hand_string

    def __len__(self):
        return len(self.__cards)

    def add(self, card):
        # Adds cards to hand, then checks if aces affect the value

        self.__cards.append(card)
        self.__value[0] += card.value()
        if(len(self.__value)==2):
            self.__value[1] += card.value()

        # If the card is an ace, and there's no other aces in the hand
        # This only happens if the hand's value is less than 12, as a
        # hand that's value is 12 + 10 = 22, so the ace must be a 1
        if((card.value()==1) & (len(self.__value)==1) & (self.__value[0]<12)):
            self.__value.append(self.__value[0] + 10)

        # checks the value of the hand if an ace is 11
        # will pop the value if it's greater than 21
        # will set hand value to 21 if it's equal to 21
        if(len(self.__value)==2):
            if(self.__value[1] > 21):
                self.__value.pop()
            elif(self.__value[1] == 21):
                self.__value.pop()
                self.__value[0] = 21

    def value(self):
        return self.__value[0]
    
    def possible_hands(self):
        return len(self.__value)
    
    def get_final_value(self):
        if len(self.__value)==2:
            self.__value[0] = self.__value[1]
    
    def get_card(self, index):
        return self.__cards[index]
    
    def ace_value(self):
        if len(self.__value) == 2:
            return self.__value[1]
        else:
            return 0