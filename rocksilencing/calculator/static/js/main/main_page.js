// tabs //

document.getElementById('input__file').addEventListener('change', function () {
  var fileName = this.files.length > 0 ? Array.from(this.files).map(file => file.name).join(', ') : 'Импорт';
  document.getElementById('file-name-text').textContent = fileName;
  document.getElementById
}
);
document.getElementById('input__file-NKT').addEventListener('change', function () {
  var fileName = this.files.length > 0 ? Array.from(this.files).map(file => file.name).join(', ') : 'Импорт';
  document.getElementById('file-name-text-NKT').textContent = fileName;
  document.getElementById
}
);

document.querySelectorAll('.tabs-wrapper').forEach((e) => {
  let tabTabs = e.querySelectorAll('.tabs .tab');
  let tabItems = e.querySelectorAll('.tabs-items .item');
  for (let i = 0; i < tabTabs.length; i++) {
    tabTabs[0].click();
    tabTabs[i].onclick = () => {
      tabTabs.forEach((e) => { e.classList.remove('on') });
      tabItems.forEach((e) => { e.classList.remove('on') });
      tabTabs[i].classList.add('on');
      tabItems[i].classList.add('on');
    }
  }
});

document.getElementById('toggleIcon1').addEventListener('click', function () {
  var containerTab = document.querySelector('.container__tab');
  if (containerTab.style.display === 'none') {
    containerTab.style.display = 'block';
  } else {
    containerTab.style.display = 'none';
  }
});

document.getElementById('toggleIcon2').addEventListener('click', function () {
  var containerTab = document.querySelector('.second_section');
  if (containerTab.style.display === 'none') {
    containerTab.style.display = 'block';
  } else {
    containerTab.style.display = 'none';
  }
});

document.getElementById('toggleIcon3').addEventListener('click', function () {
  var containerTab = document.querySelector('.third_section');
  if (containerTab.style.display === 'none') {
    containerTab.style.display = 'block';
  } else {
    containerTab.style.display = 'none';
  }
});

const svgImage = document.querySelectorAll(".main-svg")
const pressureGraph = document.getElementById("pressure_graph")
const graphSelect = document.getElementById('graph_select')
graphSelect.addEventListener('change', function () {
  if (graphSelect.value === "pressure_graph") {
    for (let i = 0; i <= svgImage.length; i++) {
      svgImage[i].classList.remove("hidden")
      svgImage[i].classList.add("visible")
    }
  } else {
    for (let i = 0; i < svgImage.length; i++) {
      svgImage[i].classList.remove("visible")
      svgImage[i].classList.add("hidden")
    }
  }
})

let hasElementsBeenAdded = false;

function updateText() {

  const mainContainer = document.querySelector('main')
 
  if (document.documentElement.clientWidth <= 500) {

    if (hasElementsBeenAdded) return

      let headerContainerMobile = document.createElement('div');
      headerContainerMobile.classList.add('header-container-mobile')
      mainContainer.prepend(headerContainerMobile);
      
      let text = [
        "Входные данные",
        "Результаты",
        "Конструкция"
      ]
      text.forEach(text => {
        let headerContainerMobile = document.querySelector('.header-container-mobile')
        let headerMobile = document.createElement('h1')
        headerMobile.classList.add('header-mobile')
        headerMobile.textContent = text;
        headerContainerMobile.appendChild(headerMobile);
      })
      const headerMobile = document.querySelector('h1')
      const section = document.querySelector('.container__tab')
      console.log(section)
      headerMobile.onclick = () => {

          section.style.display = 'block'
      
      }

      hasElementsBeenAdded = true  
  } else{
    let headerContainerMobile = document.querySelector('.header-container-mobile')
    headerContainerMobile.remove()
  }
 
}
window.addEventListener('resize', updateText);
window.addEventListener('load', updateText);



// Обновляем текст при загрузке страницы и при изменении размера окна


// function resizeGraph() {
//   const graphContainer = document.getElementById('graphPlotly');
//   if (graphContainer) {
//       Plotly.Plots.resize(graphContainer.querySelector('.plotly-graph-div'));
//   }
// }

function resizeGraph() {
  const graphContainer = document.getElementById('graphPlotly');
  const plotDiv = graphContainer ? graphContainer.querySelector('.plotly-graph-div') : null;

  if (plotDiv && plotDiv.offsetParent !== null) {
      Plotly.Plots.resize(plotDiv);
  }
}

// Перерисовка графика при загрузке страницы
document.addEventListener('DOMContentLoaded', resizeGraph);

// Перерисовка при изменении размера окна
window.addEventListener('resize', resizeGraph);




