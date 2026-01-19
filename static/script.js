document.addEventListener('DOMContentLoaded', () => {
    // Add any dynamic interactions here
    // For now, we can add a simple animation for flash messages
    const flashes = document.querySelectorAll('.flash');
    flashes.forEach(flash => {
        setTimeout(() => {
            flash.style.opacity = '0';
            flash.style.transition = 'opacity 0.5s ease';
            setTimeout(() => flash.remove(), 500);
        }, 5000);
    });
});
