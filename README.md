# Blackjack Story Mode

A complete Blackjack game with integrated story mode, featuring roguelike mechanics, survival elements, and intense narrative. Available as a web application with standalone executable distribution.

## 🎮 Game Features

### Complete Story Integration
- **47 unique story events** across 6 wealth tiers (Poor → Nearly There)
- **Forced progression system** - Casino → End Day → Morning → Afternoon → Casino
- **NPC encounter system** - Meet mechanics, shopkeepers, and mysterious characters
- **Item system** with durability tracking (9 functional items)
- **7 shops** with event-based unlocking (Doctor, Witch, Repair Shops, Auto Shop, General Store)
- **Minimalist, creepy retro aesthetic** - Hidden game mechanics for mystery
- **Roguelike card gameplay** - 3 rounds per night (4 with Golden Watch)

### Authentic Blackjack
- Professional casino rules
- Proper Ace handling (1 or 11)
- Dealer AI (hits until 17+)
- Statistics tracking
- Minimum bet system

## 🚀 Quick Start

### Option 1: Standalone Executable (Easiest)

**For Windows users:**
1. Download the latest release from [Releases](../../releases)
2. Extract the ZIP file
3. Run `BlackjackStoryMode.exe`
4. Game opens in your browser automatically!

**For Linux/Mac users:**
1. Download and extract the release for your platform
2. Make executable: `chmod +x BlackjackStoryMode`
3. Run: `./BlackjackStoryMode`

### Option 2: Run from Source

**Requirements:**
- Python 3.8 or higher
- pip package manager

**Installation:**
```bash
# Clone the repository
git clone https://github.com/DylanEaton17/blackjackRewritten.git
cd blackjackRewritten

# Install dependencies
pip install -r requirements.txt

# Run the web application
python app.py
```

**Access the game:**
Open your browser to `http://localhost:5000`

## 🎯 How to Play

### Objective
Start with $50 and reach $1,000,000 through blackjack and survival decisions.

### Game Flow
1. **Casino Night** - Play 3 blackjack rounds (4 with Golden Watch)
2. **End of Day** - Review stats, balance, rank, inventory
3. **Morning** - Experience story events, meet NPCs
4. **Afternoon** - Visit shops or return to casino
5. **Repeat** - Continue the cycle until victory or defeat

### Story Progression
- **6 Wealth Tiers:** Poor ($1-$999) → Cheap ($1K-$9.9K) → Modest ($10K-$99.9K) → Rich ($100K-$499K) → Doughman ($500K-$899K) → Nearly There ($900K+)
- Different events unlock at each tier
- Shops unlock through story events and wealth progression

### Items & Shops

**Key Items:**
- 🌟 **Golden Watch** - Extra casino round per night
- 💓 **Health Indicator** - Reveals your health status
- 😊 **Delight Indicator** - Shows happiness levels  
- 🍶 **Flask of No Bust** - Prevents blackjack busts
- 🗺️ **Map** - Unlocks Marvin's shop

**Available Shops:**
- 🏥 **Doctor's Office** - Health treatments (always available)
- 🔮 **Witch's Hut** - Potions & flasks (Rank 1+)
- 🔧 **Tom's Repair** - Item repairs (after meeting Tom)
- 🛠️ **Frank's Fix-It** - Alternative repairs (after meeting Frank)
- 🚗 **Oswald's Auto** - Car services (after meeting Oswald)
- 🏪 **Marvin's Store** - General goods (requires Map item)

## 🏗️ Building Standalone Executable

### Windows
```bash
# Run automated build script
build.bat

# Or manual build
python -m pip install -r requirements.txt
python -m PyInstaller blackjack_web.spec
```

### Linux/Mac
```bash
# Run automated build script
./build.sh

# Or manual build
python3 -m pip install -r requirements.txt
python3 -m PyInstaller blackjack_web.spec
```

**Output:** Executable in `dist/` folder

**Detailed instructions:** See [BUILD_INSTRUCTIONS.md](BUILD_INSTRUCTIONS.md)

## 📁 Project Structure

```
blackjackRewritten/
├── app.py                  # Flask web server
├── web_story.py           # Story system backend (4,800+ lines)
├── deckOfCards.py         # Card deck implementation
├── templates/             # HTML templates
│   ├── intro.html        # Opening sequence
│   ├── game.html         # Casino interface
│   ├── end_day.html      # End of day screen
│   ├── start_day.html    # Morning events
│   ├── afternoon.html    # Shop selection
│   └── shop.html         # Individual shops
├── static/               # CSS and JavaScript
│   ├── css/style.css    # Minimalist dark theme
│   └── js/game.js       # Casino mechanics
├── blackjack_web.spec   # PyInstaller configuration
├── build.bat/.sh        # Build automation scripts
└── BUILD_INSTRUCTIONS.md # Detailed build guide
```

## 🎨 Design Philosophy

**Minimalist, Creepy, Eerie Retro Aesthetic**
- Hidden game mechanics (round counter invisible)
- Conditional information display (health shown only with item)
- Mystery through discovery
- Satisfying card roguelike gameplay
- Realistic intense storytelling with life-gambling stakes

## 🔧 Development

### Running in Development Mode
```bash
python app.py
```
Server runs on `http://localhost:5000` with debug mode.

### Terminal Version (Original)
```bash
python blackjackMain.py
```
The original command-line version with full story integration.

## 📝 Technical Details

- **Backend:** Flask 3.0.0, Python 3.8+
- **Frontend:** Vanilla JavaScript, CSS3
- **Packaging:** PyInstaller 6.0+
- **Story System:** 4,800+ lines, 47 events, 3 NPC encounters
- **Game Logic:** Forced progression, session-based state

## 🐛 Known Issues & Troubleshooting

**Browser doesn't open automatically:**
- Manually navigate to `http://127.0.0.1:5000/`

**Port 5000 already in use:**
- Close other applications using that port
- Or modify port in `app.py`

**Executable security warning:**
- Application is unsigned - this is expected
- Safe to run (local server only, no external connections)

## 🤝 Contributing

This project is complete and feature-locked. Feel free to fork for your own modifications.

## 📄 License

See repository license file.

## 🎮 Credits

- **Original Game:** DylanEaton17
- **Web Implementation:** GitHub Copilot
- **Framework:** Flask (Python)

## 🎯 Version

**Current Version:** 1.0.0  
**Release Date:** December 2025  
**Status:** Complete - All phases implemented

---

**Enjoy the thrill of high-stakes blackjack combined with survival storytelling!**
