window.addEventListener('DOMContentLoaded', () => {
    // Запускаем два одновременных залпа салюта по бокам экрана
    var duration = 3 * 1000;
    var end = Date.now() + duration;

    (function frame() {
        // Салют слева
        confetti({
            particleCount: 3,
            angle: 60,
            spread: 55,
            origin: { x: 0, y: 0.8 },
            colors: ['#22c55e', '#3b82f6', '#f59e0b', '#ec4899']
        });
        // Салют справа
        confetti({
            particleCount: 3,
            angle: 120,
            spread: 55,
            origin: { x: 1, y: 0.8 },
            colors: ['#22c55e', '#3b82f6', '#f59e0b', '#ec4899']
        });

        if (Date.now() < end) {
            requestAnimationFrame(frame);
        }
    }());
});