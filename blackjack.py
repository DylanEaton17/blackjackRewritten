import random;

class Blackjack:
    __slots__=["__bet", "__deck", "__hand", "__dealer_hand", "__hand_value", "__dealer_hand_value"]

    def __init__(self, bet):
        self.__bet = bet
        self.__deck = Deck()
        self.__hand = []
        self.__dealer_hand = []
        self.__hand_value = [0]
        self.__dealer_hand_value = [0]

    def play_round():
        pass

    def hit(self):
        card = self.__deck.draw_card()
        value = value(card)


class Deck:
    __slots__ = ["__deck", "__current_card"]

    def __init__(self):
        self.__deck = self.reset()
        self.__current_card = None

    def __repr__(self):
        return str(self.__deck)

    def __len__(self):
        return len(self.__deck)

    def reset(self):
        # Both Initiates a shuffled deck of cards, and when called resets the deck back to full
        self.__deck = []
        for value in range(1, 14):
            for suit in range(4):
                # Suits
                if(suit==0):
                    suit = "Spades"
                elif(suit==1):
                    suit = "Hearts"
                elif(suit==2):
                    suit = "Clubs"
                elif(suit==3):
                    suit = "Diamonds"

                # Names
                if value == 1:
                    name = "Ace"
                elif value == 2:
                    name = "Two"
                elif value == 3:
                    name = "Three"
                elif value == 4:
                    name = "Four"
                elif value == 5:
                    name = "Five"
                elif value == 6:
                    name = "Six"
                elif value == 7:
                    name = "Seven"
                elif value == 8:
                    name = "Eight"
                elif value == 9:
                    name = "Nine"
                elif value == 10:
                    name = "Ten"
                elif value == 11:
                    name = "Jack"
                elif value == 12:
                    name = "Queen"
                elif value == 13:
                    name = "King"
                
                if value > 10:
                    value = 10

                self.__deck.append((Card(name, suit, value)))
        # Calls shuffle function, then returns the deck (for initalization)   
        self.shuffle_deck()
        return self.__deck

    def shuffle_deck(self):
        # Shuffles deck list
        random.shuffle(self.__deck)

    def draw_card(self):
        # Checks if deck has a card, then returns the top card
        if len(self.__deck) == 0:
            self.reset()
        self.__current_card = self.__deck.pop()
        return self.__current_card
    
class Card:
    __slots__ = ["__name", "__suit", "__value"]

    def __init__(self, name, suit, value):
        self.__name = name
        self.__suit = suit
        self.__value = value

    def __repr__(self):
        return(self.__name + " of " + self.__suit)

    def get_value(self):
        return self.__value

def main():
    deck = Deck()
    while len(deck)>0:
        card = deck.draw_card()
        print(card)

if __name__ == "__main__":
    main()