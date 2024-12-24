function direct_animation (data) {
        // top исправить
        // console.log(data)
        const margin = ({ top: 0, right: 30, bottom: 30, left: 40 })

        data.sort(function (a, b) {
            return a.hnkt - b.hnkt
        })
        data.sort(function (a, b) {
            return a.hek - b.hek
        })
        data.sort(function (a, b) {
            return a.hnktjg - b.hnktjg
        })
        const maxHkp = d3.max(data, function (d) {
            return +d.hkp
        })
        const maxHek = d3.max(data, function (d) {
            return +d.hek
        })
        const maxHnkt = d3.max(data, function (d) {
            return +d.hnkt
        })

        // console.log(maxHkp)
        // console.log(data)
        // for (var i = 0; i < data.length; i++) {
        //     console.log(data[i].t);
        // }
        const chart = d3.select("#chart");
        var height = maxHkp;
        var svg = d3.select("#chart")

        var yScaleAllHeihgt = d3.scaleLinear()
            .domain([d3.min(data, function (d) { return +d.hkp; }), d3.max(data, function (d) { return +d.hkp; })])
            .range([1, height + margin.top]);

        var y_axis = d3.axisRight()
            .scale(yScaleAllHeihgt)
            .ticks(30, "f")

        svg.append("g") // высота скважины
            .attr("transform", "translate(180, 0)")
            .call(y_axis)
            .selectAll("text")
            .attr("dx", ".1em")
            .attr("dy", ".3em")
            .style("font-family", "Montserrat")
            .attr("transform", "rotate(0)")
            .style("font-size", "12px")
            .style("color", "white")

        var yScaleHek = d3.scaleLinear()
            .domain([d3.min(data, function (d) { return +d.hkp; }), d3.max(data, function (d) { return +d.hek; })])
            .range([margin.top + maxHkp, margin.top + maxHkp + maxHek]);

        var y_axisHek = d3.axisRight()
            .scale(yScaleHek)
            .ticks(2, "f")

        svg.append("g") // высота скважины
            .attr("transform", "translate(150, 0)")
            .call(y_axisHek)
            .selectAll("text")
            .attr("dx", ".1em")
            .attr("dy", ".3em")
            .style("font-family", "Montserrat")
            .attr("transform", "rotate(0)")
            .style("font-size", "12px")
            .style("color", "white")

        for (var i = 0; i < data.length; i++) {
            // console.log(data[i].hnkt)
            svg.append("rect")
                .attr("x", 30)
                .attr("y", margin.top)
                .attr("width", 90)
                .attr("height", function () {
                    return data[i].hkp;
                })
                .style("fill", "rgb(184, 110, 20")

            svg.append("rect")
                .attr("x", 30)
                .attr("y", function () {
                    return margin.top + maxHkp;
                })
                .attr("width", 90)
                .attr("height", function () {
                    return data[i].hek;
                })
                .style("fill", "rgb(184, 110, 20")

            svg.append("rect")
                .attr("x", 60)
                .attr("y", margin.top)
                .attr("width", 30)
                .attr("height", function () {
                    return data[i].hnkt;
                })
                .style("fill", "rgb(184, 110, 20")

            svg.append("rect")
                .attr("x", 28)
                .attr("y", 0)
                .attr("width", 2)
                .attr("height", function () {
                    return margin.top + maxHkp + maxHek;
                })
                .style("fill", "white")

            svg.append("rect")
                .attr("x", 120)
                .attr("y", 0)
                .attr("width", 2)
                .attr("height", function () {
                    return margin.top + maxHkp + maxHek;
                })
                .style("fill", "white")

            svg.append("rect")
                .attr("x", 0)
                .attr("y", 0)
                .attr("width", 2)
                .attr("height", function () {
                    return margin.top + maxHkp + maxHek;
                })
                .style("fill", "white")

            svg.append("rect")
                .attr("x", 150)
                .attr("y", 0)
                .attr("width", 2)
                .attr("height", function () {
                    return margin.top + maxHkp + maxHek;
                })
                .style("fill", "white")
        }

        svg.append("rect")
            .attr("x", 0)
            .attr("y", 0)
            .attr("width", 150)
            .attr("height", 2)
            .style("fill", "white")

        svg.append("rect")
            .attr("x", 0)
            .attr("y", margin.top + maxHkp + maxHek - 2)
            .attr("width", 152)
            .attr("height", 3)
            .style("fill", "white")

        svg.append("rect")
            .attr("x", 30)
            .attr("y", margin.top + maxHkp + maxHek)
            .attr("width", 92)
            .attr("height", 20)
            .style("fill", "gray")



        for (var i = 1; i < data.length; i++) {
            var delay1 = i * 12; //hnkt зависит от каких данных, от кол ва массивов, у нас же прогоняется цикл, поэтому тут только меняя delay можно подогнать 1 время выполнения
            var delay2 = i * 35; //hkp
            var delay3 = i * 20; //hek
            var delay4 = i * 2000;
            // Создаем прямоугольник
            var rectAnimFirst = svg.append("rect")
                .attr("x", 60)
                .attr("y", 0)
                .attr("width", 30)
                .attr("height", 0) // Начальная высота 0
                .style("stroke", "black")
                .style("fill", "rgb(11, 11, 100)")
                .transition()
                .delay(delay1) // Применяем задержку
                .duration(500) // Продолжительность анимации
                .attr("height", function () {
                    return data[i].hnktjg+margin.top    ; // Изменяем высоту на значение из данных
                })

            var rectAnimSmall = svg.append("rect")
                .attr("x", 30)
                .attr("y", function () {
                    return margin.top + maxHkp; // Начальная позиция по оси Y
                })
                .attr("width", 90)
                .attr("height", 0) // Начальная высота 0
                .style("fill", "rgb(11, 11, 100)")
                // .style("stroke", "black")
                .transition()
                .delay(delay3) // Применяем задержку
                .duration(100) // Продолжительность анимации
                .attr("height", function () {
                    return data[i].hekjg; // Изменяем высоту на значение из данных
                })


                svg.append("rect")
                .attr("x", 30)
                .attr("y", function () {
                    return  maxHkp - data[i].hkpjg; // Начальная позиция по оси Y
                })
                .attr("width", 30)
                .attr("height", 0) // Начальная высота 0
                .style("fill", "rgb(11, 11, 100)")
                .transition()
                .delay(delay2) // Применяем задержку
                .duration(500) // Продолжительность анимации
                .attr("height", function () {
                    return  +data[i].hkpjg+margin.top; // Изменяем высоту на значение из данных
                })



                svg.append("rect")
                .attr("x", 30)
                .attr("y", function() {
                    return margin.top;
                })
                .attr("width", 30)
                .attr("height", 0)
                .style("fill", "rgb(184, 110, 20")
                .transition()
                .delay(delay4)
                .duration(1000)
                .attr("y", function() {
                    return  maxHnkt - data[i].hnkt;
                })
                .attr("height", function() {
                    return +data[i].hnkt;
                });

                svg.append("rect")
                .attr("x", 90)
                .attr("y", function() {
                    return margin.top;
                })
                .attr("width", 30)
                .attr("height", 0)
                .style("fill", "rgb(184, 110, 20")
                .transition()
                .delay(delay4)
                .duration(1000)
                .attr("y", function() {
                    return  maxHnkt - data[i].hnkt;
                })
                .attr("height", function() {
                    return +data[i].hnkt;
                });

            svg.append("rect")
                .attr("x", 30)
                .attr("y", function () {
                    return  maxHkp - data[i].hkpjg; // Начальная позиция по оси Y
                })
                .attr("width", 30)
                .attr("height", 0) // Начальная высота 0
                .style("fill", "rgb(11, 11, 100)")
                .transition()
                .delay(delay2) // Применяем задержку
                .duration(500) // Продолжительность анимации
                .attr("height", function () {
                    return  +data[i].hkpjg+margin.top; // Изменяем высоту на значение из данных
                })

            svg.append("rect")
                .attr("x", 90)
                .attr("y", function () {
                    return  maxHkp - data[i].hkpjg; // Начальная позиция по оси Y
                })
                .attr("width", 30)
                .attr("height", 0) // Начальная высота 0
                .style("fill", "rgb(11, 11, 100)")
                .transition()
                .delay(delay2) // Применяем задержку
                .duration(500) // Продолжительность анимации
                .attr("height", function () {
                    return +data[i].hkpjg+margin.top; // Изменяем высоту на значение из данных
                })

        }
    }



function back_animation(data) {
        const margin = ({ top:0, right: 30, bottom: 30, left: 40 })
        data.sort(function (a, b) {
            return a.hnkt - b.hnkt
        })
        data.sort(function (a, b) {
            return a.hek - b.hek
        })
        data.sort(function (a, b) {
            return a.hnktjg - b.hnktjg
        })
        const maxHkp = d3.max(data, function (d) {
            return +d.hkp
        })
        const maxHkpjg = d3.max(data, function (d) {
            return +d.hkpjg
        })
        const maxHnkt = d3.max(data, function (d) {
            return +d.hnkt
        })
        const maxHek = d3.max(data, function (d) {
            return +d.hek
        })
        const maxHekjg = d3.max(data, function (d) {
            return +d.hekjg
        })
        var svg = d3.select("#chart2")

        var height = maxHkp; // сделать генерацию свг

        var yScaleAllHeihgt = d3.scaleLinear()
            .domain([d3.min(data, function (d) { return +d.hkp; }), d3.max(data, function (d) { return +d.hkp; })])
            .range([ 0,maxHkpjg  ]);

        var y_axis = d3.axisRight()
            .scale(yScaleAllHeihgt)
            .ticks(30, ".1f")

        svg.append("g") // высота скважины
            .attr("transform", "translate(200, 0)")
            .call(y_axis)
            .selectAll("text")
            .attr("dx", ".1em")
            .attr("dy", ".3em")
            .style("font-family", "Montserrat")
            .attr("transform", "rotate(0)")
            .style("font-size", "12px")
            .style("color", "white")

            var yScaleHek = d3.scaleLinear()
            .domain([d3.min(data, function (d) { return +d.hkp; }), d3.max(data, function (d) { return +d.hek; })])
            .range([margin.top + maxHkpjg, margin.top + maxHkpjg + maxHek]);
//console.log(maxHek)
        var y_axisHek = d3.axisRight()
            .scale(yScaleHek)
            .ticks(4, ".1f")


        svg.append("g") // высота скважины
            .attr("transform", "translate(150, 0)")
            .call(y_axisHek)
            .selectAll("text")
            .attr("dx", ".1em")
            .attr("dy", ".3em")
            .style("font-family", "Montserrat")
            .attr("transform", "rotate(0)")
            .style("font-size", "12px")
            .style("color", "white")
console.log(maxHkp)
console.log(maxHkpjg)
console.log(maxHek)
        for (var i = 0; i < data.length; i++) {
            svg.append("rect")
                .attr("x", 30)
                .attr("y", function () {
                    return maxHkpjg - maxHkp ;
                })
                .attr("width", 90)
                .attr("height", function () {
                    return +data[i].hkp;
                })
                .style("fill", "rgb(184, 110, 20")


            svg.append("rect")
                .attr("x", 30)
                .attr("y", function () {
                    return margin.top + maxHkpjg;
                })
//                .style("stroke", "black")
                .attr("width", 90)
                .attr("height", function () {
                    return +data[i].hek;
                })
                .style("fill", "rgb(184, 110, 20")
console.log(maxHek)
            // svg.append("rect")
            //     .attr("x", 60)
            //     .attr("y", 0)
            //     .attr("width", 30)
            //     .attr("height", function () {
            //         return data[i].hnkt;
            //     })
            //     .style("fill", "rgb(184, 110, 20")

            svg.append("rect")
                .attr("x", 28)
                .attr("y", 0)
                .attr("width", 2)
                .attr("height", function () {
                    return margin.top + maxHkpjg + maxHek;
                })
                .style("fill", "white")

            svg.append("rect")
                .attr("x", 120)
                .attr("y", 0)
                .attr("width", 2)
                .attr("height", function () {
                    return margin.top + maxHkpjg + maxHek;
                })
                .style("fill", "white")

            svg.append("rect")
                .attr("x", 0)
                .attr("y", 0)
                .attr("width", 2)
                .attr("height", function () {
                    return margin.top + maxHkpjg + maxHek;
                })
                .style("fill", "white")

            svg.append("rect")
                .attr("x", 150)
                .attr("y", 0)
                .attr("width", 2)
                .attr("height", function () {
                    return margin.top + maxHkpjg + maxHek;
                })
                .style("fill", "white")
        }

        svg.append("rect")
            .attr("x", 0)
            .attr("y", 0)
            .attr("width", 150)
            .attr("height", 2)
            .style("fill", "white")

        svg.append("rect")
            .attr("x", 0)
            .attr("y", margin.top + maxHkpjg + maxHek)
            .attr("width", 152)
            .attr("height", 3)
            .style("fill", "white")

        svg.append("rect")
            .attr("x", 30)
            .attr("y", margin.top + maxHkpjg + maxHek)
            .attr("width", 92)
            .attr("height", 20)
            .style("fill", "gray")

        for (var i = 1; i < data.length; i++) {
            var delay1 = i * 10; //hnkt зависит от колва данных, от кол ва массивов, у нас же прогоняется цикл, поэтому тут только меняя delay можно подогнать 1 время выполнения
            var delay2 = i * 30; //hkp
            var delay3 = i * 20; //hek
            var delay4 = i * 250; //hek

            svg.append("rect")
                .attr("x", 60)
                .attr("y", function () {
                    return maxHnkt - data[i].hnktjg;
                })
                .attr("width", 30)
                .attr("height", 0)
                .style("stroke", "black")
                .style("fill", "rgb(11, 11, 100)")
                .transition()
                .delay(delay2)
                .duration(500)
                .attr("height", function () {
                    return data[i].hnktjg;
                })


                svg.append("rect")
                .attr("x", 60)
                .attr("y", function() {
                    return maxHkpjg - maxHkp ;
                })
                .attr("width", 30)
                .attr("height", 0)
                .style("fill", "rgb(184, 110, 20")
                .transition()
                .delay(delay4)
                .duration(500)
                .attr("y", function() {
                    return margin.top + maxHkp - data[i].hnkt;
                })
                .attr("height", function() {
                    return data[i].hnkt;
                });

            svg.append("rect")
                .attr("x", 30)
                .attr("y", function () {
                    return maxHnkt;
                })
                .attr("width", 90)
                .attr("height", 0)
                // .style("stroke", "black")
                .style("fill", "rgb(11, 11, 100)")
                .transition()
                .delay(delay3)
                .duration(500)
                .attr("height", function () {
                    return data[i].hekjg;
                })

            svg.append("rect")
                .attr("x", 30)
                .attr("y", function () {
                    return;
                })
                .attr("width", 30)
                .attr("height", 0)
                .style("fill", "rgb(11, 11, 100)")
                .transition()
                .delay(delay1)
                .duration(500)
                .attr("height", function () {
                    return data[i].hkpjg;
                })

            svg.append("rect")
                .attr("x", 90)
                .attr("y", function () {
                    return;
                })
                .attr("width", 30)
                .attr("height", 0)
                .style("fill", "rgb(11, 11, 100)")
                .transition()
                .delay(delay1)
                .duration(500)
                .attr("height", function () {
                    return data[i].hkpjg;
                })
        }
    }

// Убедитесь, что весь код выполняется после загрузки DOM
document.addEventListener('DOMContentLoaded', function() {
    // Получаем значение type_of_glush из data-атрибута body
    const typeOfGlush = document.body.dataset.typeOfGlush;

    // Получаем все элементы с классом "well-contruction"
    const wellConstruction = document.querySelectorAll(".well-contruction");

    // Обработчик клика для каждой "well-contruction"
    wellConstruction.forEach(function(well) {
        well.addEventListener('click', function() {
            let needed_div;
            let animationFunction;

            if (typeOfGlush === "direct") {
                needed_div = document.getElementById("chart");
                animationFunction = direct_animation;
            } else {
                needed_div = document.getElementById("chart2");
                animationFunction = back_animation;
            }

            if (needed_div) {
                needed_div.innerHTML = '';
                console.log(data);
                animationFunction(data);
            } else {
                console.error(`Элемент с id "${typeOfGlush === "direct" ? "chart" : "chart2"}" не найден.`);
            }
        });
    });
});
