from datetime import datetime
from django.shortcuts import render


def FilesMainWindow(request):
    # Пример данных для дизайнов
    designs = [
        {
            "name": "Дизайн A",
            "calc_type": "Тип 1",
            "field": "Месторождение 1",
            "cluster": "Куст-1",
            "well": "Скважина 1",
            "created": datetime(2024, 12, 1, 10, 30),
            "updated": datetime(2024, 12, 5, 15, 45),
        },
        {
            "name": "Дизайн B",
            "calc_type": "Тип 2",
            "field": "Месторождение 2",
            "cluster": "Куст-2",
            "well": "Скважина 2",
            "created": datetime(2024, 11, 25, 9, 15),
            "updated": datetime(2024, 12, 6, 12, 0),
        },
        {
            "name": "Дизайн C",
            "calc_type": "Тип 3",
            "field": "Месторождение 3",
            "cluster": "Куст-3",
            "well": "Скважина 3",
            "created": datetime(2024, 10, 20, 8, 45),
            "updated": datetime(2024, 12, 7, 16, 30),
        },
    ]

    # Чтобы проверить страницу без скважин надо просто раскоментить нижнюю строку
    # designs = None

    return render(request, "designs/designs.html", {"designs": designs})
