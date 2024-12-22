import json
import json
import numpy as np

from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.db.models import Min, Max

from reagent_db.models.reagent_db_models_salts import ReagentSalt, ReagentSaltSolution
from reagent_db.models.reagent_db_models_ingcorr import CorrosionInhibitor
from reagent_db.models.reagent_db_models_pavs import Surfactant
from reagent_db.models.reagent_db_models_ingsalt import ScaleInhibitor
from reagent_db.models.reagent_db_models_heavy import WeightingAgent
from reagent_db.models.reagent_db_models_polymers import Polymer
from reagent_db.models.reagent_db_models_other import OtherMaterial

from collections import defaultdict
from random import choice
from scipy.interpolate import interp1d


# База реагентов
def reagent_db_page(request):
    # Получаем все соли и их диапазоны плотностей
    bd_names_salts = ReagentSalt.objects.all().annotate(
        min_density=Min("solutions__density"), max_density=Max("solutions__density")
    )
    bd_all_solutions = ReagentSaltSolution.objects.all()
    bd_ingcorrs = CorrosionInhibitor.objects.all()
    bd_pavs = Surfactant.objects.all()
    bd_ingsalts = ScaleInhibitor.objects.all()
    bd_weights = WeightingAgent.objects.all()
    bd_polymers = Polymer.objects.all()
    bd_others = OtherMaterial.objects.all()

    # Преобразуем данные в формат JSON
    salts_json = json.dumps(list(bd_names_salts.values()), default=str)
    solutions_json = json.dumps(list(bd_all_solutions.values()), default=str)

    # Подготовка диапазонов плотностей
    ranges = {
        salt.id: {"min_density": salt.min_density, "max_density": salt.max_density}
        for salt in bd_names_salts
    }
    ranges_json = json.dumps(ranges, default=str)

    # Группируем решения по именам солей
    grouped_solutions = defaultdict(list)
    for sol in bd_all_solutions:
        grouped_solutions[sol.salt.name].append(sol)

    # Выбираем одно случайное решение для каждой соли
    random_solutions = {name: choice(sols) for name, sols in grouped_solutions.items()}

    return render(
        request,
        "reagent_db_page.html",
        {
            "bd_names_salts": bd_names_salts,
            "bd_all_solutions": bd_all_solutions,
            "bd_pavs": bd_pavs,  # Добавляем ПАВы
            "bd_ingcorrs": bd_ingcorrs,  # Добавляем ингибиторы коррозии
            "bd_ingsalts": bd_ingsalts,  # Добавляем ингибиторы солеотложений
            "bd_weights": bd_weights,
            "bd_polymers": bd_polymers,
            "bd_others": bd_others,
            "salts_json": salts_json,
            "solutions_json": solutions_json,
            "ranges_json": ranges_json,
            "random_solutions": random_solutions,
        },
    )


def calculate_consumption(request):
    try:
        salt_id = int(request.GET.get("salt_id"))
        density = float(request.GET.get("density"))

        # Получаем все данные для указанной соли
        solutions = ReagentSaltSolution.objects.filter(salt_id=salt_id).order_by(
            "density"
        )

        if not solutions.exists():
            return JsonResponse(
                {"error": "No data found for the selected salt"}, status=404
            )

        # Подготовка данных для интерполяции
        densities = np.array([sol.density for sol in solutions])
        salt_consumptions = np.array([sol.salt_consumption for sol in solutions])
        water_consumptions = np.array([sol.water_consumption for sol in solutions])

        # Интерполяция
        salt_interp = interp1d(
            densities, salt_consumptions, kind="linear", fill_value="extrapolate"
        )
        water_interp = interp1d(
            densities, water_consumptions, kind="linear", fill_value="extrapolate"
        )

        # Вычисление значений
        salt_consumption = float(salt_interp(density))
        water_consumption = float(water_interp(density))
        return JsonResponse(
            {
                "salt_consumption": round(salt_consumption, 2),
                "water_consumption": round(water_consumption, 2),
            }
        )
    except ValueError:
        return JsonResponse({"error": "Invalid input data"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
