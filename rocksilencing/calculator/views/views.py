# calculator/views.py

import os
import logging
import json
import numpy as np
import pandas as pd
import plotly.express as px

from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse

from docxtpl import DocxTemplate

from calculator.forms.forms import ModelGlushForm
from calculator.custom_functions.matmodel_glush.Matmodel import matmodel_glush
from calculator.custom_functions.matmodel_glush.matmodel_graph.graph_pressures import (
    create_matmodel_plot,
)
from reagent_db.models.reagent_db_models_salts import ReagentSalt, ReagentSaltSolution

# ВАЖНО: импорт вашей модели Design
from filesapp.models.models import Design
import numpy as np


def clean_numpy_types(value):
    """
    Рекурсивно преобразует np.int64, np.float64, np.array и т.п. в
    стандартные python-типы (int, float, list, dict).
    """
    if isinstance(value, dict):
        return {k: clean_numpy_types(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [clean_numpy_types(item) for item in value]
    elif isinstance(value, np.integer):
        return int(value)
    elif isinstance(value, np.floating):
        return float(value)
    elif isinstance(value, np.ndarray):
        return clean_numpy_types(value.tolist())
    else:
        return value


def handle_excel_file(excel_file):
    """
    Обрабатывает загруженный Excel-файл,
    возвращая список result и полином polynomial.
    """
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
        polynomial = np.poly1d([1, 0])  # Линейная ф-я y=1x + 0
    return result, polynomial


@login_required
def get_form_data(request):
    """
    Собирает данные из POST формы для расчетов глушения и возвращает словарь.
    """
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


def process_calculations(data, polynomial):
    """
    Запускает matmodel_glush и возвращает результат расчётов (список из 7 элементов).
    """
    bd_CaCl = ReagentSaltSolution.objects.filter(salt__name="CaCl2")
    bd_CaJG = ReagentSaltSolution.objects.filter(salt__name="CaЖГ")
    bd_CaKCl = ReagentSaltSolution.objects.filter(salt__name="KCl")

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
        polynom=polynomial,
    )
    return results


@login_required
def render_with_results(request, form, results, excel_result, polynomial, form_data):
    """
    Вызывает render('calculator/main_page.html') с готовыми графиками/данными.
    Сохраняет промежуточные данные в сессию (session_context), если нужно.
    """
    current_results = results[0]
    time = [elem / 60 for elem in results[2]]
    param_for_graph = results[1]
    graph = create_matmodel_plot(param_for_graph, time)
    design_data, stages, recipes_all, data_for_animation = (
        results[3],
        results[4],
        results[5],
        results[6],
    )
    cleaned_data_for_animation = clean_numpy_types(data_for_animation)
    cleaned_design_data = clean_numpy_types(design_data)
    cleaned_stages = clean_numpy_types(stages)
    cleaned_recipes_all = clean_numpy_types(recipes_all)
    cleaned_current_results = clean_numpy_types(current_results)
    # -------------------------------------
    # Сохраняем в сессию, если нужно
    # -------------------------------------
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
    # Умножим обратно, чтобы форма при повторном GET показывала мкм^2, а не м^2
    session_context["Phase_oil_permeability"] = (
        session_context["Phase_oil_permeability"] * 10**12
    )
    session_context["Phase_jgs_permeability"] = (
        session_context["Phase_jgs_permeability"] * 10**12
    )

    session_context.update(
        {
            "design": cleaned_design_data,
            "excel_file": excel_result,
            "param_for_graph": param_for_graph,
            "time": time,
            "graph": graph,
            "stages": cleaned_stages,
            "type_of_glush": session_context["Type_of_jamming"],
            "recipes_all": cleaned_recipes_all,
            "data_for_animation": cleaned_data_for_animation,  # уже чистый dict
            "current_results": cleaned_current_results,
        }
    )
    request.session["session_context"] = session_context

    return render(
        request,
        "calculator/main_page.html",
        {
            "form": form,
            "results": results,
            "current_results": cleaned_current_results,
            "graph": graph,
            "design": cleaned_design_data,
            "type_of_glush": session_context["Type_of_jamming"],
            "stages": cleaned_stages,
            "recipes_all": cleaned_recipes_all,
            "show_download_button": True,
            "data_for_animation": json.dumps(cleaned_data_for_animation),
            "excel_file": excel_result,
        },
    )


@login_required
def calculator_page(request):
    """
    Главная страница «Калькулятора глушения».
    - Считываем design_id из GET или из сессии.
    - Если POST — делаем расчёт, сохраняем в design_obj.kill_data (если есть).
    - Если GET — восстанавливаем из design_obj.kill_data или из сессии.
    """
    # 1) Считываем design_id (из GET, либо из сессии)
    design_id = request.GET.get("design_id") or request.session.get("design_id")
    design_obj = None
    if design_id:
        try:
            design_obj = Design.objects.get(pk=design_id)
            # Обновим сессию, чтобы удержать design_id при дальнейшем навигации
            request.session["design_id"] = design_id
        except Design.DoesNotExist:
            design_obj = None

    # 2) Если POST — обрабатываем форму
    if request.method == "POST":
        form = ModelGlushForm(request.POST, request.FILES)
        if form.is_valid():
            # a) Обрабатываем загруженный файл
            excel_result, polynomial = handle_excel_file(
                request.FILES.get("file_upload")
            )
            # b) Собираем данные формы
            form_data = get_form_data(request)
            # c) Выполняем расчёт
            results = process_calculations(form_data, polynomial)

            # d) Очищаем данные от numpy-типов перед сохранением
            clean_results = clean_numpy_types(results)

            # e) Если есть design_obj, сохраняем всё в kill_data
            if design_obj:
                kill_data_dict = {
                    "form_data": form_data,
                    "excel_result": excel_result,
                    "current_results": clean_results[0],
                    "param_for_graph": clean_results[1],
                    "time_array": clean_results[2],
                    "design": clean_results[3],
                    "stages": clean_results[4],
                    "recipes_all": clean_results[5],
                    "data_for_animation": clean_results[6],
                }

                kill_data_dict = clean_numpy_types(kill_data_dict)  # Очищаем данные

                design_obj.kill_data = kill_data_dict
                design_obj.save()

            # f) Рендерим результат (и сохраняем в сессию, если нужно)
            return render_with_results(
                request, form, results, excel_result, polynomial, form_data
            )
        else:
            logging.error(f"Form errors: {form.errors}")
            # Если форма невалидна, покажем страницу заново
            return render(
                request,
                "calculator/main_page.html",
                {
                    "form": form,
                    "show_download_button": False,
                },
            )

    # 3) Если GET — восстанавливаем данные
    else:
        # a) Пробуем из сессии
        saved_data = request.session.get("session_context", None)
        form = ModelGlushForm(initial=saved_data if saved_data else None)

        # b) Если у design_obj есть kill_data, подставим её
        if design_obj and design_obj.kill_data:
            kill_data = design_obj.kill_data
            # Если в kill_data есть form_data, подставим его как initial
            # Сохраняем design_id в сессию
            request.session["design_id"] = design_id
            if "form_data" in kill_data:
                initial_data = kill_data["form_data"]
                # Преобразуем фазовые проницаемости обратно в мкм²
                initial_data["Phase_oil_permeability"] *= 10**12
                initial_data["Phase_jgs_permeability"] *= 10**12
                form = ModelGlushForm(initial=initial_data)

            # Создаем график заново из сохраненных данных
            param_for_graph = kill_data.get("param_for_graph")
            time_array = kill_data.get("time_array", [])

            # Преобразуем время в минуты, как это делается в render_with_results
            time = [elem / 60 for elem in time_array] if time_array else []

            # Создаем график используя сохраненные данные
            graph = (
                create_matmodel_plot(param_for_graph, time)
                if param_for_graph and time
                else None
            )

            # Подготовим контекст с результатами
            context = {
                "graph": graph,  # Теперь используем заново созданный график
                "form": form,
                "type_of_glush": kill_data["form_data"].get("Type_of_jamming"),
                "current_results": kill_data.get("current_results"),
                "design": kill_data.get("design"),
                "stages": kill_data.get("stages"),
                "recipes_all": kill_data.get("recipes_all"),
                "show_download_button": True,
                "data_for_animation": json.dumps(
                    kill_data.get("data_for_animation", {})
                ),
                "excel_file": kill_data.get("excel_result"),
                # Сохраним эти данные в сессию для download_report
                "param_for_graph": param_for_graph,
                "time": time,
            }

            # Сохраняем контекст в сессию для использования в download_report
            request.session["session_context"] = {
                "Oil_field_name": kill_data["form_data"]["Oil_field_name"],
                "Bush_name": kill_data["form_data"]["Bush_name"],
                "Well_name": kill_data["form_data"]["Well_name"],
                "Design_name": kill_data["form_data"]["Design_name"],
                "design": kill_data["design"],
                "current_results": kill_data["current_results"],
                "stages": kill_data["stages"],
                "recipes_all": kill_data["recipes_all"],
                "type_of_glush": kill_data["form_data"]["Type_of_jamming"],
                "graph": graph,
                "param_for_graph": param_for_graph,
                "time": time,
            }

            return render(request, "calculator/main_page.html", context)
        else:
            # c) Если design_obj.kill_data нет, но есть saved_data — используем saved_data
            #    (В коде выше уже задали form initial=saved_data)
            context = {
                "form": form,
                "graph": (
                    saved_data["graph"]
                    if saved_data and "graph" in saved_data
                    else None
                ),
                "type_of_glush": saved_data["type_of_glush"] if saved_data else None,
                "current_results": (
                    saved_data["current_results"] if saved_data else None
                ),
                "design": saved_data["design"] if saved_data else None,
                "stages": saved_data["stages"] if saved_data else None,
                "recipes_all": saved_data["recipes_all"] if saved_data else None,
                "show_download_button": True if saved_data else False,
                "data_for_animation": (
                    json.dumps(saved_data["data_for_animation"])
                    if saved_data and "data_for_animation" in saved_data
                    else None
                ),
                "excel_file": saved_data["excel_file"] if saved_data else None,
            }
            return render(request, "calculator/main_page.html", context)


@login_required
def download_report(request):
    """
    Скачивание отчёта Word, используя docxtpl.
    Проверяет данные в следующем порядке:
    1. Сессия (session_context)
    2. Design объект (kill_data)
    """
    # Получаем design_id из сессии
    design_id = request.session.get("design_id")
    context_data = None

    # Сначала проверяем данные в сессии
    session_context = request.session.get("session_context")
    if session_context:
        context_data = session_context

    # Если данных в сессии нет, пробуем получить их из design объекта
    if not context_data and design_id:
        try:
            design_obj = Design.objects.get(pk=design_id)
            if design_obj.kill_data:
                # Подготавливаем контекст из kill_data
                kill_data = design_obj.kill_data
                context_data = {
                    "Oil_field_name": kill_data["form_data"]["Oil_field_name"],
                    "Bush_name": kill_data["form_data"]["Bush_name"],
                    "Well_name": kill_data["form_data"]["Well_name"],
                    "Design_name": kill_data["form_data"]["Design_name"],
                    "design": kill_data["design"],
                    "current_results": kill_data["current_results"],
                    "stages": kill_data["stages"],
                    "recipes_all": kill_data["recipes_all"],
                    "type_of_glush": kill_data["form_data"]["Type_of_jamming"],
                }
        except Design.DoesNotExist:
            pass

    if not context_data:
        return redirect("calculator:home")

    # Выбор шаблона
    if (
        "design" in context_data
        and context_data["design"].get("DESIGN_chosen_salt_name") != "без соли"
    ):
        template_path = os.path.join(
            settings.BASE_DIR,
            "calculator",
            "report_templates",
            "report_template_salt.docx",
        )
    else:
        template_path = os.path.join(
            settings.BASE_DIR,
            "calculator",
            "report_templates",
            "report_template_water.docx",
        )

    if not os.path.exists(template_path):
        logging.error(f"Template file not found at {template_path}")
        raise Http404("Template file not found.")

    doc = DocxTemplate(template_path)
    doc.render(context_data)
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
    response["Content-Disposition"] = 'attachment; filename="report.docx"'
    doc.save(response)
    return response


def FAQ_page(request):
    """
    Страница FAQ (Вопрос-Ответ) для калькулятора.
    """
    return render(request, "calculator/faq_page.html")
