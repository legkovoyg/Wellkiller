import plotly.graph_objects as go

def create_matmodel_plot(Pressures, time):
    fig = go.Figure()
    names = [
        'Устьевое давление',
        'Забойное давление',
        "Потери на трение",
        "Давление в НКТ",
        "Давление в КП",
        "Давление в ЭК"
    ]
    colors = [
        "#e55757",
        '#46d39a',
        '#4ca2fe',
        '#f6800e',
        '#f8c20b',
        "#fe0000"
    ]
    
    # Добавление данных на график
    for i in range(len(names)):
        fig.add_trace(go.Scatter(
            y=Pressures[i], 
            x=time, 
            mode='lines', 
            name=names[i], 
            line=dict(color=colors[i]), 
            line_shape='spline'
        ))
    
    # Настройка внешнего вида графика с использованием autosize
    fig.update_layout(
        autosize=True,  # Делаем график адаптивным
        plot_bgcolor='#363a46',
        paper_bgcolor='#363a46',
        font=dict(size=14, color="#aaaeb9"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        margin=dict(l=50, r=50, t=50, b=50)
    )
    
    fig.update_xaxes(
        title_text="Время обработки, мин",
        gridcolor='#444854',
        showline=False,
        zeroline=False,
        ticks="outside",
        tickwidth=1,
        tickcolor="rgb(170, 174, 185)",
        griddash='dash'
    )
    
    fig.update_yaxes(
        title_text="Давление, атм",
        ticks="outside",
        showline=False,
        zeroline=False,
        gridcolor='#444854',
        tickcolor="rgb(170, 174, 185)",
        griddash='dash'
    )
    
    # Генерация HTML-кода графика с использованием Plotly
    html_div = fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    # Оборачиваем график в контейнер
    html_with_container = f"""
    <div id="graph-container" style="width:100%; height:auto; margin:auto;">
        {html_div}
    </div>
    """
    
    return html_with_container