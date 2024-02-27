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
    __slots__=["__deck", "__hand", "__dealer_hand"]

    def __init__(self):
        self.__deck = deckOfCards.Deck()
        self.__hand = Hand("Player")
        self.__dealer_hand = Hand("Dealer")

    def play_round(self, count):
        for _ in range(count):
            self.first_deal()

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

        # Deal second card to Dealer
        card = self.draw(self.__dealer_hand)
        if(self.__dealer_hand==21):
            self.print_draw("Dealer", "second", card)
        else:
            type(red("The dealer's second card is face down"))
        print("\n")

        type(red("As of now, the dealer's cards have a known value of " + bright(str(known_value))))

        print()

        type(str(self.__hand))

        print()

        hit_or_stand()

        self.reset()
        

    def hit_or_stand(self):
        while(True):
            type("Would you like to hit or stand?")
            hit_or_stand = input().lower()
            if((hit_or_stand=="h")or(hit_or_stand=="hit")):
                self.hit()
            elif((hit_or_stand=="s")or(hit_or_stand=="stand")):
                self.stand()
            else:
               print("\n")
               type(red("I didn't quite catch that."))
               print("\n")

    def status(self):
        player_value = self.__hand.value()
        dealer_value = self.__dealer_hand.value()
        if(player_value>21):
            self.end_round("Player Bust")
        elif()

    def end_round(self, status):


    def hit(self):
        pass

    def stand(self):
        pass

    def draw(self, hand):
        card = self.__deck.draw()
        hand.add(card)
        return card
    
    def print_draw(self, name, position, card):
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
        self.__hand = Hand("Player")
        self.__dealer_hand = Hand("Dealer")





class Hand:
    __slots__ = ["__cards", "__value", "__name"]

    def __init__(self, name):
        self.__name = name
        self.__cards = []
        self.__value = [0]

    def __repr__(self):
        # Prints for dealer's hand without an ace
        if ((len(self)==1) & (self.__name == "Dealer")):
            hand_string = red(
                "The dealer's cards have a value of " + bright(str(self.__value[0]))
                )
        
        # Prints for dealer's hand with an ace
        elif ((len(self)==2) & (self.__name == "Dealer")):
            hand_string = red(
                "The dealer's cards have a value of " + bright(str((self.__value[0]))) + 
                ", or " + bright(str(self.__value[1])) + " since they have an ace"
                )
            
        # Prints for player's hand without an ace
        elif ((len(self)==1) & (self.__name == "Player")):
            hand_string = "Your cards have a value of " + green(bright(str(self.__value[0])))

        elif ((len(self)==2) & (self.__name == "Player")):
            hand_string = ("Your cards have a value of " + green(bright(str(self.__value[0]))) + 
                           ", or " + green(bright(str(self.__value[1]))) + " since you have an ace")

        # for potential debugging purposes. 
        # This intentionally leaves room for additional players
        else:
            hand_string = "This player does not exist. How are you real?"

        return hand_string

    def __len__(self):
        return len(self.__value)

    def add(self, card):
        # Adds cards to hand, then checks if aces affect the value

        self.__cards.append(card)
        self.__value[0] += card.value()

        # If the card is an ace, and there's no other aces in the hand
        # This only happens if the hand's value is less than 12, as a
        # hand that's value is 12 + 10 = 22, so the ace must be a 1
        if((card.value()==1) & (len(self)==1) & (self.__value[0]<12)):
            self.__value.append(self.__value[0] + 10)

        # checks the value of the hand if an ace is 11
        # will pop the value if it's greater than 21
        # will set hand value to 21 if it's equal to 21
        if(len(self)==2):
            if(self.__value[1] > 21):
                self.__value.pop()
            elif(self.__value[1] == 21):
                self.__value.pop()
                self.__value[0] = 21

    def value(self):
        return self.__value[0]
    
    def ace_value(self):
        if len(self.__value) == 2:
            return self.__value[1]
        else:
            return 0
    

def main():
    blackjackGame = Blackjack()
    blackjackGame.play_round(2)

if __name__ == "__main__":
    main()