from expert_systema.models.technology import Technology


def filter_technologies(
    rock_type, pressure_coefficient, temperature, is_water_sensitive
):
    # Начальная фильтрация по типу коллектора
    if rock_type == "sandstone":  # Песчаник
        collector_field = "collector_terrigenous"
    elif rock_type == "carbonate":  # Карбонат
        collector_field = "collector_carbonate"

    base_query = Technology.objects.filter(
        **{collector_field: 2}
    )  # Фильтрация по коллектору

    # Фильтрация по водочувствительности
    if is_water_sensitive:
        base_query = base_query.filter(water_compatible=True)

    # Фильтрация по температуре
    base_query = base_query.filter(
        temperature_min__lte=temperature, temperature_max__gte=temperature
    )

    # Фильтрация по коэффициенту аномальности
    pressure_mapping = {
        "less_0.8": "pressure_anpd",
        "0.8_1": "pressure_npnd",
        "1-1.1": "pressure_nd",
        "1_1.3": "pressure_npvd",
        "more_1.3": "pressure_avpd",
    }
    pressure_field = pressure_mapping.get(pressure_coefficient)
    if pressure_field:
        base_query = base_query.filter(
            **{pressure_field + "__in": [1, 2]}
        )  # Применим или частично применим

    # Ранжирование технологий
    applicable_technologies = base_query.filter(**{pressure_field: 2})  # Применим
    partially_applicable_technologies = base_query.filter(
        **{pressure_field: 1}
    )  # Частично применим

    # Группировка технологий по категориям
    grouped_technologies = {}
    for tech in applicable_technologies:
        group_name = tech.group.name
        if group_name not in grouped_technologies:
            grouped_technologies[group_name] = []
        grouped_technologies[group_name].append((tech.name, "Применим"))

    for tech in partially_applicable_technologies:
        group_name = tech.group.name
        if group_name not in grouped_technologies:
            grouped_technologies[group_name] = []
        grouped_technologies[group_name].append((tech.name, "Частично применим"))

    return grouped_technologies
