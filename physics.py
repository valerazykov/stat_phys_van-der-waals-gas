import math
from sympy import *


# Все параметры измеряются в единицах измерения Си.
# a - характеризует силу притяжения молекул, измеряется в Дж * м^3 / моль
# b - характеризует размер молекул, измеряется в м^3 / моль
# В справочниках b дается в см^3 / моль

# Приемлемые значения давления - несколько атмосфер (1 атм = 10^5 Па),
# объёма - десятые, сотые, десятки кубических метров
# температуры - 250 - 310 К

R = 8.31

MIN_PRESS = 100
MAX_PRESS = 1e7

MIN_VOL = 1e-8
MAX_VOL = 1e4

MIN_TEMP = 220
MAX_TEMP = 500

MIN_a = 0
MAX_a = 1.5

MIN_b = 1  # в см^3 / моль
MAX_b = 110  # в см^3 / моль

# b в см^3 / моль
a_b_for_real_gases = {
    "He": (0.00346, 23.8),
    "Ar": (0.1355, 32),
    "Ne": (0.0208, 16.7),
    "Kr": (0.5193, 10.6),
    "Xe": (0.4192, 51.6)
    # не одноатомные газы:
    # "N2": (0.137, 38.7),
    # "H2O": (0.5537, 30.5),
    # "O2": (0.1382, 31.9),
    # "HCN": (1.129, 88.1)
}


def b_to_SI(b):
    return b / 1e6


def p_to_atm(p):
    """from Pa to atm"""
    return p / 1e5


def p_to_pas(p):
    """from atm to pas"""
    return p * 1e5


def vol_to_cm3(vol):
    """from m^3 to cm^3"""
    return vol * 1e6


def vol_to_m3(vol):
    """from cm^3 to m^3"""
    return vol / 1e6

def energy_change(temp, vol, a, mole=1, freedoms=3):
    U_0 = mole * freedoms * R * temp[0] / 2 - mole * mole * a / vol[0]
    U_1 = mole * freedoms * R * temp[1] / 2 - mole * mole * a / vol[1]
    return U_1 - U_0


def work(temp, vol, a, b, mole=1):
    if temp[0] == temp[1]:
        answer = mole * R * temp[0] * math.log(
            (vol[1] - mole * b) / (vol[0] - mole * b))
        return answer - mole * mole * a * (1 / vol[0] - 1 / vol[1])
    elif vol[0] == vol[1]:
        return 0

    raise NotImplementedError


def warmth_change(temp, vol, a, b, mole=1, freedoms=3):
    if temp[0] == temp[1]:
        return mole * R * temp[0] * math.log(
            (vol[1] - mole * b) / (vol[0] - mole * b)
        )
    answer = energy_change(temp, vol, a, mole, freedoms)
    return answer + work(temp, vol, a, b, mole)


def entropy_change(temp, vol, b, freedoms=3):
    return (freedoms / 2 * R * math.log(temp[1] / temp[0]) +
            R * math.log((vol[1] - b) / (vol[0] - b)))


def calc_press(temp, vol, a, b, mole=1):
    return mole * R * temp / (vol - mole * b) - a * mole * mole / (vol ** 2)


def calc_volume_list(temp, press, a, b, mole=1):
    x = symbols('x', real=True)
    expr = (press * x ** 3 - (press * mole * b + mole * R * temp) * x ** 2 +
            mole ** 2 * a * x - mole ** 3 * a * b)
    return solve(expr, x)


def calc_volume(temp, press, a, b, mole=1):
    return max(calc_volume_list(temp, press, a, b, mole))


def calc_temperature(press, vol, a, b, mole=1):
    return (press + mole ** 2 * a / (vol ** 2)) * (vol - mole * b) / (mole * R)


def calc_crit_temp(a, b):
    return 8 * a / (27 * b * R)


def calc_crit_press(a, b):
    return a / (27 * b ** 2)


def calc_crit_volume(b):
    return 3 * b
