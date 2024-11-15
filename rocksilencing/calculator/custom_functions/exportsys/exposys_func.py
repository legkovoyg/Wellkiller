import json
import os
from django.conf import settings


def load_rules():
    # Корректный путь к файлу относительно BASE_DIR
    file_path = os.path.join(settings.BASE_DIR, 'calculator', 'custom_functions', 'exportsys', 'rules.json')
    
    # Проверка, существует ли файл
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл {file_path} не найден.")

    # Открытие и чтение JSON файла
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


# Функция для получения рекомендации на основе данных
def get_recommendation_from_rules(data):
    rules = load_rules()
    for rule in rules:
        # Проверка условий правила
        if (data['collector_type'] == rule['collector_type'] and
            data['pressure_type'] == rule['pressure_type'] and
            rule['temperature_min'] <= float(data['temperature']) <= rule['temperature_max'] and
            data['water_sensitive'] == rule['water_sensitive']):
            return rule['recommendation']
    return "Нет подходящей рекомендации для введённых данных"
