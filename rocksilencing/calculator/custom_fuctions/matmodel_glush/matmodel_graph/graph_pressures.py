
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
    for i in range(len(names)):
        fig.add_trace(go.Scatter(y=Pressures[i], x=time, mode='lines', name=names[i], line=dict(color=colors[i]), line_shape='spline'))
    fig.update_layout(plot_bgcolor='#363a46',
                      paper_bgcolor='#363a46',
                      font=dict(size=14, color="#aaaeb9"),
                      legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
                      margin=dict(l=100, r=100, t=100, b=100, pad=0))
    fig.update_xaxes(title_text="Время обработки, мин",
                     gridcolor='#444854',
                     showline=False,
                     zeroline=False,
                     ticks="outside",
                     tickwidth=1,
                     tickcolor="rgb(170, 174, 185)",
                     griddash='dash',
                     )
    fig.update_yaxes(title_text="Давление, атм",
                     ticks="outside",
                     showline=False,
                     zeroline=False,
                     gridcolor='#444854',
                     tickcolor="rgb(170, 174, 185)",
                     griddash='dash',
                     )
    html_div = fig.to_html(full_html=False)
    return html_div
