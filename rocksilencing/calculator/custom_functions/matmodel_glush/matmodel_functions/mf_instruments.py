def format_number(num):
    rounded_num = round(num, 1)
    formatted_num = "{:.1f}".format(rounded_num)
    return rounded_num

def pressure_format(pressure, from_Pa = True, to_atm = True):
    if from_Pa == True and to_atm == True:
        pressure = pressure / 101325
        return pressure
