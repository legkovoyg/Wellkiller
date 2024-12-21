document.addEventListener('DOMContentLoaded', function() {
    const firstSection = document.querySelectorAll('.container')
    firstSection[0].classList.add('initial')
    const techGroupSelect = document.getElementById('tech_group');
    const techNameSelect = document.getElementById('tech_name');

    const bx = document.querySelectorAll('.bx')
    const details = document.querySelectorAll('.salt-info')
    details.forEach(detail =>  {
        detail.addEventListener('click', function(){
            bx.forEach(bx => {
                 bx.classList.toggle('bx-chevron-right')
                bx.classList.toggle('bx-chevron-down')  
            })
        })
    })
    const labelRadio = document.querySelectorAll('.is_water_sensitive label')
    labelRadio.forEach(label =>{
        label.addEventListener('click', function(){
            labelRadio.forEach(lbl => lbl.classList.remove('active'));
            label.classList.add('active');
        })
    })

    if(firstSection[1]){
        firstSection[0].classList.remove('initial')
    }
  
    // Получаем данные из data-атрибута
    const technologiesData = JSON.parse(techGroupSelect.getAttribute('data-technologies') || '{}');

    // Функция обновления списка технологий
    function updateTechNames() {
        // Очищаем текущий список
        techNameSelect.innerHTML = '';

        const selectedGroup = techGroupSelect.value;
        const techList = technologiesData[selectedGroup] || [];

        // Заполняем options для второго селекта
        techList.forEach(function(item) {
            const [techName, applicability] = item;
            const option = document.createElement('option');
            option.value = techName;
            option.textContent = techName + ' (' + applicability + ')';
            techNameSelect.appendChild(option);
        });
    }

    // Инициализация при загрузке страницы
    if (Object.keys(technologiesData).length > 0) {
        updateTechNames();
    }

    // Обновление при изменении выбора в первом списке
    techGroupSelect.addEventListener('change', updateTechNames);

    
});
