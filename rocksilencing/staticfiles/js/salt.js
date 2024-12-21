// Константы для расчетов
const CONST_CL = 35.453;
const CONST_SO4 = 96.062;
const CONST_HCO3 = 61.016;
const CONST_CA = 40.078;
const CONST_MG = 24.305;
const CONST_NA = 22.99;
const CONST_BA = 137.33;
const CONST_SR = 87.62;

// Объект с ID инпутов для удобства
const inputs = {
    Cl_1: 'id_Cl_1',
    Cl_1_another: 'id_Cl_1_another',
    SO4_1: 'id_SO4_1',
    SO4_1_another: 'id_SO4_1_another',
    HCO3_1: 'id_HCO3_1',
    HCO3_1_another: 'id_HCO3_1_another',
    Ca_1: 'id_Ca_1',
    Ca_1_another: 'id_Ca_1_another',
    Mg_1: 'id_Mg_1',
    Mg_1_another: 'id_Mg_1_another',
    Na_1: 'id_Na_1',
    Na_1_another: 'id_Na_1_another',
    Ba_1: 'id_Ba_1',
    Ba_1_another: 'id_Ba_1_another',
    Sr_1: 'id_Sr_1',
    Sr_1_another: 'id_Sr_1_another',
    Cl_2: 'id_Cl_2',
    Cl_2_another: 'id_Cl_2_another',
    SO4_2: 'id_SO4_2',
    SO4_2_another: 'id_SO4_2_another',
    HCO3_2: 'id_HCO3_2',
    HCO3_2_another: 'id_HCO3_2_another',
    Ca_2: 'id_Ca_2',
    Ca_2_another: 'id_Ca_2_another',
    Mg_2: 'id_Mg_2',
    Mg_2_another: 'id_Mg_2_another',
    Na_2: 'id_Na_2',
    Na_2_another: 'id_Na_2_another',
    Ba_2: 'id_Ba_2',
    Ba_2_another: 'id_Ba_2_another',
    Sr_2: 'id_Sr_2',
    Sr_2_another: 'id_Sr_2_another',
    ro_1: 'id_ro_1',
    ro_2: 'id_ro_2'
};

// Функция для обновления значений моль/кг и мг/л
function formUpdate(concent1, concent2, roId, multiplier) {
    const moleInput = document.getElementById(concent1);
    const mgInput = document.getElementById(concent2);
    const roInput = document.getElementById(roId);
    
    if (moleInput && mgInput && roInput) {
        // Обновление значения мг/л при изменении моль/кг
        moleInput.addEventListener('input', () => {
            const mole = parseFloat(moleInput.value) || 0;
            const ro = parseFloat(roInput.value) || 1;
            mgInput.value = (mole * 1000 * multiplier * ro).toFixed(5);
        });
        
        // Обновление значения моль/кг при изменении мг/л
        mgInput.addEventListener('input', () => {
            const mg = parseFloat(mgInput.value) || 0;
            const ro = parseFloat(roInput.value) || 1;
            moleInput.value = (mg / (1000 * multiplier * ro)).toFixed(5);
        });
    }
}

// Функция демонстрации заполнения полей
function demonstrate() {
    // Устанавливаем демонстрационные значения для условий смешивания
    const temp = document.getElementById("id_Temperature");
    const pressure = document.getElementById("id_Pressure");
    const part_of_mixture = document.getElementById("id_Part_of_Mixture");

    if (temp) temp.value = 40;
    if (pressure) pressure.value = 2;
    if (part_of_mixture) part_of_mixture.value = 33;

    // Вода 1
    const ph1 = document.getElementById('id_pH_1');
    const density1 = document.getElementById('id_ro_1');
    if (ph1) ph1.value = 6;
    if (density1) density1.value = 1.176;

    const Cl_1 = document.getElementById('id_Cl_1');
    const SO4_1 = document.getElementById('id_SO4_1');
    const HCO3_1 = document.getElementById("id_HCO3_1");
    const Ca_1 = document.getElementById('id_Ca_1');
    const Mg_1 = document.getElementById('id_Mg_1');
    const Na_1 = document.getElementById('id_Na_1');
    const Ba_1 = document.getElementById('id_Ba_1');
    const Sr_1 = document.getElementById("id_Sr_1");

    if (Cl_1) Cl_1.value = 0.512;
    if (SO4_1) SO4_1.value = 0.005;
    if (HCO3_1) HCO3_1.value = 0.001;
    if (Ca_1) Ca_1.value = 0.100;
    if (Mg_1) Mg_1.value = 0.020;
    if (Na_1) Na_1.value = 2.41;
    if (Ba_1) Ba_1.value = 0;
    if (Sr_1) Sr_1.value = 0;

    const Cl_1_another = document.getElementById('id_Cl_1_another');
    const SO4_1_another = document.getElementById('id_SO4_1_another');
    const HCO3_1_another = document.getElementById("id_HCO3_1_another");
    const Ca_1_another = document.getElementById('id_Ca_1_another');
    const Mg_1_another = document.getElementById('id_Mg_1_another');
    const Na_1_another = document.getElementById('id_Na_1_another');
    const Ba_1_another = document.getElementById('id_Ba_1_another');
    const Sr_1_another = document.getElementById("id_Sr_1_another");

    if (Cl_1_another && density1) {
        Cl_1_another.value = (1000 * 0.512 * CONST_CL * parseFloat(density1.value)).toFixed(2);
    }
    if (SO4_1_another && density1) {
        SO4_1_another.value = (1000 * 0.005 * CONST_SO4 * parseFloat(density1.value)).toFixed(2);
    }
    if (HCO3_1_another && density1) {
        HCO3_1_another.value = (1000 * 0.001 * CONST_HCO3 * parseFloat(density1.value)).toFixed(2);
    }
    if (Ca_1_another && density1) {
        Ca_1_another.value = (1000 * 0.100 * CONST_CA * parseFloat(density1.value)).toFixed(2);
    }
    if (Mg_1_another && density1) {
        Mg_1_another.value = (1000 * 0.020 * CONST_MG * parseFloat(density1.value)).toFixed(2);
    }
    if (Na_1_another && density1) {
        Na_1_another.value = (1000 * 2.41 * CONST_NA * parseFloat(density1.value)).toFixed(2);
    }
    if (Ba_1_another && density1) {
        Ba_1_another.value = (1000 * 0 * CONST_BA * parseFloat(density1.value)).toFixed(2);
    }
    if (Sr_1_another && density1) {
        Sr_1_another.value = (1000 * 0 * CONST_SR * parseFloat(density1.value)).toFixed(2);
    }

    // Вода 2
    const ph2 = document.getElementById('id_pH_2');
    const density2 = document.getElementById('id_ro_2');
    if (ph2) ph2.value = 6.7;
    if (density2) density2.value = 0.788;

    const Cl_2 = document.getElementById('id_Cl_2');
    const SO4_2 = document.getElementById('id_SO4_2');
    const HCO3_2 = document.getElementById("id_HCO3_2");
    const Ca_2 = document.getElementById('id_Ca_2');
    const Mg_2 = document.getElementById('id_Mg_2');
    const Na_2 = document.getElementById('id_Na_2');
    const Ba_2 = document.getElementById('id_Ba_2');
    const Sr_2 = document.getElementById("id_Sr_2");

    if (Cl_2) Cl_2.value = 0.005;
    if (SO4_2) SO4_2.value = 0.001;
    if (HCO3_2) HCO3_2.value = 0.006;
    if (Ca_2) Ca_2.value = 0.003;
    if (Mg_2) Mg_2.value = 0.01;
    if (Na_2) Na_2.value = 0.003;
    if (Ba_2) Ba_2.value = 0;
    if (Sr_2) Sr_2.value = 0;

    const Cl_2_another = document.getElementById('id_Cl_2_another');
    const SO4_2_another = document.getElementById('id_SO4_2_another');
    const HCO3_2_another = document.getElementById("id_HCO3_2_another");
    const Ca_2_another = document.getElementById('id_Ca_2_another');
    const Mg_2_another = document.getElementById('id_Mg_2_another');
    const Na_2_another = document.getElementById('id_Na_2_another');
    const Ba_2_another = document.getElementById('id_Ba_2_another');
    const Sr_2_another = document.getElementById("id_Sr_2_another");

    if (Cl_2_another && density2) {
        Cl_2_another.value = (1000 * parseFloat(Cl_2.value) * CONST_CL * parseFloat(density2.value)).toFixed(2);
    }
    if (SO4_2_another && density2) {
        SO4_2_another.value = (1000 * parseFloat(SO4_2.value) * CONST_SO4 * parseFloat(density2.value)).toFixed(2);
    }
    if (HCO3_2_another && density2) {
        HCO3_2_another.value = (1000 * parseFloat(HCO3_2.value) * CONST_HCO3 * parseFloat(density2.value)).toFixed(2);
    }
    if (Ca_2_another && density2) {
        Ca_2_another.value = (1000 * parseFloat(Ca_2.value) * CONST_CA * parseFloat(density2.value)).toFixed(2);
    }
    if (Mg_2_another && density2) {
        Mg_2_another.value = (1000 * parseFloat(Mg_2.value) * CONST_MG * parseFloat(density2.value)).toFixed(2);
    }
    if (Na_2_another && density2) {
        Na_2_another.value = (1000 * parseFloat(Na_2.value) * CONST_NA * parseFloat(density2.value)).toFixed(2);
    }
    if (Ba_2_another && density2) {
        Ba_2_another.value = (1000 * 0 * CONST_BA * parseFloat(density2.value)).toFixed(2);
    }
    if (Sr_2_another && density2) {
        Sr_2_another.value = (1000 * 0 * CONST_SR * parseFloat(density2.value)).toFixed(2);
    }
}

// Функция для чередования классов строк таблицы
function alternateRowClasses(table) {
    const rows = table.querySelectorAll('tbody tr');
    let toggle = true; // Начинаем с gray-row

    rows.forEach(row => {
        // Удаляем предыдущие классы 'gray-row' и 'dark-row'
        row.classList.remove('gray-row', 'dark-row');

        // Добавляем класс в зависимости от toggle
        if (toggle) {
            row.classList.add('gray-row');
        } else {
            row.classList.add('dark-row');
        }

        // Переключаем toggle для следующей строки
        toggle = !toggle;
    });
}

// Функция сортировки конкретной таблицы
function sortTable(table, columnName, direction) {
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));

    const columnIndex = getColumnIndex(table, columnName);

    // Сортируем строки
    rows.sort((a, b) => {
        const aCell = a.querySelector(`td:nth-child(${columnIndex})`);
        const bCell = b.querySelector(`td:nth-child(${columnIndex})`);

        const aValue = parseFloat(aCell.textContent) || 0;
        const bValue = parseFloat(bCell.textContent) || 0;

        if (direction === 'asc') {
            return aValue - bValue;
        } else {
            return bValue - aValue;
        }
    });

    // Очищаем tbody
    while (tbody.firstChild) {
        tbody.removeChild(tbody.firstChild);
    }

    // Добавляем отсортированные строки
    rows.forEach(row => tbody.appendChild(row));

    // Перечередуем классы строк после сортировки
    alternateRowClasses(table);
}

// Функция для получения индекса столбца по data-sort
function getColumnIndex(table, columnName) {
    const headers = table.querySelectorAll('.sortable');
    for (let i = 0; i < headers.length; i++) {
        if (headers[i].getAttribute('data-sort') === columnName) {
            return i + 1; // Индексация начинается с 1 для nth-child
        }
    }
    return 1; // По умолчанию первый столбец
}

// Функция инициализации сортировки таблиц
function initializeTableSorting() {
    const tables = document.querySelectorAll('.tables table');

    tables.forEach(table => {
        const headers = table.querySelectorAll('.sortable');

        headers.forEach(header => {
            header.style.cursor = 'pointer'; // Курсор указателя для заголовков
            header.addEventListener('click', () => {
                const columnName = header.getAttribute('data-sort');
                const currentDirection = header.getAttribute('data-sort-direction') || 'asc';
                const newDirection = currentDirection === 'asc' ? 'desc' : 'asc';
                
                sortTable(table, columnName, newDirection);

                // Обновляем атрибуты сортировки и классы
                headers.forEach(h => {
                    if (h !== header) {
                        h.removeAttribute('data-sort-direction');
                        h.classList.remove('asc', 'desc');
                    }
                });
                header.setAttribute('data-sort-direction', newDirection);
                header.classList.remove('asc', 'desc');
                header.classList.add(newDirection);
            });
        });
    });
}

// Обработчик загрузки документа
document.addEventListener('DOMContentLoaded', function() {
    // Инициализация обновления полей
    formUpdate(inputs.Cl_1, inputs.Cl_1_another, inputs.ro_1, CONST_CL);
    formUpdate(inputs.SO4_1, inputs.SO4_1_another, inputs.ro_1, CONST_SO4);
    formUpdate(inputs.HCO3_1, inputs.HCO3_1_another, inputs.ro_1, CONST_HCO3);
    formUpdate(inputs.Ca_1, inputs.Ca_1_another, inputs.ro_1, CONST_CA);
    formUpdate(inputs.Mg_1, inputs.Mg_1_another, inputs.ro_1, CONST_MG);
    formUpdate(inputs.Na_1, inputs.Na_1_another, inputs.ro_1, CONST_NA);
    formUpdate(inputs.Ba_1, inputs.Ba_1_another, inputs.ro_1, CONST_BA);
    formUpdate(inputs.Sr_1, inputs.Sr_1_another, inputs.ro_1, CONST_SR);

    formUpdate(inputs.Cl_2, inputs.Cl_2_another, inputs.ro_2, CONST_CL);
    formUpdate(inputs.SO4_2, inputs.SO4_2_another, inputs.ro_2, CONST_SO4);
    formUpdate(inputs.HCO3_2, inputs.HCO3_2_another, inputs.ro_2, CONST_HCO3);
    formUpdate(inputs.Ca_2, inputs.Ca_2_another, inputs.ro_2, CONST_CA);
    formUpdate(inputs.Mg_2, inputs.Mg_2_another, inputs.ro_2, CONST_MG);
    formUpdate(inputs.Na_2, inputs.Na_2_another, inputs.ro_2, CONST_NA);
    formUpdate(inputs.Ba_2, inputs.Ba_2_another, inputs.ro_2, CONST_BA);
    formUpdate(inputs.Sr_2, inputs.Sr_2_another, inputs.ro_2, CONST_SR);

    // Инициализация сортировки таблиц
    initializeTableSorting();

    // Чередование классов строк при первоначальной загрузке
    const tables = document.querySelectorAll('.tables table');
    tables.forEach(table => {
        alternateRowClasses(table);
    });
});
