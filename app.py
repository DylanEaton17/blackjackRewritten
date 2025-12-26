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
        self.deck = deckOfCards.Deck()
        self.player_hand = Hand("Player")
        self.dealer_hand = Hand("Dealer")
        self.game_phase = "betting"  # betting, playing, dealer_turn, game_over
        self.message = ""
        self.dealer_second_card_hidden = True
        self.set_min_bet(self.balance)
        # Statistics tracking
        self.stats = {
            "hands_played": 0,
            "hands_won": 0,
            "hands_lost": 0,
            "hands_tied": 0,
            "blackjacks": 0,
            "busts": 0,
            "highest_balance": 50,
            "total_wagered": 0
        }
        
    def new_game(self):
        """Start a new game with fresh balance"""
        self.balance = 50
        self.bet = 0
        self.deck.reset()
        self.player_hand = Hand("Player")
        self.dealer_hand = Hand("Dealer")
        self.game_phase = "betting"
        self.message = "Welcome! Place your bet to start."
        self.dealer_second_card_hidden = True
        self.set_min_bet(self.balance)
        # Reset statistics
        self.stats = {
            "hands_played": 0,
            "hands_won": 0,
            "hands_lost": 0,
            "hands_tied": 0,
            "blackjacks": 0,
            "busts": 0,
            "highest_balance": 50,
            "total_wagered": 0
        }
        
    def set_min_bet(self, balance):
        """Calculate minimum bet based on balance (10% rounded down, min $1)"""
        self.min_bet = max(1, balance // 10)
    
    def place_bet(self, bet_amount):
        """Place a bet and validate it"""
        self.set_min_bet(self.balance)
        
        if bet_amount < self.min_bet:
            return False, f"Minimum bet is ${self.min_bet}"
        elif bet_amount > self.balance:
            return False, f"You don't have that much money. Balance: ${self.balance}"
        else:
            self.bet = bet_amount
            self.stats["total_wagered"] += bet_amount
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
    
    def get_dealer_message(self, outcome):
        """Get a random dealer message based on outcome"""
        win_messages = [
            "Nice hand! You got me this time.",
            "Well played. Enjoy your winnings.",
            "Lucky draw! Don't get too comfortable.",
            "Impressive. The cards were in your favor.",
            "You win this round. Congratulations."
        ]
        
        lose_messages = [
            "Better luck next time!",
            "The house always wins... eventually.",
            "Tough break. Want to try again?",
            "Not your lucky day, friend.",
            "Maybe next round will be better."
        ]
        
        tie_messages = [
            "A push. Nobody wins, nobody loses.",
            "Same value. It's a standoff.",
            "Looks like we're even this time.",
            "A tie. Your bet stays with you.",
            "Well, that was anticlimactic."
        ]
        
        blackjack_messages = [
            "BLACKJACK! What a hand!",
            "Twenty-one! Nicely done!",
            "Blackjack! The perfect hand.",
            "Natural 21! You're on fire!",
            "Blackjack! That's what I'm talking about!"
        ]
        
        if "Player Blackjack" in outcome:
            return random.choice(blackjack_messages)
        elif outcome in ["Player Wins", "Dealer Bust"]:
            return random.choice(win_messages)
        elif outcome in ["Dealer Wins", "Dealer Blackjack", "Player Bust"]:
            return random.choice(lose_messages)
        else:
            return random.choice(tie_messages)
    
    def end_round(self, outcome):
        """End the round and calculate winnings"""
        self.game_phase = "game_over"
        self.stats["hands_played"] += 1
        
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
        dealer_msg = self.get_dealer_message(outcome)
        
        if outcome in ["Player Blackjack"]:
            # Blackjack pays 3:1 (bet + 2x bet)
            winnings = self.bet * 2
            self.balance += winnings
            self.message = f"{messages[outcome]} You won ${winnings}!"
            self.stats["hands_won"] += 1
            self.stats["blackjacks"] += 1
        elif outcome in ["Player Wins", "Dealer Bust"]:
            # Regular win pays 2:1 (bet + 1x bet)
            winnings = self.bet
            self.balance += winnings
            self.message = f"{messages[outcome]} You won ${winnings}!"
            self.stats["hands_won"] += 1
        elif outcome in ["Dealer Blackjack", "Dealer Wins", "Player Bust"]:
            self.balance -= self.bet
            self.message = f"{messages[outcome]} You lost ${self.bet}."
            self.stats["hands_lost"] += 1
            if "Player Bust" in outcome:
                self.stats["busts"] += 1
        else:  # Tie
            self.message = f"{messages[outcome]} Your bet is returned."
            self.stats["hands_tied"] += 1
        
        # Track highest balance
        if self.balance > self.stats["highest_balance"]:
            self.stats["highest_balance"] = self.balance
        
        return {
            "status": "game_over",
            "outcome": outcome,
            "message": self.message,
            "dealer_message": dealer_msg,
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
            "stats": self.stats
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
                card_str = str(card)
                # Safely parse card string (format: "Name of Suit")
                if " of " in card_str:
                    parts = card_str.split(" of ", 1)
                    name = parts[0]
                    suit = parts[1]
                else:
                    # Fallback if format is unexpected
                    name = "Unknown"
                    suit = "Unknown"
                
                cards_list.append({
                    "name": name,
                    "suit": suit,
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
    """Serve main game page (casino)"""
    return render_template('game.html')


@app.route('/casino')
def casino():
    """Direct route to casino"""
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
    
    try:
        bet_amount = int(data.get('amount', 0))
    except (ValueError, TypeError):
        return jsonify({"success": False, "message": "Invalid bet amount", "state": game.get_state()})
    
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


# ===== Story Mode =====

class StoryGame:
    """Story mode game state"""
    
    def __init__(self, balance=50):
        self.balance = balance
        self.day = 1
        self.time_of_day = "Morning"
        self.health = 100
        self.max_health = 100
        self.inventory = []
        self.conditions = []
        self.location = "outside_casino"
        
    def get_state(self):
        """Get current story state"""
        return {
            "balance": self.balance,
            "day": self.day,
            "timeOfDay": self.time_of_day,
            "health": self.health,
            "maxHealth": self.max_health,
            "inventory": self.inventory,
            "conditions": self.conditions,
            "location": self.location
        }
    
    def explore(self):
        """Player explores the area"""
        events = [
            {
                "title": "Desert Exploration",
                "text": [
                    "You walk around the parking lot, kicking up dust.",
                    "The desert stretches endlessly in all directions.",
                    "You find a crumpled $5 bill under a car!"
                ]
            },
            {
                "title": "Mysterious Stranger",
                "text": [
                    "An old man approaches you.",
                    '"Good luck in there," he says with a knowing smile.',
                    '"You\'re going to need it."'
                ]
            },
            {
                "title": "Hot Day",
                "text": [
                    "The sun beats down relentlessly.",
                    "You feel your throat getting dry.",
                    "Maybe you should head inside soon."
                ]
            }
        ]
        
        event = random.choice(events)
        
        # Random chance to find money
        if random.random() < 0.3:
            found_money = random.choice([1, 5, 10])
            self.balance += found_money
            event["text"].append(f"You found ${found_money}!")
        
        return {
            "title": event["title"],
            "text": event["text"],
            "state": self.get_state()
        }
    
    def rest(self):
        """Player rests"""
        heal_amount = random.randint(5, 15)
        self.health = min(self.max_health, self.health + heal_amount)
        
        # Advance time
        if self.time_of_day == "Morning":
            self.time_of_day = "Afternoon"
        elif self.time_of_day == "Afternoon":
            self.time_of_day = "Evening"
        elif self.time_of_day == "Evening":
            self.time_of_day = "Night"
        else:
            self.time_of_day = "Morning"
            self.day += 1
        
        return {
            "title": "Rest",
            "text": [
                "You find a shady spot and rest for a while.",
                f"You recover {heal_amount} health.",
                f"Time passes... It's now {self.time_of_day}."
            ],
            "state": self.get_state()
        }
    
    def add_item(self, name, description=""):
        """Add item to inventory"""
        self.inventory.append({"name": name, "description": description})


def get_story_game():
    """Get or create story game from session"""
    if 'story_game' not in session:
        # Get balance from blackjack game if it exists
        balance = 50
        if 'game' in session:
            game_data = session['game']
            balance = game_data.get('balance', 50)
        
        story = StoryGame(balance)
        session['story_game'] = story.__dict__
    else:
        story = StoryGame()
        story.__dict__.update(session['story_game'])
    
    return story


@app.route('/intro')
def intro():
    """Intro/welcome page"""
    return render_template('intro.html')


@app.route('/story')
def story():
    """Story mode page"""
    return render_template('story.html')


@app.route('/api/story/state', methods=['GET'])
def get_story_state():
    """Get current story state"""
    story = get_story_game()
    return jsonify(story.get_state())


@app.route('/api/story/explore', methods=['POST'])
def story_explore():
    """Explore the area"""
    story = get_story_game()
    result = story.explore()
    session['story_game'] = story.__dict__
    return jsonify(result)


@app.route('/api/story/rest', methods=['POST'])
def story_rest():
    """Rest to recover health"""
    story = get_story_game()
    result = story.rest()
    session['story_game'] = story.__dict__
    return jsonify(result)


@app.route('/api/story/sync-balance', methods=['POST'])
def sync_balance():
    """Sync balance between casino and story mode"""
    data = request.json
    balance = data.get('balance', 50)
    
    # Update story game balance
    story = get_story_game()
    story.balance = balance
    session['story_game'] = story.__dict__
    
    return jsonify({"success": True, "balance": balance})


if __name__ == '__main__':
    # Development server - DO NOT use in production
    # For production, use a WSGI server like gunicorn:
    # gunicorn -w 4 -b 0.0.0.0:5000 app:app
    app.run(debug=True, host='0.0.0.0', port=5000)
