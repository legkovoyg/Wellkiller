// Вынесение traces в глобальную область
let traces = {};

document.addEventListener('DOMContentLoaded', function () {
    initialGraph()
    
    document.querySelectorAll('.tabs-wrapper').forEach(e => {
        let tabs = e.querySelectorAll('.tab')
        let innerTabs = e.querySelectorAll('.inner-tabs')
        let innerTab = e.querySelectorAll('.inner-tab')
        let btn = e.querySelectorAll('.tabs-items')
        let bxSalt = e.querySelectorAll('.inner-tab i')
        let icons = e.querySelectorAll('.tabs i')
        let buttonSalt = e.querySelectorAll('.btn-salt')
        let buttonOthers = e.querySelectorAll('.btn')

        for (let i = 0; i < tabs.length; i++) {
            tabs[i].onclick = () => {
                if (tabs[i].classList.contains('on')) {
                    tabs[i].classList.remove('on')
                    innerTabs[i].classList.remove('on')
                    icons[i].classList.remove('bx-chevron-down')
                    icons[i].classList.add('bx-chevron-right')
                } else {
                    tabs[i].classList.add('on')
                    innerTabs[i].classList.add('on')
                    icons[i].classList.remove('bx-chevron-right')
                    icons[i].classList.add('bx-chevron-down')
                }
            }
        }

        for (let i = 0; i < innerTab.length; i++) {
            innerTab[i].onclick = () => {             
                if (innerTab[i].classList.contains('on')) {
                    innerTab[i].classList.remove('on')
                    btn[i].classList.remove ('on')
                    bxSalt[i].classList.remove('bx-chevron-down')
                    bxSalt[i].classList.add('bx-chevron-right')
                } else {
                    innerTab[i].classList.add('on')
                    btn[i].classList.add('on')
                    bxSalt[i].classList.remove('bx-chevron-right')
                    bxSalt[i].classList.add('bx-chevron-down')
                }
                // Plotly.Plots.resize('plotly-graph')
            }
        }


        buttonOthers.forEach(btn => {
            btn.addEventListener('click', () => {
                let tables = document.querySelectorAll('.content__features table')  
                let target = btn.getAttribute('data-target')
                tables.forEach(table => {
                    if (table.id === target) {
                        table.style.display = 'table'
                    } else {
                        table.style.display = 'none'
                    }
                })
                let descriptionSection = document.querySelector('.content__features')
                 if (descriptionSection.style.display == 'none') {
                    descriptionSection.style.display = 'block'
                }
                Plotly.Plots.resize('plotly-graph')
            })
        })

        buttonSalt.forEach(btn => {
            btn.addEventListener('click', () => {
               
                btn.classList.toggle('active')
                let target = btn.getAttribute('data-target')
                let changedTable = document.querySelector('.changed-table')
                let tables = document.querySelectorAll('.content__features table')
                let loadedTable = document.querySelector('.loaded-table')
                
                let descriptionSection = document.querySelector('.content__features')
                let saltName = btn.textContent.trim()

                loadedTable.style.display = 'none'
                changedTable.style.display = 'table'

                tables.forEach(table => {
                    if (table.id === target) {
                        table.style.display = 'table'
                    } else {
                        table.style.display = 'none'
                    }
                })
                if (descriptionSection.style.display == 'none') {
                    descriptionSection.style.display = 'block'
                }
                // Вставляем новую строку для выбранной соли
                let tableBody = document.querySelector(".changed-table tbody");
                let elemName = saltName;
                let existingRow = document.getElementById(`${elemName}-cell`);	
                if(!existingRow){
                    let newRow = document.createElement("tr");
                    newRow.id = `${elemName}-cell`
                    newRow.innerHTML = `
                        <td>${elemName}</td>
                        <td><input type="number" step="0.01" class="density-input" id="${elemName}-density-input"></td>
                        <td id="${elemName}-salt-consumption">-</td>
                        <td id="${elemName}-water-consumption">-</td>
                    `;
                    tableBody.appendChild(newRow);
                } else {
                    existingRow.remove()
                }
                
                if (tableBody.children.length === 0) {
                    loadedTable.style.display = 'table'; 
                    changedTable.style.display = 'none';
                } else {
                    loadedTable.style.display = 'none'; 
                    changedTable.style.display = 'table'; 
                }

                const graph = document.getElementById('plotly-graph')
                const changedGraph = document.getElementById('plotly-graph-changed')
                graph.style.display = 'none'
                changedGraph.style.display = 'block'
                Plotly.Plots.resize('plotly-graph-changed')

                // Добавление или удаление графика для выбранной соли
                if (!traces[saltName]) {
                    const salt = saltsData.find(s => s.name === saltName)
                    let filteredSolutionsData = solutionsData.filter(
                        sol => sol.salt_id === salt.id
                    )

                    if (filteredSolutionsData.length) {
                        let xData = filteredSolutionsData.map(sol => sol.density)
                        let yData = filteredSolutionsData.map(sol => sol.salt_consumption)

                        let trace = {
                            x: xData,
                            y: yData,
                            mode: 'lines',
                            name: saltName,
                            showlegend: true,
                        }
                        traces[saltName] = trace

                        Plotly.addTraces('plotly-graph-changed', trace)
                    }
                } else {
                    Plotly.deleteTraces(
                        'plotly-graph-changed',
                        Object.keys(traces).indexOf(saltName)
                    )
                    delete traces[saltName] 
                }
                if (Object.keys(traces).length === 0) {
                    graph.style.display = 'block'
                    changedGraph.style.display = 'none'
                    Plotly.Plots.resize('plotly-graph')
                }
                window.addEventListener('resize', () => {
                    Plotly.Plots.resize('plotly-graph-changed')
                })
            })
           
        })
        
       
        // Заменяем на селектор выбора соли по id
        document.querySelector('#salt-choose').addEventListener('change', (event) => {
            let selectedSaltName = event.target.value.trim();
            // Ищем data-target у выбранного option
            let optionSelected = event.target.querySelector(`[data-target="${selectedSaltName}"]`);
            if(!optionSelected){
                return; // Если не нашли, значит выбрали "Выбор соли" и т.п.
            }

            let target = optionSelected.getAttribute('data-target');

            let changedTable = document.querySelector('.changed-table');
            let tables = document.querySelectorAll('.content__features table');
            let loadedTable = document.querySelector('.loaded-table');

            let descriptionSection = document.querySelector('.content__features');

            loadedTable.style.display = 'none';
            changedTable.style.display = 'table';

            tables.forEach(table => {
                if (table.id === target) {
                    table.style.display = 'table';
                } else {
                    table.style.display = 'none';
                }
            });
            if (descriptionSection.style.display == 'none') {
                descriptionSection.style.display = 'block';
            }

            let tableBody = document.querySelector(".changed-table tbody");
            let elemName = selectedSaltName;
            let existingRow = document.getElementById(`${elemName}-cell`);

            if (!existingRow) {
                let newRow = document.createElement("tr");
                newRow.id = `${elemName}-cell`;
                newRow.innerHTML = `
                    <td>${elemName}</td>
                    <td><input type="number" step="0.01" class="density-input" id="${elemName}-density-input"></td>
                    <td id="${elemName}-salt-consumption">-</td>
                    <td id="${elemName}-water-consumption">-</td>
                `;
                tableBody.appendChild(newRow);
            } else {
                existingRow.remove();
            }

            const graph = document.getElementById('plotly-graph');
            const changedGraph = document.getElementById('plotly-graph-changed');
            graph.style.display = 'none';
            changedGraph.style.display = 'block';
            Plotly.Plots.resize('plotly-graph-changed');

            if (!traces[selectedSaltName]) {
                const salt = saltsData.find(s => s.name === selectedSaltName);
                let filteredSolutionsData = solutionsData.filter(
                    sol => sol.salt_id === salt.id
                );

                if (filteredSolutionsData.length) {
                    let xData = filteredSolutionsData.map(sol => sol.density);
                    let yData = filteredSolutionsData.map(sol => sol.salt_consumption);

                    let trace = {
                        x: xData,
                        y: yData,
                        mode: 'lines',
                        name: selectedSaltName,
                        showlegend: true,
                    };
                    traces[selectedSaltName] = trace;

                    Plotly.addTraces('plotly-graph-changed', trace);
                }
            } else {
                Plotly.deleteTraces(
                    'plotly-graph-changed',
                    Object.keys(traces).indexOf(selectedSaltName)
                );
                delete traces[selectedSaltName];
            }
            window.addEventListener('resize', () => {
                Plotly.Plots.resize('plotly-graph-changed');
            });
        });
    })
   
    Plotly.newPlot('plotly-graph-changed', [], {
        paper_bgcolor: 'rgba(41, 46, 60, 1)',
        plot_bgcolor: 'rgba(41, 46, 60, 1)',
        font: {
            family: 'Inter, sans-serif',
            size: 11,
            color: 'rgba(255, 255, 255, 0.87)',
        },
        xaxis: {
            title: 'Плотность ЖГ,  г/см³',
            gridcolor: 'rgba(255, 255, 255, 0.08)',
        },
        yaxis: {
            title: 'Расход соли, кг/м³ ',
            gridcolor: 'rgba(255, 255, 255, 0.08)',
        },
        autosize: true,
        legend: {
            orientation: 'h',
            yanchor: 'top',
            y: -0.25,
            xanchor: 'center',
            x: 0.5,
        },
        height: 392,
        margin: {
            t: 20,
            b: 50,
            l: 50,
            r: 50,
        },
    })

    function initialGraph() {
        let layout = {
            paper_bgcolor: 'rgba(41, 46, 60, 1)',
            plot_bgcolor: 'rgba(41, 46, 60, 1)',
            font: {
                family: 'Inter, sans-serif',
                size: 11,
                color: 'rgba(255, 255, 255, 0.87)',
            },
            xaxis: {
                title: 'Плотность ЖГ,  г/см³',
                gridcolor: 'rgba(255, 255, 255, 0.08)',
            },
            yaxis: {
                title: 'Расход соли, кг/м³ ',
                gridcolor: 'rgba(255, 255, 255, 0.08)',
            },
            autosize: true,
            legend: {
                orientation: 'h',
                yanchor: 'top',
                y: -0.25,
                xanchor: 'center',
                x: 0.5,
            },
            height: 392,
            margin: {
                t: 20,
                b: 50,
                l: 50,
                r: 50,
            },
        }

        const data = []
        const selectedSalts = ['NaCl', 'NH4Cl', 'MgCl2']
        selectedSalts.forEach(saltName => {
            const salt = saltsData.find(s => s.name === saltName)

            if (salt) {
                const saltSolutions = solutionsData.filter(
                    solution => solution.salt_id === salt.id
                )

                if (saltSolutions.length > 0) {
                    const xData = saltSolutions.map(solution => solution.density)
                    const yData = saltSolutions.map(solution => solution.salt_consumption)

                    data.push({
                        x: xData,
                        y: yData,
                        mode: 'lines',
                        name: salt.name,
                    })
                }
            }

        })

        Plotly.newPlot('plotly-graph', data, layout)

        window.onresize = function () {
            const plotlyGraph = document.getElementById('plotly-graph')
            if (
                plotlyGraph &&
                plotlyGraph.offsetWidth > 0 &&
                plotlyGraph.offsetHeight > 0
            ) {
                Plotly.Plots.resize(plotlyGraph)
            }
        }
    }
   
})

const normalizeId = (id) => {
    return id
        .toLowerCase()
        .replace(/\s/g, '-')          // Заменяем пробелы на дефисы
        .replace(/[^a-zа-я0-9]/gi, ''); // Убираем все недопустимые символы
};

document.addEventListener('DOMContentLoaded', () => {
    // Обрабатываем ввод плотности для динамически добавляемых строк
    document.querySelector('.changed-table').addEventListener('input', (event) => {
        if (!event.target.classList.contains('density-input')) return;
        
        let row = event.target.closest('tr');
        const saltConsumptionElem = row.querySelector("td[id$='-salt-consumption']")
        const waterConsumptionElem = row.querySelector("td[id$='-water-consumption']")

        // Убираем суффикс -cell, чтобы получить имя соли
        const saltNameRaw = row.id.replace('-cell','');
        const saltSlug = normalizeId(saltNameRaw);
        const salt = saltsData.find(s => normalizeId(s.name) === saltSlug);

        if (!salt) {
            console.error(`Соль с идентификатором ${saltSlug} не найдена.`)
            return
        }

        const densityInput = event.target;
        const density = parseFloat(densityInput.value)
        if (isNaN(density)) {
            saltConsumptionElem.textContent = '-'
            waterConsumptionElem.textContent = '-'
            return
        }

        const solutionsForSalt = solutionsData.filter(
            sol => sol.salt_id === salt.id
        )
        if (solutionsForSalt.length === 0) {
            saltConsumptionElem.textContent = 'Нет данных'
            waterConsumptionElem.textContent = 'Нет данных'
            return
        }

        const minDensity = Math.min(...solutionsForSalt.map(sol => sol.density))
        const maxDensity = Math.max(...solutionsForSalt.map(sol => sol.density))

        if (density < minDensity || density > maxDensity) {
            saltConsumptionElem.textContent = 'Вне диапазона'
            waterConsumptionElem.textContent = 'Вне диапазона'
            return
        }

        fetch(`${calculateConsumptionURL}?salt_id=${salt.id}&density=${density}`)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    console.error(data.error)
                    saltConsumptionElem.textContent = 'Ошибка'
                    waterConsumptionElem.textContent = 'Ошибка'
                } else {
                    saltConsumptionElem.textContent = data.salt_consumption.toFixed(2)
                    waterConsumptionElem.textContent = data.water_consumption.toFixed(2)
                }
            })
            .catch(err => {
                console.error('Ошибка при запросе:', err)
                saltConsumptionElem.textContent = 'Ошибка'
                waterConsumptionElem.textContent = 'Ошибка'
            })
    })
    
})
document.addEventListener('DOMContentLoaded', () => {
    // Находим элементы модального окна
    const densityHeader = document.querySelector('.changed-table .density-header');
    const modalOverlay = document.getElementById('density-modal-overlay');
    const massDensityInput = document.getElementById('mass-density-input');

    // Комментарий: При клике на заголовок "Плотность раствора, г/см³" открываем модальное окно
    densityHeader.addEventListener('click', () => {
        // Отображаем модальное окно
        modalOverlay.style.display = 'flex';
        massDensityInput.focus()
    });

    document.addEventListener('keydown', function (event) {
        if (event.key === 'Escape') {
            
            if (modalOverlay) {
                modalOverlay.style.display = 'none'; 
            }
        }
    })
    
    function applyModal() {
        const newDensity = parseFloat(massDensityInput.value);

        // Проверяем валидность введенного числа
        if (isNaN(newDensity)) {
            alert('Пожалуйста, введите корректное число для плотности.');
            return;
        }

        // Находим все инпуты плотности в таблице
        const densityInputs = document.querySelectorAll('.changed-table .density-input');

        // Обновляем значение каждого инпута плотности
        densityInputs.forEach(input => {
            input.value = newDensity;
            // Инициируем событие input, чтобы сработали расчеты в основном скрипте
            const event = new Event('input', {bubbles: true});
            input.dispatchEvent(event);
        });

        // Закрываем модальное окно
        modalOverlay.style.display = 'none';
        massDensityInput.value = '';

    }
    document.addEventListener('keydown', function (event) {
        if (event.key === 'Enter') {
            applyModal()
        }
    })

    // Дополнительно: Можно закрывать окно по клику на затемненный фон
    modalOverlay.addEventListener('click', (e) => {
        if (e.target === modalOverlay) {
            modalOverlay.style.display = 'none';
            massDensityInput.value = '';
        }
    });
});
document.addEventListener('DOMContentLoaded', () => {
    // Получаем ссылку на таблицу с классом changed-table
    const changedTable = document.querySelector('.changed-table');
    if (!changedTable) return; // Если таблицы нет на странице, выходим

    const tableBody = changedTable.querySelector('tbody');

    // Находим заголовки для столбцов, по которым хотим сортировать.
    // Предполагаем, что столбцы в порядке: 
    // 1: Название соли
    // 2: Плотность
    // 3: Расход соли
    // 4: Расход пресной воды
    const saltConsumptionHeader = changedTable.querySelector('thead tr td:nth-child(3)');
    const waterConsumptionHeader = changedTable.querySelector('thead tr td:nth-child(4)');

    // Флаги направления сортировки для каждого столбца:
    // true - сортировать по возрастанию, false - по убыванию.
    let saltSortAscending = true;
    let waterSortAscending = true;

    // Функция сортировки по определенному столбцу
    // columnIndex - индекс столбца (0-базный, у нас 2 для расхода соли, 3 для воды)
    // ascending - true для возрастания, false для убывания
    function sortTableByColumn(columnIndex, ascending) {
        // Получаем все строки таблицы (кроме заголовка)
        const rows = Array.from(tableBody.querySelectorAll('tr'));

        rows.sort((a, b) => {
            const aText = a.querySelectorAll('td')[columnIndex].textContent.trim();
            const bText = b.querySelectorAll('td')[columnIndex].textContent.trim();
            
            // Преобразуем к числу (на случай, если дробные числа в виде 1,05 или 1.05)
            const aVal = parseFloat(aText.replace(',', '.'));
            const bVal = parseFloat(bText.replace(',', '.'));

            // Если не число, пусть будет 0
            const valA = isNaN(aVal) ? 0 : aVal;
            const valB = isNaN(bVal) ? 0 : bVal;

            if (valA < valB) return ascending ? -1 : 1;
            if (valA > valB) return ascending ? 1 : -1;
            return 0;
        });

        // Перестраиваем tbody новыми строками
        rows.forEach(row => tableBody.appendChild(row));
    }

    // При клике на заголовок столбца расхода соли
    saltConsumptionHeader.addEventListener('click', () => {
        sortTableByColumn(2, saltSortAscending);
        // Меняем флаг, чтобы при следующем клике сортировать в другом порядке
        saltSortAscending = !saltSortAscending;
    });

    // При клике на заголовок столбца расхода пресной воды
    waterConsumptionHeader.addEventListener('click', () => {
        sortTableByColumn(3, waterSortAscending);
        waterSortAscending = !waterSortAscending;
    });
});

