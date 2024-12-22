document.addEventListener('DOMContentLoaded', function() {
    // Инициализация состояния для всех details элементов
    const detailsElements = document.querySelectorAll('.salt-info');
    
    detailsElements.forEach((details) => {
        const icon = details.querySelector('.bx');
        const summary = details.querySelector('summary');
        
        // Добавляем обработчик только на summary
        summary.addEventListener('click', function(e) {
            e.preventDefault(); // Предотвращаем стандартное поведение details
            
            // Переключаем состояние details
            const isOpen = details.hasAttribute('open');
            if (isOpen) {
                details.removeAttribute('open');
                icon.classList.remove('bx-chevron-down');
                icon.classList.add('bx-chevron-right');
            } else {
                details.setAttribute('open', '');
                icon.classList.remove('bx-chevron-right');
                icon.classList.add('bx-chevron-down');
            }
        });
    });

    // Инициализация селектов для технологий
    const techGroupSelect = document.getElementById('tech_group');
    const techNameSelect = document.getElementById('tech_name');
    
    if (techGroupSelect && techNameSelect) {
        const technologiesData = JSON.parse(techGroupSelect.getAttribute('data-technologies') || '{}');
        
        function updateTechNames() {
            techNameSelect.innerHTML = '';
            const selectedGroup = techGroupSelect.value;
            const techList = technologiesData[selectedGroup] || [];
            
            techList.forEach(function([techName, applicability]) {
                const option = document.createElement('option');
                option.value = techName;
                option.textContent = `${techName} (${applicability})`;
                techNameSelect.appendChild(option);
            });
        }

        // Инициализация при загрузке
        updateTechNames();
        
        // Обновление при изменении группы
        techGroupSelect.addEventListener('change', updateTechNames);
    }

    // Обработка радио-кнопок
    const waterSensitiveLabels = document.querySelectorAll('.is_water_sensitive label');
    waterSensitiveLabels.forEach(label => {
        label.addEventListener('click', function() {
            waterSensitiveLabels.forEach(lbl => lbl.classList.remove('active'));
            label.classList.add('active');
        });
    });
});