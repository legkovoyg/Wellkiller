from django.shortcuts import render
from django.http import HttpResponse
from calculator.forms import Scale_Calculator_form
# from .Main import calculate
# Create your views here.

def calculator_page(request):
    return render(request,"calculator/main.html")

def scale_calculator_page(request):
    if request.method == 'POST':
        form = Scale_Calculator_form(request.POST)
        if form.is_valid():
            form.data['Cl_1'] = 444
            form.data['Bar.value'] = 222
            return render(request, "calculator/salt.html", {"form": form})
    else:
        form = Scale_Calculator_form()
    return render(request,"calculator/salt.html", {"form":form})

def reagent_base_page(request):
    return HttpResponse("Страница базы солеотложений")

def history_page(request):
    return HttpResponse("Страница истории")