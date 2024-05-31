

# Уровень (общий в скважине)
def calculate_h_yr (V_jg_reduced_post, V_nkt_oil_post, V_kp_oil_post, dV_pogl, NKT_area, KP_area, NKT_length):
    calculated_h_yr = (V_jg_reduced_post+V_nkt_oil_post+V_kp_oil_post-dV_pogl)/(NKT_area+KP_area)
    if calculated_h_yr>NKT_length:
        calculated_h_yr = NKT_length
        return calculated_h_yr
    else:
        return calculated_h_yr
# Высота нефти в НКТ
def calculate_NKT_oil_height(h_yr, Hjg_reduced_post):
    calculated_height = h_yr - Hjg_reduced_post
    if calculated_height < 0:
        calculated_height = 0
        return calculated_height
    else:
        return calculated_height
# Высота ЖГ в НКТ
def calculate_NKT_jg_height(NKT_params_oil_height, Hjg, dh_jg, V_pogl, EXP, NKT, KP, jgs_height_post, type_of_glush = "direct"):
    if type_of_glush == "direct":
        changing_param = dh_jg
        changing_area = NKT.area
    else:
        changing_param = dh_jg - V_pogl/EXP.area
        changing_area = KP.area
    if NKT_params_oil_height == 0.0:
        calculated_value = jgs_height_post + (dh_jg - V_pogl / EXP.area) * (
                changing_area / (NKT.area + KP.area))
        if calculated_value > NKT.length:
            jgs_height = NKT.length
            return jgs_height
        else:
            calculated_value_2 = jgs_height_post + changing_param * (changing_area / (NKT.area + KP.area))
            jgs_height = calculated_value_2
            return jgs_height
    else:
        jgs_height = Hjg
        return jgs_height
# Высота ЖГ в КП
def calculate_KP_jg_height(NKT_oil_height, KP_jg_height_pred,dh_jg, V_pogl, EXP_area, NKT_area, NKT_length, KP_area, NKT_jg_height, type_of_glush = "direct"):
    if type_of_glush == "direct":
        changing_area = NKT_area
        popravka = 1
    else:
        changing_area = KP_area
        popravka = -1
    if NKT_oil_height > 0:
        KP_jg_height = 0
        return KP_jg_height
    else:
        if KP_jg_height_pred + (dh_jg - V_pogl/EXP_area)*(changing_area/(NKT_area+KP_area)) > NKT_length:
            return NKT_length
        else:
            if NKT_jg_height == NKT_length:
                calculated_value = KP_jg_height_pred + (dh_jg - V_pogl/EXP_area)*(NKT_area/KP_area)**popravka
                return calculated_value
            else:
                calculated_value = KP_jg_height_pred + (dh_jg-V_pogl/EXP_area)*(changing_area/(NKT_area + KP_area))
                return calculated_value

# Высота нефти в КП
def calculate_KP_oil_height(h_yr, KP_jg_height):
    return h_yr - KP_jg_height
# Высота ЖГС в ЭКСПЛ
def calculate_EXP_jgs_height(NKT_oil_height, EXP_jg_height_pred, V_pogl, EXP_area, EXP_length):
    if NKT_oil_height > 0:
        EXP_jg_height = 0
        return EXP_jg_height
    else:
        calculated_parameter = EXP_jg_height_pred+(V_pogl/EXP_area)
        if calculated_parameter > EXP_length:
            EXP_jg_height = EXP_length
            return EXP_jg_height
        else:
            EXP_jg_height = calculated_parameter
            return EXP_jg_height
# Высота нефти в ЭКСПЛ
def calculate_EXP_oil_height(NKT_oil_height, EXP_length, EXP_jgs_height):
    if NKT_oil_height > 0:
        EXP_oil_height = EXP_length
        return EXP_oil_height
    else:
        if (EXP_length-EXP_jgs_height)<0:
            EXP_oil_height = 0
            return EXP_oil_height
        else:
            EXP_oil_height = EXP_length - EXP_jgs_height
            return EXP_oil_height
