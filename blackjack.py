import random
import deck
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
        if (char == ".") or (char == "!"):
            time.sleep(0.7)
        if char == ",":
            time.sleep(0.4)

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
    __slots__=["__bet", "__deck", "__hand", "__dealer_hand", "__hand_value", "__dealer_hand_value"]

    def __init__(self, bet):
        self.__bet = bet
        self.__deck = deck.Deck()
        self.__hand = []
        self.__dealer_hand = []

    def play_round():
        pass

    def first_deal(self):
        type("Your first card is a ")

    def draw(self, hand):
        card = self.__deck.draw()
        hand.



class Hand:
    __slots__ = ["__cards", "__value", "__name"]

    def __init__(self, name):
        self.__name = name
        self.__cards = []
        self.__value = [0]

    def __repr__(self):
        # Prints for dealer's hand without an ace
        if (len(self)==1 & self.__name == "Dealer"):
            hand_string = red(
                "The dealer's cards have a value of " + bright(str(self.__value))
                )
        
        # Prints for dealer's hand with an ace
        elif (len(self)==2 & self.__name == "Dealer"):
            hand_string = red(
                "The dealer's cards have a value of " + bright(str((self.__value[0]))) + 
                ", or " + bright(str(self.__value[1])) + " since they have an ace"
                )
            
        # Prints for player's hand without an ace
        elif (len(self)==1 & self.__name == "Player"):
            hand_string = "Your cards have a value of ", green(bright(str(self.__value[0])))

        elif (len(self)==2 & self.__name == "Player"):
            hand_string = ("Your cards have a value of ", green(bright(str(self.__value[0]))) + 
                           ", or " + green(bright(str(self.__value[1]))) + " since you have an ace")

        # for potential debugging purposes. 
        # This intentionally leaves room for additional players
        else:
            hand_string = "This player does not exist. How are you real?"

        return hand_string

    def __len__(self):
        return len(self.__cards)

    def add(self, card):
        self.__cards.append(card)
        self.__value[0] += card.get_value()

        # If the card is an ace, and there's no other aces in the hand
        # This only happens if the hand's value is less than 11, as a
        # hand that's value is 11 + 11 = 22, so the ace must be 1
        if(card.get_value()==1 & len(self)==1 & self.__value<11):
            self.__value.append(self.__value[0] + 11)

        # checks the value of the hand if an ace is 11
        # will pop the value if it's greater than 21
        # will set hand value to 21 if it's equal to 21
        if(self.__value[1] > 21):
            self.__value.pop()
        elif(self.__value[1] == 21):
            self.__value.pop()
            self.__value[0] = 21

    def value(self):
        return self.__value[0]
    
    def ace_value(self):
        return self.__value[1]

def main():
    deck = Deck()
    while len(deck)>0:
        card = deck.draw()
        print(card)

if __name__ == "__main__":
    main()