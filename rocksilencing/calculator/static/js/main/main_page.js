// tabs //

document.getElementById('input__file').addEventListener('change', function () {
  let fileName = this.files.length > 0 ? Array.from(this.files).map(file => file.name).join(', ') : 'Импорт';
  document.getElementById('file-name-text').textContent = fileName;
  document.getElementById
}
);
document.getElementById('input__file-NKT').addEventListener('change', function () {
  let fileName = this.files.length > 0 ? Array.from(this.files).map(file => file.name).join(', ') : 'Импорт';
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

let firstSection = document.querySelector('.container__tab');
if (firstSection) {
  document.getElementById('toggleIcon1').addEventListener('click', function () {

    if (containerTab.style.display === 'none') {
      containerTab.style.display = 'block';
    } else {
      containerTab.style.display = 'none';
    }
  });
}

let secondSection = document.querySelector('.second_section');
if (secondSection) {
  document.getElementById('toggleIcon2').addEventListener('click', function () {
    if (containerTab.style.display === 'none') {
      containerTab.style.display = 'block';
    } else {
      containerTab.style.display = 'none';
    }
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

  });
}

let thirdSection = document.querySelector('.third_section');
if (thirdSection) {
  document.getElementById('toggleIcon3').addEventListener('click', function () {

    if (containerTab.style.display === 'none') {
      containerTab.style.display = 'block';
    } else {
      containerTab.style.display = 'none';
    }
  });
}



function resizeGraph() {
  const graphContainer = document.getElementById('graphPlotly');
  const plotDiv = graphContainer ? graphContainer.querySelector('.plotly-graph-div') : null;

  if (plotDiv && plotDiv.offsetParent !== null) {
    Plotly.Plots.resize(plotDiv);
  }
}

document.addEventListener('DOMContentLoaded', resizeGraph);
window.addEventListener('resize', resizeGraph);
window.addEventListener('resize', mobile);
window.addEventListener('load', mobile);

let hasElementsBeenAdded = false;
let sectionsHidden = false;

function mobile() {

  const mainContainer = document.querySelector('main');
  const headerContainerMobile = document.querySelector('.header-container-mobile');
  const sections = document.querySelectorAll('.container__tab, .second_section, .third_section');
  let linkDownload = document.querySelector('.download-report-mobile')
  const urlContainer = document.getElementById('url-container');
 
 

  const rows = document.querySelectorAll('.injection-scenarious tr');

  const headersInjection = document.querySelectorAll('.header-table-inject td')
  let buttonStageNext = document.querySelector('.next-stage-image')
  let buttonStagePrevious = document.querySelector('.previous-stage-image')


  if (document.documentElement.clientWidth <= 500) {

    if (!sectionsHidden) {
      sections.forEach((section, index) => {
        section.style.display = index === 0 ? 'block' : 'none';
      });
      sectionsHidden = true;
    }

    if (!headerContainerMobile) {
      let newHeaderContainerMobile = document.createElement('div');
      newHeaderContainerMobile.classList.add('header-container-mobile');
      mainContainer.prepend(newHeaderContainerMobile);


      let titles = [
        "Входные данные",
        "Результаты",
        "Конструкция"
      ];

      titles.forEach(text => {
        let headerMobile = document.createElement('h1');
        headerMobile.classList.add('header-mobile');
        headerMobile.textContent = text;
        newHeaderContainerMobile.appendChild(headerMobile);

        headerMobile = document.querySelectorAll('.header-mobile')
        headerMobile.forEach((header, index) => {
          header.setAttribute('data-target', `#section${index + 1}`);
        })

        if (headerMobile.length > 0) {
          headerMobile[0].classList.add('active');
        }
        headerMobile.forEach((header, index) => {
          header.onclick = () => {
            sections.forEach(section => {
              section.style.display = 'none';
            });
            if (sections[index]) {
              sections[index].style.display = 'block';
            }

            headerMobile.forEach(header => {
              header.classList.remove('active');
            });


            header.classList.add('active');

            resizeGraph();
          }

        })
      });

      hasElementsBeenAdded = true;
    }
    if (!linkDownload) {
      const linkDownload = document.createElement('a');
      linkDownload.classList.add('download-report-mobile')
      if(thirdSection){
        const downloadUrl = urlContainer.getAttribute('data-download-url');
        linkDownload.href = downloadUrl;
        linkDownload.textContent = "Скачать отчёт";
        sections[1].append(linkDownload);
  
        hasElementsBeenAdded = true;
      }
    
    }
    //Таблица стадий


    headersInjection.forEach((header, index) => {
      if (index > 0) {
        if (!buttonStageNext && !buttonStagePrevious) {
          const buttonStageNext = document.createElement('img')
          buttonStageNext.src = '../static/images/main/Vector 395.svg'
          buttonStageNext.classList.add('next-stage-image')
          const buttonStagePrevious = document.createElement('img')
          buttonStagePrevious.src = '../static/images/main/Vector 396.svg'
          buttonStagePrevious.classList.add('previous-stage-image')
          header.appendChild(buttonStageNext);
          header.prepend(buttonStagePrevious);
          buttonStageNext.onclick = nextStage;
          buttonStagePrevious.onclick = previousStage;
          hasElementsBeenAdded = true;
        }

      }


    })

    let currentStage = 1;

    //Отображаем только первую стадию в начале
    rows.forEach(row => {
      for (let i = 2; i <= 4; i++) {
        const cell = row.querySelector(`.stage-${i}`);
        if (cell) {
          cell.style.display = 'none'
        }
      }
    });

    function nextStage() {
      changeStage(currentStage + 1);
    }

    function previousStage() {
      changeStage(currentStage - 1);
    }
    function changeStage(newStage) {
      const rows = document.querySelectorAll('.injection-scenarious tr');
      currentStage = Math.max(1, Math.min(4, newStage));

      // Переключение данных по стадиям
      rows.forEach(row => {
        for (let i = 1; i <= 4; i++) {
          const cell = row.querySelector(`.stage-${i}`);
          if (cell) {
            cell.style.display = (i === currentStage) ? '' : 'none';
          }
        }
      });
    }


  } else {
    if (headerContainerMobile) {
      headerContainerMobile.remove();
      hasElementsBeenAdded = false;

      sections.forEach(section => {
        section.style.display = 'block';
      });

      sectionsHidden = false;
    }
    if (linkDownload) {
      linkDownload.remove();
      hasElementsBeenAdded = false;
    }
    if (buttonStageNext && buttonStagePrevious) {
      buttonStageNext = document.querySelectorAll('.next-stage-image')
      buttonStageNext.forEach(button => {
        button.remove()
      })
      buttonStagePrevious = document.querySelectorAll('.previous-stage-image')
      buttonStagePrevious.forEach(button => {
        button.remove()
      })
      hasElementsBeenAdded = false
    }

    const cell = document.querySelectorAll('.injection-scenarious td')
    cell.forEach(cell => {
      cell.style.display = 'table-cell'
    })
  }
}

function demonstrate() {
  let mest = document.getElementById("field")
  let field = document.getElementById("bush")
  let well_name = document.getElementById("well_name")
  let design_name = document.getElementById('design_name')
  let porosity = document.getElementById('id_Porosity')
  let oil_density = document.getElementById('id_Oil_density')
  let Plast_pressure = document.getElementById('id_Plast_pressure')
  let Radius_countour = document.getElementById("id_Radius_countour")
  let Plast_thickness = document.getElementById('id_Plast_thickness')
  let From_yst_to_plast = document.getElementById('id_From_yst_to_plast')
  let False_zaboi = document.getElementById('id_False_zaboi')
  let True_zaboi = document.getElementById('id_True_zaboi')
  let NKT_length = document.getElementById("id_NKT_length")
  let NKT_inner_diameter = document.getElementById("id_NKT_inner_diameter")
  let NKT_external_diameter = document.getElementById('id_NKT_external_diameter')
  let EXP_length = document.getElementById('id_EXP_length')
  let EXP_inner_diameter = document.getElementById('id_EXP_inner_diameter')
  let EXP_external_diameter = document.getElementById('id_EXP_external_diameter')
  let Volume_of_car = document.getElementById('id_Volume_of_car')
  let Debit = document.getElementById('id_Debit')
  let YV_density = document.getElementById("id_YV_density")
  let YV_dole = document.getElementById('id_YV_dole')
  let Emul_density = document.getElementById("id_Emul_density")
  let Emul_dole = document.getElementById('id_Emul_dole')
  let Phase_oil_permeability = document.getElementById('id_Phase_oil_permeability')
  let Phase_jgs_permeability = document.getElementById('id_Phase_jgs_permeability')
  let Oil_viscosity = document.getElementById('id_Oil_viscosity')
  let Jgs_viscosity = document.getElementById('id_Jgs_viscosity')
  let Zapas = document.getElementById("id_Zapas")


  mest.value = 'Самотлорское';
  field.value = '332'
  well_name.value = '8971'
  design_name.value = 'Дизайн 1'
  porosity.value = 0.2
  oil_density.value = 800
  Plast_pressure.value = 100
  Radius_countour.value = 250
  Plast_thickness.value = 10
  From_yst_to_plast.value = 1400
  False_zaboi.value = 1500
  True_zaboi.value = 1500
  NKT_length.value = 1400
  NKT_inner_diameter.value = 0.062
  NKT_external_diameter.value = 0.073
  EXP_length.value = 100
  EXP_inner_diameter.value = 0.15
  EXP_external_diameter.value = 0.163
  Volume_of_car.value = 20
  Debit.value = 0.01
  YV_density.value = 0.88
  YV_dole.value = 0.16
  Emul_density.value = 0.8
  Emul_dole.value = 0.04
  Phase_oil_permeability.value = 0.5
  Phase_jgs_permeability.value = 1.5
  Oil_viscosity.value = 0.005
  Jgs_viscosity.value = 0.001
  Zapas.value = 0.1
}







