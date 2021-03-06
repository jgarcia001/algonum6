import sys
sys.path.append("../")

import numpy as np
import matplotlib.pyplot as plt

import methodes as m

#---------------------------------------------------------------------
#Constantes utilisees lors des tests

N = 300
h = 0.1

g = 9.81
length = 0.5
theta_init = 10.0

#---------------------------------------------------------------------
#Fonctions implementees pour le pendule a un maillon

#Retourne sous la forme d'une lambda-expression un tableau contenant:
# -les vitesses du solide
# -les accélérations du solide
def f_function():

    return (lambda x,t: np.array([x[1], ((g/length) * -(np.sin(x[0])))]))

#Retourne les solutions de l'équation du mouvement en fonction
# des conditions initiales (y_zero)
def pendulum_position_function(y_zero):

    f = f_function()
    return m.meth_n_step(y_zero, 0, N, h, f, m.step_runge_kutta_4)


def find_zero_x(y0, y1, i):
    return (-y0/(y1 - y0 )) + i

#Retourne la periode d'un systeme
def find_period(y_array, theta):
    start_periods = -1
    end_periods = -1
    half_period = 0

    n = y_array.size
    i = 1
    while (start_periods == -1) and i < n:
        if((y_array[i] * y_array[i - 1]) < 0):
            start_periods = find_zero_x(y_array[i - 1], y_array[i] ,i)
        i = i + 1

    if (start_periods == -1):
        return -1

    while i < n:
        if((y_array[i] * y_array[i - 1]) < 0):
            half_period = half_period + 1
            end_periods = find_zero_x(y_array[i - 1], y_array[i], i)
            print(i - 1)
            print(end_periods)
            print(i)
            print("       ")
        i = i + 1

    if (half_period == 0):
        return -1

    period_time = ((end_periods - start_periods)*h) / (half_period/2)

    return period_time

#---------------------------------------------------------------------
#Tests realises pour tester les fonctions precedentes

y_zero = np.empty(2)
y_array = np.empty(N)
number_angle = 89
frequency = np.empty(number_angle)
for j in range (0, number_angle, 1):
    y_zero[0] = np.radians(j + 1)
    y_zero[1] = 0

    y_array[0] = y_zero[0]
    y = pendulum_position_function(y_zero)
    for i in range (1, N):
        y_array[i] = np.degrees(y[i][0])

    period = find_period(y_array, j + 1)
    frequency[j] = 1/period

times = np.arange(0, number_angle, 1)
plt.plot(times, frequency)
frequency_little_angle = (np.sqrt(g/length)/(np.pi*2))
print(1/frequency_little_angle)
plt.plot(times, np.full((number_angle),frequency_little_angle))
plt.show()
