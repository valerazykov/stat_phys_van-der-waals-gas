import math
import numpy as np
from numpy.polynomial.polynomial import Polynomial
from sympy import symbols, solve
from sympy.calculus.util import Interval, minimum, maximum

# Все параметры измеряются в единицах измерения Си.
# a - характеризует силу притяжения молекул, измеряется в Дж * м^3 / моль
# b - характеризует размер молекул, измеряется в м^3 / моль
# В справочниках b дается в см^3 / моль

# Приемлемые значения давления - несколько атмосфер (1 атм = 10^5 Па),
# объёма - десятые, сотые, десятки кубических метров
# температуры - 250 - 310 К

EPS = 1e-12

R = 8.31

MIN_PRESS = 100
MAX_PRESS = 305 * 1e5

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


def energy(temp, vol, a, mole=1, freedoms=3):
    return mole * freedoms * R * temp / 2 - mole * mole * a / vol


def energy_change(temp, vol, a, mole=1, freedoms=3):
    U_0 = energy(temp[0], vol[0], a, mole, freedoms)
    U_1 = energy(temp[1], vol[1], a, mole, freedoms)
    return U_1 - U_0


def work(temp, vol, a, b, mole=1):
    if abs(temp[0] - temp[1]) < EPS:
        answer = mole * R * temp[0] * math.log(
            (vol[1] - mole * b) / (vol[0] - mole * b))
        return answer - mole * mole * a * (1 / vol[0] - 1 / vol[1])
    elif abs(vol[0] - vol[1]) < EPS:
        return 0

    raise NotImplementedError


def warmth_change(temp, vol, a, b, mole=1, freedoms=3):
    if abs(temp[0] - temp[1]) < EPS:
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


def calc_volume_arr(temp, press, a, b, min_vol, max_vol, mole=1) -> np.ndarray:
    coefs = np.array([- mole ** 3 * a * b, mole ** 2 * a,
                      - (press * mole * b + mole * R * temp), press],
                     dtype="float64")
    pol = Polynomial(coefs)
    roots = pol.roots()
    real_roots = np.real(roots[np.isreal(roots)])
    real_roots_in_domain = real_roots[
        (min_vol <= real_roots) & (real_roots <= max_vol)
        ]
    return real_roots_in_domain


def calc_volume(temp, press, a, b, min_vol, max_vol, mole=1):
    vol_list = calc_volume_arr(temp, press, a, b, min_vol, max_vol, mole)
    return np.max(vol_list)


def calc_temperature(press, vol, a, b, mole=1):
    return (press + mole ** 2 * a / (vol ** 2)) * (vol - mole * b) / (mole * R)


def calc_crit_temp(a, b):
    """Для 1 моля вещества"""
    return 8 * a / (27 * b * R)


def calc_crit_press(a, b):
    """Для 1 моля вещества"""
    return a / (27 * b ** 2)


def calc_crit_volume(b):
    """Для 1 моля вещества"""
    return 3 * b


def calc_min_temp(a, b):
    """
    Найти температуру, при которой изотерма касается оси V.
    (Для 1 моля вещества).
    """
    return a / (4 * R * b)


def calc_min_vol(a, b, temp_left, alpha=0.8):
    """
    Посчитать нижнюю границу для V, в зависимости от нижней границы
    температуры temp_left.
    (Для 1 моля вещества).
    """
    vol = symbols("vol", real=True)
    expr = R * temp_left / (vol - b) - a / vol ** 2 - a / (27 * b ** 2)
    return (1 - alpha) * b + alpha * min(solve(expr, vol))


def calc_max_vol(a, b, temp_right):
    """
    Посчитать верхнюю границу для V, в зависимости от верхней границы
    температуры temp_right.
    (Для 1 моля вещества).
    """
    vol = symbols("vol", real=True)
    expr = R * temp_right / (vol - b) - a / vol ** 2 - a / (27 * b ** 2)
    return max(solve(expr, vol))


def calc_min_press_for_temp_list(a, b, temp_left, min_vol, max_vol):
    """
    Посчитать нижнюю границу для p, в зависимости от нижней границы
    температуры temp_left и границ объема.
    (Для 1 моля вещества).
    """
    vol = symbols("vol", real=True)
    p = R * temp_left / (vol - b) - a / vol ** 2
    ivl = Interval(min_vol, max_vol)
    return minimum(p, vol, ivl)


def calc_max_press_for_temp_list(a, b, temp_right, min_vol, max_vol):
    """
    Посчитать верхнюю границу для p, в зависимости от верхней границы
    температуры temp_right и границ объема.
    (Для 1 моля вещества).
    """
    vol = symbols("vol", real=True)
    p = R * temp_right / (vol - b) - a / vol ** 2
    ivl = Interval(min_vol, max_vol)
    return maximum(p, vol, ivl)


def calc_borders_for_press(a, b, curr_temp, min_vol, max_vol):
    """
    Посчитать границы для p, при текущей температуре
    в зависимости от границ объема.
    (Для 1 моля вещества).
    """
    vol = symbols("vol", real=True)
    p = R * curr_temp / (vol - b) - a / (vol ** 2)
    ivl = Interval(min_vol, max_vol)
    borders = (minimum(p, vol, ivl), maximum(p, vol, ivl))
    return borders
