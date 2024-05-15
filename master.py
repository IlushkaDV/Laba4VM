# Made by IlushkaDV
from math import factorial, log
import pandas as pd
from tabulate import tabulate

def custom_function(x):
    return x ** 2 + log(x) - 4

def custom_function_derivative(x, k):
    if k == 1:
        return 2 * x + 1 / x
    elif k == 2:
        return 2 - 1 / x ** 2
    return (-1) ** ((k % 2) + 1) * factorial(k - 1) / x ** k

def middle_rectangle_method(func, a, b, n):
    h = (b - a) / n
    return sum(func(a + h * (i + 0.5)) * h for i in range(n))

def middle_rectangle_error(func, a, b, n):
    m = max(abs(custom_function_derivative(a + (b - a) * i / 1000, 2))
            for i in range(1001))
    return m / 24 * (b - a) ** 3 / n ** 2

def left_rectangle_method(func, a, b, n):
    h = (b - a) / n
    return sum(func(a + h * i) * h for i in range(n))

def right_rectangle_method(func, a, b, n):
    h = (b - a) / n
    return sum(func(a + h * i) for i in range(1, n + 1)) * h

def trapezoidal_method(func, a, b, n):
    h = (b - a) / n
    return ((func(a) + func(b)) / 2 + sum(func(a + h * i) for i in range(1, n))) * h

def simpson_method(func, a, b, n):
    h = (b - a) / n
    return sum(func(a + h * (i - 1)) + 4 * func(a + h * (i - 0.5)) + func(a + h * (i))
               for i in range(1, n + 1)) * h / 6

def left_rectangle_error(func, a, b, n):
    m = max(abs(custom_function_derivative(a + (b - a) * i / 1000, 1)) for i in range(1001))
    return m * (b - a) / 2

def right_rectangle_error(func, a, b, n):
    m = max(abs(custom_function_derivative(a + (b - a) * i / 1000, 1)) for i in range(1001))
    return m * (b - a) / 2

def trapezoidal_error(func, a, b, n):
    m = max(abs(custom_function_derivative(a + (b - a) * i / 1000, 2)) for i in range(1001))
    return m / 12 * (b - a) ** 3 / n ** 2

def simpson_error(func, a, b, n):
    m = max(abs(custom_function_derivative(a + (b - a) * i / 1000, 4)) for i in range(1001))
    return m / 2880 * (b - a) ** 5 / n ** 4

a, b = 1.5, 2
n = 1
exact_integral = -0.180236634376

result = {'j': [], 'n': [], 'I_n': [], 'delta_I_n': [], 'relative_I_n': [],
          'R_n': [], 'growth': [0]}
for i in range(15):
    n *= 2
    I_n = middle_rectangle_method(custom_function, a, b, n)
    result['j'].append(i + 1)
    result['n'].append(n)
    result['I_n'].append(I_n)
    result['delta_I_n'].append(abs(exact_integral - I_n))
    result['relative_I_n'].append(result['delta_I_n'][i] / abs(exact_integral) * 100)
    result['R_n'].append(middle_rectangle_error(custom_function, a, b, n))
    if i > 0:
        result['growth'].append(result['delta_I_n'][i] / result['delta_I_n'][i - 1])

df_middle_rect = pd.DataFrame({
    'Iteration': result['j'],
    'n': result['n'],
    'I_n': result['I_n'],
    'delta_I_n': result['delta_I_n'],
    'Relative Error (%)': result['relative_I_n'],
    'R_n': result['R_n'],
    'Growth': result['growth']
})

print("Table of values for the middle rectangle method:")
print(df_middle_rect)

calculation_results = {'method': ['Left Rectangular', "Right Rectangular",
                                  "Middle Rectangular", "Trapezoidal", "Simpson's"],
                       'I_n': [], 'delta_I_n': [], 'relative_I_n': [], 'R_n': []}
for i, (formula, error) in enumerate([(left_rectangle_method, left_rectangle_error),
                                      (right_rectangle_method, right_rectangle_error),
                                      (middle_rectangle_method, middle_rectangle_error),
                                      (trapezoidal_method, trapezoidal_error),
                                      (simpson_method, simpson_error)]):
    calculation_results['I_n'].append(formula(custom_function, a, b, 10000))
    calculation_results['delta_I_n'].append(abs(exact_integral - calculation_results['I_n'][i]))
    calculation_results['relative_I_n'].append(calculation_results['delta_I_n'][i] / abs(exact_integral) * 100)
    calculation_results['R_n'].append(error(custom_function, a, b, 10000))

table_headers = ['Method', 'I_n', 'delta_I_n', 'relative_I_n', 'R_n']
table_data = [["Left Rectangular", calculation_results['I_n'][0], calculation_results['delta_I_n'][0],
               calculation_results['relative_I_n'][0], calculation_results['R_n'][0]],
              ["Right Rectangular", calculation_results['I_n'][1], calculation_results['delta_I_n'][1],
               calculation_results['relative_I_n'][1], calculation_results['R_n'][1]],
              ["Middle Rectangular", calculation_results['I_n'][2], calculation_results['delta_I_n'][2],
               calculation_results['relative_I_n'][2], calculation_results['R_n'][2]],
              ["Trapezoidal", calculation_results['I_n'][3], calculation_results['delta_I_n'][3],
               calculation_results['relative_I_n'][3], calculation_results['R_n'][3]],
              ["Simpson's", calculation_results['I_n'][4], calculation_results['delta_I_n'][4],
               calculation_results['relative_I_n'][4], calculation_results['R_n'][4]]]

print(tabulate(table_data, headers=table_headers, tablefmt='grid'))

