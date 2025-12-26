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
});

// Load current game state
async function loadGameState() {
    try {
        const response = await fetch('/api/state');
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
    const betAmount = parseInt(betAmountInput.value);
    
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
        const betResult = await betResponse.json();
        
        if (!betResult.success) {
            showMessage(betResult.message, 'lose');
            updateUI(betResult.state);
            return;
        }
        
        // Deal cards
        const dealResponse = await fetch('/api/deal', { method: 'POST' });
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
        const state = await response.json();
        updateUI(state);
        showMessage('Place your bet for the next round.', '');
    } catch (error) {
        console.error('Error starting new round:', error);
        showMessage('Error starting new round.', 'lose');
    }
}

// Handle Game Over
function handleGameOver(result) {
    const outcome = result.outcome;
    const message = result.message;
    
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

// Update UI with game state
function updateUI(state) {
    currentState = state;
    
    // Update balance and bet
    balanceEl.textContent = `$${state.balance}`;
    currentBetEl.textContent = `$${state.bet}`;
    minBetInfo.textContent = `Min: $${state.min_bet}`;
    betAmountInput.min = state.min_bet;
    
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
