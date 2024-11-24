import json
from abc import ABC, abstractmethod
from typing import List, Dict
import os


# Интерфейс для загрузчика технологий (DIP)
class TechnologyLoader(ABC):
    @abstractmethod
    def load_technologies(self) -> List[Dict]:
        pass


# Реализация загрузчика технологий из JSON
class JSONTechnologyLoader(TechnologyLoader):
    def __init__(self, filename: str):
        # Получаем абсолютный путь к файлу относительно текущего скрипта
        self.filepath = os.path.join(os.path.dirname(__file__), filename)

    def load_technologies(self) -> List[Dict]:
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"Файл '{self.filepath}' не найден.")
        
        with open(self.filepath, "r", encoding="utf-8") as file:
            return json.load(file)


# DTO для технологии
class TechnologyDTO:
    def __init__(
        self, tech_name: str, description: str, type_: List[str], pressure: List[str],
        water_sensitive: bool, min_temperature: float, max_temperature: float,
        min_density: float, max_density: float
    ):
        self.tech_name = tech_name
        self.description = description
        self.type = type_
        self.pressure = pressure
        self.water_sensitive = water_sensitive
        self.min_temperature = min_temperature
        self.max_temperature = max_temperature
        self.min_density = min_density
        self.max_density = max_density

    def __repr__(self):
        return f"TechnologyDTO(tech_name={self.tech_name})"


# Входные данные пользователя
class UserInput:
    def __init__(self, type_: str, pressure: str, temperature: float, water_sensitive: bool):
        self.type = type_
        self.pressure = pressure
        self.temperature = temperature
        self.water_sensitive = water_sensitive


# Фильтр для технологий
class TechnologyFilter:
    def __init__(self, technologies: List[Dict]):
        self.technologies = technologies

    def filter(self, user_input: UserInput) -> List[TechnologyDTO]:
        suitable_technologies = []

        for tech in self.technologies:
            # Проверка типа коллектора
            if user_input.type not in tech["type"]:
                continue

            # Проверка типа давления
            if user_input.pressure not in tech["pressure"]:
                continue

            # Проверка водочувствительности
            if tech["water_sensitive"] != user_input.water_sensitive:
                continue

            # Проверка температуры
            if not (tech["min_temperature"] <= user_input.temperature <= tech["max_temperature"]):
                continue

            # Проверка плотности (если есть в user_input)
            if hasattr(user_input, "density"):
                if not (tech["min_density"] <= user_input.density <= tech["max_density"]):
                    continue

            # Если технология подходит, преобразуем её в DTO
            suitable_technologies.append(
                TechnologyDTO(
                    tech_name=tech["tech_name"],
                    description=tech["description"],
                    type_=tech["type"],
                    pressure=tech["pressure"],
                    water_sensitive=tech["water_sensitive"],
                    min_temperature=tech["min_temperature"],
                    max_temperature=tech["max_temperature"],
                    min_density=tech["min_density"],
                    max_density=tech["max_density"]
                )
            )

        return suitable_technologies


# Селектор технологий
class TechnologySelector:
    def __init__(self, loader: TechnologyLoader):
        self.loader = loader

    def find_technologies(self, user_input: UserInput) -> List[TechnologyDTO]:
        technologies = self.loader.load_technologies()
        filter_ = TechnologyFilter(technologies)
        return filter_.filter(user_input)


# Использование
if __name__ == "__main__":
    # Загрузка технологий из JSON
    loader = JSONTechnologyLoader("MOCK_DATA-4.json")
    selector = TechnologySelector(loader)

    # Ввод пользователя
    user_input = UserInput(
        type_="terrigenous",
        pressure="abnormal_high",
        temperature=150,
        water_sensitive=True
    )

    # Поиск подходящих технологий
    matched_technologies = selector.find_technologies(user_input)

    if matched_technologies:
        print("Подходящие технологии:")
        print(matched_technologies)
    else:
        print("Нет подходящих технологий.")
