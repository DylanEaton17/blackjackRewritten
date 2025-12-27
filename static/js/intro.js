// Intro Page JavaScript

document.addEventListener('DOMContentLoaded', () => {
    const startBtn = document.getElementById('start-journey-btn');
    
    startBtn.addEventListener('click', () => {
        // Redirect to story page
        window.location.href = '/story';
    });
});
