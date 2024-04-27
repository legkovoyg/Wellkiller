from .Methods import SI, mixing_calculator, mixing_calculator_pH, Sediment_Max, Sediment_calcit_max

def calculate(Cl_1,SO4_1,HCO3_1,Ca_1,Mg_1,Na_1,Ba_1,Sr_1,pH_1,ro_1,Cl_2,SO4_2,HCO3_2,Ca_2,Mg_2,Na_2,Ba_2,Sr_2,pH_2,ro_2, Temperature, Pressure, Part_of_Mixture):
    # Входные данные для жидкости 1
    Cl_1 = 5.845595
    SO4_1 = 0.005032
    HCO3_1 = 0.001769
    Ca_1 = 1.700765
    Mg_1 = 0.021272
    Na_1 = 2.415081
    Ba_1 = 0
    Sr_1 = 0
    pH_1 = 6.07
    ro_1 = 1.176
    # Входные данные для жидкости 2
    Cl_2 = 0.005973
    SO4_2 = 0.000159
    HCO3_2 = 0.006324
    Ca_2 = 0.002635
    Mg_2 = 0.000504
    Na_2 = 0.006328
    Ba_2 = 0
    Sr_2 = 0
    pH_2 = 6.7
    ro_2 = 0.996
    # Условия смешивания
    Temperature = 40 # Температура в градусах
    Pressure = 100 # Давление в МПа
    Part_of_Mixture = 100

    # Концентрация ионов (мг/л) в смеси двух жидкостей, pH
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
    d_Barit = Sediment_Max(Cl_of_mixture, SO4_of_mixture, HCO3_of_mixture, Ca_of_mixture,
                           Mg_of_mixture, Na_of_mixture, Ba_of_mixture, Sr_of_mixture, pH_of_mixture,
                           ro_of_mixture, Temperature, Pressure, "Barit_SI")/dt
    d_Celestin = Sediment_Max(Cl_of_mixture, SO4_of_mixture, HCO3_of_mixture, Ca_of_mixture,
                              Mg_of_mixture, Na_of_mixture, Ba_of_mixture, Sr_of_mixture, pH_of_mixture,
                              ro_of_mixture, Temperature, Pressure, "Celestin_SI")/dt
    d_Anhydrate = Sediment_Max(Cl_of_mixture, SO4_of_mixture, HCO3_of_mixture, Ca_of_mixture,
                               Mg_of_mixture, Na_of_mixture, Ba_of_mixture, Sr_of_mixture, pH_of_mixture,
                               ro_of_mixture, Temperature, Pressure, "Anhydrate_SI")/dt
    d_Bassanit = Sediment_Max(Cl_of_mixture, SO4_of_mixture, HCO3_of_mixture, Ca_of_mixture,
                              Mg_of_mixture, Na_of_mixture, Ba_of_mixture, Sr_of_mixture, pH_of_mixture,
                              ro_of_mixture, Temperature, Pressure, "Bassanit_SI")/dt
    d_Gips = Sediment_Max(Cl_of_mixture, SO4_of_mixture, HCO3_of_mixture, Ca_of_mixture,
                          Mg_of_mixture, Na_of_mixture, Ba_of_mixture, Sr_of_mixture, pH_of_mixture,
                          ro_of_mixture, Temperature, Pressure, "Gips_SI")/dt
    d_Magnium_Sulfat = Sediment_Max(Cl_of_mixture, SO4_of_mixture, HCO3_of_mixture, Ca_of_mixture,
                                    Mg_of_mixture, Na_of_mixture, Ba_of_mixture, Sr_of_mixture, pH_of_mixture,
                                    ro_of_mixture, Temperature, Pressure, "Magnium_Sulfat_SI")/dt
    d_Calcit = Sediment_calcit_max(Cl_of_mixture, SO4_of_mixture, HCO3_of_mixture, Ca_of_mixture,
                                   Mg_of_mixture, Na_of_mixture, Ba_of_mixture, Sr_of_mixture, pH_of_mixture,
                                   ro_of_mixture, Temperature, Pressure, "Calcit_SI")/dt

    Barit = 0
    Celestin = 0
    Anhydrate = 0
    Bassanit = 0
    Gips = 0
    Magnium_Sulfat = 0
    Calcit = 0


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
    Barit_result = Barit * 233.392 * ro_of_mixture
    Celestin_result = Celestin * 183.682 * ro_of_mixture
    Anhydrate_result = Anhydrate * 136.14 * ro_of_mixture
    Bassanit_result = Bassanit * 145.147 * ro_of_mixture
    Gips_result = Gips * 172.17056 * ro_of_mixture
    Magnium_Sulfat_result = Magnium_Sulfat * 120.367 * ro_of_mixture
    Calcit_result = Calcit * 100.094 * ro_of_mixture
    return Barit_result, Celestin_result, Anhydrate_result, Bassanit_result, Gips_result, Magnium_Sulfat_result, Calcit_result

calculate()