from django import forms
from django.db import models
from django.contrib.auth import get_user_model


class Scale_Calculator_form_1(forms.Form):
    # Параметры первого вещества
    Cl_1 = forms.FloatField(label="", widget=forms.NumberInput(
        attrs={'class': "input", "oninput": "limitLength(event)", "for": "Cl_1", "type": "text",
               "style": "background: #292e3c;"}))
    SO4_1 = forms.FloatField(label="", widget=forms.NumberInput(
        attrs={'class': "input", "oninput": "limitLength(event)", "for": "SO4_1", "type": "text",
               "style": "background: #363A47;"}))
    HCO3_1 = forms.FloatField(label='', widget=forms.NumberInput(
        attrs={'class': "input", "oninput": "limitLength(event)", "for": "Cl_1", "type": "text",
               "style": "background: #292e3c;"}))
    Ca_1 = forms.FloatField(label='', widget=forms.NumberInput(
        attrs={'class': "input", "oninput": "limitLength(event)", "for": "Ca_1", "type": "text",
               "style": "background: #363A47;"}))
    Mg_1 = forms.FloatField(label="", widget=forms.NumberInput(
        attrs={'class': "input", "oninput": "limitLength(event)", "for": "Mg_1", "type": "text",
               "style": "background: #292e3c;"}))
    Na_1 = forms.FloatField(label="", widget=forms.NumberInput(
        attrs={'class': "input", "oninput": "limitLength(event)", "for": "Na_1", "type": "text",
               "style": "background: #363A47;"}))
    Ba_1 = forms.FloatField(label="", widget=forms.NumberInput(
        attrs={'class': "input", "oninput": "limitLength(event)", "for": "Ba_1", "type": "text",
               "style": "background: #292e3c;"}))
    Sr_1 = forms.FloatField(label="", widget=forms.NumberInput(
        attrs={'class': "input", "oninput": "limitLength(event)", "for": "Sr_1", "type": "text",
               "style": "background:  #363A47;"}))
    pH_1 = forms.FloatField(label='', widget=forms.NumberInput(
        attrs={"type": "text", "oninput": "limitLength(event)", "id": "ph_1",
               "style": "width: 60px; border-radius: 30px; background: rgba(255, 255, 255, 0.06); border: none; outline: none; color: #fff;"}))
    ro_1 = forms.FloatField(label='', widget=forms.NumberInput(
        attrs={"type": "text", "oninput": "limitLength(event)", "id": "density_1",
               "style": "width: 60px; border-radius: 4px; background: rgba(255, 255, 255, 0.06); border: none; outline: none; color: #fff;"}))
    # Параметры второго вещества
    Cl_2 = forms.FloatField(label="", widget=forms.NumberInput(
        attrs={'class': "input", "for": "Cl_2", "type": "text", "style": "background: #292e3c;"}))
    SO4_2 = forms.FloatField(label="", widget=forms.NumberInput(
        attrs={'class': "input", "for": "SO4_2", "type": "text", "style": "background: #363A47;"}))
    HCO3_2 = forms.FloatField(label="", widget=forms.NumberInput(
        attrs={'class': "input", "for": "HCO3_2", "type": "text", "style": "background: #292e3c;"}))
    Ca_2 = forms.FloatField(label="", widget=forms.NumberInput(
        attrs={'class': "input", "for": "Ca_2", "type": "text", "style": "background: #363A47;"}))
    Mg_2 = forms.FloatField(label="", widget=forms.NumberInput(
        attrs={'class': "input", "for": "Mg_2", "type": "text", "style": "background: #292e3c;"}))
    Na_2 = forms.FloatField(label="", widget=forms.NumberInput(
        attrs={'class': "input", "for": "Na_2", "type": "text", "style": "background: #363A47;"}))
    Ba_2 = forms.FloatField(label="", widget=forms.NumberInput(
        attrs={'class': "input", "for": "Ba_2", "type": "text", "style": "background: #292e3c;"}))
    Sr_2 = forms.FloatField(label="", widget=forms.NumberInput(
        attrs={'class': "input", "for": "Sr_2", "type": "text", "style": "background: #363A47;"}))
    pH_2 = forms.FloatField(label='', widget=forms.NumberInput(
        attrs={"type": "text", "id": "ph_2",
               "style": "width: 60px; border-radius: 30px; background: rgba(255, 255, 255, 0.06); border: none;"
                        " outline: none; color: #fff;"}))
    ro_2 = forms.FloatField(label='', widget=forms.NumberInput(
        attrs={"type": "text", "id": "density_2",
               "style": "width: 60px; border-radius: 4px; background: rgba(255, 255, 255, 0.06); border: none;"
                        " outline: none; color: #fff;"}))
    # Параметры смеси
    Temperature = forms.FloatField(label='', widget=forms.NumberInput(
        attrs={"type": "text", "oninput": "limitLength(event)", "id": "ph_1",
               "style": "width: 120px; border-radius: 4px; "
                        "background: rgba(255, 255, 255, 0.06); border: none; outline: none; color: #fff; text-align:center;"}))
    Pressure = forms.FloatField(label='', widget=forms.NumberInput(
        attrs={"type": "text", "oninput": "limitLength(event)", "id": "ph_1",
               "style": "width: 120px; border-radius: 4px; "
                        "background: rgba(255, 255, 255, 0.06); border: none; outline: none; color: #fff; text-align:center;"}))
    Part_of_Mixture = forms.FloatField(label='', widget=forms.NumberInput(
        attrs={"type": "text", "oninput": "limitLength(event)", "id": "ph_1",
               "style": "width: 120px; border-radius: 4px; "
                        "background: rgba(255, 255, 255, 0.06); border: none; outline: none; color: #fff; text-align:center;"}))





class Scale_Calculator_form_2(forms.Form):
    # Параметры первого вещества
    Cl_1_another = forms.FloatField(label="", widget=forms.NumberInput(
        attrs={'class': "input", "oninput": "limitLength(event)", "step": "0.0001", "for": "Cl_1", "type": "text",
               "style": "background: #292e3c;"}))
    SO4_1_another = forms.FloatField(label="", widget=forms.NumberInput(
        attrs={'class': "input", "oninput": "limitLength(event)", "for": "SO4_1", "type": "text",
               "style": "background: #363A47;"}))
    HCO3_1_another = forms.FloatField(label='', widget=forms.NumberInput(
        attrs={'class': "input", "oninput": "limitLength(event)", "for": "Cl_1", "type": "text",
               "style": "background: #292e3c;"}))
    Ca_1_another = forms.FloatField(label='', widget=forms.NumberInput(
        attrs={'class': "input", "oninput": "limitLength(event)", "for": "Ca_1", "type": "text",
               "style": "background: #363A47;"}))
    Mg_1_another = forms.FloatField(label="", widget=forms.NumberInput(
        attrs={'class': "input", "oninput": "limitLength(event)", "for": "Mg_1", "type": "text",
               "style": "background: #292e3c;"}))
    Na_1_another = forms.FloatField(label="", widget=forms.NumberInput(
        attrs={'class': "input", "oninput": "limitLength(event)", "for": "Na_1", "type": "text",
               "style": "background: #363A47;"}))
    Ba_1_another = forms.FloatField(label="", widget=forms.NumberInput(
        attrs={'class': "input", "oninput": "limitLength(event)", "for": "Ba_1", "type": "text",
               "style": "background: #292e3c;"}))
    Sr_1_another = forms.FloatField(label="", widget=forms.NumberInput(
        attrs={'class': "input", "oninput": "limitLength(event)", "for": "Sr_1", "type": "text",
               "style": "background:  #363A47;"}))

    # Параметры второго вещества
    Cl_2_another = forms.FloatField(label="", widget=forms.NumberInput(
        attrs={'class': "input", "oninput": "limitLength(event)", "for": "Cl_2", "type": "text",
               "style": "background: #292e3c;"}))
    SO4_2_another = forms.FloatField(label="", widget=forms.NumberInput(
        attrs={'class': "input", "oninput": "limitLength(event)", "for": "SO4_2", "type": "text",
               "style": "background: #363A47;"}))
    HCO3_2_another = forms.FloatField(label="", widget=forms.NumberInput(
        attrs={'class': "input", "oninput": "limitLength(event)", "for": "HCO3_2", "type": "text",
               "style": "background: #292e3c;"}))
    Ca_2_another = forms.FloatField(label="", widget=forms.NumberInput(
        attrs={'class': "input", "oninput": "limitLength(event)", "for": "Ca_2", "type": "text",
               "style": "background: #363A47;"}))
    Mg_2_another = forms.FloatField(label="", widget=forms.NumberInput(
        attrs={'class': "input", "oninput": "limitLength(event)", "for": "Mg_2", "type": "text",
               "style": "background: #292e3c;"}))
    Na_2_another = forms.FloatField(label="", widget=forms.NumberInput(
        attrs={'class': "input", "oninput": "limitLength(event)", "for": "Na_2", "type": "text",
               "style": "background: #363A47;"}))
    Ba_2_another = forms.FloatField(label="", widget=forms.NumberInput(
        attrs={'class': "input", "oninput": "limitLength(event)", "for": "Ba_2", "type": "text",
               "style": "background: #292e3c;"}))
    Sr_2_another = forms.FloatField(label="", widget=forms.NumberInput(
        attrs={'class': "input", "oninput": "limitLength(event)", "for": "Sr_2", "type": "text",
               "style": "background: #363A47;"}))


class ModelGlushForm(forms.Form):
    Oil_field_name = forms.CharField(label='Месторождение',
                                     widget=forms.TextInput(attrs={"id": "field", "style": "background: #363A47;"}))
    Bush_name = forms.CharField(label='', widget=forms.TextInput(attrs={"id": "bush", "style": "background: #292e3c;"}))
    Well_name = forms.CharField(label='',
                                widget=forms.TextInput(attrs={"id": "well_name", "style": "background: #363A47;"}))
    Design_name = forms.CharField(label='',
                                  widget=forms.TextInput(attrs={"id": "design_name", "style": "background: #292e3c;"}))
    types_of_exp = [
        ('УЭЦН', 'УЭЦН'),
        ('УШГН', 'УШГН')
    ]
    EXP_type = forms.ChoiceField(widget=forms.Select(
        attrs={"margin": "0", "padding": "0", "box-sizing": "border-box", "style": "background: #363A47;", "color": "black"}),
                                 choices=types_of_exp)
    types_of_glush = [
        ("НКТ", "НКТ"),
        ("Затруб", " Затруб")
    ]
    Glush_type = forms.ChoiceField(widget=forms.Select(
        attrs={"margin": "0", "padding": "0", "box-sizing": "border-box", "style": "background: #292e3c;", "color": "black"}),
                                   choices=types_of_glush)
    Oil_density = forms.FloatField(label="", widget=forms.NumberInput(
        attrs={'class': "input", "oninput": "limitLength(event)", "type": "text", "style": "background: #363A47;"}))
    Plast_pressure = forms.FloatField(label="", widget=forms.NumberInput(
        attrs={'class': "input", "oninput": "limitLength(event)", "type": "text", "style": "background: #292e3c;"}))
    Plast_thickness = forms.FloatField(label="", widget=forms.NumberInput(
        attrs={'class': "input", "oninput": "limitLength(event)", "type": "text", "style": "background: #292e3c;"}))
    Well_length = forms.FloatField(label="", widget=forms.NumberInput(
        attrs={'class': "input", "oninput": "limitLength(event)", "type": "text", "style": "background: #363A47;"}))
    NKT_length = forms.FloatField(label="", widget=forms.NumberInput(
        attrs={'class': "input", "oninput": "limitLength(event)", "type": "text", "style": "background: #292e3c;"}))
    EXP_length = forms.FloatField(label="", widget=forms.NumberInput(
        attrs={'class': "input", "oninput": "limitLength(event)", "type": "text", "style": "background: #363A47;"}))
    NKT_inner_diameter = forms.FloatField(label="", widget=forms.NumberInput(
        attrs={'class': "input", "oninput": "limitLength(event)", "type": "text", "style": "background: #363A47;"}))
    NKT_external_diameter = forms.FloatField(label="", widget=forms.NumberInput(
        attrs={'class': "input", "oninput": "limitLength(event)", "type": "text", "style": "background: #292e3c;"}))
    EXP_inner_diameter = forms.FloatField(label="", widget=forms.NumberInput(
        attrs={'class': "input", "oninput": "limitLength(event)", "type": "text", "style": "background: #292e3c;"}))
    EXP_external_diameter = forms.FloatField(label="", widget=forms.NumberInput(
        attrs={'class': "input", "oninput": "limitLength(event)", "type": "text", "style": "background: #363A47;"}))
    Volume_of_car = forms.FloatField(label="", widget=forms.NumberInput(
        attrs={'class': "input", "oninput": "limitLength(event)", "type": "text", "style": "background: #363A47;"}))
    Debit = forms.FloatField(label="", widget=forms.NumberInput(
        attrs={'class': "input", "oninput": "limitLength(event)", "type": "text", "style": "background: #292e3c;"}))
    # Jgs_density = forms.FloatField(label="", widget=forms.NumberInput(
    #     attrs={'class': "input", "oninput": "limitLength(event)", "type": "text", "style": "background: #363A47;"}))
    types_of_jgs = [
        ("CaCl","CaCl"),
        ("KCl", "KCl"),
        ("CaЖГ", "CaЖГ"),
        ('без соли','без соли')
    ]
    Type_of_jgs = forms.ChoiceField(widget=forms.Select(
        attrs={"margin": "0", "padding": "0", "box-sizing": "border-box", "style": "background: #363A47;", "color": "black"}),
                                   choices=types_of_jgs)
    Phase_oil_permeability = forms.FloatField(label="", widget=forms.NumberInput(
        attrs={'class': "input", "oninput": "limitLength(event)", "type": "text", "style": "background: #292e3c;"}))
    Phase_jgs_permeability = forms.FloatField(label="", widget=forms.NumberInput(
        attrs={'class': "input", "oninput": "limitLength(event)", "type": "text", "style": "background: #363A47;"}))
    Oil_viscosity = forms.FloatField(label="", widget=forms.NumberInput(
        attrs={'class': "input", "oninput": "limitLength(event)", "type": "text", "style": "background: #292e3c;"}))
    Jgs_viscosity = forms.FloatField(label="", widget=forms.NumberInput(
        attrs={'class': "input", "oninput": "limitLength(event)", "type": "text", "style": "background: #363A47;"}))
    Radius_countour = forms.FloatField(label="", widget=forms.NumberInput(
        attrs={'class': "input", "oninput": "limitLength(event)", "type": "text", "style": "background: #363A47;"}))
    Porosity = forms.FloatField(label="", widget=forms.NumberInput(
        attrs={'class': "input", "oninput": "limitLength(event)", "type": "text", "style": "background: #292e3c;"}))
    YV_dole = forms.FloatField(label="", widget=forms.NumberInput(
        attrs={'class': "input", "oninput": "limitLength(event)", "type": "text", "style": "background: #292e3c;"}))
    YV_density = forms.FloatField(label="", widget=forms.NumberInput(
        attrs={'class': "input", "oninput": "limitLength(event)", "type": "text", "style": "background: #363A47;"}))
    Emul_dole = forms.FloatField(label="", widget=forms.NumberInput(
        attrs={'class': "input", "oninput": "limitLength(event)", "type": "text", "style": "background: #292e3c;"}))
    Emul_density = forms.FloatField(label="", widget=forms.NumberInput(
        attrs={'class': "input", "oninput": "limitLength(event)", "type": "text", "style": "background:  #363A47;"}))
    Zapas = forms.FloatField(label="", widget=forms.NumberInput(
        attrs={'class': "input", "oninput": "limitLength(event)", "type": "text", "style": "background: #292e3c;"}))
    False_zaboi = forms.FloatField(label="", widget=forms.NumberInput(
        attrs={'class': "input", "oninput": "limitLength(event)", "type": "text", "style": "background: #292e3c;"}))
    True_zaboi = forms.FloatField(label="", widget=forms.NumberInput(
        attrs={'class': "input", "oninput": "limitLength(event)", "type": "text", "style": "background:  #363A47;"}))
    From_yst_to_plast = forms.FloatField(label="", widget=forms.NumberInput(
        attrs={'class': "input", "oninput": "limitLength(event)", "type": "text", "style": "background:  #363A47;"}))
