import math
import sympy
import numpy

# Дано
Plast_pressure = 10132500
h = 10
len_of_Well = 1500
dl = 10
len_of_NKT = 1400
ro_of_oil = 800
ro_of_wellkilling_liquid = 1070
g = 9.81
diameter_of_NKT_internal = 0.062
diameter_of_NKT_external = 0.073
diameter_of_EXP_internal = 0.15
diameter_of_EXP_external = 0.163
debit = 0.01

k_nulevoe = 1.5*10**(-12)
mu_nulevoe = 0.001
k_r = 5*10**(-13)
mu_r = 0.005
rc = 0.1
Rk = 250
m = 0.2

class Tube:
    def __init__(self,name, external_diameter, internal_diameter,length):
        self.name = name
        self.external_diameter = external_diameter
        self.internal_diameter = internal_diameter
        self.length = length
        self.area,self.volume = 0, 0,
    def calculate_area(self):
        area = math.pi * (self.internal_diameter**2)/4
        return area
    def calculate_volume (self):
        volume = self.length*self.area
        self.volume = volume
        return self.volume

NKT_Tube = Tube("NKT",diameter_of_NKT_external, diameter_of_NKT_internal, len_of_NKT)
print(NKT_Tube.calculate_area())
NKT_Tube.calculate_volume()
EXP_Tube = Tube("EXP",diameter_of_EXP_external, diameter_of_EXP_internal, len_of_Well)
print(EXP_Tube.calculate_area())
EXP_Tube.calculate_volume()


class Substance:
    def __init__(self,name, density,):
        self.name = name
        self.density = density

Wellkilling_fluid = Substance("Wellkilling_fluid", 1070)
Oil = Substance('Oil', 800)