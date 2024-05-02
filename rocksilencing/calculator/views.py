import plotly.express as px
from django.shortcuts import render
from django.http import HttpResponse
from calculator.forms import Scale_Calculator_form_1, Scale_Calculator_form_2
from calculator.Method_for_salt_calculator import calculate_full_result

# from .Main import calculate
# Create your views here.

def calculator_page(request):
    return render(request,"calculator/main_page.html")

def scale_calculator_page(request):
    if request.method == 'POST':
        x = [5, 15, 25, 35, 45, 55]
        y1 = [0.8, 0.6, 0.4, 0.2, 0, 0]
        y2 = [1.2, 1, 0.8, 0.6, 0.4, 0.2]
        form = Scale_Calculator_form_1(request.POST)
        if form.is_valid():
            # Входные данные для жидкости 1
            Cl_1 = float(request.POST['Cl_1'])
            SO4_1 = float(request.POST['SO4_1'])
            HCO3_1 = float(request.POST['HCO3_1'])
            Ca_1 = float(request.POST['Ca_1'])
            Mg_1 = float(request.POST['Mg_1'])
            Na_1 = float(request.POST['Na_1'])
            Ba_1 = float(request.POST['Ba_1'])
            Sr_1 = float(request.POST['Sr_1'])
            pH_1 = float(request.POST['pH_1'])
            ro_1 = float(request.POST['ro_1'])
            # Входные данные для жидкости 2
            Cl_2 = float(request.POST['Cl_2'])
            SO4_2 = float(request.POST['SO4_2'])
            HCO3_2 = float(request.POST['HCO3_2'])
            Ca_2 = float(request.POST['Ca_2'])
            Mg_2 = float(request.POST['Mg_2'])
            Na_2 = float(request.POST['Na_2'])
            Ba_2 = float(request.POST['Ba_2'])
            Sr_2 = float(request.POST['Sr_2'])
            pH_2 = float(request.POST['pH_2'])
            ro_2 = float(request.POST['ro_2'])
            # Условия смешивания
            Temperature = float(request.POST['Temperature'])  # Температура в градусах
            Pressure = float(request.POST['Pressure'])  # Давление в МПа
            custom_Part_of_Mixture = float(request.POST['Part_of_Mixture'])
            Parts_of_Mixture = [0, 5 ,10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

            fig = px.line(x=x, y=y1, name='First data')
            fig.add_trace(px.line(x=x, y=y2, name='Second data').data[0])
            fig.update_layout(
                title='My Graph',
                xaxis_title='X Axis',
                yaxis_title='Y Axis'
            )

            fig.update_xaxes(
                range=[0, 60]
            )

            fig.update_yaxes(
                range=[0, 1.5]
            )
            fig.write_html("templates/plot.html")

            if custom_Part_of_Mixture not in Parts_of_Mixture:
                Parts_of_Mixture.append(custom_Part_of_Mixture)
            all_results = []
            print(custom_Part_of_Mixture)
            for each_elem in Parts_of_Mixture:
                result = calculate_full_result(Cl_1,Cl_2,SO4_1,SO4_2,HCO3_1, HCO3_2, Ca_1,Ca_2,Mg_1,Mg_2,Na_1, Na_2, Ba_1, Ba_2,Sr_1,Sr_2,pH_1,pH_2,ro_1,ro_2, Temperature, Pressure, each_elem)
                all_results.append(result)

            return render(request, "calculator/salt.html", {"form": form, "all_results": all_results,"custom_Part_of_Mixture":custom_Part_of_Mixture})
    else:
        form = Scale_Calculator_form_1()
        form_2 = Scale_Calculator_form_2()
    return render(request,"calculator/salt.html", {"form": form, "form_2":form_2})

def reagent_base_page(request):
    return HttpResponse("Страница базы солеотложений")

def history_page(request):
    return HttpResponse("Страница истории")

def FAQ_page(request):
    return  HttpResponse("FAQ page")