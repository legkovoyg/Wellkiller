from django import forms


class ModelGlushForm(forms.Form):
    Oil_field_name = forms.CharField(
        label="Месторождение",
        widget=forms.TextInput(attrs={"id": "field", "style": "background: #363A47;"}),
    )
    Bush_name = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={"id": "bush", "style": "background: #292e3c;"}),
    )
    Well_name = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={"id": "well_name", "style": "background: #363A47;"}
        ),
    )
    Design_name = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={"id": "design_name", "style": "background: #292e3c;"}
        ),
    )
    types_of_exp = [("УЭЦН", "УЭЦН"), ("УШГН", "УШГН")]
    EXP_type = forms.ChoiceField(
        widget=forms.Select(
            attrs={
                "margin": "0",
                "padding": "0",
                "box-sizing": "border-box",
                "style": "background: #363A47;",
                "color": "black",
            }
        ),
        choices=types_of_exp,
    )
    Oil_density = forms.FloatField(
        label="",
        widget=forms.NumberInput(
            attrs={
                "class": "input",
                "oninput": "limitLength(event)",
                "type": "text",
                "style": "background: #363A47;",
            }
        ),
    )
    Plast_pressure = forms.FloatField(
        label="",
        widget=forms.NumberInput(
            attrs={
                "class": "input",
                "oninput": "limitLength(event)",
                "type": "text",
                "style": "background: #292e3c;",
            }
        ),
    )
    Plast_thickness = forms.FloatField(
        label="",
        widget=forms.NumberInput(
            attrs={
                "class": "input",
                "oninput": "limitLength(event)",
                "type": "text",
                "style": "background: #292e3c;",
            }
        ),
    )

    NKT_length = forms.FloatField(
        label="",
        widget=forms.NumberInput(
            attrs={
                "class": "input",
                "oninput": "limitLength(event)",
                "type": "text",
                "style": "background: #292e3c;",
            }
        ),
    )
    EXP_length = forms.FloatField(
        label="",
        widget=forms.NumberInput(
            attrs={
                "class": "input",
                "oninput": "limitLength(event)",
                "type": "text",
                "style": "background: #363A47;",
            }
        ),
    )
    NKT_inner_diameter = forms.FloatField(
        label="",
        widget=forms.NumberInput(
            attrs={
                "class": "input",
                "oninput": "limitLength(event)",
                "type": "text",
                "style": "background: #363A47;",
            }
        ),
    )
    NKT_external_diameter = forms.FloatField(
        label="",
        widget=forms.NumberInput(
            attrs={
                "class": "input",
                "oninput": "limitLength(event)",
                "type": "text",
                "style": "background: #292e3c;",
            }
        ),
    )
    EXP_inner_diameter = forms.FloatField(
        label="",
        widget=forms.NumberInput(
            attrs={
                "class": "input",
                "oninput": "limitLength(event)",
                "type": "text",
                "style": "background: #292e3c;",
            }
        ),
    )
    EXP_external_diameter = forms.FloatField(
        label="",
        widget=forms.NumberInput(
            attrs={
                "class": "input",
                "oninput": "limitLength(event)",
                "type": "text",
                "style": "background: #363A47;",
            }
        ),
    )
    Volume_of_car = forms.FloatField(
        label="",
        widget=forms.NumberInput(
            attrs={
                "class": "input",
                "oninput": "limitLength(event)",
                "type": "text",
                "style": "background: #363A47;",
            }
        ),
    )
    Debit = forms.FloatField(
        label="",
        widget=forms.NumberInput(
            attrs={
                "class": "input",
                "oninput": "limitLength(event)",
                "type": "text",
                "style": "background: #292e3c;",
            }
        ),
    )
    # Jgs_density = forms.FloatField(label="", widget=forms.NumberInput(
    #     attrs={'class': "input", "oninput": "limitLength(event)", "type": "text", "style": "background: #363A47;"}))
    types_of_jgs = [
        ("CaCl", "CaCl"),
        # ("KCl", "KCl"),
        ("CaЖГ", "CaЖГ"),
        ("без соли", "без соли"),
    ]
    Type_of_jgs = forms.ChoiceField(
        widget=forms.Select(
            attrs={
                "margin": "0",
                "padding": "0",
                "box-sizing": "border-box",
                "style": "background: #363A47;",
                "color": "black",
            }
        ),
        choices=types_of_jgs,
    )
    Phase_oil_permeability = forms.FloatField(
        label="",
        widget=forms.NumberInput(
            attrs={
                "class": "input",
                "oninput": "limitLength(event)",
                "type": "text",
                "style": "background: #292e3c;",
            }
        ),
    )
    Phase_jgs_permeability = forms.FloatField(
        label="",
        widget=forms.NumberInput(
            attrs={
                "class": "input",
                "oninput": "limitLength(event)",
                "type": "text",
                "style": "background: #363A47;",
            }
        ),
    )
    Oil_viscosity = forms.FloatField(
        label="",
        widget=forms.NumberInput(
            attrs={
                "class": "input",
                "oninput": "limitLength(event)",
                "type": "text",
                "style": "background: #292e3c;",
            }
        ),
    )
    Jgs_viscosity = forms.FloatField(
        label="",
        widget=forms.NumberInput(
            attrs={
                "class": "input",
                "oninput": "limitLength(event)",
                "type": "text",
                "style": "background: #363A47;",
            }
        ),
    )
    Radius_countour = forms.FloatField(
        label="",
        widget=forms.NumberInput(
            attrs={
                "class": "input",
                "oninput": "limitLength(event)",
                "type": "text",
                "style": "background: #363A47;",
            }
        ),
    )
    Porosity = forms.FloatField(
        label="",
        widget=forms.NumberInput(
            attrs={
                "class": "input",
                "oninput": "limitLength(event)",
                "type": "text",
                "style": "background: #292e3c;",
            }
        ),
    )
    YV_dole = forms.FloatField(
        label="",
        widget=forms.NumberInput(
            attrs={
                "class": "input",
                "oninput": "limitLength(event)",
                "type": "text",
                "style": "background: #292e3c;",
            }
        ),
    )
    YV_density = forms.FloatField(
        label="",
        widget=forms.NumberInput(
            attrs={
                "class": "input",
                "oninput": "limitLength(event)",
                "type": "text",
                "style": "background: #363A47;",
            }
        ),
    )
    Emul_dole = forms.FloatField(
        label="",
        widget=forms.NumberInput(
            attrs={
                "class": "input",
                "oninput": "limitLength(event)",
                "type": "text",
                "style": "background: #292e3c;",
            }
        ),
    )
    Emul_density = forms.FloatField(
        label="",
        widget=forms.NumberInput(
            attrs={
                "class": "input",
                "oninput": "limitLength(event)",
                "type": "text",
                "style": "background:  #363A47;",
            }
        ),
    )
    Zapas = forms.FloatField(
        label="",
        widget=forms.NumberInput(
            attrs={
                "class": "input",
                "oninput": "limitLength(event)",
                "type": "text",
                "style": "background: #292e3c;",
            }
        ),
    )
    False_zaboi = forms.FloatField(
        label="",
        widget=forms.NumberInput(
            attrs={
                "class": "input",
                "oninput": "limitLength(event)",
                "type": "text",
                "style": "background: #292e3c;",
            }
        ),
    )
    True_zaboi = forms.FloatField(
        label="",
        widget=forms.NumberInput(
            attrs={
                "class": "input",
                "oninput": "limitLength(event)",
                "type": "text",
                "style": "background:  #363A47;",
            }
        ),
    )
    From_yst_to_plast = forms.FloatField(
        label="",
        widget=forms.NumberInput(
            attrs={
                "class": "input",
                "oninput": "limitLength(event)",
                "type": "text",
                "style": "background:  #363A47;",
            }
        ),
    )
    types_of_jamming = [("direct", "Прямая"), ("back", "Обратная")]
    Type_of_jamming = forms.ChoiceField(
        widget=forms.Select(
            attrs={
                "margin": "0",
                "padding": "0",
                "box-sizing": "border-box",
                "style": "background: #363A47;",
                "color": "black",
            }
        ),
        choices=types_of_jamming,
    )
    Excel_load = forms.FileField(required=False)
