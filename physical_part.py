import math
from sympy import *

# Все параметры измеряются в единицах измерения Си, кроме параметров а и b
# a - характеризует силу притяжения молекул, измеряется в Дж * м^3 / моль
# b - характеризует размер молекул, измеряется в 10^(-6) м^3 / моль
# Эти параметры в таких единицах даются в справочниках, это стандарт

def energy_change(temp, vol, press, a, b, mole, freedoms = 3):
    b = b / 1000000
    U_0 = mole * freedoms * 8.31 * temp[0] / 2 - mole * mole * a / vol[0]
    U_1 = mole * freedoms * 8.31 * temp[1] / 2 - mole * mole * a / vol[1]
    return U_1 - U_0


def work_change(temp, vol, press, a, b, mole, freedoms = 3):
    b = b / 1000000
    if temp[0] == temp[1]:
        answer =  mole * 8.31 * temp[0] * math.log((vol[1] - mole * b) / (vol[0] - mole * b))
        return answer - mole * mole * a * (1 / vol[0] - 1 / vol[1])
    step_vol = (vol[1] - vol[0]) / 10**5
    step_temp = (temp[1] - temp[0]) / 10**5
    answer = 0
    for i in range(10**5):
        curr_vol = vol[0] + (i - 0.5) * step_vol
        curr_temp = temp[0] + (i - 0.5) * step_temp
        curr_press = mole * 8.31 * curr_temp / (curr_vol - mole * b) - a * mole * mole / (curr_vol ** 2)
        answer += step_vol * curr_press
    return answer


def warmth_change(temp, vol, press, a, b, mole, freedoms = 3):
    b = b / 1000000
    if temp[0] == temp[1]:
        return mole * 8.31 * temp[0] * math.log((vol[1] - mole * b) / (vol[0] - mole * b))
    answer =  energy_change(temp, vol, press, a, b * 1000000, mole, freedoms)
    return answer + work_change(temp, vol, press, a, b * 1000000, mole, freedoms)

def entropy_change(temp, vol, press, a, b, mole, freedoms = 3):
    b = b / 1000000
    return freedoms / 2 * 8.31 * math.log(temp[1] / (temp[0] + 0.00001)) + 8.31 * math.log((vol[1] - b) / (vol[0] - b))

def press(temp, vol, a, b, mole):
    b = b / 1000000
    return mole * 8.31 * temp / (vol - mole * b) - a * mole * mole / (vol ** 2)

def volume(temp, press, a, b, mole):
    b = b / 1000000
    x = symbols('x', real = True)
    expr = press * x ** 3 - (press * mole * b + mole * 8.31 * temp) * x ** 2 + mole ** 2 * a * x - mole ** 3 * a * b
    return max(solve(expr, x))

def temperature(press, vol, a, b, mole):
    b = b / 1000000
    return (press + mole ** 2 * a / (vol ** 2)) * (vol - mole * b) / (mole * 8.31)

# Приемлемые значения давления - несколько атмосфер (1 атм = 10^5 Па), объёма - десятые, сотые, десятки кубических метров
# температуры - 250 - 310 К

def min_press():
    return 100

def max_press():
    return 10000000

def min_vol():
    return 10**(-8)

def max_vol():
    return 10**4

def min_temp():
    return 220

def max_temp():
    return 500

def min_a():
    return 0

def max_a():
    return 1.5

def min_b():
    return 1

def max_b():
    return 110

def default_mole():
    return 1

def a_b_for_He():
    return (0.00346, 23.8)

def a_b_for_Ar():
    return (0.1355, 32)

def a_b_for_Ne():
    return (0.0208, 16.7)

def a_b_for_N_2():
    return (0.137, 38.7)

def a_b_for_H_2_O():
    return (0.5537, 30.5)

def a_b_for_O_2():
    return (0.1382, 31.9)

def a_b_for_HCN():
    return (1.129, 88.1)
