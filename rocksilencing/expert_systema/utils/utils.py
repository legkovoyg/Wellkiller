from expert_systema.models.technology import Technology


def filter_technologies(
    rock_type, pressure_coefficient, temperature, is_water_sensitive
):
    # Проверка входных параметров
    if not all([rock_type, pressure_coefficient, temperature]):
        return None

    # Определение типа коллектора
    collector_mapping = {
        "sandstone": "collector_terrigenous",
        "carbonate": "collector_carbonate",
    }

    collector_field = collector_mapping.get(rock_type)
    if not collector_field:
        return None

    # Базовый запрос
    base_query = Technology.objects.filter(**{collector_field: 2})

    if is_water_sensitive:
        base_query = base_query.filter(water_compatible=True)

    base_query = base_query.filter(
        temperature_min__lte=temperature, temperature_max__gte=temperature
    )

    # Фильтрация по давлению
    pressure_mapping = {
        "less_0.8": "pressure_anpd",
        "0.8_1": "pressure_npnd",
        "1-1.1": "pressure_nd",
        "1_1.3": "pressure_npvd",
        "more_1.3": "pressure_avpd",
    }

    pressure_field = pressure_mapping.get(pressure_coefficient)
    if not pressure_field:
        return None

    # Фильтруем по полям давления (>=1)
    # (Вы делаете __in: [1, 2], чтобы подобрать и "полностью", и "частично применимые")
    base_query = base_query.filter(**{pressure_field + "__in": [1, 2]})

    # Готовим словарь для группировок
    # Ключ — название группы, значение — список кортежей (Technology, "Применим"/"Частично применим")
    grouped_technologies = {}

    # Сначала обрабатываем "полностью применим" (==2)
    for tech in base_query.filter(**{pressure_field: 2}):
        group_name = tech.group.name
        if group_name not in grouped_technologies:
            grouped_technologies[group_name] = []
        # ВАЖНО: Вместо (tech.name, "Применим") теперь (tech, "Применим")
        grouped_technologies[group_name].append((tech, "Применим"))

    # Затем "частично применим" (==1)
    for tech in base_query.filter(**{pressure_field: 1}):
        group_name = tech.group.name
        if group_name not in grouped_technologies:
            grouped_technologies[group_name] = []
        # Аналогично
        grouped_technologies[group_name].append((tech, "Частично применим"))

    return grouped_technologies
