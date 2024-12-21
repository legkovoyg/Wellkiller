document.addEventListener('DOMContentLoaded', function() {
    const modalOverlay = document.querySelector('.modal-overlay');
    const createDesignTrigger = document.querySelector('.create-design-trigger');
    const modalClose = document.querySelector('.modal-close');
    const modalCancel = document.querySelector('.modal-btn.cancel');

    if (createDesignTrigger) {
        // Открытие модального окна
        createDesignTrigger.addEventListener('click', () => {
            modalOverlay.classList.add('active');
        });
    }

    if (modalClose) {
        modalClose.addEventListener('click', () => {
            modalOverlay.classList.remove('active');
        });
    }

    if (modalCancel) {
        modalCancel.addEventListener('click', () => {
            modalOverlay.classList.remove('active');
        });
    }

    modalOverlay.addEventListener('click', (e) => {
        if (e.target === modalOverlay) {
            modalOverlay.classList.remove('active');
        }
    });
});
