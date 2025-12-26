// Game state
let currentState = null;

// DOM Elements
const balanceEl = document.getElementById('balance');
const currentBetEl = document.getElementById('current-bet');
const messageEl = document.getElementById('message');
const dealerCardsEl = document.getElementById('dealer-cards');
const playerCardsEl = document.getElementById('player-cards');
const dealerValueEl = document.getElementById('dealer-value');
const playerValueEl = document.getElementById('player-value');
const dealerMessageEl = document.getElementById('dealer-message');

const bettingSection = document.getElementById('betting-section');
const actionButtons = document.getElementById('action-buttons');
const newRoundSection = document.getElementById('new-round-section');

const betAmountInput = document.getElementById('bet-amount');
const minBetInfo = document.getElementById('min-bet-info');
const dealBtn = document.getElementById('deal-btn');
const hitBtn = document.getElementById('hit-btn');
const standBtn = document.getElementById('stand-btn');
const newRoundBtn = document.getElementById('new-round-btn');
const newGameBtn = document.getElementById('new-game-btn');
const leaveCasinoBtn = document.getElementById('leave-casino-btn');

// Stats elements
const statsToggle = document.getElementById('stats-toggle');
const statsContent = document.getElementById('stats-content');

// Suit symbols
const suitSymbols = {
    'Hearts': '♥',
    'Diamonds': '♦',
    'Spades': '♠',
    'Clubs': '♣'
};

// Initialize game on load
document.addEventListener('DOMContentLoaded', () => {
    loadGameState();
    
    // Event listeners
    dealBtn.addEventListener('click', handleDeal);
    hitBtn.addEventListener('click', handleHit);
    standBtn.addEventListener('click', handleStand);
    newRoundBtn.addEventListener('click', handleNewRound);
    newGameBtn.addEventListener('click', handleNewGame);
    leaveCasinoBtn.addEventListener('click', handleLeaveCasino);
    
    // Stats toggle
    statsToggle.addEventListener('click', () => {
        if (statsContent.style.display === 'none') {
            statsContent.style.display = 'block';
            statsToggle.textContent = '📊 Stats ▼';
        } else {
            statsContent.style.display = 'none';
            statsToggle.textContent = '📊 Stats';
        }
    });
    
    // Quick bet buttons
    document.querySelectorAll('.btn-chip').forEach(btn => {
        btn.addEventListener('click', () => {
            const amount = btn.dataset.amount;
            if (amount === 'min') {
                betAmountInput.value = currentState ? currentState.min_bet : 1;
            } else if (amount === 'max') {
                betAmountInput.value = currentState ? currentState.balance : 50;
            } else {
                betAmountInput.value = amount;
            }
        });
    });
});

// Load current game state
async function loadGameState() {
    try {
        const response = await fetch('/api/state');
        if (!response.ok) {
            throw new Error('Failed to load game state');
        }
        const state = await response.json();
        updateUI(state);
    } catch (error) {
        console.error('Error loading game state:', error);
        showMessage('Error loading game. Please refresh the page.', 'lose');
    }
}

// Handle New Game
async function handleNewGame() {
    try {
        const response = await fetch('/api/new-game', { method: 'POST' });
        if (!response.ok) {
            throw new Error('Failed to start new game');
        }
        const state = await response.json();
        updateUI(state);
        showMessage('New game started! Place your bet.', '');
    } catch (error) {
        console.error('Error starting new game:', error);
        showMessage('Error starting new game.', 'lose');
    }
}

// Handle Deal (Place Bet & Deal Cards)
async function handleDeal() {
    const betAmount = parseInt(betAmountInput.value, 10);
    
    if (!betAmount || betAmount < 1) {
        showMessage('Please enter a valid bet amount.', 'lose');
        return;
    }
    
    try {
        // Place bet
        const betResponse = await fetch('/api/bet', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ amount: betAmount })
        });
        
        if (!betResponse.ok) {
            throw new Error('Failed to place bet');
        }
        
        const betResult = await betResponse.json();
        
        if (!betResult.success) {
            showMessage(betResult.message, 'lose');
            updateUI(betResult.state);
            return;
        }
        
        // Deal cards
        const dealResponse = await fetch('/api/deal', { method: 'POST' });
        
        if (!dealResponse.ok) {
            throw new Error('Failed to deal cards');
        }
        
        const dealResult = await dealResponse.json();
        
        updateUI(dealResult.state);
        
        // Check if game ended immediately (blackjack)
        if (dealResult.state.game_phase === 'game_over') {
            handleGameOver(dealResult.result);
        } else {
            showMessage(dealResult.state.message, '');
        }
        
    } catch (error) {
        console.error('Error dealing cards:', error);
        showMessage('Error dealing cards.', 'lose');
    }
}

// Handle Hit
async function handleHit() {
    try {
        const response = await fetch('/api/hit', { method: 'POST' });
        if (!response.ok) {
            throw new Error('Failed to hit');
        }
        const result = await response.json();
        
        updateUI(result.state);
        
        if (result.state.game_phase === 'game_over') {
            handleGameOver(result.result);
        } else {
            showMessage(result.state.message, '');
        }
        
    } catch (error) {
        console.error('Error hitting:', error);
        showMessage('Error hitting.', 'lose');
    }
}

// Handle Stand
async function handleStand() {
    try {
        const response = await fetch('/api/stand', { method: 'POST' });
        if (!response.ok) {
            throw new Error('Failed to stand');
        }
        const result = await response.json();
        
        updateUI(result.state);
        handleGameOver(result.result);
        
    } catch (error) {
        console.error('Error standing:', error);
        showMessage('Error standing.', 'lose');
    }
}

// Handle New Round
async function handleNewRound() {
    try {
        const response = await fetch('/api/new-round', { method: 'POST' });
        if (!response.ok) {
            throw new Error('Failed to start new round');
        }
        const state = await response.json();
        updateUI(state);
        showMessage('Place your bet for the next round.', '');
        // Clear dealer message
        if (dealerMessageEl) {
            dealerMessageEl.textContent = '';
        }
    } catch (error) {
        console.error('Error starting new round:', error);
        showMessage('Error starting new round.', 'lose');
    }
}

// Handle Game Over
function handleGameOver(result) {
    const outcome = result.outcome;
    const message = result.message;
    const dealerMessage = result.dealer_message;
    
    // Show dealer message
    if (dealerMessage && dealerMessageEl) {
        dealerMessageEl.textContent = dealerMessage;
        dealerMessageEl.style.opacity = '0';
        setTimeout(() => {
            dealerMessageEl.style.transition = 'opacity 0.5s';
            dealerMessageEl.style.opacity = '1';
        }, 500);
    }
    
    // Determine message type based on outcome
    const winOutcomes = ['Player Blackjack', 'Player Wins', 'Dealer Bust'];
    const tieOutcomes = ['Tie', 'Tie Blackjack'];
    const loseOutcomes = ['Dealer Blackjack', 'Dealer Wins', 'Player Bust'];
    
    if (winOutcomes.includes(outcome)) {
        showMessage(message, 'win');
    } else if (tieOutcomes.includes(outcome)) {
        showMessage(message, 'tie');
    } else if (loseOutcomes.includes(outcome)) {
        showMessage(message, 'lose');
    } else {
        showMessage(message, '');
    }
}

// Update Statistics Display
function updateStats(stats) {
    if (!stats) return;
    
    document.getElementById('stat-hands-played').textContent = stats.hands_played;
    document.getElementById('stat-wins').textContent = stats.hands_won;
    document.getElementById('stat-losses').textContent = stats.hands_lost;
    document.getElementById('stat-ties').textContent = stats.hands_tied;
    document.getElementById('stat-blackjacks').textContent = stats.blackjacks;
    document.getElementById('stat-highest').textContent = `$${stats.highest_balance}`;
    
    // Calculate win rate
    const winRate = stats.hands_played > 0 
        ? Math.round((stats.hands_won / stats.hands_played) * 100) 
        : 0;
    document.getElementById('stat-win-rate').textContent = `${winRate}%`;
}

// Update UI with game state
function updateUI(state) {
    currentState = state;
    
    // Update balance and bet
    balanceEl.textContent = `$${state.balance}`;
    currentBetEl.textContent = `$${state.bet}`;
    minBetInfo.textContent = `Min: $${state.min_bet}`;
    betAmountInput.min = state.min_bet;
    
    // Update statistics
    if (state.stats) {
        updateStats(state.stats);
    }
    
    // Update hands
    displayHand(dealerCardsEl, state.dealer_hand);
    displayHand(playerCardsEl, state.player_hand);
    
    // Update hand values
    dealerValueEl.textContent = `Value: ${state.dealer_hand.value}`;
    playerValueEl.textContent = `Value: ${state.player_hand.value}`;
    
    if (state.player_hand.has_ace) {
        playerValueEl.textContent += ' (Soft Hand)';
    }
    
    // Update UI sections based on game phase
    updateButtonStates(state.game_phase);
}

// Display hand of cards
function displayHand(container, hand) {
    container.innerHTML = '';
    
    if (!hand || !hand.cards || hand.cards.length === 0) {
        return;
    }
    
    hand.cards.forEach(card => {
        const cardEl = createCardElement(card);
        container.appendChild(cardEl);
    });
}

// Create card element
function createCardElement(card) {
    const cardDiv = document.createElement('div');
    cardDiv.className = 'card';
    
    if (card.hidden) {
        cardDiv.classList.add('hidden');
        return cardDiv;
    }
    
    const suit = card.suit;
    const suitSymbol = suitSymbols[suit] || suit;
    const suitClass = suit.toLowerCase();
    
    // Card display value
    let displayValue = card.name;
    if (card.name === 'Ace') displayValue = 'A';
    else if (card.name === 'Jack') displayValue = 'J';
    else if (card.name === 'Queen') displayValue = 'Q';
    else if (card.name === 'King') displayValue = 'K';
    else if (card.value > 0) displayValue = card.value;
    
    cardDiv.innerHTML = `
        <div class="card-top ${suitClass}">
            <div class="card-value">${displayValue}</div>
            <div class="card-suit">${suitSymbol}</div>
        </div>
        <div class="card-center ${suitClass}">${suitSymbol}</div>
        <div class="card-bottom ${suitClass}">
            <div class="card-value">${displayValue}</div>
            <div class="card-suit">${suitSymbol}</div>
        </div>
    `;
    
    return cardDiv;
}

// Update button states based on game phase
function updateButtonStates(gamePhase) {
    // Hide all sections first
    bettingSection.style.display = 'none';
    actionButtons.style.display = 'none';
    newRoundSection.style.display = 'none';
    
    switch(gamePhase) {
        case 'betting':
            bettingSection.style.display = 'block';
            break;
        case 'playing':
            actionButtons.style.display = 'block';
            hitBtn.disabled = false;
            standBtn.disabled = false;
            break;
        case 'dealer_turn':
            actionButtons.style.display = 'block';
            hitBtn.disabled = true;
            standBtn.disabled = true;
            break;
        case 'game_over':
            newRoundSection.style.display = 'block';
            break;
    }
}

// Show message
function showMessage(text, type) {
    messageEl.textContent = text;
    messageEl.className = 'message';
    if (type) {
        messageEl.classList.add(type);
    }
}

// Handle Leave Casino
async function handleLeaveCasino() {
    try {
        // Sync balance to story mode
        const balance = currentState ? currentState.balance : 50;
        await fetch('/api/story/sync-balance', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ balance: balance })
        });
        
        // Navigate to story page
        window.location.href = '/story';
    } catch (error) {
        console.error('Error leaving casino:', error);
        showMessage('Error leaving casino.', 'lose');
    }
}
