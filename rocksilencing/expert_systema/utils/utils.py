from expert_systema.models.technology import Technology


def filter_technologies(rock_type, pressure_coefficient, temperature, is_water_sensitive):
    # Вывод входных параметров
    print("Вызов filter_technologies с параметрами:")
    print("rock_type:", rock_type)
    print("pressure_coefficient:", pressure_coefficient)
    print("temperature:", temperature)
    print("is_water_sensitive:", is_water_sensitive)

    # Проверка входных параметров
    if not all([rock_type, pressure_coefficient, temperature]):
        print("Один из обязательных параметров отсутствует. Возвращаем None.")
        return None

    # Определение типа коллектора на основе типа горной породы
    collector_mapping = {
        "sandstone": "collector_terrigenous",
        "carbonate": "collector_carbonate",
    }
    collector_field = collector_mapping.get(rock_type)
    print("Определённый collector_field:", collector_field)
    if not collector_field:
        print("Нет сопоставления для rock_type. Возвращаем None.")
        return None

    # Базовый запрос: выбираем технологии, где значение collector_field равно 2
    base_query = Technology.objects.filter(**{collector_field: 2})
    print("Кол-во технологий после фильтра по коллектору:", base_query.count())

    # Если технология чувствительна к воде – фильтруем по water_compatible
    if is_water_sensitive:
        base_query = base_query.filter(water_compatible=True)
        print("После фильтрации по water_compatible, технологий:", base_query.count())

    # Фильтрация по диапазону температур
    base_query = base_query.filter(
        temperature_min__lte=temperature,
        temperature_max__gte=temperature
    )
    print("После фильтрации по температуре, технологий:", base_query.count())

    # Отображение давления по pressure_coefficient
    pressure_mapping = {
        "less_0.8": "pressure_anpd",
        "0.8_1": "pressure_npnd",
        "1-1.1": "pressure_nd",
        "1_1.3": "pressure_npvd",
        "more_1.3": "pressure_avpd",
    }
    pressure_field = pressure_mapping.get(pressure_coefficient)
    print("Определённое pressure_field:", pressure_field)
    if not pressure_field:
        print("pressure_coefficient не найден в mapping. Возвращаем None.")
        return None

    # Фильтрация по давлению: оставляем технологии, у которых по pressure_field значение 1 или 2
    base_query = base_query.filter(**{pressure_field + "__in": [1, 2]})
    print("После фильтрации по давлению, технологий:", base_query.count())

    # Готовим словарь для группировки технологий по группам
    grouped_technologies = {}

    # Проходим по всем оставшимся технологиям и рассчитываем общий статус
    for tech in base_query:
        # 1. Collector: уже гарантированно 2 (так как мы фильтровали по нему)
        collector_applicability = 2

        # 2. Water: если требуется, то проверяем поле water_compatible
        water_applicability = 2 if (not is_water_sensitive or tech.water_compatible) else 0

        # 3. Temperature: поскольку технология проходит фильтр температур, считаем 2
        temperature_applicability = 2

        # 4. Pressure: значение из выбранного pressure_field, может быть 1 или 2
        pressure_applicability = getattr(tech, pressure_field)

        # Собираем значения в список для вычисления общего статуса
        values = [collector_applicability, water_applicability, temperature_applicability, pressure_applicability]
        print(f"Технология {tech.name}: collector={collector_applicability}, water={water_applicability}, "
              f"temperature={temperature_applicability}, pressure={pressure_applicability}")

        # Если хоть один критерий не применим (0), технология не применима
        if 0 in values:
            overall_status = "Не применим"
        # Если все критерии полностью применимы (все 2)
        elif all(v == 2 for v in values):
            overall_status = "Применим"
        # Если ни один не равен 0, но есть хотя бы один 1, то технология частично применима
        else:
            overall_status = "Частично применим"

        print(f"Технология {tech.name} итоговый статус: {overall_status}")

        # Группируем по имени группы технологии
        group_name = tech.group.name
        if group_name not in grouped_technologies:
            grouped_technologies[group_name] = []
        grouped_technologies[group_name].append((tech, overall_status))

    print("Итоговая группировка технологий:")
    for group, techs in grouped_technologies.items():
        print(f"Группа: {group} – {len(techs)} технологий")
    return grouped_technologies

