import math

def calculate_com_U_stat(pressure, length, density, g):
    calculated_value = length - pressure/(density * g)
    if calculated_value < 0:
        return 0
    else:
        return calculated_value

def calculate_com_volume_of_jgs(debit, time, case = None, density_of_oil = None, density_of_jgs = None):
    if case == "reduced":
        return debit * time, (debit * time * density_of_jgs) / density_of_oil
    else:
        return debit * time

def calculate_com_liquid_level_of_jgs(volume, area, case = None, density_of_oil = None, density_of_jgs = None):
    if case == "reduced":
        return volume/area, (volume/area) * (density_of_jgs/ density_of_oil)
    else:
        return volume/area


def calculate_com_dh(height_current, height_post, case = None, density_of_oil = None, density_of_jgs = None):
    if case == "None":
        dh = height_current-height_post
        return dh
    else:
        dh = height_current-height_post
        dh_reduced = (height_current-height_post) * (density_of_jgs/density_of_oil)
        return dh, dh_reduced


# Дебит поглощения пластом
def Q(height, P_post, P_post_post, radius_oil_post, radius_contour,  radius_well, mu_oil, mu_jgs, permeability_oil, permeability_jgs):
    multiplier = 2 * math.pi * height * (P_post - P_post_post)
    denominator = (math.log(radius_oil_post/radius_well) * (mu_oil/permeability_oil)) + (math.log(radius_contour/radius_oil_post) * (mu_jgs/permeability_jgs))
    return multiplier/denominator
# Объем поглощения за время dt
def Vpogl (Q, dt):
    return Q*dt

# Радиус проникновения
def calculate_Rn (Rn_post, Q, h, m, dt):
    Rn = Rn_post +(Q*dt/(2*math.pi*h*Rn_post*m))
    return Rn
