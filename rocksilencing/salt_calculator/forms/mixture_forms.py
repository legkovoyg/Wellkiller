from django import forms
from django.db import models
from django.contrib.auth import get_user_model


class Scale_Calculator_form_1(forms.Form):
    # Параметры первого вещества
    Cl_1 = forms.FloatField(
        label="",
        widget=forms.NumberInput(
            attrs={
                "class": "input",
                "oninput": "limitLength(event)",
                "for": "Cl_1",
                "type": "text",
                "style": "background: #292e3c;text-align: center;",
            }
        ),
    )
    SO4_1 = forms.FloatField(
        label="",
        widget=forms.NumberInput(
            attrs={
                "class": "input",
                "oninput": "limitLength(event)",
                "for": "SO4_1",
                "type": "text",
                "style": "background: #363A47;text-align: center;",
            }
        ),
    )
    HCO3_1 = forms.FloatField(
        label="",
        widget=forms.NumberInput(
            attrs={
                "class": "input",
                "oninput": "limitLength(event)",
                "for": "Cl_1",
                "type": "text",
                "style": "background: #292e3c;text-align: center;",
            }
        ),
    )
    Ca_1 = forms.FloatField(
        label="",
        widget=forms.NumberInput(
            attrs={
                "class": "input",
                "oninput": "limitLength(event)",
                "for": "Ca_1",
                "type": "text",
                "style": "background: #363A47;text-align: center;",
            }
        ),
    )
    Mg_1 = forms.FloatField(
        label="",
        widget=forms.NumberInput(
            attrs={
                "class": "input",
                "oninput": "limitLength(event)",
                "for": "Mg_1",
                "type": "text",
                "style": "background: #292e3c;text-align: center;",
            }
        ),
    )
    Na_1 = forms.FloatField(
        label="",
        widget=forms.NumberInput(
            attrs={
                "class": "input",
                "oninput": "limitLength(event)",
                "for": "Na_1",
                "type": "text",
                "style": "background: #363A47;text-align: center;",
            }
        ),
    )
    Ba_1 = forms.FloatField(
        label="",
        widget=forms.NumberInput(
            attrs={
                "class": "input",
                "oninput": "limitLength(event)",
                "for": "Ba_1",
                "type": "text",
                "style": "background: #292e3c;text-align: center;",
            }
        ),
    )
    Sr_1 = forms.FloatField(
        label="",
        widget=forms.NumberInput(
            attrs={
                "class": "input",
                "oninput": "limitLength(event)",
                "for": "Sr_1",
                "type": "text",
                "style": "background:  #363A47;text-align: center;",
            }
        ),
    )
    pH_1 = forms.FloatField(
        label="",
        widget=forms.NumberInput(
            attrs={
                "type": "text",
                "oninput": "limitLength(event)",
                "id": "ph_1",
                "style": "width: 60px;text-align:center; border-radius: 30px; background: rgba(255, 255, 255, 0.06); border: none; outline: none; color: #fff;",
            }
        ),
    )
    ro_1 = forms.FloatField(
        label="",
        widget=forms.NumberInput(
            attrs={
                "type": "text",
                "oninput": "limitLength(event)",
                "id": "density_1",
                "style": "width: 60px;text-align:center; border-radius: 4px; background: rgba(255, 255, 255, 0.06); border: none; outline: none; color: #fff;",
            }
        ),
    )
    # Параметры второго вещества
    Cl_2 = forms.FloatField(
        label="",
        widget=forms.NumberInput(
            attrs={
                "class": "input",
                "for": "Cl_2",
                "type": "text",
                "style": "background: #292e3c; text-align: center;",
            }
        ),
    )
    SO4_2 = forms.FloatField(
        label="",
        widget=forms.NumberInput(
            attrs={
                "class": "input",
                "for": "SO4_2",
                "type": "text",
                "style": "background: #363A47; text-align: center;",
            }
        ),
    )
    HCO3_2 = forms.FloatField(
        label="",
        widget=forms.NumberInput(
            attrs={
                "class": "input",
                "for": "HCO3_2",
                "type": "text",
                "style": "background: #292e3c; text-align: center;",
            }
        ),
    )
    Ca_2 = forms.FloatField(
        label="",
        widget=forms.NumberInput(
            attrs={
                "class": "input",
                "for": "Ca_2",
                "type": "text",
                "style": "background: #363A47; text-align: center;",
            }
        ),
    )
    Mg_2 = forms.FloatField(
        label="",
        widget=forms.NumberInput(
            attrs={
                "class": "input",
                "for": "Mg_2",
                "type": "text",
                "style": "background: #292e3c;text-align: center;",
            }
        ),
    )
    Na_2 = forms.FloatField(
        label="",
        widget=forms.NumberInput(
            attrs={
                "class": "input",
                "for": "Na_2",
                "type": "text",
                "style": "background: #363A47;text-align: center;",
            }
        ),
    )
    Ba_2 = forms.FloatField(
        label="",
        widget=forms.NumberInput(
            attrs={
                "class": "input",
                "for": "Ba_2",
                "type": "text",
                "style": "background: #292e3c;text-align: center;",
            }
        ),
    )
    Sr_2 = forms.FloatField(
        label="",
        widget=forms.NumberInput(
            attrs={
                "class": "input",
                "for": "Sr_2",
                "type": "text",
                "style": "background: #363A47;text-align: center;",
            }
        ),
    )
    pH_2 = forms.FloatField(
        label="",
        widget=forms.NumberInput(
            attrs={
                "type": "text",
                "id": "ph_2",
                "style": "width: 60px; border-radius: 30px; background: rgba(255, 255, 255, 0.06); border: none;"
                " outline: none;text-align:center; color: #fff;",
            }
        ),
    )
    ro_2 = forms.FloatField(
        label="",
        widget=forms.NumberInput(
            attrs={
                "type": "text",
                "id": "density_2",
                "style": "width: 60px; border-radius: 4px; background: rgba(255, 255, 255, 0.06); border: none;"
                " outline: none;text-align:center; color: #fff;",
            }
        ),
    )
    # Параметры смеси
    Temperature = forms.FloatField(
        label="",
        widget=forms.NumberInput(
            attrs={
                "type": "text",
                "oninput": "limitLength(event)",
                "id": "T_1",
                "style": "border-radius: 4px;  text-align: center;"
                "background: #363A47; border: none; outline: none; color: rgba(255, 255, 255, 0.64); ",
            }
        ),
    )
    Pressure = forms.FloatField(
        label="",
        widget=forms.NumberInput(
            attrs={
                "type": "text",
                "oninput": "limitLength(event)",
                "id": "P_1",
                "style": "border-radius: 4px;  text-align: center;"
                " background: #292e3c; border: none; outline: none; color: rgba(255, 255, 255, 0.64); ",
            }
        ),
    )
    Part_of_Mixture = forms.FloatField(
        label="",
        widget=forms.NumberInput(
            attrs={
                "type": "text",
                "oninput": "limitLength(event)",
                "id": "PoM_1",
                "style": "   border-radius: 4px;  text-align: center;"
                "background: #363A47;  border: none; outline: none; color: rgba(255, 255, 255, 0.64);",
            }
        ),
    )


class Scale_Calculator_form_2(forms.Form):
    # Параметры первого вещества
    Cl_1_another = forms.FloatField(
        label="",
        widget=forms.NumberInput(
            attrs={
                "class": "input",
                "oninput": "limitLength(event)",
                "step": "0.0001",
                "for": "Cl_1",
                "type": "text",
                "style": "background: #292e3c; text-align: center;",
            }
        ),
    )
    SO4_1_another = forms.FloatField(
        label="",
        widget=forms.NumberInput(
            attrs={
                "class": "input",
                "oninput": "limitLength(event)",
                "for": "SO4_1",
                "type": "text",
                "style": "background: #363A47;text-align: center;",
            }
        ),
    )
    HCO3_1_another = forms.FloatField(
        label="",
        widget=forms.NumberInput(
            attrs={
                "class": "input",
                "oninput": "limitLength(event)",
                "for": "Cl_1",
                "type": "text",
                "style": "background: #292e3c;text-align: center;",
            }
        ),
    )
    Ca_1_another = forms.FloatField(
        label="",
        widget=forms.NumberInput(
            attrs={
                "class": "input",
                "oninput": "limitLength(event)",
                "for": "Ca_1",
                "type": "text",
                "style": "background: #363A47;text-align: center;",
            }
        ),
    )
    Mg_1_another = forms.FloatField(
        label="",
        widget=forms.NumberInput(
            attrs={
                "class": "input",
                "oninput": "limitLength(event)",
                "for": "Mg_1",
                "type": "text",
                "style": "background: #292e3c;text-align: center;",
            }
        ),
    )
    Na_1_another = forms.FloatField(
        label="",
        widget=forms.NumberInput(
            attrs={
                "class": "input",
                "oninput": "limitLength(event)",
                "for": "Na_1",
                "type": "text",
                "style": "background: #363A47;text-align: center;",
            }
        ),
    )
    Ba_1_another = forms.FloatField(
        label="",
        widget=forms.NumberInput(
            attrs={
                "class": "input",
                "oninput": "limitLength(event)",
                "for": "Ba_1",
                "type": "text",
                "style": "background: #292e3c;text-align: center;",
            }
        ),
    )
    Sr_1_another = forms.FloatField(
        label="",
        widget=forms.NumberInput(
            attrs={
                "class": "input",
                "oninput": "limitLength(event)",
                "for": "Sr_1",
                "type": "text",
                "style": "background:  #363A47;text-align: center;",
            }
        ),
    )

    # Параметры второго вещества
    Cl_2_another = forms.FloatField(
        label="",
        widget=forms.NumberInput(
            attrs={
                "class": "input",
                "oninput": "limitLength(event)",
                "for": "Cl_2",
                "type": "text",
                "style": "background: #292e3c;text-align: center;",
            }
        ),
    )
    SO4_2_another = forms.FloatField(
        label="",
        widget=forms.NumberInput(
            attrs={
                "class": "input",
                "oninput": "limitLength(event)",
                "for": "SO4_2",
                "type": "text",
                "style": "background: #363A47;text-align: center;",
            }
        ),
    )
    HCO3_2_another = forms.FloatField(
        label="",
        widget=forms.NumberInput(
            attrs={
                "class": "input",
                "oninput": "limitLength(event)",
                "for": "HCO3_2",
                "type": "text",
                "style": "background: #292e3c;text-align: center;",
            }
        ),
    )
    Ca_2_another = forms.FloatField(
        label="",
        widget=forms.NumberInput(
            attrs={
                "class": "input",
                "oninput": "limitLength(event)",
                "for": "Ca_2",
                "type": "text",
                "style": "background: #363A47;text-align: center;",
            }
        ),
    )
    Mg_2_another = forms.FloatField(
        label="",
        widget=forms.NumberInput(
            attrs={
                "class": "input",
                "oninput": "limitLength(event)",
                "for": "Mg_2",
                "type": "text",
                "style": "background: #292e3c;text-align: center;",
            }
        ),
    )
    Na_2_another = forms.FloatField(
        label="",
        widget=forms.NumberInput(
            attrs={
                "class": "input",
                "oninput": "limitLength(event)",
                "for": "Na_2",
                "type": "text",
                "style": "background: #363A47;text-align: center;",
            }
        ),
    )
    Ba_2_another = forms.FloatField(
        label="",
        widget=forms.NumberInput(
            attrs={
                "class": "input",
                "oninput": "limitLength(event)",
                "for": "Ba_2",
                "type": "text",
                "style": "background: #292e3c;text-align: center;",
            }
        ),
    )
    Sr_2_another = forms.FloatField(
        label="",
        widget=forms.NumberInput(
            attrs={
                "class": "input",
                "oninput": "limitLength(event)",
                "for": "Sr_2",
                "type": "text",
                "style": "background: #363A47;text-align: center;",
            }
        ),
    )
