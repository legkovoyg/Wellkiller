
// Константы для расчетов
var constanta_Cl = 35.453
var constanta_SO4 = 96.062
var constanta_HCO3 = 61.016
var constanta_Ca = 40.078
var constanta_Mg = 24.305
var constanta_Na = 22.99
var constanta_Ba = 137.33
var constanta_Sr = 87.62

// Переменные для первых инпутов (да я знаю что так нельзя писать)

// Сам инпут моль/кг
var Cl_1_input = 'id_Cl_1'
// Сам инпут мг/л
var Cl_1_another_input = 'id_Cl_1_another'
// Число обозначающее номер инпута в таблице (крайний слева)
var CL_1_input_number = "Cl_number_1"
var SO4_1_input = 'id_SO4_1'
var SO4_1_another_input = 'id_SO4_1_another'
var SO4_1_input_number = "SO4_number_1"
var HCO3_1_input = 'id_HCO3_1'
var HCO3_1_another_input = 'id_HCO3_1_another'
var HCO3_1_input_number = "HCO3_number_1"
var Ca_1_input = 'id_Ca_1'
var Ca_1_another_input = 'id_Ca_1_another'
var Ca_1_input_number = "Ca_number_1"
var Mg_1_input = 'id_Mg_1'
var Mg_1_another_input = 'id_Mg_1_another'
var Mg_1_input_number = "Mg_number_1"
var Na_1_input = 'id_Na_1'
var Na_1_another_input = 'id_Na_1_another'
var Na_1_input_number = "Na_number_1"
var Ba_1_input = 'id_Ba_1'
var Ba_1_another_input = 'id_Ba_1_another'
var Ba_1_input_number = "Ba_number_1"
var Sr_1_input = 'id_Sr_1'
var Sr_1_another_input = 'id_Sr_1_another'
var Sr_1_input_number = "Sr_number_1"

// Переменные для вторых инпутов
var Cl_2_input = 'id_Cl_2'
var Cl_2_another_input = 'id_Cl_2_another'
var Cl_2_input_number = "Cl_number_2"
var SO4_2_input = 'id_SO4_2'
var SO4_2_another_input = 'id_SO4_2_another'
var SO4_2_input_number = "SO4_number_2"
var HCO3_2_input = 'id_HCO3_2'
var HCO3_2_another_input = 'id_HCO3_2_another'
var HCO3_2_input_number = "HCO3_number_2"
var Ca_2_input = 'id_Ca_2'
var Ca_2_another_input = 'id_Ca_2_another'
var Ca_2_input_number = "Ca_number_2"
var Mg_2_input = 'id_Mg_2'
var Mg_2_another_input = 'id_Mg_2_another'
var Mg_2_input_number = "Mg_number_2"
var Na_2_input = 'id_Na_2'
var Na_2_another_input = 'id_Na_2_another'
var Na_2_input_number = "Na_number_2"
var Ba_2_input = 'id_Ba_2'
var Ba_2_another_input = 'id_Ba_2_another'
var Ba_2_input_number = "Ba_number_2"
var Sr_2_input = 'id_Sr_2'
var Sr_2_another_input = 'id_Sr_2_another'
var Sr_2_input_number = "Sr_number_2"

var ro_smesi_1 = "density_1"
var ro_smesi_2 = "density_2"

function form_update (concent_1, concent_2, ro_id, multiplier) {
    var mole_value = document.getElementById(concent_1);
    var mg_value = document.getElementById(concent_2);
    var ro_smesi_1 = document.getElementById(ro_id);
    if (mole_value && mg_value && ro_smesi_1) {
        mole_value.addEventListener('input', function() {
            var newValue = parseFloat(mole_value.value);
            mg_value.value = (newValue*(1000*multiplier*ro_smesi_1.value)).toFixed(5);
        });

        mg_value.addEventListener('input', function() {
            var newValue = parseFloat(mg_value.value);
            mole_value.value = (newValue / (1000 * multiplier * ro_smesi_1.value)).toFixed(5);
        });
    }
};

document.addEventListener('DOMContentLoaded', function() {
    form_update(Cl_1_input, Cl_1_another_input, ro_smesi_1, constanta_Cl)
    form_update(SO4_1_input, SO4_1_another_input, ro_smesi_1, constanta_SO4)
    form_update(HCO3_1_input, HCO3_1_another_input, ro_smesi_1, constanta_HCO3)
    form_update(Ca_1_input, Ca_1_another_input, ro_smesi_1, constanta_Ca)
    form_update(Mg_1_input, Mg_1_another_input, ro_smesi_1, constanta_Mg)
    form_update(Na_1_input, Na_1_another_input, ro_smesi_1, constanta_Na)
    form_update(Ba_1_input, Ba_1_another_input, ro_smesi_1, constanta_Ba)
    form_update(Sr_1_input, Sr_1_another_input, ro_smesi_1, constanta_Sr)

    form_update(Cl_2_input, Cl_2_another_input, ro_smesi_2, constanta_Cl)
    form_update(SO4_2_input, SO4_2_another_input, ro_smesi_2, constanta_SO4)
    form_update(HCO3_2_input, HCO3_2_another_input, ro_smesi_2, constanta_HCO3)
    form_update(Ca_2_input, Ca_2_another_input, ro_smesi_2, constanta_Ca)
    form_update(Mg_2_input, Mg_2_another_input, ro_smesi_2, constanta_Mg)
    form_update(Na_2_input, Na_2_another_input, ro_smesi_2, constanta_Na)
    form_update(Ba_2_input, Ba_2_another_input, ro_smesi_2, constanta_Ba)
    form_update(Sr_2_input, Sr_2_another_input, ro_smesi_2, constanta_Sr)
});


function limitLength(event) {
    const input = event.target;
    const maxLength = 7; // Максимальное количество символов, включая десятичный разделитель
    const value = input.value;

    // Проверяем, есть ли введенные данные
    if (value === '') return;

    // Разбиваем введенное значение на целую и дробную части
    const parts = value.split('.');
    const integerPart = parts[0];
    const decimalPart = parts[1] || '';

    // Проверяем длину целой части
    if (integerPart.length >= maxLength - decimalPart.length) {
        // Если длина целой части превышает допустимое значение, обрезаем ее
        input.value = integerPart.substring(0, maxLength - decimalPart.length);
    }
}

//var elements = document.getElementsByClassName('number_of_element');
//Array.from(elements).forEach(function(element) {
//    element.addEventListener("focus", function() {
//        // Меняем цвет целевого элемента при фокусировке на инпуте
//        element.style.Color = "blue";
//    });
//    element.addEventListener("blur", function() {
//        // Меняем цвет целевого элемента при потере фокуса
//        element.style.Color = "red";
//    });
//});
//console.log(elements)



//// Получаем все инпуты формы form
//var formInputs = document.querySelectorAll('input');
//console.log(formInputs)
//// Добавляем обработчик события click к каждому инпуту формы form
//formInputs.forEach(function(input) {
//    input.addEventListener('focus', function() {
//        // Получаем значение инпута
//        var value = this.value;
//        console.log(value)
//        // Получаем соответствующий элемент <td> с классом 'number_of_element'
//        var tdElement = this.closest('tr').querySelector('.number_of_element');
//        console.log(tdElement)
//        // Меняем цвет текста в <td>
//        if (value === 'NaN' ) {
//            tdElement.style.color = ''; // Возвращаем стандартный цвет, если значение пустое
//        }
//        else {
//            tdElement.style.color = '#1d9a6c'; // Или любой другой цвет, который вы хотите установить
//        }
//    });
//});

