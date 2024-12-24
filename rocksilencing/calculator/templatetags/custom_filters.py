# calculator/templatetags/custom_filters.py

from django import template

register = template.Library()


@register.filter
def in_list(value, list_values):
    """
    Проверяет, находится ли value в списке list_values, разделённом запятыми.
    Использование:
    {% if calc_type|in_list:"Глушение скважины,Глушение скважины c экспертной системе,Все включено" %}
        ... показываем элемент ...
    {% endif %}
    """
    if not value or not list_values:
        return False
    return value in list_values.split(",")
