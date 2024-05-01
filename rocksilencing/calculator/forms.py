from django import forms
from django.contrib.auth import get_user_model



class Scale_Calculator_form(forms.Form):
    # Параметры первого вещества
    Cl_1 = forms.FloatField(label = "", widget = forms.NumberInput(
        attrs = {'class':"input","for":"Cl_1","type":"text", "style":"background: #292e3c;"}))
    SO4_1  = forms.FloatField(label="", widget = forms.NumberInput(
        attrs = {'class':"input","for":"SO4_1","type":"text", "style":"background: #363A47;"}))
    HCO3_1 = forms.FloatField(label = '', widget= forms.NumberInput(
        attrs = {'class':"input","for":"Cl_1","type":"text", "style":"background: #292e3c;"}))
    Ca_1 = forms.FloatField(label = '', widget= forms.NumberInput(
        attrs = {'class':"input","for":"Ca_1","type":"text", "style":"background: #363A47;"}))
    Mg_1 = forms.FloatField(label="", widget=forms.NumberInput(
        attrs = {'class':"input","for":"Mg_1","type":"text", "style":"background: #292e3c;"}))
    Na_1 = forms.FloatField(label="", widget=forms.NumberInput(
        attrs = {'class':"input","for":"Na_1","type":"text", "style":"background: #363A47;"}))
    Ba_1 = forms.FloatField(label="",widget=forms.NumberInput(
        attrs={'class': "input","for":"Ba_1","type":"text", "style":"background: #292e3c;"}))
    Sr_1 = forms.FloatField(label="",widget=forms.NumberInput(
        attrs={'class': "input","for":"Sr_1","type":"text", "style":"background:  #363A47;"}))
    pH_1 = forms.FloatField(label='',widget=forms.NumberInput(
        attrs={"type":"text", "id":"ph_1", "style":"width: 60px border-radius: 4px; background: rgba(255, 255, 255, 0.06); border: none; outline: none; color: #fff;"}))
    ro_1 = forms.FloatField(label='', widget=forms.NumberInput(
        attrs={"type":"text", "id":"density_1" ,"style":"width: 60px; border-radius: 4px; background: rgba(255, 255, 255, 0.06); border: none; outline: none; color: #fff;"}))

    # Параметры второго вещества

    Cl_2 = forms.FloatField(label = "", widget = forms.NumberInput(
        attrs = {'class':"input","for":"Cl_2","type":"text", "style":"background: #292e3c;"}))
    SO4_2 = forms.FloatField(label = "", widget = forms.NumberInput(
        attrs = {'class':"input","for":"SO4_2","type":"text", "style":"background: #363A47;"}))
    HCO3_2 = forms.FloatField(label = "", widget = forms.NumberInput(
        attrs = {'class':"input","for":"HCO3_2","type":"text", "style":"background: #292e3c;"}))
    Ca_2 = forms.FloatField(label = "", widget = forms.NumberInput(
        attrs = {'class':"input","for":"Ca_2","type":"text", "style":"background: #363A47;"}))
    Mg_2 = forms.FloatField(label = "", widget = forms.NumberInput(
        attrs = {'class':"input","for":"Mg_2","type":"text", "style":"background: #292e3c;"}))
    Na_2 = forms.FloatField(label = "", widget = forms.NumberInput(
        attrs = {'class':"input","for":"Na_2","type":"text", "style":"background: #363A47;"}))
    Ba_2 = forms.FloatField(label = "", widget = forms.NumberInput(
        attrs = {'class':"input","for":"Ba_2","type":"text", "style":"background: #292e3c;"}))
    Sr_2 = forms.FloatField(label = "", widget = forms.NumberInput(
        attrs = {'class':"input","for":"Sr_2","type":"text", "style":"background: #363A47;"}))
    pH_2 = forms.FloatField(label='',widget=forms.NumberInput(
        attrs={"type":"text", "id":"ph_2",
               "style":"width: 60px border-radius: 4px; background: rgba(255, 255, 255, 0.06); border: none;"
                       " outline: none; color: #fff;"}))
    ro_2 = forms.FloatField(label='', widget=forms.NumberInput(
        attrs={"type":"text", "id":"density_2" ,
               "style":"width: 60px; border-radius: 4px; background: rgba(255, 255, 255, 0.06); border: none;"
                       " outline: none; color: #fff;"}))
    Temperature = forms.FloatField (label='',widget=forms.NumberInput(
        attrs={"type":"text", "id":"ph_1", "style":"width: 60px border-radius: 4px; "
        "background: rgba(255, 255, 255, 0.06); border: none; outline: none; color: #fff; text-align:center;"}))
    Pressure =   forms.FloatField (label='',widget=forms.NumberInput(
        attrs={"type":"text", "id":"ph_1", "style":"width: 60px border-radius: 4px; "
        "background: rgba(255, 255, 255, 0.06); border: none; outline: none; color: #fff; text-align:center;"}))
    Part_of_Mixture = forms.FloatField (label='',widget=forms.NumberInput(
        attrs={"type":"text", "id":"ph_1", "style":"width: 60px border-radius: 4px; "
        "background: rgba(255, 255, 255, 0.06); border: none; outline: none; color: #fff; text-align:center;"}))




