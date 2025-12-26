# blackjackRewritten

A Blackjack game implementation in Python, available in both terminal and web versions.

## Web Version (Recommended)

Play Blackjack in your browser with a clean, casino-themed interface!

### Requirements
- Python 3.7+
- Flask

### Installation & Running

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the web application:
```bash
python app.py
```

3. Open your browser and visit:
```
http://localhost:5000
```

### How to Play (Web Version)
1. You start with $50
2. Enter your bet amount (must meet minimum bet requirement)
3. Click "Place Bet & Deal" to start the round
4. Click "Hit" to draw another card, or "Stand" to end your turn
5. Dealer automatically plays after you stand
6. Blackjack pays 3:1, regular win pays 2:1
7. Click "New Round" to play again with your current balance
8. Click "New Game" to reset your balance to $50

## Terminal Version

The original terminal-based version with colorful output and additional features.

### Features
- Interactive terminal gameplay
- Colorful text output using colorama
- Betting system with minimum bets
- Dealer AI (hits until 17+)
- Proper Ace handling (1 or 11)

### Running
```bash
python blackjackMain.py
```
