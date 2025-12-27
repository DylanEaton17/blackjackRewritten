from flask import Flask, render_template, jsonify, request, session
import os
import random
import deckOfCards
from web_story import WebPlayer

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
        # Round tracking for forced progression
        self.rounds_played = 0
        self.max_rounds_per_night = 3  # Base limit, can be increased by Golden Watch
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
        self.rounds_played = 0
        self.max_rounds_per_night = 3
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
            "stats": self.stats,
            "rounds_played": self.rounds_played,
            "rounds_remaining": self.get_rounds_remaining(),
            "round_limit_reached": self.check_round_limit()
        }
    
    def reset_for_new_round(self):
        """Reset for a new round while keeping balance"""
        self.bet = 0
        self.player_hand = Hand("Player")
        self.dealer_hand = Hand("Dealer")
        self.game_phase = "betting"
        self.dealer_second_card_hidden = True
        
        # Increment rounds played
        self.rounds_played += 1
        
        # Check if max rounds reached
        if self.rounds_played >= self.max_rounds_per_night:
            self.message = f"You've played {self.rounds_played} rounds. Time to leave the casino..."
        else:
            rounds_left = self.max_rounds_per_night - self.rounds_played
            self.message = f"Place your bet for the next round. ({rounds_left} rounds remaining)"
    
    def check_round_limit(self):
        """Check if maximum rounds per night has been reached"""
        return self.rounds_played >= self.max_rounds_per_night
    
    def get_rounds_remaining(self):
        """Get number of rounds remaining"""
        return max(0, self.max_rounds_per_night - self.rounds_played)
    
    def set_max_rounds(self, has_golden_watch):
        """Set maximum rounds based on Golden Watch ownership"""
        self.max_rounds_per_night = 4 if has_golden_watch else 3


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
    """Direct route to casino - integrate with player state for round limits"""
    player = get_player()
    game = get_game()
    
    # Set max rounds based on Golden Watch ownership
    has_watch = player.has_item("Golden Watch")
    game.set_max_rounds(has_watch)
    
    # Sync balance from story mode
    if hasattr(player, 'balance'):
        game.balance = player.balance
    
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

def get_player():
    """Get or create player from session"""
    if 'player' not in session:
        # Get balance from blackjack game if it exists
        balance = 50
        if 'game' in session:
            game_data = session['game']
            balance = game_data.get('balance', 50)
        
        player = WebPlayer()
        player.balance = balance
        session['player'] = player.to_dict()
    else:
        player = WebPlayer.from_dict(session['player'])
    
    return player


def save_player(player):
    """Save player to session"""
    session['player'] = player.to_dict()


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
    player = get_player()
    return jsonify(player.to_dict())


@app.route('/api/story/opening', methods=['GET'])
def get_opening():
    """Get opening sequence"""
    player = get_player()
    result = player.opening_lines()
    save_player(player)
    return jsonify(result)


@app.route('/api/story/start-night', methods=['GET'])
def get_start_night():
    """Get start of night (casino) sequence"""
    player = get_player()
    result = player.start_night()
    save_player(player)
    return jsonify(result)


@app.route('/end-day')
def end_day_page():
    """End of day page"""
    return render_template('end_day.html')


@app.route('/start-day')
def start_day_page():
    """Start of day page"""
    return render_template('start_day.html')


@app.route('/afternoon')
def afternoon_page():
    """Afternoon page"""
    return render_template('afternoon.html')


@app.route('/shop/<shop_id>')
def shop_page(shop_id):
    """Individual shop interface"""
    player = get_player()
    
    # Get shop dialogue based on shop_id
    shop_data = None
    if shop_id == "doctor":
        shop_data = player.doctor_dialogue()
    elif shop_id == "witch":
        shop_data = player.witch_dialogue()
    elif shop_id == "tom":
        shop_data = player.tom_dialogue()
    elif shop_id == "frank":
        shop_data = player.frank_dialogue()
    elif shop_id == "oswald":
        shop_data = player.oswald_dialogue()
    elif shop_id == "marvin":
        shop_data = player.marvin_dialogue()
    
    if not shop_data:
        return render_template('afternoon.html')  # Redirect back if invalid shop
    
    return render_template('shop.html', shop_data=shop_data, shop_id=shop_id)


@app.route('/api/shop/purchase', methods=['POST'])
def shop_purchase():
    """Process shop purchase"""
    player = get_player()
    data = request.get_json()
    
    item = data.get('item')
    price = data.get('price')
    shop_id = data.get('shop_id')
    
    # Check if player can afford
    if player.balance < price:
        return jsonify({"success": False, "message": "Not enough money!"})
    
    # Process purchase based on shop and item
    success = False
    message = ""
    
    if shop_id == "doctor":
        if item == "cure_sickness":
            player.sick = False
            player.balance -= price
            success = True
            message = "You feel much better now."
        elif item == "heal_injuries":
            player.injured = False
            player.balance -= price
            success = True
            message = "Your injuries have been treated."
        elif item == "restore_health":
            player.health = 100
            player.balance -= price
            success = True
            message = "Your health has been fully restored."
    
    elif shop_id == "witch":
        if item == "no_bust_flask":
            player.inventory.append("Flask of No Bust")
            player.flask = 4
            player.balance -= price
            success = True
            message = "You acquired the mystical Flask of No Bust!"
        elif item == "healing_potion":
            player.health = min(100, player.health + 30)
            player.balance -= price
            success = True
            message = "The potion heals you for 30 HP."
    
    elif shop_id in ["tom", "frank"]:
        # Repair item
        if item in player.broken_inventory:
            player.broken_inventory.remove(item)
            player.inventory.append(item)
            player.balance -= price
            success = True
            message = f"{item} has been repaired!"
    
    elif shop_id == "oswald":
        if item == "oil_change":
            player.oil_change = True
            player.balance -= price
            success = True
            message = "Oil changed. Your car runs smoother."
        elif item == "tune_up":
            player.tune_up = True
            player.balance -= price
            success = True
            message = "Engine tuned up. Better performance!"
        elif item == "full_service":
            player.oil_change = True
            player.tune_up = True
            player.balance -= price
            success = True
            message = "Full service complete. Your car is in great shape!"
    
    elif shop_id == "marvin":
        # Add item to inventory
        player.inventory.append(item)
        player.balance -= price
        success = True
        message = f"Purchased {item}!"
    
    save_player(player)
    
    return jsonify({
        "success": success,
        "message": message,
        "balance": player.balance
    })


@app.route('/api/story/end-day', methods=['GET', 'POST'])
def api_end_day():
    """End of day sequence after casino"""
    player = get_player()
    
    # Get quote from WebLists
    from web_story import WebLists
    lists = WebLists()
    quote = lists.get_random_quote()
    
    result = {
        "success": True,
        "day": player.day,
        "balance": player.balance,
        "rank": player.get_rank_name(),
        "health": player.health,
        "quote": quote,
        "message": f"Day {player.day} complete. You ended with ${player.balance}."
    }
    
    # Increment day for next cycle
    player.day += 1
    save_player(player)
    
    return jsonify(result)


@app.route('/api/story/start-day', methods=['GET', 'POST'])
def api_start_day():
    """Morning/start of day phase"""
    player = get_player()
    
    # Trigger a day event
    event_result = player.trigger_event('day')
    
    result = {
        "success": True,
        "message": f"Day {player.day} begins...",
        "event": event_result if event_result else None
    }
    
    save_player(player)
    return jsonify(result)


@app.route('/api/story/afternoon', methods=['GET', 'POST'])
def api_afternoon():
    """Afternoon phase"""
    player = get_player()
    
    # Get available shops based on rank
    shops = []
    rank = player.get_rank()
    
    # Always available
    shops.append({"name": "Doctor", "id": "doctor", "locked": False})
    
    # Marvin only if player has the Map
    if player.has_item("Map"):
        shops.append({"name": "Marvin's Store", "id": "marvin", "locked": False})
    
    # Unlock based on rank
    if rank >= 1:
        shops.append({"name": "Witch", "id": "witch", "locked": False})
        shops.append({"name": "Tom's Repair", "id": "tom", "locked": False})
    else:
        shops.append({"name": "Witch", "id": "witch", "locked": True})
        shops.append({"name": "Tom's Repair", "id": "tom", "locked": True})
    
    if rank >= 2:
        shops.append({"name": "Frank's Fix-It", "id": "frank", "locked": False})
    else:
        shops.append({"name": "Frank's Fix-It", "id": "frank", "locked": True})
    
    if rank >= 3:
        shops.append({"name": "Oswald's Auto", "id": "oswald", "locked": False})
    else:
        shops.append({"name": "Oswald's Auto", "id": "oswald", "locked": True})
    
    result = {
        "success": True,
        "shops": shops
    }
    
    save_player(player)
    return jsonify(result)


@app.route('/api/story/event-choice', methods=['POST'])
def api_event_choice():
    """Handle player choice in an event"""
    player = get_player()
    data = request.get_json()
    choice = data.get('choice')
    
    # Process choice (simplified for now)
    result = {
        "success": True,
        "continue_to_afternoon": True
    }
    
    save_player(player)
    return jsonify(result)


@app.route('/api/story/sync-balance', methods=['POST'])
def sync_balance():
    """Sync balance between casino and story mode"""
    data = request.json
    balance = data.get('balance', 50)
    
    # Update player balance
    player = get_player()
    player.balance = balance
    save_player(player)
    
    return jsonify({"success": True, "balance": balance})


@app.route('/api/casino/check-end-night', methods=['GET'])
def check_end_night():
    """Check if casino session should end and redirect to end_day"""
    game = get_game()
    player = get_player()
    
    if game.check_round_limit():
        # Sync balance back to story mode
        player.balance = game.balance
        save_player(player)
        
        return jsonify({
            "should_end": True,
            "rounds_played": game.rounds_played,
            "final_balance": game.balance,
            "redirect_to": "/end-day"
        })
    else:
        return jsonify({
            "should_end": False,
            "rounds_remaining": game.get_rounds_remaining(),
            "rounds_played": game.rounds_played
        })


if __name__ == '__main__':
    # Development server - DO NOT use in production
    # For production, use a WSGI server like gunicorn:
    # gunicorn -w 4 -b 0.0.0.0:5000 app:app
    app.run(debug=True, host='0.0.0.0', port=5000)
