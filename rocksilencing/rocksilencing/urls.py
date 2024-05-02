"""
URL configuration for rocksilencing project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from calculator.views import calculator_page, scale_calculator_page, reagent_base_page, history_page, FAQ_page

from users.views import logout_user, login_user, register_user
from rocksilencing import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', calculator_page),
    path('calculator/', calculator_page, name='calculator'),
    path('calculator/scale_calculator/', scale_calculator_page, name = 'scale_calculator'),
    path('calculator/reagent_base/', reagent_base_page, name = 'reagent_base'),
    path('calculator/history_page/', history_page, name = 'history_page'),
    path('calculator/FAQ_page', FAQ_page, name = 'FAQ_page'),
    path('users/', include('users.urls', namespace = "users"))
]
