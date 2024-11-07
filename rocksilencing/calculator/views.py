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


# from .Main import calculate
# Create your views here.
# Страница калькулятора
def calculator_page(request):
    if request.method == 'POST':
        form = ModelGlushForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES.get('file_upload', None)
            if excel_file:
                excel_df = pd.read_excel(excel_file, engine = 'openpyxl')
                excel_datas = excel_df.to_dict(orient = "list")
                result = [{'count': count, 'md_start': md_start, 'md_end': md_end, 'tvd_start': tvd_start, 'tvd_end': tvd_end, "ext_d":ext_d, 'thick':thick} for count, md_start, md_end, tvd_start, tvd_end, ext_d, thick in zip(excel_datas['count'], excel_datas['md_start'], excel_datas['md_end'], excel_datas['tvd_start'], excel_datas['tvd_end'], excel_datas['ext_d'], excel_datas['thick'])]
                x = np.array(excel_datas['md_start'])
                y = np.array(excel_datas['tvd_start'])
                coefficients = np.polyfit(x, y, 1)
                polynominal = np.poly1d(coefficients)
            else:
                polynominal = 1
            Plast_pressure = float(request.POST["Plast_pressure"])
            h = float(request.POST["Plast_thickness"])
            Length_of_Well = float(request.POST["True_zaboi"])
            L_of_Wells = float(request.POST["NKT_length"])
            ro_oil = float(request.POST["Oil_density"])
            # ro_jgs = float(request.POST["Jgs_density"])
            d_NKT = float(request.POST["NKT_inner_diameter"])
            D_NKT = float(request.POST["NKT_external_diameter"])
            d_exp = float(request.POST["EXP_inner_diameter"])
            D_exp = float(request.POST["EXP_external_diameter"])
            Q = float(request.POST["Debit"])
            k_jg = float(request.POST["Phase_jgs_permeability"]) / 10 ** 12
            mu_jg = float(request.POST["Jgs_viscosity"])
            k_oil = float(request.POST["Phase_oil_permeability"]) / 10 ** 12
            mu_oil = float(request.POST["Oil_viscosity"])
            Rk = float(request.POST['Radius_countour'])
            m = float(request.POST['Porosity'])
            YV_density = float(request.POST["YV_density"])
            YV_dole = float(request.POST["YV_dole"])
            emul_density = float(request.POST["Emul_density"])
            emul_dole = float(request.POST["Emul_dole"])
            zapas = float(request.POST["Zapas"])
            car_volume = float(request.POST['Volume_of_car'])
            jgs_type = str(request.POST['Type_of_jgs'])
            Type_of_jamming = str(request.POST['Type_of_jamming'])
            bd_CaCl = Solution.objects.filter(salt__name="CaCl")
            bd_CaJG = Solution.objects.filter(salt__name="CaЖГ")
            bd_CaKCl = Solution.objects.filter(salt__name="KCl")
            results = matmodel_glush(Plast_pressure * 101325, h, Length_of_Well, L_of_Wells, ro_oil, d_NKT, D_NKT,
                                     d_exp, D_exp, Q,
                                     k_jg, mu_jg, k_oil, mu_oil, Rk, m, 30, YV_density, YV_dole, emul_density,
                                     emul_dole, zapas, bd_CaCl, bd_CaJG, chosen_salt=jgs_type, volume_car=car_volume,
                                     type_of_glush=Type_of_jamming, polynom = polynominal)
            current_results = results[0]
            time = []
            for each_elem in results[2]:
                each_elem = each_elem/60
                time.append(each_elem)
            graph = create_matmodel_plot(results[1], time)
            design = results[3]
            stages = results[4]
            recipes_all = results[5]
            data_for_animation = results[6]
            
            if excel_file:
                request.session['report_context'] = {
                    'Q': Q,
                    'k_jg': k_jg,
                    'mu_jg': mu_jg,
                    'k_oil': k_oil,
                    'mu_oil': mu_oil,
                    'Rk': Rk,
                    'm': m,
                    'YV_density': YV_density,
                    'YV_dole': YV_dole,
                    'emul_density': emul_density,
                    'emul_dole': emul_dole,
                    'zapas': zapas,
                    'car_volume': car_volume,
                    'jgs_type': jgs_type,
                    'current_results': current_results,
                    'stages': stages,
                    'recipes_all': recipes_all,
                    "design": design,
                    'excel_file': result}
                return render(request, "calculator/main_page.html", {
                    "form": form,
                    "results": results,
                    "current_results": current_results,
                    "type_of_glush": Type_of_jamming,
                    "graph": graph,
                    "design": design,
                    "stages": stages,
                    "recipes_all": recipes_all,
                    "show_download_button": True,
                    "data_for_animation": json.dumps(data_for_animation),
                    'excel_file': result
                })
            else:
                request.session['report_context'] = {
                    'Q': Q,
                    'k_jg': k_jg,
                    'mu_jg': mu_jg,
                    'k_oil': k_oil,
                    'mu_oil': mu_oil,
                    'Rk': Rk,
                    'm': m,
                    'YV_density': YV_density,
                    'YV_dole': YV_dole,
                    'emul_density': emul_density,
                    'emul_dole': emul_dole,
                    'zapas': zapas,
                    'car_volume': car_volume,
                    'jgs_type': jgs_type,
                    'current_results': current_results,
                    'stages': stages,
                    'recipes_all': recipes_all,
                    "design": design}
                return render(request, "calculator/main_page.html", {
                    "form": form,
                    "results": results,
                    "current_results": current_results,
                    "type_of_glush": Type_of_jamming,
                    "graph": graph,
                    "design": design,
                    "stages": stages,
                    "recipes_all": recipes_all,
                    "show_download_button": True,
                    "data_for_animation": json.dumps(data_for_animation),
                })

        else:
            print(form.errors)
    else:
        form = ModelGlushForm()
    return render(request, "calculator/main_page.html", {"form": form})


# Скачивание отчета
def download_report(request):
    report_context = request.session.get('report_context')
    if not report_context:
        return redirect('calculator_page')  # Перенаправление, если контекста нет
    print(report_context['design']['DESIGN_chosen_salt_name'])
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
            print(custom_Part_of_Mixture)
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
    print(bd_names_salts)
    return render(request, 'calculator/reagent_page.html',
                  {"bd_all_salts": bd_all_salts, "bd_names_salts": bd_names_salts})


def history_page(request):
    return HttpResponse("Страница истории")


def FAQ_page(request):
    return render(request, "calculator/faq_page.html")
