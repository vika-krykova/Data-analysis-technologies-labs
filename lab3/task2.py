import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import numpy as np
from scipy.linalg import solve
import matplotlib.pyplot as plt

data = np.genfromtxt('data2.csv', delimiter=';', encoding='utf-8-sig')
print("Форма data2:", data.shape)
discounts = data[:, 0]
profits = data[:, 1]

sample_indices_2 = [0, len(discounts) // 2, len(discounts) - 1]
sample_x_2 = discounts[sample_indices_2]
sample_y_2 = profits[sample_indices_2]

design_matrix_2 = np.vander(sample_x_2, 3)
coefficients_2 = solve(design_matrix_2, sample_y_2)
fitted_profits_2 = np.polyval(coefficients_2, discounts)
rss_2 = np.sum((profits - fitted_profits_2) ** 2)

plt.figure(figsize=(9, 5))
plt.scatter(discounts, profits, color='blue', label='Исходные данные')
plt.plot(discounts, fitted_profits_2, 'r-', linewidth=2, label='Полином 2 степени')
plt.xlabel('Скидка, %')
plt.ylabel('Прибыль')
plt.title('Аппроксимация полиномом 2 степени')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('polynomial_2.png', dpi=150, bbox_inches='tight')
plt.show()

sample_indices_3 = [0, len(discounts) // 3, 2 * len(discounts) // 3, len(discounts) - 1]
sample_x_3 = discounts[sample_indices_3]
sample_y_3 = profits[sample_indices_3]

design_matrix_3 = np.vander(sample_x_3, 4)
coefficients_3 = solve(design_matrix_3, sample_y_3)
fitted_profits_3 = np.polyval(coefficients_3, discounts)
rss_3 = np.sum((profits - fitted_profits_3) ** 2)

plt.figure(figsize=(9, 5))
plt.scatter(discounts, profits, color='blue', label='Исходные данные')
plt.plot(discounts, fitted_profits_3, 'g-', linewidth=2, label='Полином 3 степени')
plt.xlabel('Скидка, %')
plt.ylabel('Прибыль')
plt.title('Аппроксимация полиномом 3 степени')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('polynomial_3.png', dpi=150, bbox_inches='tight')
plt.show()

if rss_2 < rss_3:
    best_coefficients = coefficients_2
    best_degree = 2
    best_rss = rss_2
else:
    best_coefficients = coefficients_3
    best_degree = 3
    best_rss = rss_3

print(f"\nRSS (2 степень) = {rss_2:.6f}")
print(f"RSS (3 степень) = {rss_3:.6f}")
print(f"\nЛучшая модель: полином {best_degree} степени (RSS = {best_rss:.6f})")
print(f"\nПрогноз прибыли при скидке 6%: {np.polyval(best_coefficients, 6):.4f}")
print(f"Прогноз прибыли при скидке 8%: {np.polyval(best_coefficients, 8):.4f}")