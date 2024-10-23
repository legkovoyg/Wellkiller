import plotly.express as px
import os
import logging
import json
import numpy as np
import pandas as pd
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from calculator.forms import Scale_Calculator_form_1, Scale_Calculator_form_2, ModelGlushForm
from calculator.custom_fuctions.Method_for_salt_calculator import calculate_full_result
from calculator.custom_fuctions.graph_method import create_plot
from calculator.custom_fuctions.matmodel_glush.Matmodel import matmodel_glush
from calculator.custom_fuctions.matmodel_glush.matmodel_graph.graph_pressures import create_matmodel_plot
from docxtpl import DocxTemplate
from calculator.models import Salt, Solution
from sklearn.linear_model import LinearRegression



# Страница калькулятора

def handle_excel_file(excel_file):
    if excel_file:
        excel_df = pd.read_excel(excel_file, engine='openpyxl')
        excel_datas = excel_df.to_dict(orient='list')
        result = [{'count': count, 'md_start': md_start, 'md_end': md_end, 'tvd_start': tvd_start, 'tvd_end': tvd_end, 
                   'ext_d': ext_d, 'thick': thick} 
                  for count, md_start, md_end, tvd_start, tvd_end, ext_d, thick 
                  in zip(excel_datas['count'], excel_datas['md_start'], excel_datas['md_end'], 
                         excel_datas['tvd_start'], excel_datas['tvd_end'], 
                         excel_datas['ext_d'], excel_datas['thick'])]
        
        x = np.array(excel_datas['md_start'])
        y = np.array(excel_datas['tvd_start'])
        coefficients = np.polyfit(x, y, 1)
        polynomial = np.poly1d(coefficients)
    else:
        result = []
        polynomial = 1
    return result, polynomial

def get_form_data(request):
    return {
        # Общие данные
        "Oil_field_name": str(request.POST['Oil_field_name']),
        "Bush_name": str(request.POST["Bush_name"]),
        "Well_name": str(request.POST['Well_name']),
        "Design_name": str(request.POST["Design_name"]),
        "EXP_type":str(request.POST['EXP_type']),
        "Porosity": float(request.POST['Porosity']),
        "Oil_density": float(request.POST["Oil_density"]),
        "Plast_pressure": float(request.POST["Plast_pressure"]),
        "Radius_countour": float(request.POST['Radius_countour']),
        "Plast_thickness": float(request.POST["Plast_thickness"]),
        "Length_of_Well": float(request.POST["True_zaboi"]),
        "False_zaboi":float(request.POST["False_zaboi"]),
        # Колонна и скважина
        "L_of_Wells": float(request.POST["NKT_length"]),
        "NKT_inner_diameter": float(request.POST["NKT_inner_diameter"]),
        "NKT_external_diameter": float(request.POST["NKT_external_diameter"]),
        "EXP_inner_diameter": float(request.POST["EXP_inner_diameter"]),
        "EXP_external_diameter": float(request.POST["EXP_external_diameter"]),

        #НКТ и штанги
        #Способ закачки
        "Volume_of_car": float(request.POST['Volume_of_car']),
        "Debit": float(request.POST["Debit"]),
        "YV_density": float(request.POST["YV_density"]),
        "YV_dole": float(request.POST["YV_dole"]),
        "Emul_density": float(request.POST["Emul_density"]),
        "Emul_dole": float(request.POST["Emul_dole"]),
        "Type_of_jgs": str(request.POST['Type_of_jgs']),
        "Phase_oil_permeability": float(request.POST["Phase_oil_permeability"]) / 10 ** 12,
        "Phase_jgs_permeability": float(request.POST["Phase_jgs_permeability"]) / 10 ** 12,
        "Oil_viscosity": float(request.POST["Oil_viscosity"]),
        "Jgs_viscosity": float(request.POST["Jgs_viscosity"]),
        "Zapas": float(request.POST["Zapas"]),
        "Type_of_jamming": str(request.POST['Type_of_jamming'])
    }

def process_calculations(data, polynominal):
    bd_CaCl = Solution.objects.filter(salt__name="CaCl")
    bd_CaJG = Solution.objects.filter(salt__name="CaЖГ")
    bd_CaKCl = Solution.objects.filter(salt__name="KCl")
    
    results = matmodel_glush(
        data['Plast_pressure'] * 101325, data['Plast_thickness'], data['Length_of_Well'], data['L_of_Wells'], data['Oil_density'], 
        data['NKT_inner_diameter'], data['NKT_external_diameter'], data['EXP_inner_diameter'], data['EXP_external_diameter'], data['Debit'], data['Phase_jgs_permeability'], data['Jgs_viscosity'], 
        data['Phase_oil_permeability'], data['Oil_viscosity'], data['Radius_countour'], data['Porosity'], 30, data['YV_density'], data['YV_dole'], 
        data['Emul_density'], data['Emul_dole'], data['Zapas'], bd_CaCl, bd_CaJG, chosen_salt=data['Type_of_jgs'], 
        volume_car=data['Volume_of_car'], type_of_glush=data['Type_of_jamming'], polynom=polynominal
    )
    
    return results

def render_with_results(request, form, results, result, polynomial, form_data):
    current_results = results[0]
    time = [elem / 60 for elem in results[2]]
    graph = create_matmodel_plot(results[1], time)
    design, stages, recipes_all, data_for_animation = results[3], results[4], results[5], results[6]

    keys = ["Oil_field_name", 
    "Bush_name",
    "Well_name",
    "Design_name",
    "EXP_type",
    "Porosity",
    "Oil_density",
    "Plast_pressure",
    "Radius_countour",
    "Plast_thickness",
    "NKT_inner_diameter",
    "NKT_external_diameter",
    "EXP_inner_diameter",
    "EXP_external_diameter",
    "Volume_of_car",
    "Debit",
    "YV_density",
    "YV_dole",
    "Emul_density",
    "Emul_dole",
    "Type_of_jgs",
    "Phase_oil_permeability",
    "Phase_jgs_permeability",
    "Oil_viscosity",
    "Jgs_viscosity",
    "Zapas",
    "Type_of_jamming"]
    report_context = {key: form_data[key] for key in keys}
    # Добавляем дополнительные элементы
    report_context.update({
    'design': design,
    'excel_file': result,
    'data_for_animation': json.dumps(data_for_animation)
    })
    request.session['report_context'] = report_context
    

    return render(request, "calculator/main_page.html", {
        "form": form,
        "results": results,
        "current_results": current_results,
        "graph": graph,
        "design": design,
        "stages": stages,
        "recipes_all": recipes_all,
        "show_download_button": True,
        "data_for_animation": json.dumps(data_for_animation),
        "excel_file": result
    })


def calculator_page(request):
    if request.method == 'POST':
        form = ModelGlushForm(request.POST, request.FILES)
        if form.is_valid():
            result, polynomial = handle_excel_file(request.FILES.get('file_upload', None))
            form_data = get_form_data(request)
            results = process_calculations(form_data, polynomial)
            return render_with_results(request, form, results, result, polynomial, form_data)
        else:
            print(form.errors)
    else:
        saved_data = request.session.get('report_context', None)
        form = ModelGlushForm(initial=saved_data if saved_data else None)
        return render(request, "calculator/main_page.html", {
            "form": form,
            "current_results": saved_data.get('current_results') if saved_data else None,
            "design": saved_data.get('design') if saved_data else None,
            "stages": saved_data.get('stages') if saved_data else None,
            "recipes_all": saved_data.get('recipes_all') if saved_data else None,
            "show_download_button": True if saved_data else None,
            "data_for_animation": saved_data.get('data_for_animation') if saved_data else None
        })



# Скачивание отчета
def download_report(request):
    report_context = request.session.get('report_context')
    if not report_context:
        return redirect('calculator_page')  # Перенаправление, если контекста нет

    if report_context['design']['DESIGN_chosen_salt_name'] != 'без соли':
        # Построение пути к файлу шаблона
        template_path = os.path.join(settings.BASE_DIR, 'calculator', 'report_templates', 'report_template_salt.docx')
        logging.debug(f"Template path: {template_path}")
    else:
        template_path = os.path.join(settings.BASE_DIR, 'calculator', 'report_templates', 'report_template_water.docx')
        logging.debug(f"Template path: {template_path}")

    # Проверка существования файла шаблона
    if not os.path.exists(template_path):
        logging.error(f"Template file not found at {template_path}")
        raise Http404("Template file not found.")

    # Загрузка шаблона и вставка данных
    doc = DocxTemplate(template_path)
    doc.render(report_context)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = 'attachment; filename="report.docx"'
    doc.save(response)
    return response


# Страница калькулятора солеотложений
def scale_calculator_page(request):
    if request.method == 'POST':
        x = [5, 15, 25, 35, 45, 55]
        y1 = [0.8, 0.6, 0.4, 0.2, 0, 0]
        y2 = [1.2, 1, 0.8, 0.6, 0.4, 0.2]
        form = Scale_Calculator_form_1(request.POST)
        form_2 = Scale_Calculator_form_2(request.POST)
        if form.is_valid():
            # Входные данные для жидкости 1
            Cl_1 = float(request.POST['Cl_1'])
            SO4_1 = float(request.POST['SO4_1'])
            HCO3_1 = float(request.POST['HCO3_1'])
            Ca_1 = float(request.POST['Ca_1'])
            Mg_1 = float(request.POST['Mg_1'])
            Na_1 = float(request.POST['Na_1'])
            Ba_1 = float(request.POST['Ba_1'])
            Sr_1 = float(request.POST['Sr_1'])
            pH_1 = float(request.POST['pH_1'])
            ro_1 = float(request.POST['ro_1'])
            # Входные данные для жидкости 2
            Cl_2 = float(request.POST['Cl_2'])
            SO4_2 = float(request.POST['SO4_2'])
            HCO3_2 = float(request.POST['HCO3_2'])
            Ca_2 = float(request.POST['Ca_2'])
            Mg_2 = float(request.POST['Mg_2'])
            Na_2 = float(request.POST['Na_2'])
            Ba_2 = float(request.POST['Ba_2'])
            Sr_2 = float(request.POST['Sr_2'])
            pH_2 = float(request.POST['pH_2'])
            ro_2 = float(request.POST['ro_2'])
            # Входные данные для жидкости 1
            Cl_1_another = float(request.POST['Cl_1_another'])
            SO4_1_another = float(request.POST['SO4_1_another'])
            HCO3_1_another = float(request.POST['HCO3_1_another'])
            Ca_1_another = float(request.POST['Ca_1_another'])
            Mg_1_another = float(request.POST['Mg_1_another'])
            Na_1_another = float(request.POST['Na_1_another'])
            Ba_1_another = float(request.POST['Ba_1_another'])
            Sr_1_another = float(request.POST['Sr_1_another'])
            # Входные данные для жидкости 2
            Cl_2_another = float(request.POST['Cl_2_another'])
            SO4_2_another = float(request.POST['SO4_2_another'])
            HCO3_2_another = float(request.POST['HCO3_2_another'])
            Ca_2_another = float(request.POST['Ca_2_another'])
            Mg_2_another = float(request.POST['Mg_2_another'])
            Na_2_another = float(request.POST['Na_2_another'])
            Ba_2_another = float(request.POST['Ba_2_another'])
            Sr_2_another = float(request.POST['Sr_2_another'])
            # Условия смешивания
            Temperature = float(request.POST['Temperature'])  # Температура в градусах
            Pressure = float(request.POST['Pressure'])  # Давление в МПа
            custom_Part_of_Mixture = float(request.POST['Part_of_Mixture'])
            Parts_of_Mixture = [0, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
            if custom_Part_of_Mixture not in Parts_of_Mixture:
                Parts_of_Mixture.append(custom_Part_of_Mixture)
            all_results = []
            # print(custom_Part_of_Mixture)
            for each_elem in Parts_of_Mixture:
                result = calculate_full_result(Cl_1, Cl_2, SO4_1, SO4_2, HCO3_1, HCO3_2, Ca_1, Ca_2, Mg_1, Mg_2, Na_1,
                                               Na_2, Ba_1, Ba_2, Sr_1, Sr_2, pH_1, pH_2, ro_1, ro_2, Temperature,
                                               Pressure, each_elem)
                all_results.append(result)
            graph = create_plot(all_results)
            return render(request, "calculator/salt.html", {"form": form,"form_2":form_2,
                                                            "all_results": all_results,
                                                            "custom_Part_of_Mixture": custom_Part_of_Mixture,
                                                            'graph': graph})
    else:
        form = Scale_Calculator_form_1()
        form_2 = Scale_Calculator_form_2()

    return render(request, "calculator/salt.html", {"form": form, "form_2": form_2})


# База реагентов
def reagent_base_page(request):
    bd_all_salts = Solution.objects.all()
    bd_names_salts = Salt.objects.all()
    # print(bd_all_salts)
    # print(bd_names_salts)
    return render(request, 'calculator/reagent_page.html',
                  {"bd_all_salts": bd_all_salts, "bd_names_salts": bd_names_salts})


def history_page(request):
    return HttpResponse("Страница истории")


def FAQ_page(request):
    return render(request, "calculator/faq_page.html")
