def create_a_rec(data):
    rules = [
        {
            "conditions": {
                "collector_type": lambda x: x > 500,
                "pressure_type": lambda x: x == "нефть", 
                "temperature": lambda x: x > 150,
                "water_sensitive": lambda x:x == "not_water_sensitive",
            },
            "recommendation": "Использовать метод А",
        },
        {
            "conditions": {
                "pressure": lambda x: x <= 500,
                "fluid_type": lambda x: x == "газ",
            },
            "recommendation": "Использовать метод B",
        },
        # Добавьте больше правил по необходимости
    ]


    def get_recommendation(data):
        for rule in rules:
            if all(condition(data[key]) for key, condition in rule["conditions"].items()):
                return rule["recommendation"]
        return "Нет подходящей рекомендации"


    # Сбор данных от пользователя
    data = {}
    data["pressure"] = float(input("Введите давление: "))
    data["fluid_type"] = input("Введите тип флюида (нефть/газ): ")

    # Получение рекомендации
    recommendation = get_recommendation(data)
    print(f"Рекомендация: {recommendation}")
