import math



#Расчет индекса насыщения вещества
def SI (Cl, SO4, HCO3, Ca, Mg, Na, Ba, Sr, pH, ro, Temperature, Pressure, substance, medium = None, less = None):
    constant = math.log(10)
    if substance == "Barit_SI":
        a = 10.00066
        b = -0.0075607
        c = 0.000037746
        d = -0.0077088
        e = -4.0622
        f = 2.787
        g = -0.619
        h = -0.00333
        current_substance = Ba
        another_component = SO4
        pH_constant = 0
    elif substance == "Celestin_SI":
        a = 6.16746
        b = 0.0046877
        c = 0.000018594
        d = -0.0060872
        e = -2.14194
        f = 0.944
        g = -0.0865
        h = -0.0033714
        current_substance = Sr
        another_component = SO4
        pH_constant = 0
    elif substance == "Anhydrate_SI":
        a = 3.18266
        b = 0.01681
        c = 0.00000060912
        d = -0.0049313
        e = -2.09624
        f = 1.267
        g = -0.19
        h = -0.005751
        current_substance = Ca
        another_component = SO4
        pH_constant = 0
    elif substance == "Bassanit_SI":
        a = 4.00733
        b = -0.0019123
        c = 0.000036936
        d = -0.010254
        e = -1.7546
        f = 0.562
        g = -0.0217
        h = -0.0011585
        current_substance = Ca
        another_component = SO4
        pH_constant = 0
    elif substance == "Gips_SI":
        a = 3.59973
        b = 0.00056134
        c = 0.000029254
        d = -0.0081018
        e = -0.91388
        f = 0.0524
        g = 0.0852
        h = -0.003762
        current_substance = Ca
        another_component = SO4
        pH_constant = 0
    elif substance == "Magnium_Sulfat_SI":
        a = 2.36134
        b = 0.0036565
        c = 0.000014752
        d = -0.0011314
        e = -3.98832
        f = 2.28
        g = -0.459
        h = -0.00109
        current_substance = Mg
        another_component = SO4
        pH_constant = 0
    elif substance == "Calcit_SI":
        a = -2.242
        b = 0.01637
        c = 0.00000611
        d = -0.00704
        e = -1.429
        f = 0.316
        g = 0.0537
        h = 0.002335
        current_substance = Ca
        another_component = HCO3
        pH_constant = pH
    if medium is not None:
        if less == "yes":
            current_substance = medium
        else:
            another_component = medium
    Ionic_Power = ((Cl + HCO3 + Na) + 4 * (SO4 + Ca + Mg + Ba + Sr)) / 2
    if current_substance * another_component != 0:
        SI = (math.log(current_substance * another_component)/constant) + pH_constant + a + (b * Temperature) + c * (Temperature**2) + d * Pressure + e * (Ionic_Power**0.5) + f * Ionic_Power + g * (Ionic_Power**1.5) + h * Temperature * (Ionic_Power**0.5)
    else:
        SI = 0
    return SI
#Расчет концентрации ионов и плотности (правильный)
def mixing_calculator(concentration_1, concentration_2, part_of_mixture_1, part_of_mixture_2 = None):
    if part_of_mixture_2 == None:
        part_of_mixture_2 = 100 - part_of_mixture_1
    else:
        part_of_mixture_2 = part_of_mixture_2
    result = (concentration_1*part_of_mixture_1 + concentration_2 * part_of_mixture_2)/100
    return result
# Расчет pH смеси (правильный)
def mixing_calculator_pH (pH_1, pH_2, part_of_mixture_1, part_of_mixture_2 = None):
    if part_of_mixture_2 == None:
        part_of_mixture_2 = 100 - part_of_mixture_1
    else:
        part_of_mixture_2 = part_of_mixture_2
    result = -math.log(((10 ** -pH_1) * part_of_mixture_1 + (10 ** -pH_2) * part_of_mixture_2) / 100) / math.log(10)
    return result
# Расчет максимального количества осадка вещества методом деления
def Sediment_Max (Cl, SO4, HCO3, Ca, Mg, Na, Ba, Sr, pH, ro, Temperature, Pressure, substance):
    if substance == "Barit_SI":
        current_substance = Ba
    elif substance == "Celestin_SI":
        current_substance = Sr
    elif substance == "Anhydrate_SI":
        current_substance = Ca
    elif substance == "Bassanit_SI":
        current_substance = Ca
    elif substance == "Gips_SI":
        current_substance = Ca
    elif substance == "Magnium_Sulfat_SI":
        current_substance = Mg
    elif substance == "Calcit_SI":
        current_substance = Ca
    if current_substance < SO4:
        max = current_substance
        medium = max/2
        while abs(max-medium)> 0.0000001:
            if SI (Cl, SO4, HCO3, Ca, Mg, Na, Ba, Sr, pH, ro, Temperature, Pressure, substance, medium=medium, less = "yes") > 0:
                max = medium
                medium = max/2
            else:
                medium = max - (max - medium)/2
        return current_substance - max
    else:
        max = SO4
        medium = max/2
        while abs(max-medium)> 0.0000001:
            if SI (Cl, SO4, HCO3, Ca, Mg, Na, Ba, Sr, pH, ro, Temperature, Pressure, substance, medium=medium, less = "no") > 0:
                max = medium
                medium = max/2
            else:
                medium = max - (max - medium)/2
        return SO4-max
# Расчет максимального количества осадка вещества (кальцит) методом деления отдельный потому что другой впадлу делать
def Sediment_calcit_max (Cl, SO4, HCO3, Ca, Mg, Na, Ba, Sr, pH, ro, Temperature, Pressure, substance):
    if substance == "Calcit_SI":
        current_substance = Ca
    if Ca < HCO3:
        max = Ca
        medium = max/2
        while abs(max - medium) > 0.0000001:
            if SI(Cl, SO4, HCO3, medium, Mg, Na, Ba, Sr, pH, ro, Temperature, Pressure, substance) > 0:
                max = medium
                medium = max/2
            else:
                medium = (max+medium)/2
        return Ca - max
    else:
        max = HCO3
        medium = max/2
        while abs(max-medium)> 0.0000001:
            if SI(Cl, SO4, medium, Ca, Mg, Na, Ba, Sr, pH, ro, Temperature, Pressure, substance) > 0:
                max = medium
                medium = max/2
            else:
                medium = (max + medium)/2
        return HCO3 - max

def calculate_full_result(Cl_1,Cl_2,SO4_1,SO4_2,HCO3_1, HCO3_2, Ca_1,Ca_2,Mg_1,Mg_2,Na_1, Na_2, Ba_1, Ba_2,Sr_1,Sr_2,pH_1,pH_2,ro_1,ro_2, Temperature, Pressure, Part_of_Mixture):


    # Концентрация ионов (мг/л) в смеси двух жидкостей, pH, проверено
    Cl_of_mixture = mixing_calculator(Cl_1, Cl_2, Part_of_Mixture)
    SO4_of_mixture = mixing_calculator(SO4_1, SO4_2, Part_of_Mixture)
    HCO3_of_mixture = mixing_calculator(HCO3_1, HCO3_2, Part_of_Mixture)
    Ca_of_mixture = mixing_calculator(Ca_1, Ca_2, Part_of_Mixture)
    Mg_of_mixture = mixing_calculator(Mg_1, Mg_2, Part_of_Mixture)
    Na_of_mixture = mixing_calculator(Na_1, Na_2, Part_of_Mixture)
    Ba_of_mixture = mixing_calculator(Ba_1, Ba_2, Part_of_Mixture)
    Sr_of_mixture = mixing_calculator(Sr_1, Sr_2, Part_of_Mixture)
    ro_of_mixture = mixing_calculator(ro_1, ro_2, Part_of_Mixture)
    pH_of_mixture = mixing_calculator_pH(pH_1, pH_2, Part_of_Mixture)

    # Количество итераций
    dt = 1000
    # Расчет максимальной массы выпадения соли за шаг итерации
    d_Barit = Sediment_Max(Cl_of_mixture, SO4_of_mixture, HCO3_of_mixture, Ca_of_mixture, Mg_of_mixture, Na_of_mixture, Ba_of_mixture, Sr_of_mixture, pH_of_mixture, ro_of_mixture, Temperature, Pressure, "Barit_SI")/dt
    d_Celestin = Sediment_Max(Cl_of_mixture, SO4_of_mixture, HCO3_of_mixture, Ca_of_mixture, Mg_of_mixture, Na_of_mixture, Ba_of_mixture, Sr_of_mixture, pH_of_mixture, ro_of_mixture, Temperature, Pressure, "Celestin_SI")/dt
    d_Anhydrate = Sediment_Max(Cl_of_mixture, SO4_of_mixture, HCO3_of_mixture, Ca_of_mixture, Mg_of_mixture, Na_of_mixture, Ba_of_mixture, Sr_of_mixture, pH_of_mixture, ro_of_mixture, Temperature, Pressure, "Anhydrate_SI")/dt
    d_Bassanit = Sediment_Max(Cl_of_mixture, SO4_of_mixture, HCO3_of_mixture, Ca_of_mixture, Mg_of_mixture, Na_of_mixture, Ba_of_mixture, Sr_of_mixture, pH_of_mixture, ro_of_mixture, Temperature, Pressure, "Bassanit_SI")/dt
    d_Gips = Sediment_Max(Cl_of_mixture, SO4_of_mixture, HCO3_of_mixture, Ca_of_mixture, Mg_of_mixture, Na_of_mixture, Ba_of_mixture, Sr_of_mixture, pH_of_mixture, ro_of_mixture, Temperature, Pressure, "Gips_SI")/dt
    d_Magnium_Sulfat = Sediment_Max(Cl_of_mixture, SO4_of_mixture, HCO3_of_mixture, Ca_of_mixture, Mg_of_mixture, Na_of_mixture, Ba_of_mixture, Sr_of_mixture, pH_of_mixture, ro_of_mixture, Temperature, Pressure, "Magnium_Sulfat_SI")/dt
    d_Calcit = Sediment_calcit_max(Cl_of_mixture, SO4_of_mixture, HCO3_of_mixture, Ca_of_mixture, Mg_of_mixture, Na_of_mixture, Ba_of_mixture, Sr_of_mixture, pH_of_mixture, ro_of_mixture, Temperature, Pressure, "Calcit_SI")/dt

    Barit,Celestin,Anhydrate,Bassanit,Gips,Magnium_Sulfat,Calcit = 0, 0, 0, 0, 0, 0, 0

    for i in range(dt):
        if SI (Cl_of_mixture, SO4_of_mixture, HCO3_of_mixture, Ca_of_mixture, Mg_of_mixture, Na_of_mixture, Ba_of_mixture, Sr_of_mixture, pH_of_mixture, ro_of_mixture, Temperature, Pressure, "Barit_SI") > 0:
            Barit = Barit + d_Barit
            Ba_of_mixture = Ba_of_mixture - d_Barit
            SO4_of_mixture = SO4_of_mixture - d_Barit
        if SI (Cl_of_mixture, SO4_of_mixture, HCO3_of_mixture, Ca_of_mixture, Mg_of_mixture, Na_of_mixture, Ba_of_mixture, Sr_of_mixture, pH_of_mixture, ro_of_mixture, Temperature, Pressure, "Celestin_SI") > 0:
            Celestin = Celestin + d_Celestin
            Sr_of_mixture = Sr_of_mixture - d_Celestin
            SO4_of_mixture = SO4_of_mixture - d_Celestin
        if SI (Cl_of_mixture, SO4_of_mixture, HCO3_of_mixture, Ca_of_mixture, Mg_of_mixture, Na_of_mixture, Ba_of_mixture, Sr_of_mixture, pH_of_mixture, ro_of_mixture, Temperature, Pressure, "Anhydrate_SI")>0:
            Anhydrate = Anhydrate + d_Anhydrate
            Ca_of_mixture = Ca_of_mixture - d_Anhydrate
            SO4_of_mixture = SO4_of_mixture - d_Anhydrate
        if SI (Cl_of_mixture, SO4_of_mixture, HCO3_of_mixture, Ca_of_mixture, Mg_of_mixture, Na_of_mixture, Ba_of_mixture, Sr_of_mixture, pH_of_mixture, ro_of_mixture, Temperature, Pressure, "Bassanit_SI") >0:
            Bassanit = Bassanit + d_Bassanit
            Ca_of_mixture = Ca_of_mixture - d_Bassanit
            SO4_of_mixture = SO4_of_mixture - d_Bassanit
        if SI (Cl_of_mixture, SO4_of_mixture, HCO3_of_mixture, Ca_of_mixture, Mg_of_mixture, Na_of_mixture, Ba_of_mixture, Sr_of_mixture, pH_of_mixture, ro_of_mixture, Temperature, Pressure, "Gips_SI") > 0:
            Gips = Gips + d_Gips
            Ca_of_mixture = Ca_of_mixture - d_Gips
            SO4_of_mixture = SO4_of_mixture - d_Gips
        if SI (Cl_of_mixture, SO4_of_mixture, HCO3_of_mixture, Ca_of_mixture, Mg_of_mixture, Na_of_mixture, Ba_of_mixture, Sr_of_mixture, pH_of_mixture, ro_of_mixture, Temperature, Pressure, "Magnium_Sulfat_SI") > 0:
            Magnium_Sulfat = Magnium_Sulfat + d_Magnium_Sulfat
            Mg_of_mixture = Mg_of_mixture - d_Magnium_Sulfat
            SO4_of_mixture = SO4_of_mixture - d_Magnium_Sulfat
        if SI (Cl_of_mixture, SO4_of_mixture, HCO3_of_mixture, Ca_of_mixture, Mg_of_mixture, Na_of_mixture, Ba_of_mixture, Sr_of_mixture, pH_of_mixture, ro_of_mixture, Temperature, Pressure, "Calcit_SI") > 0:
            Calcit = Calcit + d_Calcit
            Ca_of_mixture = Ca_of_mixture - d_Calcit
            HCO3_of_mixture = HCO3_of_mixture - d_Calcit

    mass_of_Barit = Barit*233.392*ro_of_mixture
    mass_of_Celestine = Celestin*183.682*ro_of_mixture
    mass_of_Anhydrate = Anhydrate*136.14*ro_of_mixture
    mass_of_Bassanite = Bassanit*145.147*ro_of_mixture
    mass_of_Gips = Gips*172.17056*ro_of_mixture
    mass_of_Magnium_Sulfat = Magnium_Sulfat*120.367*ro_of_mixture
    mass_of_Calcit = Calcit*100.094*ro_of_mixture

    return {"Barit": round(mass_of_Barit,5),
            "Part_of_mixture": round(Part_of_Mixture, 5),
            "Celestine": round(mass_of_Celestine,5),
            "Anhydrate": round(mass_of_Anhydrate,5),
            "Bassanit": round(mass_of_Bassanite,5),
            "Gips": round(mass_of_Gips,5),
            "Magnium_Sulfat": round(mass_of_Magnium_Sulfat,5),
            "Calcit": round(mass_of_Calcit,5)}

