# Все функции по работе с давлениями #
import math
# Потери на трение (Pтр)
def calculate_Pressure_friction (NKT_oil_height, NKT_jgs_height, KP_oil_height, KP_jgs_height, NKT_length,NKT_inner_diameter,
                                 NKT_external_diameter, EXP_inner_diameter, NKT_speed, KP_speed, mu_oil, mu_jgs):
    if NKT_oil_height + NKT_jgs_height < NKT_length:
        Pressure_friction = 0
        return Pressure_friction
    else:
        Pressure_friction = (((32*NKT_speed)/(NKT_inner_diameter**2))*(mu_oil*NKT_oil_height+mu_jgs*NKT_jgs_height)+
                             ((32*KP_speed)/(EXP_inner_diameter**2 - NKT_external_diameter**2))*(mu_oil*KP_oil_height+
                                                                                                 mu_jgs*KP_jgs_height))
        return Pressure_friction

# Давление устьевое (Pу)
def calculate_Pressure_wellhead(Pressure_stabilized, Pressure_friction):
    return Pressure_stabilized + Pressure_friction

# Давление в каком-то пространстве (НКТ, КП, ЭКСПЛ)
def calculate_Pressure_at_Wellspace (Wellspace_oil_height, density_oil, Wellspace_jgs_height, density_jgs):
    return 9.81*(Wellspace_oil_height*density_oil+Wellspace_jgs_height*density_jgs)

# Давление на забое
def calculate_Pressure_downhole (Pressure_wellhead, Pressure_NKT, Pressure_EXP):
    return Pressure_wellhead+Pressure_EXP+Pressure_NKT
