// --------------------- Константы для расчётов ---------------------
const CONST_CL   = 35.453;
const CONST_SO4  = 96.062;
const CONST_HCO3 = 61.016;
const CONST_CA   = 40.078;
const CONST_MG   = 24.305;
const CONST_NA   = 22.99;
const CONST_BA   = 137.33;
const CONST_SR   = 87.62;

// Отключаем проверку limitLength (заглушка, если вдруг где-то используется)
function limitLength() {
    return true;
}

// --------------------- ID инпутов ---------------------
// Эти ключи соответствуют name полям Django-формы,
// а значения — атрибутам id, которые генерируются по умолчанию (id_ИМЯПОЛЯ).
// Например, {{ form.Cl_1 }} обычно генерирует <input id="id_Cl_1" name="Cl_1" ...>
const inputs = {
    // Вода 1
    Cl_1:          'id_Cl_1',
    Cl_1_another:  'id_Cl_1_another',
    SO4_1:         'id_SO4_1',
    SO4_1_another: 'id_SO4_1_another',
    HCO3_1:        'id_HCO3_1',
    HCO3_1_another:'id_HCO3_1_another',
    Ca_1:          'id_Ca_1',
    Ca_1_another:  'id_Ca_1_another',
    Mg_1:          'id_Mg_1',
    Mg_1_another:  'id_Mg_1_another',
    Na_1:          'id_Na_1',
    Na_1_another:  'id_Na_1_another',
    Ba_1:          'id_Ba_1',
    Ba_1_another:  'id_Ba_1_another',
    Sr_1:          'id_Sr_1',
    Sr_1_another:  'id_Sr_1_another',

    // Вода 2
    Cl_2:          'id_Cl_2',
    Cl_2_another:  'id_Cl_2_another',
    SO4_2:         'id_SO4_2',
    SO4_2_another: 'id_SO4_2_another',
    HCO3_2:        'id_HCO3_2',
    HCO3_2_another:'id_HCO3_2_another',
    Ca_2:          'id_Ca_2',
    Ca_2_another:  'id_Ca_2_another',
    Mg_2:          'id_Mg_2',
    Mg_2_another:  'id_Mg_2_another',
    Na_2:          'id_Na_2',
    Na_2_another:  'id_Na_2_another',
    Ba_2:          'id_Ba_2',
    Ba_2_another:  'id_Ba_2_another',
    Sr_2:          'id_Sr_2',
    Sr_2_another:  'id_Sr_2_another',

    // Плотности
    ro_1:          'density_1',
    ro_2:          'density_2'
};

// --------------------- ФУНКЦИИ ---------------------

/**
 * Функция связывает два поля:
 *  - первое поле (moleInput)  — ввод моль/кг
 *  - второе поле (mgInput)    — ввод мг/л
 * а также учитывает плотность (roId).
 *
 * multiplier — это молярная масса соответствующего иона.
 */
function formUpdate(moleId, mgId, roId, multiplier) {
    const moleInput = document.getElementById(moleId);
    const mgInput   = document.getElementById(mgId);
    const roInput   = document.getElementById(roId);
    
    // Проверяем, существуют ли вообще такие элементы
    if (moleInput && mgInput && roInput) {

        // Когда пользователь вводит значение в поле "моль/кг"...
        moleInput.addEventListener('input', () => {
            const mole = parseFloat(moleInput.value) || 0;
            const ro   = parseFloat(roInput.value)   || 1;
            // мг/л = (моль/кг) * 1000 * (молярная масса) * плотность
            const mgPerLiter = mole * 1000 * multiplier * ro;
            mgInput.value = mgPerLiter.toFixed(5);
        });

        // Когда пользователь вводит значение в поле "мг/л"...
        mgInput.addEventListener('input', () => {
            const mg = parseFloat(mgInput.value) || 0;
            const ro = parseFloat(roInput.value) || 1;
            // моль/кг = (мг/л) / [ 1000 * (молярная масса) * плотность ]
            const mole = mg / (1000 * multiplier * ro);
            moleInput.value = mole.toFixed(5);
        });
    }
}

/**
 * Функция заполняет демо-данные и вызывает 'input' событие для пересчёта.
 * Вызывается по кнопке "демо" в HTML.
 */
function demonstrate() {
   const demoValues = {
       // Общие параметры
       Temperature: 40,
       Pressure: 2, 
       Part_of_Mixture: 33,

       // Параметры воды 1
       pH_1: 6,
       ro_1: 1.176,
       Cl_1: 0.512,
       SO4_1: 0.005,
       HCO3_1: 0.001,
       Ca_1: 0.100,
       Mg_1: 0.020,
       Na_1: 2.41,
       Ba_1: 0,
       Sr_1: 0,

       // Параметры воды 2
       pH_2: 6.7,
       ro_2: 1.232,
       Cl_2: 0.005,
       SO4_2: 0.001,
       HCO3_2: 0.006,
       Ca_2: 0.003,
       Mg_2: 0.01,
       Na_2: 0.003,
       Ba_2: 0,
       Sr_2: 0
   };

   // Заполняем значения и рассчитываем мг/л
   Object.entries(demoValues).forEach(([key, value]) => {
       const input = document.getElementById('id_' + key);
       if (input) {
           input.value = value;
           const event = new Event('input', {bubbles: true});
           input.dispatchEvent(event);
       }
   });
   
   // Рассчитываем значения мг/л для воды 1
   document.getElementById('id_Cl_1_another').value = (demoValues.Cl_1 * 1000 * CONST_CL * demoValues.ro_1).toFixed(3);
   document.getElementById('id_SO4_1_another').value = (demoValues.SO4_1 * 1000 * CONST_SO4 * demoValues.ro_1).toFixed(3);
   document.getElementById('id_HCO3_1_another').value = (demoValues.HCO3_1 * 1000 * CONST_HCO3 * demoValues.ro_1).toFixed(3);
   document.getElementById('id_Ca_1_another').value = (demoValues.Ca_1 * 1000 * CONST_CA * demoValues.ro_1).toFixed(3);
   document.getElementById('id_Mg_1_another').value = (demoValues.Mg_1 * 1000 * CONST_MG * demoValues.ro_1).toFixed(3);
   document.getElementById('id_Na_1_another').value = (demoValues.Na_1 * 1000 * CONST_NA * demoValues.ro_1).toFixed(3);
   document.getElementById('id_Ba_1_another').value = (demoValues.Ba_1 * 1000 * CONST_BA * demoValues.ro_1).toFixed(3);
   document.getElementById('id_Sr_1_another').value = (demoValues.Sr_1 * 1000 * CONST_SR * demoValues.ro_1).toFixed(3);

   // Рассчитываем значения мг/л для воды 2
   document.getElementById('id_Cl_2_another').value = (demoValues.Cl_2 * 1000 * CONST_CL * demoValues.ro_2).toFixed(3);
   document.getElementById('id_SO4_2_another').value = (demoValues.SO4_2 * 1000 * CONST_SO4 * demoValues.ro_2).toFixed(3);
   document.getElementById('id_HCO3_2_another').value = (demoValues.HCO3_2 * 1000 * CONST_HCO3 * demoValues.ro_2).toFixed(3);
   document.getElementById('id_Ca_2_another').value = (demoValues.Ca_2 * 1000 * CONST_CA * demoValues.ro_2).toFixed(3);
   document.getElementById('id_Mg_2_another').value = (demoValues.Mg_2 * 1000 * CONST_MG * demoValues.ro_2).toFixed(3);
   document.getElementById('id_Na_2_another').value = (demoValues.Na_2 * 1000 * CONST_NA * demoValues.ro_2).toFixed(3);
   document.getElementById('id_Ba_2_another').value = (demoValues.Ba_2 * 1000 * CONST_BA * demoValues.ro_2).toFixed(3);
   document.getElementById('id_Sr_2_another').value = (demoValues.Sr_2 * 1000 * CONST_SR * demoValues.ro_2).toFixed(3);
   // Заполнение этих конкретных полей
document.querySelector('input[name="Temperature"]').value = demoValues.Temperature;
document.querySelector('input[name="Pressure"]').value = demoValues.Pressure;
document.querySelector('input[name="Part_of_Mixture"]').value = demoValues.Part_of_Mixture;
document.querySelector('input[name="pH_1"]').value = demoValues.pH_1;
document.querySelector('input[name="ro_1"]').value = demoValues.ro_1;
document.querySelector('input[name="pH_2"]').value = demoValues.pH_2;
document.querySelector('input[name="ro_2"]').value = demoValues.ro_2;
};


const tableToggle = document.querySelector('.third_section-table')
const graphToggle = document.querySelector('.third_section-graph')
const graphSection = document.querySelector('.graph')
const tableSection = document.querySelector('.third-section__child')

tableToggle.addEventListener('click', function () {
    tableSection.style.display = 'block'
    graphSection.style.display = 'none'
    tableToggle.classList.add('active')
    graphToggle.classList.remove('active')
} )
graphToggle.addEventListener('click', function () {
    graphSection.style.display = 'block'
    tableSection.style.display = 'none'
    graphToggle.classList.add('active')
    tableToggle.classList.remove('active')
} )




/**
 * Применяет чередование классов строк таблицы (для визуала).
 * Меняем строки на 'gray-row' / 'dark-row'.
 */
function alternateRowClasses(table) {
    const rows = table.querySelectorAll('tbody tr');
    let toggle = true; // начнём, например, с 'gray-row'

    rows.forEach(row => {
        // Сначала убираем предыдущие классы
        row.classList.remove('gray-row', 'dark-row');
        // Добавляем новый
        row.classList.add(toggle ? 'gray-row' : 'dark-row');
        toggle = !toggle;
    });
}

/**
 * Сортируем таблицу по указанному столбцу (columnName) и направлению (asc / desc).
 */
function sortTable(table, columnName, direction) {
    const tbody = table.querySelector('tbody');
    const rows  = Array.from(tbody.querySelectorAll('tr'));
    
    // Узнаём номер столбца, по которому сортировать
    const columnIndex = getColumnIndex(table, columnName);

    // Сортируем строки
    rows.sort((a, b) => {
        const aCell  = a.querySelector(`td:nth-child(${columnIndex})`);
        const bCell  = b.querySelector(`td:nth-child(${columnIndex})`);
        const aValue = parseFloat(aCell?.textContent) || 0;
        const bValue = parseFloat(bCell?.textContent) || 0;
        return direction === 'asc' ? (aValue - bValue) : (bValue - aValue);
    });

    // Удаляем всё из tbody и заполняем заново отсортированными строками
    while (tbody.firstChild) {
        tbody.removeChild(tbody.firstChild);
    }
    rows.forEach(row => tbody.appendChild(row));

    // После сортировки заново чередуем классы
    alternateRowClasses(table);
}

/**
 * Возвращает индекс столбца (начиная с 1), который надо сортировать,
 * по атрибуту data-sort в ячейках thead.
 */
function getColumnIndex(table, columnName) {
    const headers = table.querySelectorAll('.sortable');
    for (let i = 0; i < headers.length; i++) {
        if (headers[i].getAttribute('data-sort') === columnName) {
            // nth-child в CSS считаем с 1
            return i + 1;
        }
    }
    // Если вдруг не нашли — по умолчанию первый столбец
    return 1;
}

/**
 * Инициализирует клик по заголовкам сортируемых столбцов.
 */
function initializeTableSorting() {
    const tables = document.querySelectorAll('.tables table');

    tables.forEach(table => {
        const headers = table.querySelectorAll('.sortable');
        headers.forEach(header => {
            header.style.cursor = 'pointer'; 
            header.addEventListener('click', () => {
                const columnName      = header.getAttribute('data-sort');
                const currentDir      = header.getAttribute('data-sort-direction') || 'asc';
                const newDirection    = currentDir === 'asc' ? 'desc' : 'asc';
                
                sortTable(table, columnName, newDirection);

                // Сбрасываем у других заголовков стрелочки, чтобы показывать направление только у одного
                headers.forEach(h => {
                    if (h !== header) {
                        h.removeAttribute('data-sort-direction');
                        h.classList.remove('asc', 'desc');
                    }
                });
                // Обновляем класс текущего заголовка
                header.setAttribute('data-sort-direction', newDirection);
                header.classList.remove('asc', 'desc');
                header.classList.add(newDirection);
            });
        });
    });
}

/**
 * При загрузке DOM вешаем слушатели на все поля для воды 1 и воды 2,
 * а также инициализируем сортировку и делаем чередование строк в таблицах.
 */
document.addEventListener('DOMContentLoaded', function() {
    // ------------------ Вешаем слушатели для первой воды ------------------
    formUpdate(inputs.Cl_1,   inputs.Cl_1_another,   inputs.ro_1, CONST_CL);
    formUpdate(inputs.SO4_1,  inputs.SO4_1_another,  inputs.ro_1, CONST_SO4);
    formUpdate(inputs.HCO3_1, inputs.HCO3_1_another, inputs.ro_1, CONST_HCO3);
    formUpdate(inputs.Ca_1,   inputs.Ca_1_another,   inputs.ro_1, CONST_CA);
    formUpdate(inputs.Mg_1,   inputs.Mg_1_another,   inputs.ro_1, CONST_MG);
    formUpdate(inputs.Na_1,   inputs.Na_1_another,   inputs.ro_1, CONST_NA);
    formUpdate(inputs.Ba_1,   inputs.Ba_1_another,   inputs.ro_1, CONST_BA);
    formUpdate(inputs.Sr_1,   inputs.Sr_1_another,   inputs.ro_1, CONST_SR);

    // ------------------ Вешаем слушатели для второй воды ------------------
    formUpdate(inputs.Cl_2,   inputs.Cl_2_another,   inputs.ro_2, CONST_CL);
    formUpdate(inputs.SO4_2,  inputs.SO4_2_another,  inputs.ro_2, CONST_SO4);
    formUpdate(inputs.HCO3_2, inputs.HCO3_2_another, inputs.ro_2, CONST_HCO3);
    formUpdate(inputs.Ca_2,   inputs.Ca_2_another,   inputs.ro_2, CONST_CA);
    formUpdate(inputs.Mg_2,   inputs.Mg_2_another,   inputs.ro_2, CONST_MG);
    formUpdate(inputs.Na_2,   inputs.Na_2_another,   inputs.ro_2, CONST_NA);
    formUpdate(inputs.Ba_2,   inputs.Ba_2_another,   inputs.ro_2, CONST_BA);
    formUpdate(inputs.Sr_2,   inputs.Sr_2_another,   inputs.ro_2, CONST_SR);

    // Инициализация сортировки
    initializeTableSorting();

    // Чередуем классы строк при первой загрузке
    const tables = document.querySelectorAll('.tables table');
    tables.forEach(table => {
        alternateRowClasses(table);
    });
});

// Чтобы кнопка <button onclick="demonstrate()"> могла найти эту функцию
// в глобальной области, делаем так:
window.demonstrate = demonstrate;
