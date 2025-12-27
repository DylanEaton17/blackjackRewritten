// Story Mode JavaScript

let gameState = {
    balance: 50,
    day: 1,
    timeOfDay: 'Morning',
    health: 100,
    maxHealth: 100,
    inventory: [],
    conditions: [],
    location: 'outside_casino'
};

// DOM Elements
const balanceEl = document.getElementById('balance');
const dayEl = document.getElementById('day');
const timeEl = document.getElementById('time-of-day');
const healthFillEl = document.getElementById('health-fill');
const healthValueEl = document.getElementById('health-value');
const conditionEl = document.getElementById('condition');
const locationTitleEl = document.getElementById('location-title');
const eventTextEl = document.getElementById('event-text');
const inventoryListEl = document.getElementById('inventory-list');

// Buttons
const enterCasinoBtn = document.getElementById('enter-casino-btn');
const exploreBtn = document.getElementById('explore-btn');
const restBtn = document.getElementById('rest-btn');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadGameState();
    updateUI();
    
    // Event listeners
    enterCasinoBtn.addEventListener('click', enterCasino);
    exploreBtn.addEventListener('click', explore);
    restBtn.addEventListener('click', rest);
});

// Load game state from server
async function loadGameState() {
    try {
        const response = await fetch('/api/story/state');
        if (response.ok) {
            const data = await response.json();
            gameState = { ...gameState, ...data };
            updateUI();
        }
    } catch (error) {
        console.error('Error loading game state:', error);
    }
}

// Update UI
function updateUI() {
    balanceEl.textContent = `$${gameState.balance}`;
    dayEl.textContent = gameState.day;
    timeEl.textContent = gameState.timeOfDay;
    
    // Update health bar
    const healthPercent = (gameState.health / gameState.maxHealth) * 100;
    healthFillEl.style.width = `${healthPercent}%`;
    healthValueEl.textContent = `${gameState.health}/${gameState.maxHealth}`;
    
    // Update condition
    if (gameState.conditions.length > 0) {
        conditionEl.textContent = gameState.conditions.join(', ');
        conditionEl.className = 'status-value status-warning';
    } else {
        conditionEl.textContent = 'Healthy';
        conditionEl.className = 'status-value status-good';
    }
    
    // Update inventory
    updateInventory();
}

// Update inventory display
function updateInventory() {
    if (gameState.inventory.length === 0) {
        inventoryListEl.innerHTML = '<div class="empty-message">No items yet</div>';
    } else {
        inventoryListEl.innerHTML = gameState.inventory.map(item => `
            <div class="inventory-item">
                <div class="item-name">${item.name}</div>
                ${item.description ? `<div class="item-description">${item.description}</div>` : ''}
            </div>
        `).join('');
    }
}

// Enter Casino
function enterCasino() {
    window.location.href = '/casino';
}

// Explore Area
async function explore() {
    try {
        const response = await fetch('/api/story/explore', { method: 'POST' });
        if (response.ok) {
            const data = await response.json();
            displayEvent(data);
            if (data.state) {
                gameState = { ...gameState, ...data.state };
                updateUI();
            }
        }
    } catch (error) {
        console.error('Error exploring:', error);
    }
}

// Rest
async function rest() {
    try {
        const response = await fetch('/api/story/rest', { method: 'POST' });
        if (response.ok) {
            const data = await response.json();
            displayEvent(data);
            if (data.state) {
                gameState = { ...gameState, ...data.state };
                updateUI();
            }
        }
    } catch (error) {
        console.error('Error resting:', error);
    }
}

// Display event text
function displayEvent(data) {
    if (data.title) {
        locationTitleEl.textContent = data.title;
    }
    
    if (data.text) {
        eventTextEl.innerHTML = data.text.map(line => `<p>${line}</p>`).join('');
    }
}
