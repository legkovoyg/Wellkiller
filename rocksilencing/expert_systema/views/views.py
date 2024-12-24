import json
from django.shortcuts import render, redirect
from expert_systema.forms.forms import ReservoirCharacteristicsForm
from expert_systema.utils.utils import filter_technologies  # <-- ваша функция
from filesapp.models.models import Design
from expert_systema.models.technology import Technology
from expert_systema.models.technology_group import TechnologyGroup


def reservoir_characteristics_view(request):
    """
    View для обработки характеристик коллектора и подбора технологий.
    """
    design_id = request.GET.get("design_id")
    design_obj = None
    if design_id:
        try:
            design_obj = Design.objects.get(pk=design_id)
        except Design.DoesNotExist:
            design_obj = None

    if request.method == "POST":
        if "tech_group" in request.POST and "tech_name" in request.POST:
            tech_group = request.POST.get("tech_group")
            tech_name = request.POST.get("tech_name")

            request.session["selected_group"] = tech_group
            request.session["selected_technology"] = tech_name

            if design_obj:
                expert_data = design_obj.expert_data or {}
                expert_data["technology_group"] = tech_group
                expert_data["technology"] = tech_name
                design_obj.expert_data = expert_data
                design_obj.save()

            calc_type = request.session.get("calc_type")
            if calc_type == "Экспертная система":
                return redirect("filesapp:files_main_window")
            elif calc_type in [
                "Глушение скважины c экспертной системой",
                "Всё включено",
            ]:
                return redirect("calculator:home")
            return redirect("filesapp:files_main_window")

        form = ReservoirCharacteristicsForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            grouped_results = filter_technologies(
                cleaned_data["rock_type"],
                cleaned_data["pressure_coefficient"],
                cleaned_data["temperature"],
                cleaned_data["is_water_sensitive"],
            )

            serialized_technologies = {}
            for group_name, tech_list in (grouped_results or {}).items():
                serialized_techs = []
                for tech_obj, applicability in tech_list:
                    # Собираем все типы компонентов
                    components_data = {
                        "reagent_salts": [
                            {
                                "id": salt.id,
                                "name": salt.name,
                                "full_name": salt.full_name,
                                "description": salt.description,
                            }
                            for salt in tech_obj.reagent_salts.all()
                        ],
                        "surfactants": [
                            {
                                "id": surf.id,
                                "name": surf.name,
                                "type": surf.type,
                                "application": surf.application,
                            }
                            for surf in tech_obj.surfactants.all()
                        ],
                        "polymers": [
                            {
                                "id": poly.id,
                                "name": poly.name,
                                "type": poly.type,
                                "application": poly.application,
                            }
                            for poly in tech_obj.polymers.all()
                        ],
                        "weighting_agents": [
                            {
                                "id": agent.id,
                                "name": agent.name,
                                "type": agent.type,
                                "application": agent.application,
                            }
                            for agent in tech_obj.weighting_agents.all()
                        ],
                        "other_materials": [
                            {
                                "id": mat.id,
                                "name": mat.name,
                                "type": mat.type,
                                "application": mat.application,
                            }
                            for mat in tech_obj.other_materials.all()
                        ],
                        "corrosion_inhibitors": [
                            {
                                "id": inhib.id,
                                "name": inhib.name,
                                "type": inhib.type,
                                "application": inhib.application,
                            }
                            for inhib in tech_obj.corrosion_inhibitors.all()
                        ],
                        "scale_inhibitors": [
                            {
                                "id": inhib.id,
                                "name": inhib.name,
                                "type": inhib.type,
                                "application": inhib.application,
                            }
                            for inhib in tech_obj.scale_inhibitors.all()
                        ],
                    }

                    # Формируем строку состава для отображения
                    components_text = []

                    # Добавляем соли
                    if components_data["reagent_salts"]:
                        salts = [
                            f"{salt['name']} ({salt['full_name']})"
                            for salt in components_data["reagent_salts"]
                        ]
                        components_text.append(f"Соли: {', '.join(salts)}")

                    # Добавляем ПАВ
                    if components_data["surfactants"]:
                        surfs = [
                            surf["name"] for surf in components_data["surfactants"]
                        ]
                        components_text.append(f"ПАВ: {', '.join(surfs)}")

                    # Добавляем полимеры
                    if components_data["polymers"]:
                        polys = [poly["name"] for poly in components_data["polymers"]]
                        components_text.append(f"Полимеры: {', '.join(polys)}")

                    # Добавляем утяжелители
                    if components_data["weighting_agents"]:
                        agents = [
                            agent["name"]
                            for agent in components_data["weighting_agents"]
                        ]
                        components_text.append(f"Утяжелители: {', '.join(agents)}")

                    # Добавляем ингибиторы коррозии
                    if components_data["corrosion_inhibitors"]:
                        inhibs = [
                            inhib["name"]
                            for inhib in components_data["corrosion_inhibitors"]
                        ]
                        components_text.append(
                            f"Ингибиторы коррозии: {', '.join(inhibs)}"
                        )

                    # Добавляем ингибиторы солеотложений
                    if components_data["scale_inhibitors"]:
                        inhibs = [
                            inhib["name"]
                            for inhib in components_data["scale_inhibitors"]
                        ]
                        components_text.append(
                            f"Ингибиторы солеотложений: {', '.join(inhibs)}"
                        )

                    # Добавляем прочие материалы
                    if components_data["other_materials"]:
                        mats = [
                            mat["name"] for mat in components_data["other_materials"]
                        ]
                        components_text.append(f"Прочие компоненты: {', '.join(mats)}")

                    tech_data = {
                        "id": tech_obj.id,
                        "name": tech_obj.name,
                        "short_name": tech_obj.short_name,
                        "notes": tech_obj.notes,
                        "applicability": applicability,
                        "components": components_data,
                        "components_text": (
                            "; ".join(components_text)
                            if components_text
                            else "Состав не определен"
                        ),
                    }

                    serialized_techs.append(tech_data)

                serialized_technologies[group_name] = serialized_techs

            if design_obj:
                expert_data = design_obj.expert_data or {}
                expert_data["form_data"] = cleaned_data
                expert_data["technologies"] = serialized_technologies
                expert_data.pop("technology_group", None)
                expert_data.pop("technology", None)
                design_obj.expert_data = expert_data
                design_obj.save()

            return render(
                request,
                "reservoir_characteristics_form.html",
                {
                    "form": form,
                    "technologies": grouped_results,
                    "technologies_json": json.dumps(
                        serialized_technologies, ensure_ascii=False
                    ),
                    "selected_group": None,
                    "selected_technology": None,
                },
            )

        return render(
            request,
            "reservoir_characteristics_form.html",
            {
                "form": form,
                "technologies": None,
                "technologies_json": "",
                "selected_group": None,
                "selected_technology": None,
            },
        )

    else:
        if design_obj and design_obj.expert_data:
            expert_data = design_obj.expert_data
            form_data = expert_data.get("form_data", {})
            technologies = expert_data.get("technologies", {})
            tech_group = expert_data.get("technology_group")
            tech_name = expert_data.get("technology")

            form = ReservoirCharacteristicsForm(initial=form_data)

            return render(
                request,
                "reservoir_characteristics_form.html",
                {
                    "form": form,
                    "technologies": technologies,
                    "technologies_json": (
                        json.dumps(technologies) if technologies else ""
                    ),
                    "selected_group": tech_group,
                    "selected_technology": tech_name,
                },
            )

        form = ReservoirCharacteristicsForm()
        return render(
            request,
            "reservoir_characteristics_form.html",
            {
                "form": form,
                "technologies": None,
                "technologies_json": "",
                "selected_group": None,
                "selected_technology": None,
            },
        )
