import math


third = 1.0 / 3.0
two_thirds = 2.0 / 3.0
pi_div_3 = third * math.pi
tau = math.pi * 2


def wrap_unit(x):
    mod = math.fmod(x, 1)

    return mod if mod >= 0 else 1 - mod


def clip(x, a=0, b=1):
    return min(max(x, a), b)


def interpolate(a, b, x):
    return a + (b - a) * x
