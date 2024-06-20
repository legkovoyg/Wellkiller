import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

def create_plot(results):
    needed_Calcit = []
    needed_Gips = []
    needed_Bassanit = []
    needed_Anhydrate = []
    needed_Celestine = []
    needed_Barit= []
    needed_percentage = []
    max_value = 0
    for each_elem in results:
        for key, value in each_elem.items():
            if key is not "Part_of_mixture":
                if value > max_value:
                    max_value = value
            else:
                continue
        needed_Calcit.append(each_elem["Calcit"])
        needed_Gips.append(each_elem["Gips"])
        needed_Bassanit.append(each_elem["Bassanit"])
        needed_Anhydrate.append(each_elem["Anhydrate"])
        needed_Celestine.append(each_elem["Celestine"])
        needed_Barit.append(each_elem["Barit"])
        needed_percentage.append(each_elem["Part_of_mixture"])

    fig = go.Figure()
    fig.add_trace(go.Scatter(x = needed_percentage, y = needed_Calcit, fill='tonexty', mode='none', name='Кальцит CaCO3', fillcolor='#ffc000',stackgroup='one' ))
    fig.add_trace(
        go.Scatter(x=needed_percentage, y=needed_Gips, fill='tonexty', mode='none', name='Гипс CaSO4x2H2O', fillcolor='#1c9a6b',stackgroup='one'))
    fig.add_trace(
        go.Scatter(x=needed_percentage, y=needed_Bassanit, fill='tonexty', mode='none', name='Бассанит CaSO4x0.5H2O',
                   fillcolor='#f5800e',stackgroup='one'))
    fig.add_trace(
        go.Scatter(x=needed_percentage, y=needed_Anhydrate, fill='tonexty', mode='none', name='Ангидрит CaSO4',
                   fillcolor='#871d99',stackgroup='one'))
    fig.add_trace(
        go.Scatter(x=needed_percentage, y=needed_Celestine, fill='tonexty', mode='none', name='Целестин SrSO4',
                   fillcolor='#d0326b',stackgroup='one'))
    fig.add_trace(
        go.Scatter(x=needed_percentage, y=needed_Barit, fill='tonexty', mode='none', name='Барит BrSO4',
                   fillcolor='#0700b1',stackgroup='one'))
    fig.update_layout(plot_bgcolor='#363a46',
                      paper_bgcolor='#363a46',
                      font=dict(size = 14, color = "#aaaeb9"),
                      legend=dict(orientation="h", yanchor = "bottom", y=1.02, xanchor="center", x=0.5),
                      # width = 1700,
                      # height = 800,
                      margin=dict(l=100, r=100, t=100, b=100, pad=0))
    # Название оси x, y
    fig.update_xaxes(title_text = "Доля первой воды, %",
                     gridcolor = '#444854',
                     showline = False,
                     zeroline = False,
                     dtick = 10,
                     ticks = "outside",
                     tickwidth = 1,
                     tickcolor = "rgb(170, 174, 185)",
                     griddash='dash',
                     )
    fig.update_yaxes(title_text="Масса осадка, мг/л",
                     ticks="outside",
                     showline = False,
                     zeroline=False,
                     gridcolor='#444854',
                     tickwidth=1,
                     tickcolor="rgb(170, 174, 185)",
                     griddash = 'dash',
                     )

    html_div = fig.to_html(full_html = False)
    return html_div
