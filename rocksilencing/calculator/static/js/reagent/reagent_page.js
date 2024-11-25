document.querySelectorAll('.tabs-wrapper').forEach(e => {
	let tabs = e.querySelectorAll('.tab');
	let innerTabs = e.querySelectorAll('.inner-tabs');
	let innerTab = e.querySelectorAll('.inner-tabs span');
	let btn = e.querySelectorAll('.tabs-items');
	let bxSalt = e.querySelectorAll('.inner-tab-salt i');
	let icons = e.querySelectorAll('.tabs i');
	let buttons = e.querySelectorAll('.btn');
	let traces = {}; // Хранит состояния графиков

	for (let i = 0; i < tabs.length; i++) {
		tabs[i].onclick = () => {
			if (tabs[i].classList.contains('on')) {
				tabs[i].classList.remove('on');
				innerTabs[i].classList.remove('on');
				icons[i].classList.remove('bx-chevron-down');
				icons[i].classList.add('bx-chevron-right');
			} else {
				tabs[i].classList.add('on');
				innerTabs[i].classList.add('on');
				icons[i].classList.remove('bx-chevron-right');
				icons[i].classList.add('bx-chevron-down');
			}
		};
	}

	for (let i = 0; i < btn.length; i++) {
		innerTab[i].onclick = () => {
			if (innerTab[i].classList.contains('on')) {
				innerTab[i].classList.remove('on');
				btn[i].classList.remove('on');
				bxSalt[i].classList.remove('bx-chevron-down');
				bxSalt[i].classList.add('bx-chevron-right');
			} else {
				innerTab[i].classList.add('on');
				btn[i].classList.add('on');
				bxSalt[i].classList.remove('bx-chevron-right');
				bxSalt[i].classList.add('bx-chevron-down');
			}
			Plotly.Plots.resize('plotly-chart');
			console.log('resize1');
		};
	}

	buttons.forEach(btn => {
		btn.addEventListener('click', () => {
			btn.classList.toggle('active');
			let target = btn.getAttribute('data-target');
			console.log(target);

			let tables = document.querySelectorAll('.content__features table');
			let salts = document.querySelectorAll(
				'.content__table table tr:not(:first-child)'
			);
			let header = document.querySelector('.content__features');

			tables.forEach(table => {
				if (table.id === target) {
					table.style.display = 'table';
				} else {
					table.style.display = 'none';
				}
			});
			salts.forEach(salt => {
				if (salt.id === target) {
					salt.style.display = 'table-row';
				} else {
					salt.style.display = 'none';
				}
			});
			if (header.style.display == 'none') {
				header.style.display = 'block';
			}

			let saltName = btn.textContent.trim();
			// Получаем название соли
			if (!traces[saltName]) {
				const salt = saltsData.find(s => s.name === saltName);
				let filteredSolutionsData = solutionsData.filter(sol => sol.salt_id === salt.id);

				if (filteredSolutionsData.length) {
					let xData = filteredSolutionsData.map(sol => sol.density);
					let yData = filteredSolutionsData.map(sol => sol.salt_consumption);

					let trace = {
						x: xData,
						y: yData,
						mode: 'lines',
						name: saltName, // Название графика для легенды
						showlegend: true // Гарантирует отображение легенды
					};
					traces[saltName] = trace;

					// Добавляем новый график
					Plotly.addTraces('plotly-chart', trace);
				} 
			} else {
				// Убираем график
				Plotly.deleteTraces('plotly-chart', Object.keys(traces).indexOf(saltName));
				
				// Удаляем из переменной отслеживания traces
				delete traces[saltName];
			}
			Plotly.Plots.resize('plotly-chart');
		});
	});
});

Plotly.newPlot('plotly-chart', [], {
	paper_bgcolor: 'rgba(41, 46, 60, 1)',
	plot_bgcolor: 'rgba(41, 46, 60, 1)',
	font: {
		family: 'Inter, sans-serif',
		size: 11,
		color: 'rgba(255, 255, 255, 0.87)'
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
		x: 0.5
	},
	height: 392,
	margin: {
		t: 50, // Отступ сверху
		b: 50, // Отступ снизу
		l: 50, // Отступ слева
		r: 50  // Отступ справа
	},
});

window.addEventListener('resize', () => {
	Plotly.Plots.resize('plotly-chart');
});
