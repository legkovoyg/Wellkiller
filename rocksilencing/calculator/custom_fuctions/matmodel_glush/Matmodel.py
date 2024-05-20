from calculator.custom_fuctions.matmodel_glush.matmodel_functions import mf_pressures as mfP
from calculator.custom_fuctions.matmodel_glush.matmodel_functions import mf_heights as mfH
from calculator.custom_fuctions.matmodel_glush.matmodel_functions import mf_commons as mfCom
from calculator.custom_fuctions.matmodel_glush.matmodel_functions import mf_constructions as mfCon
import calculator.custom_fuctions.matmodel_glush.matmodel_classes as mc
import math
from scipy.interpolate import interp1d

# Дано
Plast_pressure = 10132500  # Па
h = 10  # м
Length_of_Well = 1500  # м
# L_of_Wells = 1400  # м
ro_oil = 800  # м
# м

d_NKT = 0.062  # м
D_NKT = 0.073  # м
d_exp = 0.15  # м
D_exp = 0.163  # м
Q = 0.01  # м*3/с
k_jg = 0.0000000000015
mu_jg = 0.001
k_oil = 0.0000000000005
mu_oil = 0.005

Rk = 250
m = 0.2
dt = 50


def matmodel_glush(Plast_pressure, h, Length_of_Well, L_of_Wells, ro_oil, d_NKT, D_NKT, d_exp, D_exp, Q, k_jg,
                   mu_jg, k_oil, mu_oil, Rk, m, dt, YV_density, YV_dole, emul_density, emul_dole, zapas, bd_CaCl,
                   bd_CaJG, chosen_salt, volume_car):
    rc = d_exp / 2
    g = 9.81  # м/c**2mf.
    # Расчет параметров конструкции скважин
    ## Площади
    Area_NKT = mfCon.calculate_area(d_NKT)
    Area_EXP = mfCon.calculate_area(d_exp)
    Area_KP = mfCon.calculate_area((d_exp, D_NKT), case="KP")
    ## Длины участков
    Length_NKT = L_of_Wells
    Length_KP = L_of_Wells
    Length_EXP = Length_of_Well - L_of_Wells
    ## Объемы участков
    Volume_NKT = mfCon.calculate_volume_of_tube(area=Area_NKT, length=Length_NKT)
    Volume_KP = mfCon.calculate_volume_of_tube(area=Area_KP, length=Length_KP)
    Volume_EXP = mfCon.calculate_volume_of_tube(area=Area_EXP, length=Length_EXP)

    # Классы конструкций скважин - тут содержится вся информация о конструкции участков скважины
    NKT = mc.Construction(type='NKT',
                          length=Length_NKT,
                          area=Area_NKT,
                          volume=Volume_NKT,
                          inner_diameter=d_NKT,
                          external_diameter=D_NKT)
    EXP = mc.Construction(type='EXP',
                          length=Length_EXP,
                          area=Area_EXP,
                          volume=Volume_EXP,
                          inner_diameter=d_exp,
                          external_diameter=D_exp, )
    KP = mc.Construction(type='KP',
                         length=Length_KP,
                         area=Area_KP,
                         volume=Volume_KP)

    FULL_EXP = mc.Construction(type='NKT',
                               length=L_of_Wells,
                               area=Area_EXP,
                               volume=L_of_Wells * Area_EXP,
                               inner_diameter=d_exp,
                               external_diameter=D_exp)
    # Дизайн глушения
    Design = mc.DesignGlush(volume_car=volume_car, YV_density=YV_density, YV_dole=YV_dole, emul_density=emul_density,
                            emul_dole=emul_dole, zapas=zapas, chosen_salt=chosen_salt)
    DESIGN_volume_glush = Design.calculate_glush_volume(NKT, EXP, KP, one_cycle=True)
    DESIGN_volume_zapas = Design.rash_glush_volume_zapas
    DESIGN_volume_bez_zapasa = Design.rash_glush_volume
    DESIGN_volume_oil = Design.calculate_volume_oil()
    DESIGN_volume_emul = Design.calculate_volume_emul()
    DESIGN_volume_rast = Design.calculate_volume_of_rast()
    DESIGN_jgs_density = Design.calculate_theory_jgs_density(plast_pressure=Plast_pressure / 101300,
                                                             from_yst_to_plast=L_of_Wells)
    DESIGN_pressure_zapas = Design.calculate_pressure_zapas(plast_pressure=Plast_pressure / 101300,
                                                            from_yst_to_plast=L_of_Wells)
    DESIGN_safe_jgs_density = Design.calculate_safe_jgs_density(plast_pressure=Plast_pressure / 101300,
                                                                from_yst_to_plast=L_of_Wells)

    DESIGN_true_jgs_density = Design.calculate_true_jgs_density()
    DESIGN_recommendations_result = Design.recommended_choose_salt(bd_CaCl, bd_CaJG, Q)
    DESIGN_recommended_salt_name = DESIGN_recommendations_result[0]
    DESIGN_recommended_salt_debit = DESIGN_recommendations_result[1]
    DESIGN_recommended_water_debit = DESIGN_recommendations_result[2]
    DESIGN_chosen_results = Design.choose_salt(bd_CaCl, bd_CaJG, Q)
    DESIGN_chosen_salt_name = DESIGN_chosen_results[0]
    DESIGN_chosen_salt_debit = DESIGN_chosen_results[1]
    DESIGN_chosen_water_debit = DESIGN_chosen_results[2]
    DESIGN_mass = Design.calculate_mass()
    DESIGN_water_mass = DESIGN_mass[0]
    DESIGN_water_volume = Design.calculate_water_volume()
    DESIGN_salt_mass = DESIGN_mass[1]

    print(Design.rash_glush_volume_with_zapas)
    print(Design.volume_car)
    print(Design.volume_of_rast)
    RECIPE_YV_st1 = Design. RECIPE_YV(stage=1)
    RECIPE_EMUL_st1 = Design.RECIPE_EMUL(stage=1)
    RECIPE_SOLERAST_st1 = Design.RECIPE_SOLE_RAST(stage=1)
    RECIPE_BP_st1 = Design.RECIPE_BP(stage=1)

    RECIPE_YV_st2 = Design. RECIPE_YV(stage=2)
    RECIPE_EMUL_st2 = Design.RECIPE_EMUL(stage=2)
    RECIPE_SOLERAST_st2 = Design.RECIPE_SOLE_RAST(stage=2)
    RECIPE_BP_st2 = Design.RECIPE_BP(stage=2)

    RECIPE_YV_st3 = Design. RECIPE_YV(stage=3)
    RECIPE_EMUL_st3 = Design.RECIPE_EMUL(stage=3)
    RECIPE_SOLERAST_st3 = Design.RECIPE_SOLE_RAST(stage=3)
    RECIPE_BP_st3 = Design.RECIPE_BP(stage=3)

    RECIPE_YV_st4 = Design. RECIPE_YV(stage=4)
    RECIPE_EMUL_st4 = Design.RECIPE_EMUL(stage=4)
    RECIPE_SOLERAST_st4 = Design.RECIPE_SOLE_RAST(stage=4)
    RECIPE_BP_st4 = Design.RECIPE_BP(stage=4)

    # Расчет статического уровня скважин
    U_stat = mfCom.calculate_com_U_stat(pressure=Plast_pressure,
                                        length=Length_of_Well,
                                        density=ro_oil,
                                        g=9.81)
    ro_jgs = Design.true_jgs_density * 1000
    print(f"ЭТО DESIGN_volume_glush - {DESIGN_volume_glush}")
    print(f"ЭТО DESIGN_volume_oil - {DESIGN_volume_oil}")
    print(f"ЭТО DESIGN_volume_emul - {DESIGN_volume_emul}")
    print(f"ЭТО DESIGN_volume_rast - {DESIGN_volume_rast}")
    print(f"ЭТО DESIGN_jgs_density - {DESIGN_jgs_density}")
    print(f"ЭТО DESIGN_pressure_zapas - {DESIGN_pressure_zapas}")
    print(f"ЭТО DESIGN_safe_jgs_density - {DESIGN_safe_jgs_density}")
    print(f"ЭТО DESIGN_recommended_salt_name - {DESIGN_recommended_salt_name}")
    print(f"ЭТО DESIGN_recommended_salt_debit - {DESIGN_recommended_salt_debit}")
    print(f"ЭТО DESIGN_recommended_water_debit - {DESIGN_recommended_water_debit}")
    print(f"ЭТО DESIGN_chosen_salt_name - {DESIGN_chosen_salt_name}")
    print(f"ЭТО DESIGN_chosen_salt_debit - {DESIGN_chosen_salt_debit}")
    print(f"ЭТО DESIGN_chosen_water_debit - {DESIGN_chosen_water_debit}")
    print(f"ЭТО DESIGN_water_mass - {DESIGN_water_mass}")
    print(f"ЭТО DESIGN_salt_mass - {DESIGN_salt_mass}")
    # dt = input()

    # Этап инициализации - глушение началось, прошло 0 сек
    t_0 = 0
    init_usl_Volume_jg = 0
    init_usl_Volume_jg_reduced = 0
    init_usl_Height_jg = 0
    init_usl_dh_jg = 0
    init_usl_dh_jg_reduced = 0
    init_usl_Height_jg_reduced = 0
    init_usl_Speed_reduced = 0
    init_usl_h_yr = NKT.length - U_stat
    ## Уровни нефти в участках скважины (этап 0)
    init_oil_level_NKT = NKT.length - U_stat
    init_oil_level_KP = NKT.length - U_stat
    init_oil_level_EXP = Length_of_Well - NKT.length
    ## Уровни ЖГС в участках скважины (этап 0)
    init_jgs_level_NKT = 0
    init_jgs_level_KP = 0
    init_jgs_level_EXP = 0
    ## Объемы нефти в участках скважины (этап 0)
    init_oil_volume_NKT = init_oil_level_NKT * NKT.area
    init_oil_volume_KP = init_oil_level_KP * KP.area
    init_oil_volume_EXP = init_oil_level_EXP * EXP.area
    ## Скорости движения жидкости в участках скважины (этап 0)
    init_v_NKT = 0
    init_v_KP = 0
    init_v_EXP = 0
    ## Дебиты и объемы поглощения (этап 0)
    init_Q_pogl = 0
    init_V_pogl = 0
    init_R_oil = 0.1
    init_dV_pogl = 0
    init_Pressure_friction = mfP.calculate_Pressure_friction(init_oil_level_NKT, init_jgs_level_NKT, init_oil_level_KP,
                                                             init_jgs_level_KP, NKT.length, NKT.inner_diameter,
                                                             NKT.external_diameter, EXP.inner_diameter, init_v_NKT,
                                                             init_v_KP, mu_oil, mu_jg)
    init_Pressure_yst = mfP.calculate_Pressure_wellhead(101325, init_Pressure_friction)
    init_Pressure_NKT = mfP.calculate_Pressure_at_Wellspace(Wellspace_oil_height=init_oil_level_NKT, density_oil=ro_oil,
                                                            Wellspace_jgs_height=init_jgs_level_NKT, density_jgs=ro_jgs)
    init_Pressure_KP = mfP.calculate_Pressure_at_Wellspace(Wellspace_oil_height=init_oil_level_KP, density_oil=ro_oil,
                                                           Wellspace_jgs_height=init_jgs_level_KP, density_jgs=ro_jgs)
    init_Pressure_EXP = mfP.calculate_Pressure_at_Wellspace(Wellspace_oil_height=init_oil_level_EXP, density_oil=ro_oil,
                                                            Wellspace_jgs_height=init_jgs_level_EXP, density_jgs=ro_jgs)
    init_Pressure_downhole = mfP.calculate_Pressure_downhole(
        Pressure_wellhead=init_Pressure_yst, Pressure_NKT=init_Pressure_NKT, Pressure_EXP=init_Pressure_EXP
    )
    init_Pressure_overall = init_Pressure_yst + init_Pressure_NKT + init_Pressure_EXP

    # Этап после инициализации, глушение началось
    t_1 = t_0 + dt
    stage_1_Vjg, stage_1_Vjg_reduced = mfCom.calculate_com_volume_of_jgs(debit=Q,
                                                                         time=t_1,
                                                                         case="reduced",
                                                                         density_of_oil=ro_oil,
                                                                         density_of_jgs=ro_jgs)
    stage_1_Height_jg, stage_1_Height_jg_reduced = mfCom.calculate_com_liquid_level_of_jgs(stage_1_Vjg, area=NKT.area,
                                                                                           case='reduced',
                                                                                           density_of_oil=ro_oil,
                                                                                           density_of_jgs=ro_jgs)
    stage_1_dh_jg, stage_1_dh_jg_reduced = mfCom.calculate_com_dh(height_current=stage_1_Height_jg,
                                                                  height_post=init_usl_Height_jg, case="reduced",
                                                                  density_of_oil=ro_oil, density_of_jgs=ro_jgs)
    stage_1_Speed_reduced = math.sqrt(2 * g * stage_1_dh_jg_reduced)
    stage_1_h_yr = mfH.calculate_h_yr(init_usl_Volume_jg_reduced, init_oil_volume_NKT, init_oil_volume_KP, init_dV_pogl,
                                      NKT.area, KP.area, NKT.length)
    Height_of_well = NKT.length - U_stat
    ## Уровни нефти в участках скважины (этап 1)
    stage_1_oil_level_NKT = NKT.length - U_stat
    stage_1_oil_level_KP = NKT.length - U_stat
    stage_1_oil_level_EXP = Length_of_Well - NKT.length
    ## Уровни ЖГС в участках скважины (этап 1)
    stage_1_jgs_level_NKT = mfH.calculate_NKT_jg_height(stage_1_oil_level_NKT, stage_1_Height_jg, NKT.length)
    stage_1_jgs_level_KP = 0
    stage_1_jgs_level_EXP = 0
    ## Объемы нефти в участках скважины (этап 1)
    stage_1_oil_volume_NKT = stage_1_oil_level_NKT * NKT.area
    stage_1_oil_volume_KP = (stage_1_oil_level_KP * KP.area)
    stage_1_oil_volume_EXP = ((Length_of_Well - NKT.length) * math.pi * EXP.inner_diameter ** 2) / 4
    ## Объемы ЖГС в участках скважины (этап 1)
    stage_1_jgs_volume_NKT = stage_1_jgs_level_NKT * NKT.area
    stage_1_jgs_volume_KP = 0
    stage_1_jgs_volume_EXP = 0
    ## Скорости движения жидкости в участках скважины (этап 1)
    stage_1_v_NKT = 0
    stage_1_v_KP = 0
    stage_1_v_EXP = 0
    ## Параметры
    stage_1_Q_pogl = 0
    stage_1_V_pogl = 0
    stage_1_R_oil = 0.1
    stage_1_dV_pogl = init_V_pogl - stage_1_V_pogl
    ## Давления
    stage_1_Pressure_friction = mfP.calculate_Pressure_friction(stage_1_oil_level_NKT, stage_1_jgs_level_NKT,
                                                                stage_1_oil_level_KP,
                                                                stage_1_jgs_level_KP, NKT.length, NKT.inner_diameter,
                                                                NKT.external_diameter, EXP.inner_diameter,
                                                                stage_1_v_NKT,
                                                                stage_1_v_KP, mu_oil, mu_jg)
    stage_1_Pressure_yst = mfP.calculate_Pressure_wellhead(101325, stage_1_Pressure_friction)
    stage_1_Pressure_NKT = mfP.calculate_Pressure_at_Wellspace(Wellspace_oil_height=stage_1_oil_level_NKT,
                                                               density_oil=ro_oil,
                                                               Wellspace_jgs_height=stage_1_jgs_level_NKT,
                                                               density_jgs=ro_jgs)
    stage_1_Pressure_KP = mfP.calculate_Pressure_at_Wellspace(Wellspace_oil_height=stage_1_oil_level_KP,
                                                              density_oil=ro_oil,
                                                              Wellspace_jgs_height=stage_1_jgs_level_KP,
                                                              density_jgs=ro_jgs)
    stage_1_Pressure_EXP = mfP.calculate_Pressure_at_Wellspace(Wellspace_oil_height=stage_1_oil_level_EXP,
                                                               density_oil=ro_oil,
                                                               Wellspace_jgs_height=stage_1_jgs_level_EXP,
                                                               density_jgs=ro_jgs)
    stage_1_Pressure_downhole = mfP.calculate_Pressure_downhole(
        Pressure_wellhead=stage_1_Pressure_yst, Pressure_NKT=stage_1_Pressure_NKT, Pressure_EXP=stage_1_Pressure_EXP
    )
    stage_1_Pressure_overall = stage_1_Pressure_yst + stage_1_Pressure_NKT + stage_1_Pressure_EXP
    print("Q")
    ## Объявление классов участков скважины (этап 1)
    NKT_params = mc.WellSpace(name="NKT",
                              t=None,
                              dt=dt,
                              oil_volume=None,
                              oil_height=None,
                              jgs_volume=None,
                              jgs_height=None,
                              pressure=None,
                              construction=NKT)
    KP_params = mc.WellSpace(name="KP",
                             t=None,
                             dt=dt,
                             oil_volume=None,
                             oil_height=None,
                             jgs_volume=None,
                             jgs_height=None,
                             pressure=None,
                             construction=KP)
    EXP_params = mc.WellSpace(
        name="EXP",
        t=None,
        dt=dt,
        oil_volume=None,
        oil_height=None,
        jgs_volume=None,
        jgs_height=None,
        pressure=None,
        construction=EXP)

    Oil = mc.Fluid(
        name="oil",
        viscosity=mu_oil,
        density=ro_oil,
        phase_permeability=k_oil)
    Jgs = mc.Fluid(name='jgs',
                   viscosity=mu_jg,
                   density=ro_jgs,
                   phase_permeability=k_jg)
    Reservoir = mc.Reservoir(porosity=m,
                             permeability_oil=k_oil,
                             permeability_jgs=k_jg,
                             height=h,
                             pressure=101325)
    tech_params = mc.TechnicalCalculations(Q_pogl=None,
                                           V_pogl=None,
                                           dV_pogl=None,
                                           Rn=None,
                                           pressure_friction=None,
                                           pressure_wellhead=None,
                                           pressure_downhole=None,
                                           pressure_overall=None,
                                           Rk=Rk,
                                           dt=dt,
                                           Q=Q,
                                           )

    # Объявление пост и пост-пост параметров участков скважины и технических параметров
    post_params_NKT = {
        "t": t_1,
        "oil_volume": stage_1_oil_volume_NKT,
        "oil_height": stage_1_oil_level_NKT,
        "jgs_volume": stage_1_jgs_volume_NKT,
        "jgs_height": stage_1_jgs_level_NKT,
        "pressure": stage_1_Pressure_NKT}
    post_post_params_NKT = {
        "t": t_0,
        "oil_volume": init_oil_volume_NKT,
        "oil_height": init_oil_level_NKT,
        "jgs_volume": 0,
        "jgs_height": init_jgs_level_NKT,
        "pressure": init_Pressure_NKT}
    post_params_KP = {
        "t": t_1,
        "oil_volume": stage_1_oil_volume_KP,
        "oil_height": stage_1_oil_level_KP,
        "jgs_volume": stage_1_jgs_volume_KP,
        "jgs_height": stage_1_jgs_level_KP,
        "pressure": stage_1_Pressure_KP}
    post_post_params_KP = {
        "t": t_0,
        "oil_volume": init_oil_volume_KP,
        "oil_height": init_oil_level_KP,
        "jgs_volume": 0,
        "jgs_height": init_jgs_level_KP,
        "pressure": init_Pressure_KP}
    post_params_EXP = {
        "t": t_1,
        "oil_volume": stage_1_oil_volume_EXP,
        "oil_height": stage_1_oil_level_EXP,
        "jgs_volume": stage_1_jgs_volume_EXP,
        "jgs_height": stage_1_jgs_level_EXP,
        "pressure": stage_1_Pressure_EXP}
    post_post_params_EXP = {
        "t": t_0,
        "oil_volume": init_oil_volume_EXP,
        "oil_height": init_oil_level_EXP,
        "jgs_volume": 0,
        "jgs_height": init_jgs_level_EXP,
        "pressure": init_Pressure_EXP}
    post_tech = {
        "Q_pogl": stage_1_Q_pogl,
        "V_pogl": stage_1_V_pogl,
        "dV_pogl": stage_1_dV_pogl,
        "Rn": stage_1_R_oil,
        "pressure_friction": stage_1_Pressure_friction,
        "pressure_wellhead": stage_1_Pressure_yst,
        "pressure_downhole": stage_1_Pressure_downhole,
        "pressure_overall": stage_1_Pressure_overall,
    }
    post_post_tech = {
        "Q_pogl": init_Q_pogl,
        "V_pogl": init_V_pogl,
        "dV_pogl": init_dV_pogl,
        "Rn": init_R_oil,
        "pressure_friction": init_Pressure_friction,
        "pressure_wellhead": init_Pressure_yst,
        "pressure_downhole": init_Pressure_downhole,
        "pressure_overall": init_Pressure_overall,
    }

    # Сохраняем параметры
    NKT_params.save_params(post_params_NKT, "post")
    NKT_params.save_params(post_post_params_NKT, "post_post")
    KP_params.save_params(post_params_KP, "post")
    KP_params.save_params(post_post_params_KP, "post_post")
    EXP_params.save_params(post_params_EXP, "post")
    EXP_params.save_params(post_post_params_EXP, "post_post")

    tech_params.save_params(post_tech, "post")
    tech_params.save_params(post_post_tech, "post_post")

    # Объявляем класс в котором происходят обычные вычисления
    All_common_calculations = mc.CommonCalculations(Vjg=None,
                                                    Vjg_reduced=None,
                                                    Hjg=None,
                                                    Hjg_reduced=None,
                                                    dh_jg=None,
                                                    dh_jg_reduced=None,
                                                    speed=None,
                                                    h_yr=None,
                                                    dV_pogl=None)
    # Записываем его параметры с предыдущего шага (этап 1)
    post_parameters_for_calculations = {"Vjg": stage_1_Vjg,
                                        "Vjg_reduced": stage_1_Vjg_reduced,
                                        "Hjg": stage_1_Height_jg,
                                        "Hjg_reduced": stage_1_Height_jg_reduced,
                                        "dh_jg": stage_1_dh_jg,
                                        "dh_jg_reduced": stage_1_dh_jg_reduced,
                                        "speed": stage_1_Speed_reduced,
                                        "h_yr": stage_1_h_yr,
                                        "dV_pogl": stage_1_dV_pogl}
    # Записываем его параметры с пост-пост шага (этап 0)
    post_post_parameters_for_calculations = {"Vjg": init_usl_Volume_jg,
                                             "Vjg_reduced": init_usl_Volume_jg_reduced,
                                             "Hjg": init_usl_Height_jg,
                                             "Hjg_reduced": init_usl_Height_jg_reduced,
                                             "dh_jg": init_usl_dh_jg,
                                             "dh_jg_reduced": init_usl_dh_jg_reduced,
                                             "speed": init_usl_Speed_reduced,
                                             "h_yr": init_usl_h_yr,
                                             "dV_pogl": init_dV_pogl}

    # Сохраняем параметры как атрибуты класса
    All_common_calculations.save_params(post_parameters_for_calculations, "post")
    All_common_calculations.save_params(post_post_parameters_for_calculations, "post_post")
    t = t_1
    iteration_count = 0
    t_array = [t_0, t_1]
    P_yst = [init_Pressure_yst, stage_1_Pressure_yst]
    p_overall = [init_Pressure_downhole, stage_1_Pressure_overall]
    P_friction = [init_Pressure_friction, stage_1_Pressure_friction]
    P_NKT = [init_Pressure_NKT, stage_1_Pressure_NKT]
    P_KP = [init_Pressure_KP, stage_1_Pressure_KP]
    P_EXP = [init_v_EXP, stage_1_Pressure_EXP]
    time_to_glush = DESIGN_volume_glush / Q
    while t < time_to_glush:
        t = t + dt
        t_array.append(t)
        print("Итерация началась")
        All_common_calculations.Vjg, All_common_calculations.Vjg_reduced = All_common_calculations.calculateVjgs(
            debit=Q,
            time=t,
            density_of_oil=Oil.density,
            density_of_jgs=Jgs.density)
        All_common_calculations.Hjg, All_common_calculations.Hjg_reduced = All_common_calculations.calculateHjg(
            NKT.area)
        All_common_calculations.dh_jg, All_common_calculations.dh_jg_reduced = All_common_calculations.calculatedh()
        All_common_calculations.speed = All_common_calculations.calculatespeed()
        print(All_common_calculations.Vjg)
        print(DESIGN_volume_glush)
        tech_params.Q_pogl = tech_params.calculate_Q_pogl(plast_thickness=Reservoir.height,
                                                          Fluid_oil=Oil,
                                                          Fluid_jgs=Jgs,
                                                          EXP_construction=EXP)
        tech_params.V_pogl = tech_params.calculate_V_pogl()
        tech_params.Rn = tech_params.calculate_Rn(Reservoir)
        tech_params.dV_pogl = tech_params.calculate_dV_pogl()
        All_common_calculations.h_yr = All_common_calculations.calculate_h_yr(NKT_params=NKT_params,
                                                                              KP_params=KP_params,
                                                                              NKT=NKT, KP=KP, tech_params=tech_params)
        NKT_params.oil_height = NKT_params.calculate_level_oil_NKT(All_common_calculations)
        NKT_params.jgs_height = NKT_params.calculate_level_jgs_NKT(All_common_calculations.Hjg)
        KP_params.jgs_height = KP_params.calculate_level_jgs_KP(NKT_params=NKT_params, tech_params=tech_params,
                                                                NKT_construction=NKT)
        KP_params.oil_height = KP_params.calculate_level_oil_KP(common=All_common_calculations)
        EXP_params.jgs_height = EXP_params.calculate_level_jgs_EXP(NKT_params=NKT_params, tech_params=tech_params)
        EXP_params.oil_height = EXP_params.calculate_level_oil_EXP(NKT_params=NKT_params, EXP_params=EXP_params)
        if iteration_count == 0:
            NKT_speed = (NKT_params.oil_height_post - NKT_params.oil_height) / dt
            KP_speed = (KP_params.oil_height - KP_params.oil_height_post) / dt
        elif iteration_count == 1:
            NKT_speed = (NKT_params.oil_height_post - NKT_params.oil_height) / dt
            KP_speed = (KP_params.oil_height - KP_params.oil_height_post) / dt
        else:
            NKT_speed = NKT_speed
            KP_speed = KP_speed
        tech_params.pressure_friction = tech_params.calculate_pressure_friction(NKT_params, KP_params, NKT, EXP, Oil,
                                                                                Jgs, NKT_speed, KP_speed)
        tech_params.pressure_wellhead = tech_params.calculate_pressure_wellhead(Reservoir=Reservoir)
        NKT_params.pressure = NKT_params.calculate_pressure(Oil, Jgs)
        KP_params.pressure = KP_params.calculate_pressure(Oil, Jgs)
        EXP_params.pressure = EXP_params.calculate_pressure(Oil, Jgs)
        tech_params.pressure_overall = tech_params.calculate_pressure_overall(NKT_params=NKT_params,
                                                                              EXP_params=EXP_params)
        NKT_params.oil_volume = NKT_params.calculate_volume_NKT_oil(NKT)
        NKT_params.jgs_volume = NKT_params.calculate_volume_NKT_jgs(NKT)
        KP_params.oil_volume = KP_params.calculate_volume_KP_oil(KP)
        KP_params.jgs_volume = KP_params.calculate_volume_KP_jgs(KP)
        EXP_params.oil_volume = EXP_params.calculate_volume_EXP_oil(EXP)
        EXP_params.jgs_volume = EXP_params.calculate_volume_EXP_jgs(EXP)
        iteration_count += 1
        P_yst.append(tech_params.pressure_wellhead)
        p_overall.append(tech_params.pressure_overall)
        P_friction.append(tech_params.pressure_friction)
        P_NKT.append(NKT_params.pressure)
        P_KP.append(KP_params.pressure)
        P_EXP.append(EXP_params.pressure)
        # print(f"Это Vjg {All_common_calculations.Vjg}\n"
        #       f"Это Hjg {All_common_calculations.Hjg}\n"
        #       f"Это dh_jg {All_common_calculations.dh_jg}\n"
        #       f"Это скорость {All_common_calculations.speed}\n"
        #       f"Это Q_pogl {tech_params.Q_pogl}\n"
        #       f"Это dV_pogl {tech_params.dV_pogl}\n"
        #       f"Это V_pogl {tech_params.V_pogl}\n"
        #       f"Это Rn {tech_params.Rn} \n "
        #       f"Это h_yr {All_common_calculations.h_yr} \n"
        #       f"Это NKT oil_height {NKT_params.oil_height} \n"
        #       f"Это NKT jgs_height {NKT_params.jgs_height} \n"
        #       f"Это KP jgs_height {KP_params.jgs_height} \n"
        #       f"Это KP oil_height {KP_params.oil_height} \n"
        #       f"Это EXP jgs_height {EXP_params.jgs_height} \n"
        #       f"Это EXP oil_height {EXP_params.oil_height} \n"
        #       f"Это Pressure friction {tech_params.pressure_friction} \n"
        #       f"Это Pressure wellhead {tech_params.pressure_wellhead} \n"
        #       f"Это Pressure NKT {NKT_params.pressure} \n"
        #       f"Это Pressure KP {KP_params.pressure} \n"
        #       f"Это Pressure EXP {EXP_params.pressure} \n"
        #       f"Это Pressure overall {tech_params.pressure_overall} \n"
        #       f"Это объем жидкости нефть в НКТ {NKT_params.oil_volume}\n"
        #       f"Это объем жидкости ЖГС в НКТ {NKT_params.jgs_volume}\n"
        #       f"Это объем жидкости нефть в КП {KP_params.oil_volume}\n"
        #       f"Это объем жидкости ЖГС в КП {KP_params.jgs_volume}\n"
        #       f"Это объем жидкости нефть в ЭКСПЛ {EXP_params.oil_volume}\n"
        #       f"Это объем жидкости ЖГС в ЭКСПЛ {EXP_params.jgs_volume}\n"
        #       )
    P_yst = [x / 10 ** 6 for x in P_yst]
    P_friction = [x / 10 ** 6 for x in P_friction]
    P_NKT = [x / 10 ** 6 for x in P_NKT]
    P_KP = [x / 10 ** 6 for x in P_KP]
    P_EXP = [x / 10 ** 6 for x in P_EXP]
    p_overall = [x / 10 ** 6 for x in p_overall]
    Pressures_array = [P_yst, p_overall, P_friction, P_NKT, P_KP, P_EXP]

    print(All_common_calculations.Vjg)
    results = {
        "EXP_volume": round(EXP.volume, 2),
        "NKT_volume": round(NKT.volume, 2),
        "KP_volume": round(KP.volume, 2),
        "FULL_EXP_volume": round(FULL_EXP.volume, 2),
        "Vjg": round(All_common_calculations.Vjg, 2),
        "Vjg_self": round(All_common_calculations.Vjg * 1.1, 2)
    }
    DESIGN = {
        "DESIGN_volume_glush": round(DESIGN_volume_glush, 2),
        "DESIGN_volume_oil": round(DESIGN_volume_oil, 2),
        "DESIGN_volume_emul": round(DESIGN_volume_emul, 2),
        "DESIGN_volume_rast": round(DESIGN_volume_rast, 2),
        "DESIGN_jgs_density": round(DESIGN_jgs_density, 2),
        "DESIGN_pressure_zapas": round(DESIGN_pressure_zapas, 2),
        "DESIGN_true_jgs_density": round(DESIGN_true_jgs_density, 2),
        "DESIGN_safe_jgs_density": round(DESIGN_safe_jgs_density, 2),
        "DESIGN_recommended_salt_name": DESIGN_recommended_salt_name,
        "DESIGN_recommended_salt_debit": DESIGN_recommended_salt_debit,
        "DESIGN_recommended_water_debit": DESIGN_recommended_water_debit,
        "DESIGN_chosen_salt_name": DESIGN_chosen_salt_name,
        "DESIGN_chosen_salt_debit": DESIGN_chosen_salt_debit,
        "DESIGN_chosen_water_debit": DESIGN_chosen_water_debit,
        "DESIGN_water_mass": DESIGN_water_mass,
        "DESIGN_salt_mass": DESIGN_salt_mass,
        "DESIGN_water_volume": round(DESIGN_water_volume, 2),
        "DESIGN_volume_zapas": round(DESIGN_volume_zapas, 2),
        'DESIGN_volume_bez_zapasa': round(DESIGN_volume_bez_zapasa, 2),
        'DESIGN_counts_of_zak':1,

    }

    STAGES = {
        "RECIPE_YV_st1" : round(RECIPE_YV_st1,2),
        "RECIPE_EMUL_st1" : round(RECIPE_EMUL_st1,2),
        "RECIPE_SOLERAST_st1" : round(RECIPE_SOLERAST_st1,2),
        "RECIPE_BP_st1" : round(RECIPE_BP_st1,2),
        "RECIPE_YV_st2" : round(RECIPE_YV_st2,2),
        "RECIPE_EMUL_st2" : round(RECIPE_EMUL_st2,2),
        "RECIPE_SOLERAST_st2" : round(RECIPE_SOLERAST_st2,2),
        "RECIPE_BP_st2" : round(RECIPE_BP_st2,2),
        "RECIPE_YV_st3" : round(RECIPE_YV_st3,2),
        "RECIPE_EMUL_st3" : round(RECIPE_EMUL_st3,2),
        "RECIPE_SOLERAST_st3" : round(RECIPE_SOLERAST_st3,2),
        "RECIPE_BP_st3" : round(RECIPE_BP_st3,2),
        "RECIPE_YV_st4" : round(RECIPE_YV_st4,2),
        "RECIPE_EMUL_st4" : round(RECIPE_EMUL_st4,2),
        "RECIPE_SOLERAST_st4" : round(RECIPE_SOLERAST_st4,2),
        "RECIPE_BP_st4" : round(RECIPE_BP_st4,2)
    }
    print(DESIGN)
    return results, Pressures_array, t_array, DESIGN, STAGES

    # stage_1_Speed_reduced = math.sqrt(2 * g * stage_1_Height_jg_reduced)
    # h_yr = mfH.calculate_h_yr()
    # print(stage_1_Height_jg_reduced)
    # print(t)
# matmodel_glush(Plast_pressure, h, Length_of_Well, L_of_Wells, ro_oil, ro_jgs,d_NKT, D_NKT, d_exp, D_exp, Q, k_jg, mu_jg, k_oil, mu_oil,Rk, m, 20)
# matmodel_glush(10132500.0, 10.0, 1500.0, 1400.0, 800.0, 1070.0, 0.062, 0.073, 0.15, 0.163, 0.1, 1.5e-12, 0.001, 5e-13, 0.005, 250.0, 0.2,20)
