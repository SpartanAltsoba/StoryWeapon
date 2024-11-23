// static/js/effects.js

function initializeCoinImageEffects() {
    const coinImageContainer = document.querySelector('.coin-image-container');
    if (coinImageContainer) {
        coinImageContainer.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.15)';
            this.style.opacity = '1';
            this.style.transition = 'transform 0.3s, opacity 0.3s';
        });
        coinImageContainer.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
            this.style.opacity = '0.85';
            this.style.transition = 'transform 0.3s, opacity 0.3s';
        });
    }
}

// Initialize effects on document ready
$(document).ready(function() {
    initializeCoinImageEffects();
});
