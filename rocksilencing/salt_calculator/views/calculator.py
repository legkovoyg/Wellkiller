# salt_calculator/views.py

import os
from io import BytesIO

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required

import plotly.graph_objects as go
import plotly.io as pio

from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm

# Импорт вашей модели Design
from filesapp.models.models import Design

# Импорт форм и сервисов
from salt_calculator.forms.mixture_forms import (
    Scale_Calculator_form_1,
    Scale_Calculator_form_2,
)
from salt_calculator.services.mixture_service import (
    MixtureCalculationService,
    MixtureData,
)
from salt_calculator.services.graph_service import create_plot


@login_required
def salt_calculator_page(request):
    """
    Страница «Расчет совместимости вод» (солеотложения).

    Логика:
      - При GET:
         1) design_id = GET ? session
         2) Если существует Design с таким design_id, сохраняем его в session["design_id"] (refresh).
         3) Если у Design есть scale_data, восстанавливаем формы и граф.
         4) Иначе, если есть session["salt_session_context"], берем оттуда.
         5) Иначе — пустые формы.

      - При POST:
         1) Проверяем валидность form_1 и form_2.
         2) Если валидны, считаем all_results, генерируем graph.
         3) Сохраняем (обе формы, результаты) в session["salt_session_context"].
         4) Если design_obj, то в design_obj.scale_data.
         5) Рендерим страницу с результатами.
    """

    # 1. Считываем design_id из GET, если нет — из сессии
    design_id = request.GET.get("design_id") or request.session.get("design_id")
    design_obj = None
    if design_id:
        try:
            design_obj = Design.objects.get(pk=design_id)
            # Если нашли дизайн — обновим сессию (чтобы при последующих заходах не терялся)
            request.session["design_id"] = str(design_obj.id)
        except Design.DoesNotExist:
            design_obj = None

    # ---------------------- POST-запрос ----------------------
    if request.method == "POST":
        form_1 = Scale_Calculator_form_1(request.POST)
        form_2 = Scale_Calculator_form_2(request.POST)

        if form_1.is_valid() and form_2.is_valid():
            # Достаём "чистые" данные из обеих форм
            cleaned_data_1 = dict(form_1.cleaned_data)
            cleaned_data_2 = dict(form_2.cleaned_data)

            # Подготовим параметры для MixtureData (пример):
            mixture1 = MixtureData(
                Cl=float(cleaned_data_1["Cl_1"]),
                SO4=float(cleaned_data_1["SO4_1"]),
                HCO3=float(cleaned_data_1["HCO3_1"]),
                Ca=float(cleaned_data_1["Ca_1"]),
                Mg=float(cleaned_data_1["Mg_1"]),
                Na=float(cleaned_data_1["Na_1"]),
                Ba=float(cleaned_data_1["Ba_1"]),
                Sr=float(cleaned_data_1["Sr_1"]),
                pH=float(cleaned_data_1["pH_1"]),
                ro=float(cleaned_data_1["ro_1"]),
            )
            mixture2 = MixtureData(
                Cl=float(cleaned_data_1["Cl_2"]),
                SO4=float(cleaned_data_1["SO4_2"]),
                HCO3=float(cleaned_data_1["HCO3_2"]),
                Ca=float(cleaned_data_1["Ca_2"]),
                Mg=float(cleaned_data_1["Mg_2"]),
                Na=float(cleaned_data_1["Na_2"]),
                Ba=float(cleaned_data_1["Ba_2"]),
                Sr=float(cleaned_data_1["Sr_2"]),
                pH=float(cleaned_data_1["pH_2"]),
                ro=float(cleaned_data_1["ro_2"]),
            )

            temperature = float(cleaned_data_1["Temperature"])
            pressure = float(cleaned_data_1["Pressure"])
            custom_part = float(cleaned_data_1["Part_of_Mixture"])

            # Запускаем расчёты
            service = MixtureCalculationService(
                mixture1, mixture2, temperature, pressure
            )
            all_results = service.calculate_all_mixtures(custom_part)

            # Создаем график
            graph_html, graph_dict = create_plot(all_results)

            # Сохраняем в сессию
            salt_session_context = {
                "form_data_1": cleaned_data_1,
                "form_data_2": cleaned_data_2,
                "all_results": all_results,
                "custom_Part_of_Mixture": custom_part,
                "graph_dict": graph_dict,
            }
            request.session["salt_session_context"] = salt_session_context

            # Если есть design_obj, сохраняем в design_obj.scale_data
            if design_obj:
                design_obj.scale_data = salt_session_context
                design_obj.save()

            # Рендерим результат
            context = {
                "form": form_1,
                "form_2": form_2,
                "all_results": all_results,
                "custom_Part_of_Mixture": custom_part,
                "graph": graph_html,
            }
            return render(request, "salt.html", context)
        else:
            # Одна из форм не валидна
            context = {
                "form": form_1,
                "form_2": form_2,
                "all_results": None,
                "custom_Part_of_Mixture": None,
                "graph": None,
                "errors_1": form_1.errors,
                "errors_2": form_2.errors,
            }
            return render(request, "salt.html", context)

    # ---------------------- GET-запрос ----------------------
    if design_obj and design_obj.scale_data:
        # Если у Design уже есть scale_data
        scale_data = design_obj.scale_data
        form_data_1 = scale_data.get("form_data_1", {})
        form_data_2 = scale_data.get("form_data_2", {})

        form_1 = Scale_Calculator_form_1(initial=form_data_1)
        form_2 = Scale_Calculator_form_2(initial=form_data_2)

        # Восстанавливаем граф (если есть graph_dict)
        graph_html = None
        if "graph_dict" in scale_data:
            fig = go.Figure(scale_data["graph_dict"])
            graph_html = pio.to_html(fig, full_html=False)

        context = {
            "form": form_1,
            "form_2": form_2,
            "all_results": scale_data.get("all_results"),
            "custom_Part_of_Mixture": scale_data.get("custom_Part_of_Mixture"),
            "graph": graph_html,
        }
        return render(request, "salt.html", context)

    else:
        # Нет scale_data в Design (или нет Design вообще).
        # Тогда пробуем загрузить из сессии:
        salt_saved_data = request.session.get("salt_session_context")
        if salt_saved_data:
            # Восстанавливаем формы из сессии
            form_data_1 = salt_saved_data.get("form_data_1", {})
            form_data_2 = salt_saved_data.get("form_data_2", {})

            form_1 = Scale_Calculator_form_1(initial=form_data_1)
            form_2 = Scale_Calculator_form_2(initial=form_data_2)

            graph_html = None
            graph_dict = salt_saved_data.get("graph_dict")
            if graph_dict:
                fig = go.Figure(graph_dict)
                graph_html = pio.to_html(fig, full_html=False)

            context = {
                "form": form_1,
                "form_2": form_2,
                "all_results": salt_saved_data.get("all_results"),
                "custom_Part_of_Mixture": salt_saved_data.get("custom_Part_of_Mixture"),
                "graph": graph_html,
            }
            return render(request, "salt.html", context)
        else:
            # Вообще ничего нет — пустые формы
            context = {
                "form": Scale_Calculator_form_1(),
                "form_2": Scale_Calculator_form_2(),
                "all_results": None,
                "custom_Part_of_Mixture": None,
                "graph": None,
            }
            return render(request, "salt.html", context)


@login_required
def download_scale_calc_report(request):
    """
    Скачивание отчёта Word, опираясь на данные в сессии (salt_session_context).
    """
    salt_session_context = request.session.get("salt_session_context")
    if not salt_session_context:
        return redirect(
            "salt_calculator:calculator"
        )  # Или на нужную страницу, если данных нет

    template_path = os.path.join(
        settings.BASE_DIR, "salt_calculator", "reports", "salt_calculator_template.docx"
    )
    doc = DocxTemplate(template_path)

    # Создаём копию контекста для рендера
    context_for_doc = salt_session_context.copy()

    # Если есть данные графа — добавляем в отчёт
    if graph_dict := salt_session_context.get("graph_dict"):
        fig = go.Figure(graph_dict)
        graph_image = pio.to_image(fig, format="png")
        image_stream = BytesIO(graph_image)

        # Создаём InlineImage только для шаблона
        graph_image_inline = InlineImage(doc, image_stream, width=Mm(150))
        context_for_doc["graph_image"] = graph_image_inline

    # Рендерим шаблон
    doc.render(context_for_doc)

    # Возвращаем документ
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
    response["Content-Disposition"] = (
        'attachment; filename="scale_calculator_report.docx"'
    )
    doc.save(response)
    return response
