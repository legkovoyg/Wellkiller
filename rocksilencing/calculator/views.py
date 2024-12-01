import plotly.express as px
import os
import logging
import json
import numpy as np
import pandas as pd
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from calculator.forms import (
    Scale_Calculator_form_1,
    Scale_Calculator_form_2,
    ModelGlushForm,
    ExpertSysForm,
)
from calculator.custom_functions.Method_for_salt_calculator import calculate_full_result
from calculator.custom_functions.graph_method import create_plot
from calculator.custom_functions.matmodel_glush.Matmodel import matmodel_glush
from calculator.custom_functions.matmodel_glush.matmodel_graph.graph_pressures import (
    create_matmodel_plot,
)
from calculator.custom_functions.exportsys.exposys_func import (
    load_rules,
    get_recommendation_from_rules,
)
from docxtpl import DocxTemplate
from calculator.models import Salt, Solution
from sklearn.linear_model import LinearRegression
from django.db.models import Min, Max


# Страница калькулятора


def handle_excel_file(excel_file):
    if excel_file:
        excel_df = pd.read_excel(excel_file, engine="openpyxl")
        excel_datas = excel_df.to_dict(orient="list")
        result = [
            {
                "count": count,
                "md_start": md_start,
                "md_end": md_end,
                "tvd_start": tvd_start,
                "tvd_end": tvd_end,
                "ext_d": ext_d,
                "thick": thick,
            }
            for count, md_start, md_end, tvd_start, tvd_end, ext_d, thick in zip(
                excel_datas["count"],
                excel_datas["md_start"],
                excel_datas["md_end"],
                excel_datas["tvd_start"],
                excel_datas["tvd_end"],
                excel_datas["ext_d"],
                excel_datas["thick"],
            )
        ]

        x = np.array(excel_datas["md_start"])
        y = np.array(excel_datas["tvd_start"])
        coefficients = np.polyfit(x, y, 1)
        polynomial = np.poly1d(coefficients)
    else:
        result = []
        polynomial = 1
    return result, polynomial


@login_required
def get_form_data(request):
    return {
        # Общие данные
        "Oil_field_name": str(request.POST["Oil_field_name"]),
        "Bush_name": str(request.POST["Bush_name"]),
        "Well_name": str(request.POST["Well_name"]),
        "Design_name": str(request.POST["Design_name"]),
        "EXP_type": str(request.POST["EXP_type"]),
        "Porosity": float(request.POST["Porosity"]),
        "Oil_density": float(request.POST["Oil_density"]),
        "Plast_pressure": float(request.POST["Plast_pressure"]),
        "Radius_countour": float(request.POST["Radius_countour"]),
        "Plast_thickness": float(request.POST["Plast_thickness"]),
        "From_yst_to_plast": float(request.POST["From_yst_to_plast"]),
        "True_zaboi": float(request.POST["True_zaboi"]),
        "False_zaboi": float(request.POST["False_zaboi"]),
        # Колонна и скважина
        "NKT_length": float(request.POST["NKT_length"]),
        "NKT_inner_diameter": float(request.POST["NKT_inner_diameter"]),
        "NKT_external_diameter": float(request.POST["NKT_external_diameter"]),
        "EXP_length": float(request.POST["EXP_length"]),
        "EXP_inner_diameter": float(request.POST["EXP_inner_diameter"]),
        "EXP_external_diameter": float(request.POST["EXP_external_diameter"]),
        # НКТ и штанги
        # Способ закачки
        "Volume_of_car": float(request.POST["Volume_of_car"]),
        "Debit": float(request.POST["Debit"]),
        "YV_density": float(request.POST["YV_density"]),
        "YV_dole": float(request.POST["YV_dole"]),
        "Emul_density": float(request.POST["Emul_density"]),
        "Emul_dole": float(request.POST["Emul_dole"]),
        "Type_of_jgs": str(request.POST["Type_of_jgs"]),
        "Phase_oil_permeability": float(request.POST["Phase_oil_permeability"])
        / 10**12,
        "Phase_jgs_permeability": float(request.POST["Phase_jgs_permeability"])
        / 10**12,
        "Oil_viscosity": float(request.POST["Oil_viscosity"]),
        "Jgs_viscosity": float(request.POST["Jgs_viscosity"]),
        "Zapas": float(request.POST["Zapas"]),
        "Type_of_jamming": str(request.POST["Type_of_jamming"]),
    }


def process_calculations(data, polynominal):
    bd_CaCl = Solution.objects.filter(salt__name="CaCl")
    bd_CaJG = Solution.objects.filter(salt__name="CaЖГ")
    bd_CaKCl = Solution.objects.filter(salt__name="KCl")

    results = matmodel_glush(
        data["Plast_pressure"] * 101325,
        data["Plast_thickness"],
        data["True_zaboi"],
        data["NKT_length"],
        data["Oil_density"],
        data["NKT_inner_diameter"],
        data["NKT_external_diameter"],
        data["EXP_inner_diameter"],
        data["EXP_external_diameter"],
        data["Debit"],
        data["Phase_jgs_permeability"],
        data["Jgs_viscosity"],
        data["Phase_oil_permeability"],
        data["Oil_viscosity"],
        data["Radius_countour"],
        data["Porosity"],
        30,
        data["YV_density"],
        data["YV_dole"],
        data["Emul_density"],
        data["Emul_dole"],
        data["Zapas"],
        bd_CaCl,
        bd_CaJG,
        chosen_salt=data["Type_of_jgs"],
        volume_car=data["Volume_of_car"],
        type_of_glush=data["Type_of_jamming"],
        polynom=polynominal,
    )

    return results


@login_required
def render_with_results(request, form, results, result, polynomial, form_data):
    current_results = results[0]
    time = [elem / 60 for elem in results[2]]
    param_for_graph = results[1]
    graph = create_matmodel_plot(param_for_graph, time)
    design, stages, recipes_all, data_for_animation = (
        results[3],
        results[4],
        results[5],
        results[6],
    )
    keys = [
        "Oil_field_name",
        "Bush_name",
        "Well_name",
        "Design_name",
        "EXP_type",
        "Porosity",
        "Oil_density",
        "Plast_pressure",
        "Radius_countour",
        "Plast_thickness",
        "From_yst_to_plast",
        "True_zaboi",
        "False_zaboi",
        "NKT_length",
        "NKT_inner_diameter",
        "NKT_external_diameter",
        "EXP_length",
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
        "Type_of_jamming",
    ]

    session_context = {key: form_data[key] for key in keys}
    session_context["Phase_oil_permeability"] = (
        session_context["Phase_oil_permeability"] * 10**12
    )
    session_context["Phase_jgs_permeability"] = (
        session_context["Phase_jgs_permeability"] * 10**12
    )
    # Добавляем дополнительные элементы
    session_context.update(
        {
            "design": design,
            "excel_file": result,
            "param_for_graph": param_for_graph,
            "time": time,
            "graph": graph,
            "stages": stages,
            "type_of_glush": session_context["Type_of_jamming"],
            "recipes_all": recipes_all,
            "data_for_animation": json.dumps(data_for_animation),
            "current_results": current_results,
        }
    )
    request.session["session_context"] = session_context

    return render(
        request,
        "calculator/main_page.html",
        {
            "form": form,
            "results": results,
            "current_results": current_results,
            "graph": graph,
            "design": design,
            "type_of_glush": session_context["Type_of_jamming"],
            "stages": stages,
            "recipes_all": recipes_all,
            "show_download_button": True,
            "data_for_animation": json.dumps(data_for_animation),
            "excel_file": result,
        },
    )


@login_required
def calculator_page(request):
    if request.method == "POST":
        form = ModelGlushForm(request.POST, request.FILES)
        if form.is_valid():
            result, polynomial = handle_excel_file(
                request.FILES.get("file_upload", None)
            )
            form_data = get_form_data(request)
            results = process_calculations(form_data, polynomial)
            return render_with_results(
                request, form, results, result, polynomial, form_data
            )
        else:
            print(form.errors)
    else:
        saved_data = request.session.get("session_context", None)
        form = ModelGlushForm(initial=saved_data if saved_data else None)
        return render(
            request,
            "calculator/main_page.html",
            {
                "graph": saved_data.get("graph") if saved_data else None,
                "form": form,
                "type_of_glush": (
                    saved_data.get("type_of_glush") if saved_data else None
                ),
                "current_results": (
                    saved_data.get("current_results") if saved_data else None
                ),
                "design": saved_data.get("design") if saved_data else None,
                "stages": saved_data.get("stages") if saved_data else None,
                "recipes_all": saved_data.get("recipes_all") if saved_data else None,
                "show_download_button": True if saved_data else None,
                "data_for_animation": (
                    saved_data.get("data_for_animation") if saved_data else None
                ),
            },
        )


# Скачивание отчета
@login_required
def download_report(request):
    session_context = request.session.get("session_context")
    if not session_context:
        return redirect("calculator_page")  # Перенаправление, если контекста нет

    if session_context["design"]["DESIGN_chosen_salt_name"] != "без соли":
        # Построение пути к файлу шаблона
        template_path = os.path.join(
            settings.BASE_DIR,
            "calculator",
            "report_templates",
            "report_template_salt.docx",
        )
        logging.debug(f"Template path: {template_path}")
    else:
        template_path = os.path.join(
            settings.BASE_DIR,
            "calculator",
            "report_templates",
            "report_template_water.docx",
        )
        logging.debug(f"Template path: {template_path}")

    # Проверка существования файла шаблона
    if not os.path.exists(template_path):
        logging.error(f"Template file not found at {template_path}")
        raise Http404("Template file not found.")

    # Загрузка шаблона и вставка данных
    doc = DocxTemplate(template_path)
    doc.render(session_context)
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
    response["Content-Disposition"] = 'attachment; filename="report.docx"'
    doc.save(response)
    return response


# Страница калькулятора солеотложений
@login_required
def scale_calculator_page(request):
    if request.method == "POST":
        # Исходные данные графика
        x = [5, 15, 25, 35, 45, 55]
        y1 = [0.8, 0.6, 0.4, 0.2, 0, 0]
        y2 = [1.2, 1, 0.8, 0.6, 0.4, 0.2]

        # Инициализация форм
        form = Scale_Calculator_form_1(request.POST)
        form_2 = Scale_Calculator_form_2(request.POST)

        if form.is_valid():
            # Входные данные для жидкости 1
            Cl_1 = float(form.cleaned_data["Cl_1"])
            SO4_1 = float(form.cleaned_data["SO4_1"])
            HCO3_1 = float(form.cleaned_data["HCO3_1"])
            Ca_1 = float(form.cleaned_data["Ca_1"])
            Mg_1 = float(form.cleaned_data["Mg_1"])
            Na_1 = float(form.cleaned_data["Na_1"])
            Ba_1 = float(form.cleaned_data["Ba_1"])
            Sr_1 = float(form.cleaned_data["Sr_1"])
            pH_1 = float(form.cleaned_data["pH_1"])
            ro_1 = float(form.cleaned_data["ro_1"])

            # Входные данные для жидкости 2
            Cl_2 = float(form.cleaned_data["Cl_2"])
            SO4_2 = float(form.cleaned_data["SO4_2"])
            HCO3_2 = float(form.cleaned_data["HCO3_2"])
            Ca_2 = float(form.cleaned_data["Ca_2"])
            Mg_2 = float(form.cleaned_data["Mg_2"])
            Na_2 = float(form.cleaned_data["Na_2"])
            Ba_2 = float(form.cleaned_data["Ba_2"])
            Sr_2 = float(form.cleaned_data["Sr_2"])
            pH_2 = float(form.cleaned_data["pH_2"])
            ro_2 = float(form.cleaned_data["ro_2"])

            # Условия смешивания
            Temperature = float(form.cleaned_data["Temperature"])
            Pressure = float(form.cleaned_data["Pressure"])
            custom_Part_of_Mixture = float(form.cleaned_data["Part_of_Mixture"])

            Parts_of_Mixture = [0, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
            if custom_Part_of_Mixture not in Parts_of_Mixture:
                Parts_of_Mixture.append(custom_Part_of_Mixture)

            all_results = []
            for each_elem in Parts_of_Mixture:
                result = calculate_full_result(
                    Cl_1,
                    Cl_2,
                    SO4_1,
                    SO4_2,
                    HCO3_1,
                    HCO3_2,
                    Ca_1,
                    Ca_2,
                    Mg_1,
                    Mg_2,
                    Na_1,
                    Na_2,
                    Ba_1,
                    Ba_2,
                    Sr_1,
                    Sr_2,
                    pH_1,
                    pH_2,
                    ro_1,
                    ro_2,
                    Temperature,
                    Pressure,
                    each_elem,
                )
                all_results.append(result)

            # Создаем график
            graph = create_plot(all_results)

            # Сохраняем данные в сессию
            salt_session_context = {
                "form_data": request.POST,
                "all_results": all_results,
                "custom_Part_of_Mixture": custom_Part_of_Mixture,
                "graph": graph,
            }
            request.session["salt_session_context"] = salt_session_context

            return render(
                request,
                "calculator/salt.html",
                {
                    "form": form,
                    "form_2": form_2,
                    "all_results": all_results,
                    "custom_Part_of_Mixture": custom_Part_of_Mixture,
                    "graph": graph,
                },
            )
    else:
        # Загружаем данные из сессии, если они есть
        salt_saved_data = request.session.get("salt_session_context")

        if salt_saved_data:
            form = Scale_Calculator_form_1(initial=salt_saved_data["form_data"])
            form_2 = Scale_Calculator_form_2(initial=salt_saved_data["form_data"])
            all_results = salt_saved_data.get("all_results")
            custom_Part_of_Mixture = salt_saved_data.get("custom_Part_of_Mixture")
            graph = salt_saved_data.get("graph")
        else:
            form = Scale_Calculator_form_1()
            form_2 = Scale_Calculator_form_2()
            all_results = None
            custom_Part_of_Mixture = None
            graph = None

        return render(
            request,
            "calculator/salt.html",
            {
                "form": form,
                "form_2": form_2,
                "all_results": all_results,
                "custom_Part_of_Mixture": custom_Part_of_Mixture,
                "graph": graph,
            },
        )


# База реагентов
@login_required
def reagent_base_page(request):
    # Получаем все соли и вычисляем для каждой из них минимальную и максимальную плотность
    bd_names_salts = Salt.objects.all().annotate(
        min_density=Min("solutions__density"), max_density=Max("solutions__density")
    )
    bd_all_solutions = Solution.objects.all()

    return render(
        request,
        "calculator/reagent_page.html",
        {"bd_names_salts": bd_names_salts, "bd_all_solutions": bd_all_solutions},
    )


@login_required
def expert_sys_page(request):
    data = {}
    recommendation = None

    if request.method == "POST":
        form = ExpertSysForm(request.POST)
        if form.is_valid():
            # Получаем данные из формы
            print(form)
            data = form.cleaned_data
            print(data)
            # Получаем рекомендацию на основе введённых данных
            recommendation = get_recommendation_from_rules(data)
            print(f"Введённые данные: {data}")  # Для отладки
            print(f"Рекомендация: {recommendation}")  # Для отладки
    else:
        form = ExpertSysForm()

    return render(
        request,
        "calculator/expertsys.html",
        {
            "form": form,
            "data": data,
            "recommendation": recommendation,
        },
    )


@login_required
def history_page(request):
    return HttpResponse("Страница истории")


@login_required
def FAQ_page(request):
    return render(request, "calculator/faq_page.html")
