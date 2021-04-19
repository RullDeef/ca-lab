from typing import Callable as func
from math import exp, sin, cos, pi

from numpy import linspace
from matplotlib import pyplot as plt

from gauss import gauss_integrate
from simpson import simpson_integrate


def composite_integrate(f: func, a1: float, b1: float, a2: float, b2: float,
                        method_1: func, method_2: func, n1: int,
                        n2: int) -> float:
    F = lambda y: method_1(lambda x: f(x, y), a1, b1, n1)
    return method_2(F, a2, b2, n2)


def function_integrator(f: func, a: float, b: float, c: float, d: float,
                        n: int, m: int) -> float:
    return composite_integrate(f, a, b, c, d, gauss_integrate,
                               simpson_integrate, n, m)


def function(t: float, n: int, m: int) -> float:
    L_R = lambda theta, phi: 2 * cos(theta) / (1 - sin(theta)**2 * cos(phi)**2)
    f = lambda theta, phi: (1 - exp(-t * L_R(theta, phi))) * cos(theta) * sin(
        theta)

    return 4 / pi * function_integrator(f, 0, pi / 2, 0, pi / 2, n, m)
