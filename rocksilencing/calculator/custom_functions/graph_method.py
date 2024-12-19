import plotly.graph_objects as go
import pandas as pd
from typing import List, Dict


def create_plot(results: List[Dict]) -> str:
    """
    Создает график с накопительными областями, показывающий состав различных минералов.

    Аргументы:
        results: Список словарей, содержащий данные о составе минералов и процентном
                соотношении смеси. Каждый словарь должен содержать ключи для каждого
                минерала (Calcit, Gips и т.д.) и Part_of_mixture для процентного соотношения.

    Возвращает:
        str: HTML-представление графика, готовое для встраивания в веб-страницу

    Пример входных данных:
        [
            {
                "Part_of_mixture": 0,
                "Calcit": 100,
                "Gips": 50,
                ...
            },
            ...
        ]
    """
    # Определяем конфигурацию для каждого минерала:
    # - name: название для легенды
    # - color: цвет для области на графике
    minerals = {
        "Calcit": {"name": "Кальцит CaCO3", "color": "#ffc000"},
        "Gips": {"name": "Гипс CaSO4x2H2O", "color": "#1c9a6b"},
        "Bassanit": {"name": "Бассанит CaSO4x0.5H2O", "color": "#f5800e"},
        "Anhydrate": {"name": "Ангидрит CaSO4", "color": "#871d99"},
        "Celestine": {"name": "Целестин SrSO4", "color": "#d0326b"},
        "Barit": {"name": "Барит BrSO4", "color": "#0700b1"},
    }

    # Преобразуем список словарей в DataFrame для удобной работы с данными
    df = pd.DataFrame(results)

    # Создаем базовую фигуру
    fig = go.Figure()

    # Добавляем слои для каждого минерала
    for mineral, properties in minerals.items():
        fig.add_trace(
            go.Scatter(
                x=df["Part_of_mixture"],  # Процентное соотношение смеси
                y=df[mineral],  # Количество минерала
                fill="tonexty",  # Заполнение области под линией
                mode="none",  # Отключаем отображение линий и маркеров
                name=properties["name"],  # Название для легенды
                fillcolor=properties["color"],  # Цвет заполнения
                stackgroup="one",  # Группировка для накопительного графика
            )
        )

    # Настраиваем общий вид графика
    fig.update_layout(
        # Цвета фона
        plot_bgcolor="#363a46",  # Цвет фона области графика
        paper_bgcolor="#363a46",  # Цвет фона вокруг графика
        # Настройки шрифта
        font=dict(size=14, color="#aaaeb9"),
        # Настройки легенды
        legend=dict(
            orientation="h",  # Горизонтальное расположение
            yanchor="bottom",  # Привязка к нижней части
            y=1.02,  # Положение по вертикали
            xanchor="center",  # Привязка к центру
            x=0.5,  # Положение по горизонтали
        ),
        # Отступы
        margin=dict(
            l=100,
            r=100,  # Слева и справа
            t=100,
            b=100,  # Сверху и снизу
            pad=0,  # Дополнительный отступ
        ),
    )

    # Общие настройки для осей
    axis_common_props = dict(
        showline=False,  # Отключаем линии осей
        zeroline=False,  # Отключаем нулевую линию
        gridcolor="#444854",  # Цвет сетки
        tickwidth=1,  # Толщина отметок
        tickcolor="rgb(170, 174, 185)",  # Цвет отметок
        griddash="dash",  # Пунктирная сетка
        ticks="outside",  # Отметки снаружи
    )

    # Настройки оси X
    fig.update_xaxes(
        title_text="Доля первой воды, %",  # Подпись оси
        dtick=10,  # Шаг делений
        **axis_common_props  # Добавляем общие настройки
    )

    # Настройки оси Y
    fig.update_yaxes(
        title_text="Масса осадка, мг/л",  # Подпись оси
        **axis_common_props  # Добавляем общие настройки
    )

    # Преобразуем график в HTML
    return fig.to_html(full_html=False)
