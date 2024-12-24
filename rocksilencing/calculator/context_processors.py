# calculator/context_processors.py


def calc_type_processor(request):
    """
    Добавляет переменную calc_type в контекст шаблонов.
    Если calc_type не установлен, устанавливает значение по умолчанию 'Все включено'.
    """
    return {"calc_type": request.session.get("calc_type", "Все включено")}
