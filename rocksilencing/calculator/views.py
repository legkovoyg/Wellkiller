from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def calculator_page(request):
    return render(request,"calculator/main.html")