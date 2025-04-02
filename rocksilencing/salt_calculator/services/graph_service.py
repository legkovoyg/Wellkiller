import plotly.graph_objects as go
import pandas as pd
import numpy as np
from typing import List, Dict, Tuple


def create_plot(results: List[Dict]) -> Tuple[str, Dict]:
    """
    Создает график с накопительными областями, показывающий состав различных минералов.

    Возвращает:
    Tuple[str, Dict]: кортеж из HTML-представления графика и словаря с данными графика
    """
    # Определяем конфигурацию для каждого минерала
    minerals = {
        "Calcit": {"name": "Кальцит CaCO3", "color": "#ffc000"},
        "Gips": {"name": "Гипс CaSO4x2H2O", "color": "#1c9a6b"},
        "Bassanit": {"name": "Бассанит CaSO4x0.5H2O", "color": "#f5800e"},
        "Anhydrate": {"name": "Ангидрит CaSO4", "color": "#871d99"},
        "Celestine": {"name": "Целестин SrSO4", "color": "#d0326b"},
        "Barit": {"name": "Барит BrSO4", "color": "#0700b1"},
    }

    # Преобразуем список словарей в DataFrame
    df = pd.DataFrame(results)

    # Создаем базовую фигуру
    fig = go.Figure()

    # Добавляем слои для каждого минерала
    for mineral, properties in minerals.items():
        fig.add_trace(
            go.Scatter(
                x=df["Part_of_mixture"].tolist(),  # Преобразуем в список
                y=df[mineral].tolist(),  # Преобразуем в список
                fill="tonexty",
                mode="none",
                name=properties["name"],
                fillcolor=properties["color"],
                stackgroup="one",
            )
        )

    # Настраиваем общий вид графика
    fig.update_layout(
        plot_bgcolor="#363a46",
        paper_bgcolor="#363a46",
        font=dict(size=14, color="#aaaeb9"),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
        ),
        margin=dict(
            l=100,
            r=100,
            t=100,
            b=100,
            pad=0,
        ),
    )

    # Общие настройки для осей
    axis_common_props = dict(
        showline=False,
        zeroline=False,
        gridcolor="#444854",
        tickwidth=1,
        tickcolor="rgb(170, 174, 185)",
        griddash="dash",
        ticks="outside",
    )

    # Настройки осей
    fig.update_xaxes(title_text="Доля первой воды, %", dtick=10, **axis_common_props)
    fig.update_yaxes(title_text="Масса осадка, мг/л", **axis_common_props)

    # Получаем данные графика для сохранения
    graph_dict = fig.to_dict()

    # Удаляем template, если он случайно попал в layout
    if "layout" in graph_dict and "template" in graph_dict["layout"]:
        del graph_dict["layout"]["template"]

    # Преобразуем numpy массивы в списки в словаре графика
    def convert_numpy_to_list(obj):
        if isinstance(obj, (np.ndarray, np.generic)):
            return obj.tolist()
        elif isinstance(obj, dict):
            return {key: convert_numpy_to_list(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [convert_numpy_to_list(item) for item in obj]
        return obj

    graph_dict = convert_numpy_to_list(graph_dict)

    # Получаем HTML представление
    graph_html = fig.to_html(full_html=False)

    return graph_html, graph_dict
