

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
def calculate_NKT_jg_height(NKT_oil_height, Hjg, NKT_length):
    calculated_check = NKT_oil_height + Hjg
    if calculated_check > NKT_length:
        return NKT_length-NKT_oil_height
    else:
        return Hjg
# Высота ЖГ в КП
def calculate_KP_jg_height(NKT_oil_height, KP_jg_height_pred,Q_of_car, Q_pogl, dt, KP_area, NKT_length):
    if NKT_oil_height > 0:
        KP_jg_height = 0
        return KP_jg_height
    else:
        KP_jg_height =  KP_jg_height_pred +((Q_of_car - Q_pogl)*dt/KP_area)
        if KP_jg_height > NKT_length:
            KP_jg_height = NKT_length
            return KP_jg_height
        else:
            return KP_jg_height
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
