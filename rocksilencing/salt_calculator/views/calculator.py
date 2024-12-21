from django.shortcuts import render, redirect
from django.http import HttpResponse
import plotly.graph_objects as go
import plotly.io as pio
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
from io import BytesIO
import os
from django.conf import settings

from ..forms.mixture_forms import Scale_Calculator_form_1, Scale_Calculator_form_2
from ..services.mixture_service import MixtureCalculationService, MixtureData
from ..services.graph_service import create_plot


def salt_calculator_page(request):
    if request.method == "POST":
        form = Scale_Calculator_form_1(request.POST)
        form_2 = Scale_Calculator_form_2(request.POST)

        if form.is_valid():
            # Создаем объекты данных смесей
            mixture1 = MixtureData(
                Cl=float(form.cleaned_data["Cl_1"]),
                SO4=float(form.cleaned_data["SO4_1"]),
                HCO3=float(form.cleaned_data["HCO3_1"]),
                Ca=float(form.cleaned_data["Ca_1"]),
                Mg=float(form.cleaned_data["Mg_1"]),
                Na=float(form.cleaned_data["Na_1"]),
                Ba=float(form.cleaned_data["Ba_1"]),
                Sr=float(form.cleaned_data["Sr_1"]),
                pH=float(form.cleaned_data["pH_1"]),
                ro=float(form.cleaned_data["ro_1"]),
            )
            mixture2 = MixtureData(
                Cl=float(form.cleaned_data["Cl_2"]),
                SO4=float(form.cleaned_data["SO4_2"]),
                HCO3=float(form.cleaned_data["HCO3_2"]),
                Ca=float(form.cleaned_data["Ca_2"]),
                Mg=float(form.cleaned_data["Mg_2"]),
                Na=float(form.cleaned_data["Na_2"]),
                Ba=float(form.cleaned_data["Ba_2"]),
                Sr=float(form.cleaned_data["Sr_2"]),
                pH=float(form.cleaned_data["pH_2"]),
                ro=float(form.cleaned_data["ro_2"]),
            )

            # Получаем параметры смешивания
            temperature = float(form.cleaned_data["Temperature"])
            pressure = float(form.cleaned_data["Pressure"])
            custom_part = float(form.cleaned_data["Part_of_Mixture"])

            # Создаем сервис и получаем результаты
            service = MixtureCalculationService(
                mixture1, mixture2, temperature, pressure
            )
            all_results = service.calculate_all_mixtures(custom_part)

            # Создаем график
            graph_html, graph_dict = create_plot(all_results)

            # Сохраняем контекст в сессию
            salt_session_context = {
                "form_data": request.POST,
                "all_results": all_results,
                "custom_Part_of_Mixture": custom_part,
                "graph_dict": graph_dict,
            }
            request.session["salt_session_context"] = salt_session_context

            context = {
                "form": form,
                "form_2": form_2,
                "all_results": all_results,
                "custom_Part_of_Mixture": custom_part,
                "graph": graph_html,
            }
            return render(request, "salt.html", context)

    # GET-запрос
    salt_saved_data = request.session.get("salt_session_context")
    if salt_saved_data:
        form = Scale_Calculator_form_1(initial=salt_saved_data["form_data"])
        form_2 = Scale_Calculator_form_2(initial=salt_saved_data["form_data"])
        graph_html = None
        if graph_dict := salt_saved_data.get("graph_dict"):
            fig = go.Figure(graph_dict)
            graph_html = pio.to_html(fig, full_html=False)

        context = {
            "form": form,
            "form_2": form_2,
            "all_results": salt_saved_data.get("all_results"),
            "custom_Part_of_Mixture": salt_saved_data.get("custom_Part_of_Mixture"),
            "graph": graph_html,
        }
    else:
        context = {
            "form": Scale_Calculator_form_1(),
            "form_2": Scale_Calculator_form_2(),
            "all_results": None,
            "custom_Part_of_Mixture": None,
            "graph": None,
        }

    return render(request, "salt.html", context)


def download_scale_calc_report(request):
    salt_session_context = request.session.get("salt_session_context")
    if not salt_session_context:
        return redirect("scale_calculator")

    template_path = os.path.join(
        settings.BASE_DIR, "salt_calculator", "reports", "salt_calculator_template.docx"
    )
    doc = DocxTemplate(template_path)

    if graph_dict := salt_session_context.get("graph_dict"):
        fig = go.Figure(graph_dict)
        graph_image = pio.to_image(fig, format="png")
        image_stream = BytesIO(graph_image)
        salt_session_context["graph_image"] = InlineImage(
            doc, image_stream, width=Mm(150)
        )

    doc.render(salt_session_context)
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
    response["Content-Disposition"] = (
        'attachment; filename="scale_calculator_report.docx"'
    )
    doc.save(response)
    return response
