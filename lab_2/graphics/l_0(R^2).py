import numpy as np
import matplotlib.pyplot as plt

# Обновленные данные
R_squared = np.array([0.007225, 0.013225, 0.021025, 0.030625, 0.042025, 0.055225])  # R^2
I = np.array([0.03144282, 0.05014466, 0.06431077, 0.07958544, 0.10787481, 0.050145])  # I

# Строим график
plt.figure(figsize=(8, 6))
plt.plot(R_squared, I, marker='o', linestyle='-', color='b', label=r'$I_0$ vs $R^2$')

# Настроим график
plt.title(r'Зависимость $I_0$ от $R^2$', fontsize=14)
plt.xlabel(r'$R^2 \, (\text{м}^2)$', fontsize=12)
plt.ylabel(r'$I_0 \, (\text{кг} \cdot \text{м}^2)$', fontsize=12)
plt.grid(True)
plt.legend()

# Показать график
plt.tight_layout()
plt.show()