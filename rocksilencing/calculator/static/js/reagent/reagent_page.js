document.addEventListener('DOMContentLoaded', function () {
	initialGraph()

	document.querySelectorAll('.tabs-wrapper').forEach(e => {
		let tabs = e.querySelectorAll('.tab')
		let innerTabs = e.querySelectorAll('.inner-tabs')
		let innerTab = e.querySelectorAll('.inner-tabs span')
		let btn = e.querySelectorAll('.tabs-items')
		let bxSalt = e.querySelectorAll('.inner-tab-salt i')
		let icons = e.querySelectorAll('.tabs i')
		let buttons = e.querySelectorAll('.btn')
		let traces = {} // Хранит состояния графиков
		let visibleSalts = []

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

		for (let i = 0; i < btn.length; i++) {
			innerTab[i].onclick = () => {
				if (innerTab[i].classList.contains('on')) {
					innerTab[i].classList.remove('on')
					btn[i].classList.remove('on')
					bxSalt[i].classList.remove('bx-chevron-down')
					bxSalt[i].classList.add('bx-chevron-right')
				} else {
					innerTab[i].classList.add('on')
					btn[i].classList.add('on')
					bxSalt[i].classList.remove('bx-chevron-right')
					bxSalt[i].classList.add('bx-chevron-down')
				}
				Plotly.Plots.resize('plotly-graph')
				console.log('resize1')
			}
		}

		buttons.forEach(btn => {
			btn.addEventListener('click', () => {
				btn.classList.toggle('active')
				let target = btn.getAttribute('data-target')
				let changedTable = document.querySelector('.changed-table')
				let tables = document.querySelectorAll('.content__features table')
				let loadedTable = document.querySelector('.loaded-table')
				let salts = document.querySelectorAll(
					'.changed-table tr:not(:first-child)'
				)
				let header = document.querySelector('.content__features')
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

				if (visibleSalts.includes(target)) {
					visibleSalts = visibleSalts.filter(salt => salt !== target)
				} else {
					visibleSalts.push(target)
				}

				salts.forEach(salt => {
					if (visibleSalts.includes(salt.id)) {
						salt.style.display = 'table-row'
					} else {
						salt.style.display = 'none'
					}
				})

				if (header.style.display == 'none') {
					header.style.display = 'block'
				}

				const graph = document.getElementById('plotly-graph')
				const changedGraph = document.getElementById('plotly-graph-changed')
				graph.style.display = 'none'
				changedGraph.style.display = 'block'
				Plotly.Plots.resize('plotly-graph-changed')

				// Получаем название соли
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

						// Добавляем новый график
						Plotly.addTraces('plotly-graph-changed', trace)
					}
				} else {
					// Убираем график
					Plotly.deleteTraces(
						'plotly-graph-changed',
						Object.keys(traces).indexOf(saltName)
					)

					// Удаляем из переменной отслеживания traces
					delete traces[saltName]
				}
				window.addEventListener('resize', () => {
					Plotly.Plots.resize('plotly-graph-changed')
				})
			})
		})
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
	// Получаем все строки таблицы
	const rows = document.querySelectorAll('.changed-table tr')

	rows.forEach(row => {
		const densityInput = row.querySelector('.density-input')
		const saltConsumptionElem = row.querySelector("td[id$='-salt-consumption']")
		const waterConsumptionElem = row.querySelector(
			"td[id$='-water-consumption']"
		)

		if (densityInput) {
			densityInput.addEventListener('input', () => {
				const saltSlug = normalizeId(row.id); // Приводим `id` строки к предсказуемому формату
				const salt = saltsData.find(s => normalizeId(s.name) === saltSlug);
				console.log(saltSlug)
				console.log(salt)

				if (!salt) {
					console.error(`Соль с идентификатором ${saltSlug} не найдена.`)
					return
				}

				const density = parseFloat(densityInput.value)
				if (isNaN(density)) {
					saltConsumptionElem.textContent = '-'
					waterConsumptionElem.textContent = '-'
					return
				}

				// Проверка диапазона плотности
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

				// Отправляем запрос на сервер
				fetch(`/calculate_consumption/?salt_id=${salt.id}&density=${density}`)
					.then(response => response.json())
					.then(data => {
						if (data.error) {
							console.error(data.error)
							saltConsumptionElem.textContent = 'Ошибка'
							waterConsumptionElem.textContent = 'Ошибка'
						} else {
							saltConsumptionElem.textContent = data.salt_consumption.toFixed(2)
							waterConsumptionElem.textContent =
								data.water_consumption.toFixed(2)
						}
					})
					.catch(err => {
						console.error('Ошибка при запросе:', err)
						saltConsumptionElem.textContent = 'Ошибка'
						waterConsumptionElem.textContent = 'Ошибка'
					})
			})
		}
	})
})
