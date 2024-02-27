import random
import deckOfCards
from colorama import Fore, Back, Style
import time
import random
import sys

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
        if (char == ".") or (char == "!") or (char == ":"):
            time.sleep(0.5)
            if char == ",":
                time.sleep(0.4)

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



class Blackjack:
    __slots__=["__balance", "__bet", "__min_bet", "__dealer_happiness", "__deck", "__hand", "__dealer_hand", "__player"]

    def __init__(self, player):
        self.__balance = 50
        self.__bet = 0
        self.__min_bet = 1
        self.__dealer_happiness = 50
        self.__deck = deckOfCards.Deck()
        self.__hand = Hand("Player")
        self.__dealer_hand = Hand("Dealer")
        self.__player = player

    def update_player(self, player):
        self.__balance = player.get_balance()

    def play_round(self, count):
        for _ in range(count):
            type("You have " + green(bright("$" + str(self.__balance))))
            print()
            while(True):
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

                type(str(self.__dealer_hand))
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

    def anger_dealer(self, value):
        if(self.__dealer_happiness - value <= 0):
            self.__dealer_happiness = 0
        else:
            self.__dealer_happiness -= value

    def dealer_calm_down(self, value):
        if(self.__dealer_happiness + value >= 100):
            self.__dealer_happiness = 100
        else:
            self.__dealer_happiness += value

    def bet(self):
        bet = None
        while bet is None:
            type("The Dealer expects you to bet at least " + green(bright("$" + str(self.__min_bet))))
            print("")
            type("How much would you like to bet? ")
            try:
                bet = int(input(""))
            except ValueError:
                print("")
                type(red("The Dealer looks at you confused. Perhaps he didn't hear you."))
                print("\n")

        print("")

        if(0<int(bet)<=self.__balance):
            self.__bet = bet
            return True
        elif((int(bet) < self.__min_bet)):
            if self.__dealer_happiness >= 30: type(red("The Dealer doesn't like that bet."))
            elif self.__dealer_happiness >= 25: slowtype(red("The Dealer looks at you with an aggressive eye. Maybe try betting more cash!"))
            elif self.__dealer_happiness >= 20: slowtype(red("The Dealer is infuriated. You've insulted him. You should bet more cash."))
            elif self.__dealer_happiness >= 15: slowtype(red("The Dealer gets up from his chair and charges his relover. Bet more cash. You'll regret it if you don't."))
            elif self.__dealer_happiness >= 0: 
                slowtype(red("The Dealer fires three shots into your chest. You bleed out, and as you fade from reality, you see the Dealer reach into your pockets, and take every last penny from your lifeless body."))
                self.__player.kill()
            self.anger_dealer(5)
            print("\n")

        else:
            type(red("The dealer looks at you confused. You don't have that much money."))
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
            type(red("The Dealer's second card is face down"))
        print("\n")

        # Prints Dealer's starting hand value. This is a special case (known value or 21 with a wink).
        if((self.__dealer_hand.value()!=21) & (known_value==1)):
            type(red("As of now, the Dealer's hand has a known value of " + bright(str(1)) + ", or " + bright(str(11)) + ", since they have an ace"))
        elif(self.__dealer_hand.value()==21):
            type(red("The Dealer's hand has a value of " + bright(str(21)) + " ;)"))
        else:
            type(red("As of now, the Dealer's hand has a known value of " + bright(str(known_value))))

        print()

        # Prints player's starting hand value.
        type(str(self.__hand))
        print()

    def hit_or_stand(self):
        type("Would you like to hit or stand? ")
        hit_or_stand = input().lower()
        if((hit_or_stand=="h")or(hit_or_stand=="hit")):
            self.hit()
            return False
        elif((hit_or_stand=="s")or(hit_or_stand=="stand")):
            self.__hand.get_final_value()
            print()
            type("You decided to stand at a value of " + green(bright(str(self.__hand.value()))))
            return True
        else:
            print()
            type(red("I didn't quite catch that."))
            print("\n")

    def hit(self):
        # Hits a player's hand, then types their hand's value
        print()
        card = self.draw(self.__hand)
        self.print_draw("Player", "next", card)
        print()
        type(str(self.__hand))
        print()

    def dealer_hit(self):
        # Checks if the dealer has a hand that can be hit (value less than 17)
        # if it can, the hand will be hit, and the value will be typed
        if(self.__dealer_hand.value()>=17):
            self.__dealer_hand.get_final_value()
            print()
            type(red("The Dealer stands at " + bright(str(self.__dealer_hand.value()))))
            print()
            return True
        elif(self.__dealer_hand.possible_hands()==2):
            if(self.__dealer_hand.ace_value()>=17):
                self.__dealer_hand.get_final_value()
                print()
                type(red("The Dealer stands at " + bright(str(self.__dealer_hand.value()))))
                print()
                return True
        print()
        if(len(self.__dealer_hand)>2):
            type(red("The Dealer hits"))
        else:
            type(red("The Dealer's hand has a value under 17 so they hit"))
        card = self.draw(self.__dealer_hand)
        print()
        self.print_draw("Dealer", "next", card)
        print()
        type(str(self.__dealer_hand))
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

        match status:
            case "Player Blackjack": 
                type(yellow(bright("You got a Blackjack! You Win! Yay!")))
                print()
                type(yellow(bright("You had " + green("$" + str(self.__balance)) + yellow(", and with a bet of ") + green("$" + str(self.__bet)) + yellow(", you've tripled it!"))))
                print("\n")
                type(yellow(bright("Your new balance is " + green("$" + str(self.__balance) + " + $" + str(self.__bet*2) + " = $" + str(self.__balance+(2*self.__bet))))))
                self.__balance += 2*self.__bet

            case "Player Wins":
                type(magenta(bright("Congrats! You Win! Get REKT, dealer!")))
                print()
                type(magenta(bright("You had " + green("$" + str(self.__balance)) + magenta(", and with a bet of ") + green("$" + str(self.__bet)) + magenta(", you've doubled it!"))))
                print("\n")
                type(magenta(bright("Your new balance is " + green("$" + str(self.__balance) + " + $" + str(self.__bet) + " = $" + str(self.__balance + self.__bet)))))
                self.__balance += self.__bet


            case "Dealer Bust":
                type(magenta(bright("The dealer went over 21! Bust! You Win!")))
                print()
                type(magenta(bright("You had " + green("$" + str(self.__balance)) + magenta(", and with a bet of ") + green("$" + str(self.__bet)) + magenta(", you've doubled it!"))))
                print("\n")
                type(magenta(bright("Your new balance is " + green("$" + str(self.__balance) + " + $" + str(self.__bet) + " = $" + str(self.__balance + self.__bet)))))
                self.__balance += self.__bet


            case "Dealer Blackjack":
                type(red(bright("The dealer gets a Blackjack and wins! Too bad! So sad! Get good, kiddo!")))
                print()
                type(red(bright("You had " + green("$" + str(self.__balance)) + red(" and lost your bet of ") + green("$" + str(self.__bet)))))
                print("\n")
                type(red(bright("Your new balance is " + green("$" + str(self.__balance) + red(" - $" + str(self.__bet)) + green(" = $" + str((self.__balance - self.__bet)))))))
                self.__balance -= self.__bet

            case "Dealer Wins":
                type(red(bright("The dealer wins! Too bad! So sad! Stay mad!")))
                print()
                type(red(bright("You had " + green("$" + str(self.__balance)) + red(" and lost your bet of ") + green("$" + str(self.__bet)))))
                print("\n")
                type(red(bright("Your new balance is " + green("$" + str(self.__balance) + red(" - $" + str(self.__bet)) + green(" = $" + str((self.__balance - self.__bet)))))))
                self.__balance -= self.__bet


            case "Player Bust":
                type(red(bright("Bust! The dealer wins! Too bad! So sad! You suuuuck!")))
                print()
                type(red(bright("You had " + green("$" + str(self.__balance)) + red(" and lost your bet of ") + green("$" + str(self.__bet)))))
                print("\n")
                type(red(bright("Your new balance is " + green("$" + str(self.__balance) + red(" - $" + str(self.__bet)) + green(" = $" + str((self.__balance - self.__bet)))))))
                self.__balance -= self.__bet

            case "Tie":
                type(cyan(bright("Since you and the dealer have the same value, it's a draw. So, so very lame.")))
                print()
                type(cyan(bright("You had " + green("$" + str(self.__balance)) + cyan(", and you win back your bet of ") + green("$" + str(self.__bet)))))
                print("\n")
                type(cyan(bright("Your balance is still " + green("$" + str(self.__balance)))))

            case "Tie Blackjack":
                type(cyan(bright("You and the dealer both got a Blackjack. How boring.")))
                print()
                type(cyan(bright("You had " + green("$" + str(self.__balance)) + cyan(", and you win back your bet of ") + green("$" + str(self.__bet)))))
                print("\n")
                type(cyan(bright("Your balance is still " + green("$" + str(self.__balance)))))

        self.__player.set_balance(self.__balance)
        self.__player.status()
        print()
        return True


    def draw(self, hand):
        card = self.__deck.draw()
        hand.add(card)
        return card
    
    def print_draw(self, name, position, card):
        # Prints the drawn card, for either the player or dealer
        # Can specify first, second, or next card drawn (could be any word)
        if name == "Player":
            if((card.value()==1) or card.value()==8):
                type("Your " + position + " card is an " + bright(magenta(str(card))))
            else:
                type("Your " + position + " card is a " + bright(magenta(str(card))))

        elif name == "Dealer":
            if((card.value()==1) or card.value()==8):
                type(red("The Dealer's " + position + " card is an " + bright(str(card))))
            else:
                type(red("The Dealer's " + position + " card is a " + bright(str(card))))
    
    def reset(self):
        # Resets hands
        self.__hand = Hand("Player")
        self.__dealer_hand = Hand("Dealer")

    def hard_reset(self):
        # Resets hands, deck, and possibly anything else I can think of
        self.reset()
        self.__deck = deckOfCards.Deck()



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