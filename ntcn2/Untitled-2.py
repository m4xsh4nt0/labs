
import numpy as np
import sympy as sp
from scipy import integrate
import matplotlib.pyplot as plt

# Для красивых математических выражений в выводе

print("="*70)
print("ВАРИАНТ 2. РЕШЕНИЕ ВСЕХ ЗАДАНИЙ")
print("="*70)

# %% ЗАДАНИЕ 1
print("\n" + "="*50)
print("ЗАДАНИЕ 1: Матрица 5x5 случайных чисел (0,2), транспонирование, определитель")
print("="*50)

# Создаем матрицу 5x5 случайных вещественных чисел в интервале (0, 2)
matrix_1 = np.random.uniform(0, 2, (5, 5))
print("Исходная матрица:")
print(matrix_1)

# Транспонируем
matrix_1_transposed = matrix_1.T
print("\nТранспонированная матрица:")
print(matrix_1_transposed)

# Вычисляем определитель
det_1 = np.linalg.det(matrix_1_transposed)
print(f"\nОпределитель транспонированной матрицы: {det_1:.6f}")

# %% ЗАДАНИЕ 2
print("\n" + "="*50)
print("ЗАДАНИЕ 2: Умножение матрицы на вектор-столбец")
print("="*50)

# Создаем матрицу 3x3 и вектор-столбец 3x1
A_2 = np.array([[1, 2, 3],
                [4, 5, 6],
                [7, 8, 10]])  # Используем невырожденную матрицу
b_2 = np.array([[2], [1], [3]])  # Вектор-столбец

print("Матрица A:")
print(A_2)
print("\nВектор-столбец b:")
print(b_2)

# Умножение матриц
result_2 = np.dot(A_2, b_2)  # или A_2 @ b_2
print("\nРезультат умножения A * b:")
print(result_2)

# Проверка размерностей
print(f"\nРазмерности: A {A_2.shape}, b {b_2.shape}, результат {result_2.shape}")

# %% ЗАДАНИЕ 3
print("\n" + "="*50)
print("ЗАДАНИЕ 3: Упрощение выражения и вычисление значения с SymPy")
print("="*50)

# Определяем символы
a, b = sp.symbols('a b')

# Исходное выражение
expr = (28*a/b) * (a + b) + (2*a - 7*b)**2
print("Исходное выражение:")
print(expr)

# Упрощаем
expr_simplified = sp.factor(sp.simplify(sp.together(expr)))
print("\nУпрощенное выражение:")
print(expr_simplified)

# Подставляем значения a = sqrt(3), b = -3.42
a_val = sp.sqrt(3)
b_val = -3.42
expr_value = expr_simplified.subs({a: a_val, b: b_val})

print(f"\nЗначение выражения при a = √3, b = {b_val}:")
print(f"Точное значение: {expr_value}")
print(f"Численное значение: {float(expr_value):.6f}")

# %% ЗАДАНИЕ 4
print("\n" + "="*50)
print("ЗАДАНИЕ 4: Частные производные выражения из задания 3")
print("="*50)

# Выражение из предыдущего задания
expr_4 = (28*a/b) * (a + b) + (2*a - 7*b)**2

# Частные производные
derivative_a = sp.diff(expr_4, a)
derivative_b = sp.diff(expr_4, b)

print("Частная производная по a:")
sp.pprint(derivative_a)

print("\nЧастная производная по b:")
sp.pprint(derivative_b)

# Упрощенные версии
print("\nУпрощенная частная производная по a:")
sp.pprint(sp.simplify(derivative_a))

print("\nУпрощенная частная производная по b:")
sp.pprint(sp.simplify(derivative_b))

# %% ЗАДАНИЕ 5
print("\n" + "="*50)
print("ЗАДАНИЕ 5: Собственные векторы и собственные значения матрицы")
print("="*50)

A_5 = np.array([[0, -3, -1],
                [3, 8, 2],
                [-7, -15, -3]])

print("Матрица A:")
print(A_5)

# Вычисляем собственные значения и векторы
eigenvalues, eigenvectors = np.linalg.eig(A_5)

print("\nСобственные значения:")
for i, val in enumerate(eigenvalues):
    print(f"λ{i+1} = {val:.6f}")

print("\nСобственные векторы (каждый столбец соответствует собственному значению):")
print(eigenvectors)

# %% ЗАДАНИЕ 6
print("\n" + "="*50)
print("ЗАДАНИЕ 6: Интеграл ∫ dx/√(1+x²) от 0 до 4 (SciPy и SymPy)")
print("="*50)

# Способ 1: SciPy
def integrand_6(x):
    return 1 / np.sqrt(1 + x**2)

result_scipy_6, error_scipy_6 = integrate.quad(integrand_6, 0, 4)
print("Метод SciPy (quad):")
print(f"Значение интеграла: {result_scipy_6:.10f}")

# Способ 2: SymPy
x = sp.Symbol('x')
integrand_sympy_6 = 1 / sp.sqrt(1 + x**2)
result_sympy_6 = sp.integrate(integrand_sympy_6, (x, 0, 4))

print("\nМетод SymPy:")
print(f"Значение интеграла: {float(result_sympy_6):.10f}")

# %% ЗАДАНИЕ 7
print("\n" + "="*50)
print("ЗАДАНИЕ 7: Двойной интеграл ∫∫ cos(x+y) dy dx от 0 до π/2 и от 0 до x")
print("="*50)

# Способ 1: SciPy (двойной интеграл)
def integrand_7(y, x):
    return np.cos(x + y)

# Для dblquad порядок аргументов: функция f(y, x), затем пределы для x и y
result_scipy_7, error_scipy_7 = integrate.dblquad(integrand_7, 0, np.pi/2, lambda x: 0, lambda x: x)# lambda это функции без имени
print("Метод SciPy (dblquad):")
print(f"Значение интеграла: {result_scipy_7:.10f}")

# Способ 2: SymPy
x, y = sp.symbols('x y')
integrand_sympy_7 = sp.cos(x + y)
# Сначала интегрируем по y от 0 до x, затем по x от 0 до π/2
inner_integral = sp.integrate(integrand_sympy_7, (y, 0, x))
result_sympy_7 = sp.integrate(inner_integral, (x, 0, sp.pi/2))

print("\nМетод SymPy:")
print(f"Численное значение: {float(result_sympy_7):.10f}")

# %% ЗАДАНИЕ 8
print("\n" + "="*50)
print("ЗАДАНИЕ 8: Построение графиков y = ln(x+5) и y = 3x-2")
print("="*50)

# Определяем функции
def f1(x):
    return np.log(x + 5)  # ln(x+5) в Python - это np.log

def f2(x):
    return 3*x - 2

# Создаем массив x
x_vals = np.linspace(-4.9, 5, 1000)  # Начинаем чуть больше -5, чтобы избежать ln(0)

# Вычисляем y
y1_vals = f1(x_vals)
y2_vals = f2(x_vals)

# Находим точку пересечения (решаем уравнение ln(x+5) = 3x-2)
# Это трансцендентное уравнение, решаем численно
from scipy.optimize import fsolve

def equation(x):
    return np.log(x + 5) - (3*x - 2)

# Начальное приближение - графически видно, что пересечение где-то около 0
x_intersect = fsolve(equation, 0)[0]
y_intersect = f1(x_intersect)

print(f"Точка пересечения: x = {x_intersect:.6f}, y = {y_intersect:.6f}")

# Построение графика
plt.figure(figsize=(12, 8))

# Графики функций
plt.plot(x_vals, y1_vals, 'b-', linewidth=2, label='y = ln(x+5)')
plt.plot(x_vals, y2_vals, 'r-', linewidth=2, label='y = 3x-2')

# Точка пересечения
plt.plot(x_intersect, y_intersect, 'o', color='orange', markersize=10, 
         label=f'Точка пересечения ({x_intersect:.3f}, {y_intersect:.3f})')

# Оформление графика
plt.xlabel('Ось X', fontsize=12)
plt.ylabel('Ось Y', fontsize=12)
plt.title('Графики функций y = ln(x+5) и y = 3x-2', fontsize=14)
plt.grid(True, alpha=0.3)
plt.legend(fontsize=12)

# Добавляем горизонтальную и вертикальную линии через 0
plt.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
plt.axvline(x=0, color='k', linestyle='-', linewidth=0.5)

# Устанавливаем пределы для лучшего обзора
plt.xlim(-5, 5)
plt.ylim(-10, 15)

plt.show()

print("\n" + "="*70)
print("ВСЕ ЗАДАНИЯ ВЫПОЛНЕНЫ УСПЕШНО!")
print("="*70)