import math
# Вычисление площади по диаметру
def calculate_area(d, case = None):
    if case == "KP":
        return (math.pi * (d[0] ** 2 - d[1]**2)) / 4
    else:
        return (math.pi * d ** 2) / 4
# Вычисление объема трубы по площади и высоте
def calculate_volume_of_tube(area, length):
        return area*length