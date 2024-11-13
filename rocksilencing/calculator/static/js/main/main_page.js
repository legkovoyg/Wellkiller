// tabs //

document.getElementById('input__file').addEventListener ('change', function() {
  var fileName = this.files.length > 0 ? Array.from(this.files).map(file => file.name).join(', ') : 'Импорт';
  document.getElementById('file-name-text').textContent = fileName;
  document.getElementById }
);
document.getElementById('input__file-NKT').addEventListener ('change', function() {
  var fileName = this.files.length > 0 ? Array.from(this.files).map(file => file.name).join(', ') : 'Импорт';
  document.getElementById('file-name-text-NKT').textContent = fileName;
  document.getElementById }
);

document.querySelectorAll('.tabs-wrapper').forEach((e) => {
  let tabTabs = e.querySelectorAll('.tabs .tab');
  let tabItems = e.querySelectorAll('.tabs-items .item');
    for(let i =0;i<tabTabs.length;i++) {
        tabTabs[0].click();
         tabTabs[i].onclick = () => {
          tabTabs.forEach((e)  => { e.classList.remove('on') }); 
          tabItems.forEach((e)  => { e.classList.remove('on') });
          tabTabs[i].classList.add('on');
          tabItems[i].classList.add('on');
     }
   }
 });

document.getElementById('toggleIcon1').addEventListener('click', function() {
    var containerTab = document.querySelector('.container__tab');
    if (containerTab.style.display === 'none') {
        containerTab.style.display = 'block';
    } else {
        containerTab.style.display = 'none';
    }
});

document.getElementById('toggleIcon2').addEventListener('click', function() {
    var containerTab = document.querySelector('.second_section');
    if (containerTab.style.display === 'none') {
        containerTab.style.display = 'block';
    } else {
        containerTab.style.display = 'none';
    }
});

document.getElementById('toggleIcon3').addEventListener('click', function() {
    var containerTab = document.querySelector('.third_section');
    if (containerTab.style.display === 'none') {
        containerTab.style.display = 'block';
    } else {
        containerTab.style.display = 'none';
    }
});

const svgImage = document.querySelectorAll(".main-svg")
console.log(svgImage);
const pressureGraph = document.getElementById("pressure_graph")
const graphSelect = document.getElementById('graph_select')
graphSelect.addEventListener('change', function(){
  if (graphSelect.value === "pressure_graph"){
    for(let i=0; i <= svgImage.length; i++){
      svgImage[i].classList.remove("hidden")
      svgImage[i].classList.add("visible")
    }
  } else {
    for(let i=0; i < svgImage.length; i++){
      svgImage[i].classList.remove("visible")
      svgImage[i].classList.add("hidden")    }
  }
})


// PLOT/GRAPH //

// Set dimensions and margins for the chart

const margin = { top: 70, right: 30, bottom: 40, left: 80 };
const width = 1200 - margin.left - margin.right;
const height = 500 - margin.top - margin.bottom;

// Set up the x and y scales

const x = d3.scaleTime()
  .range([0, width]);

const y = d3.scaleLinear()
  .range([height, 0]);


// Create the line generator

const line = d3.line()
  .x(d => x(d.date))
  .y(d => y(d.population));
// Create the SVG element and append it to the chart container

const svg = d3.select("#chart-container")
  .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

// create tooltip div

// const tooltip = d3.select("#testtooltip")
//   .append("div")
//   .attr("class", "tooltip");

// Create a fake data

d3.csv("/mainPage/jdi_data_daily.csv").then(function (data) {
    
  // Parse the date and convert the population to a number
  const parseDate = d3.timeParse("%Y-%m-%d");
  data.forEach(d => {
    d.date = parseDate(d.date);
    d.population = +d.population;
  });
    console.log(data)


// Define the x and y domains

x.domain(d3.extent(data, d => d.date));
y.domain([90000, d3.max(data, d => d.population)]);


  // Add the x-axis
  svg.append("g")
  .style("font-family", "inter")
    .attr("transform", `translate(0,${height})`)
    .style("font-size", "14px")
    .call(d3.axisBottom(x)
      .tickValues(x.ticks(d3.timeMonth.every(6))) 
      .tickFormat(d3.timeFormat("%b %Y"))) 
    .call(g => g.select(".domain").remove()) 
    .selectAll(".tick line") 
    .style("stroke-opacity", 0)
  svg.selectAll(".tick text")
    .attr("fill", "#777");


// Add the y-axis
svg.append("g")
.style("font-family", "inter")
.style("font-size", "14px")
.call(d3.axisLeft(y)
  .ticks((d3.max(data, d => d.population) - 65000) / 5000)
  .tickFormat(d => {
      return `${(d / 1000).toFixed(0)}k`;
  })
  .tickSize(0)
  .tickPadding(10))
.call(g => g.select(".domain").remove()) 
.selectAll(".tick text")
.style("fill", "#777") 
.style("visibility", (d, i, nodes) => {
  if (i === 0) {
    return "hidden"; 
  } else {
    return "visible"; 
  }
});

// Add vertical gridlines
svg.selectAll("xGrid")
.data(x.ticks().slice(1))
.join("line")
.attr("x1", d => x(d))
.attr("x2", d => x(d))
.attr("y1", 0)
.attr("y2", height)
.attr("stroke", "#e0e0e0")
.attr("stroke-width", .1);

// Add horizontal gridlines

svg.selectAll("yGrid")
.data(y.ticks((d3.max(data, d => d.population) - 65000) / 5000).slice(1))
.join("line")
.attr("x1", 0)
.attr("x2", width)
.attr("y1", d => y(d))
.attr("y2", d => y(d))
.attr("stroke", "#e0e0e0")
.attr("stroke-width", .1)




// Add the line path to the SVG element

svg.append("path")
  .datum(data)
  .attr("fill", "none")
  .attr("stroke", "green")
  .attr("stroke-width", 1)
  .attr("d", line);


// Add a circle element

const circle = svg.append("circle")
 .attr("r", 0)
 .attr("fill", "green")
 .style("stroke", "white")
 .attr("opacity", .70)
 .style("pointer-events", "none");



const listeningRect = svg.append("rect")
 .attr("width", width)
 .attr("height", height);


// nasha mouse 

 listeningRect.on("mousemove", function (event) {
  const [xCoord] = d3.pointer(event, this);
  const bisectDate = d3.bisector(d => d.date).left;
  const x0 = x.invert(xCoord);
  const i = bisectDate(data, x0, 1);
  const d0 = data[i - 1];
  const d1 = data[i];
  const d = x0 - d0.date > d1.date - x0 ? d1 : d0;
  const xPos = x(d.date);
  const yPos = y(d.population);

// update circle

circle.attr("cx", xPos)
      .attr("cy", yPos);

      // console.log(xPos)
 })
//////
 circle.transition()
      .duration(50)
      .attr("r", 5);

    // add in  our tooltip

    tooltip
      .style("display", "block")
      .style("left", `${xPos + 100}px`)
      .style("top", `${yPos + 50}px`)
      .html(`<strong>Date:</strong> ${d.date.toLocaleDateString()}<br><strong>Population:</strong> ${d.population !== undefined ? (d.population / 1000).toFixed(0) + 'k' : 'N/A'}`)
  });
  // listening rectangle mouse leave function

  listeningRect.on("mouseleave", function () {
    circle.transition()
      .duration(50)
      .attr("r", 0);

    tooltip.style("display", "none");
  });
  
  
// // Add Y-axis label

svg.append("text")
.attr("transform", "rotate(-90)")
.attr("y", 0 - margin.left)
.attr("x", 0 - (height / 2))
.attr("dy", "1em")
.style("text-anchor", "middle")
.style("font-size", "20px")
.style("fill", "#777")
.style("font-family", "inter")
.text("Количество заключенных");

svg.append("text")
.attr("transform", "rotate(90)")   
.attr("y", 0 - (width / 2))
.attr("x", 0 - margin.right)
.attr("dy", "1em")
.style("text-anchor", "middle")
.style("font-size", "20px")
.style("fill", "#777")
.style("font-family", "inter")
.text("Время");

// Add the chart title

svg.append("text")
.attr("class", "chart-title")
.attr("x", margin.left - 115)
.attr("y", margin.top - 100)
.style("font-size", "24px")
.style("font-weight", "bold")
.style("font-family", "inter")
.text("Тестовый график для обучения(график численности заключенных)");


function demonstrate(){
var mest = document.getElementById("field")
var field = document.getElementById("bush")
var well_name = document.getElementById("well_name")
var design_name = document.getElementById('design_name')
var porosity = document.getElementById('id_Porosity')
var oil_density = document.getElementById('id_Oil_density')
var Plast_pressure = document.getElementById('id_Plast_pressure')
var Radius_countour = document.getElementById("id_Radius_countour")
var Plast_thickness = document.getElementById('id_Plast_thickness')
var From_yst_to_plast = document.getElementById('id_From_yst_to_plast')
var False_zaboi = document.getElementById('id_False_zaboi')
var True_zaboi = document.getElementById('id_True_zaboi')
var NKT_length = document.getElementById("id_NKT_length")
var NKT_inner_diameter = document.getElementById("id_NKT_inner_diameter")
var NKT_external_diameter = document.getElementById('id_NKT_external_diameter')
var EXP_length = document.getElementById('id_EXP_length')
var EXP_inner_diameter = document.getElementById('id_EXP_inner_diameter')
var EXP_external_diameter = document.getElementById('id_EXP_external_diameter')
var Volume_of_car = document.getElementById('id_Volume_of_car')
var Debit = document.getElementById('id_Debit')
var YV_density = document.getElementById("id_YV_density")
var YV_dole = document.getElementById('id_YV_dole')
var Emul_density = document.getElementById("id_Emul_density")
var Emul_dole = document.getElementById('id_Emul_dole')
var Phase_oil_permeability = document.getElementById('id_Phase_oil_permeability')
var Phase_jgs_permeability = document.getElementById('id_Phase_jgs_permeability')
var Oil_viscosity = document.getElementById('id_Oil_viscosity')
var Jgs_viscosity = document.getElementById('id_Jgs_viscosity')
var Zapas = document.getElementById("id_Zapas")


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
console.log(mest.value)};



