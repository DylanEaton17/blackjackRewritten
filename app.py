from flask import Flask, render_template, jsonify, request, session
import os
import random
import deckOfCards

app = Flask(__name__)
app.secret_key = os.urandom(24)

class WebBlackjack:
    """Web-friendly Blackjack game without terminal dependencies"""
    
    def __init__(self):
        self.balance = 50
        self.bet = 0
        self.min_bet = 1
        self.deck = deckOfCards.Deck()
        self.player_hand = Hand("Player")
        self.dealer_hand = Hand("Dealer")
        self.game_phase = "betting"  # betting, playing, dealer_turn, game_over
        self.message = ""
        self.dealer_second_card_hidden = True
        
    def new_game(self):
        """Start a new game with fresh balance"""
        self.balance = 50
        self.bet = 0
        self.min_bet = 1
        self.deck.reset()
        self.player_hand = Hand("Player")
        self.dealer_hand = Hand("Dealer")
        self.game_phase = "betting"
        self.message = "Welcome! Place your bet to start."
        self.dealer_second_card_hidden = True
        
    def set_min_bet(self, balance):
        """Calculate minimum bet based on balance"""
        balance_str = str(balance)
        balance_len = len(balance_str)
        if balance_len == 1:
            self.min_bet = 1
        elif balance_len == 2:
            self.min_bet = int(balance_str[0])
        else:
            new_balance_str = balance_str[0] + balance_str[1]
            for _ in range(balance_len - 3):
                new_balance_str += "0"
            self.min_bet = int(new_balance_str)
    
    def place_bet(self, bet_amount):
        """Place a bet and validate it"""
        self.set_min_bet(self.balance)
        
        if bet_amount < self.min_bet:
            return False, f"Minimum bet is ${self.min_bet}"
        elif bet_amount > self.balance:
            return False, f"You don't have that much money. Balance: ${self.balance}"
        else:
            self.bet = bet_amount
            self.game_phase = "dealing"
            return True, f"Bet placed: ${bet_amount}"
    
    def deal_initial_cards(self):
        """Deal initial two cards to player and dealer"""
        # Reset hands
        self.player_hand = Hand("Player")
        self.dealer_hand = Hand("Dealer")
        
        # Deal cards
        self.player_hand.add(self.deck.draw())
        self.dealer_hand.add(self.deck.draw())
        self.player_hand.add(self.deck.draw())
        self.dealer_hand.add(self.deck.draw())
        
        self.dealer_second_card_hidden = True
        
        # Check for blackjacks
        player_value = self.player_hand.value()
        dealer_value = self.dealer_hand.value()
        
        if player_value == 21 and dealer_value == 21:
            self.dealer_second_card_hidden = False
            return self.end_round("Tie Blackjack")
        elif player_value == 21:
            self.dealer_second_card_hidden = False
            return self.end_round("Player Blackjack")
        elif dealer_value == 21:
            self.dealer_second_card_hidden = False
            return self.end_round("Dealer Blackjack")
        
        self.game_phase = "playing"
        self.message = "Your turn! Hit or Stand?"
        return {"status": "playing"}
    
    def hit(self):
        """Player hits - draw a card"""
        if self.game_phase != "playing":
            return {"error": "Cannot hit now"}
        
        card = self.deck.draw()
        self.player_hand.add(card)
        
        player_value = self.player_hand.value()
        
        if player_value > 21:
            return self.end_round("Player Bust")
        elif player_value == 21:
            return self.stand()
        
        self.message = f"You drew a card. Current value: {player_value}"
        return {"status": "playing"}
    
    def stand(self):
        """Player stands - dealer's turn"""
        if self.game_phase != "playing":
            return {"error": "Cannot stand now"}
        
        self.game_phase = "dealer_turn"
        self.dealer_second_card_hidden = False
        
        # Dealer draws until 17+
        while self.dealer_hand.value() < 17:
            card = self.deck.draw()
            self.dealer_hand.add(card)
        
        # Determine winner
        player_value = self.player_hand.value()
        dealer_value = self.dealer_hand.value()
        
        if dealer_value > 21:
            return self.end_round("Dealer Bust")
        elif player_value > dealer_value:
            return self.end_round("Player Wins")
        elif player_value == dealer_value:
            return self.end_round("Tie")
        else:
            return self.end_round("Dealer Wins")
    
    def end_round(self, outcome):
        """End the round and calculate winnings"""
        self.game_phase = "game_over"
        
        messages = {
            "Player Blackjack": "Blackjack! You win!",
            "Player Wins": "You win!",
            "Dealer Bust": "Dealer busts! You win!",
            "Dealer Blackjack": "Dealer has Blackjack. You lose.",
            "Dealer Wins": "Dealer wins.",
            "Player Bust": "Bust! You lose.",
            "Tie": "It's a tie!",
            "Tie Blackjack": "Both have Blackjack! It's a tie!"
        }
        
        old_balance = self.balance
        
        if outcome in ["Player Blackjack"]:
            # Blackjack pays 3:1 (bet + 2x bet)
            winnings = self.bet * 2
            self.balance += winnings
            self.message = f"{messages[outcome]} You won ${winnings}!"
        elif outcome in ["Player Wins", "Dealer Bust"]:
            # Regular win pays 2:1 (bet + 1x bet)
            winnings = self.bet
            self.balance += winnings
            self.message = f"{messages[outcome]} You won ${winnings}!"
        elif outcome in ["Dealer Blackjack", "Dealer Wins", "Player Bust"]:
            self.balance -= self.bet
            self.message = f"{messages[outcome]} You lost ${self.bet}."
        else:  # Tie
            self.message = f"{messages[outcome]} Your bet is returned."
        
        return {
            "status": "game_over",
            "outcome": outcome,
            "message": self.message,
            "old_balance": old_balance,
            "new_balance": self.balance
        }
    
    def get_state(self):
        """Get current game state as JSON"""
        return {
            "balance": self.balance,
            "bet": self.bet,
            "min_bet": self.min_bet,
            "game_phase": self.game_phase,
            "message": self.message,
            "player_hand": self.player_hand.to_dict(),
            "dealer_hand": self.dealer_hand.to_dict(hide_second=self.dealer_second_card_hidden),
        }
    
    def reset_for_new_round(self):
        """Reset for a new round while keeping balance"""
        self.bet = 0
        self.player_hand = Hand("Player")
        self.dealer_hand = Hand("Dealer")
        self.game_phase = "betting"
        self.message = "Place your bet for the next round."
        self.dealer_second_card_hidden = True


class Hand:
    """Simplified Hand class without terminal output"""
    
    def __init__(self, name):
        self.name = name
        self.cards = []
        self._value = [0]
    
    def add(self, card):
        """Add card to hand and update value"""
        self.cards.append(card)
        self._value[0] += card.value()
        if len(self._value) == 2:
            self._value[1] += card.value()
        
        # If the card is an ace and there's no other ace in hand
        if card.value() == 1 and len(self._value) == 1 and self._value[0] < 12:
            self._value.append(self._value[0] + 10)
        
        # Check ace value
        if len(self._value) == 2:
            if self._value[1] > 21:
                self._value.pop()
            elif self._value[1] == 21:
                self._value.pop()
                self._value[0] = 21
    
    def value(self):
        """Get hand value"""
        return self._value[0]
    
    def has_ace(self):
        """Check if hand has ace with alternate value"""
        return len(self._value) == 2
    
    def to_dict(self, hide_second=False):
        """Convert hand to dictionary for JSON"""
        cards_list = []
        for i, card in enumerate(self.cards):
            if hide_second and i == 1:
                cards_list.append({"name": "Hidden", "suit": "Hidden", "value": 0, "hidden": True})
            else:
                cards_list.append({
                    "name": str(card).split(" of ")[0],
                    "suit": str(card).split(" of ")[1],
                    "value": card.value(),
                    "hidden": False
                })
        
        return {
            "cards": cards_list,
            "value": self._value[0] if not hide_second else (self.cards[0].value() if self.cards else 0),
            "has_ace": len(self._value) == 2 and not hide_second
        }


# Store game instances per session
def get_game():
    """Get or create game instance for current session"""
    if 'game_id' not in session:
        session['game_id'] = os.urandom(16).hex()
    
    game_id = session['game_id']
    
    if not hasattr(app, 'games'):
        app.games = {}
    
    if game_id not in app.games:
        app.games[game_id] = WebBlackjack()
    
    return app.games[game_id]


@app.route('/')
def index():
    """Serve main game page"""
    return render_template('game.html')


@app.route('/api/new-game', methods=['POST'])
def new_game():
    """Start a new game"""
    game = get_game()
    game.new_game()
    return jsonify(game.get_state())


@app.route('/api/bet', methods=['POST'])
def place_bet():
    """Place a bet"""
    game = get_game()
    data = request.get_json()
    bet_amount = int(data.get('amount', 0))
    
    success, message = game.place_bet(bet_amount)
    
    if success:
        return jsonify({"success": True, "message": message, "state": game.get_state()})
    else:
        return jsonify({"success": False, "message": message, "state": game.get_state()})


@app.route('/api/deal', methods=['POST'])
def deal():
    """Deal initial cards"""
    game = get_game()
    result = game.deal_initial_cards()
    return jsonify({"result": result, "state": game.get_state()})


@app.route('/api/hit', methods=['POST'])
def hit():
    """Player hits"""
    game = get_game()
    result = game.hit()
    return jsonify({"result": result, "state": game.get_state()})


@app.route('/api/stand', methods=['POST'])
def stand():
    """Player stands"""
    game = get_game()
    result = game.stand()
    return jsonify({"result": result, "state": game.get_state()})


@app.route('/api/state', methods=['GET'])
def get_state():
    """Get current game state"""
    game = get_game()
    return jsonify(game.get_state())


@app.route('/api/new-round', methods=['POST'])
def new_round():
    """Start a new round (keep balance)"""
    game = get_game()
    game.reset_for_new_round()
    return jsonify(game.get_state())


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
