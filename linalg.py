def vec2_neg(v):
    return -v[0], -v[1]


def vec2_add(v1, v2):
    return v1[0] + v2[0], v1[1] + v2[1]


def vec2_add3(v1, v2, v3):
    return v1[0] + v2[0] + v3[0], v1[1] + v2[1] + v3[1]


def vec2_sub(v1, v2):
    return v1[0] - v2[0], v1[1] - v2[1]


def vec2_mul(v1, v2):
    return v1[0] * v2[0], v1[1] * v2[1]


def vec2_div(v1, v2):
    return v1[0] / v2[0], v1[1] / v2[1]


def vec2_muls(v, x):
    return v[0] * x, v[1] * x


def vec2_divs(v, x):
    return v[0] / x, v[1] / x


def vec2_rotate(v, sn, cs):
    return v[0] * cs - v[1] * sn, v[0] * sn + v[1] * cs
