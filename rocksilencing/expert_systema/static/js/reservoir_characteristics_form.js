// file: reservoir_characteristics_form.js

document.addEventListener('DOMContentLoaded', function() {
    // --- 1) Логика раскрывающихся details ---
    const detailsElements = document.querySelectorAll('.salt-info');
    detailsElements.forEach((details) => {
        const icon = details.querySelector('.bx');
        const summary = details.querySelector('summary');
        
        // Обработчик на summary для переключения open
        summary.addEventListener('click', function(e) {
            e.preventDefault(); // Предотвращаем стандартное поведение details
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

    // --- 2) Селектор групп/технологий ---
    const techGroupSelect = document.getElementById('tech_group');
    const techNameSelect = document.getElementById('tech_name');

    if (techGroupSelect && techNameSelect) {
        // Прочитаем JSON со всеми технологиями
        const technologiesData = JSON.parse(techGroupSelect.getAttribute('data-technologies') || '{}');
        
        // Прочитаем выбранную группу/технологию (из data-атрибутов)
        const selectedGroup = techGroupSelect.getAttribute('data-selected-group') || '';
        const selectedTechnology = techGroupSelect.getAttribute('data-selected-technology') || '';

        // Функция, которая заполняет techNameSelect исходя из выбранной группы
        function updateTechNames(groupValue) {
            techNameSelect.innerHTML = '';
            if (!groupValue || !technologiesData[groupValue]) {
                return;
            }
            const techList = technologiesData[groupValue] || [];
            techList.forEach((tech) => {
                const option = document.createElement('option');
                option.value = tech.name;
                option.textContent = `${tech.name} (${tech.applicability})`;
                techNameSelect.appendChild(option);
            });
        }

        // Сразу при загрузке страницы:
        // 1) Если selectedGroup есть, выберем её (HTML уже поставил selected в <option>, но на всякий случай)
        if (selectedGroup) {
            techGroupSelect.value = selectedGroup;
        }

        // 2) Заполним второй селект
        updateTechNames(techGroupSelect.value);

        // 3) Поставим выбранную технологию, если есть
        if (selectedTechnology) {
            techNameSelect.value = selectedTechnology;
        }

        // Когда пользователь меняет группу — обновляем список технологий
        techGroupSelect.addEventListener('change', function() {
            updateTechNames(this.value);
            // Сбросим выбранную технологию
            techNameSelect.value = '';
        });
    }

    // --- 3) Обработка радио-кнопок (активность) ---
    const waterSensitiveLabels = document.querySelectorAll('.is_water_sensitive label');
    waterSensitiveLabels.forEach(label => {
        label.addEventListener('click', function() {
            waterSensitiveLabels.forEach(lbl => lbl.classList.remove('active'));
            label.classList.add('active');
        });
    });

    // --- 4) Работа с чекбоксом "доп. вопросы" ---
    const checkbox = document.querySelector('.checkbox-container input');
    const addedQuestions = document.querySelector('.added-questions');
    if (checkbox && addedQuestions) {
        checkbox.addEventListener('click', function(){
            addedQuestions.classList.toggle('hidden');
        });
    }
});
