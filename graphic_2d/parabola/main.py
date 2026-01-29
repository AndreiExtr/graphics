import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math

# функция обновления графика
def update_plot():
    try:
        a = float(entry_a.get())
        b = float(entry_b.get())
        c = float(entry_c.get())
    except ValueError:
        return

    x = np.linspace(-20, 20, 400)
    y = a * x**2 + b * x + c

    ax.clear()
    ax.plot(x, y, color="#a81010", label="Парабола")
    ax.axhline(0)
    ax.axvline(0)
    ax.set_title(f"y = {a}x² + {b}x + {c}", fontsize=14)
    ax.grid()
    ax.set_ylim(-50, 100) # ограничение по оси Y от -50 до 100

    # --- Вершина ---
    x_vertex = -b / (2 * a)
    y_vertex = a * x_vertex**2 + b * x_vertex + c
    ax.plot(x_vertex, y_vertex, 'bo', label="Вершина")
    ax.annotate(f'({x_vertex:.2f}, {y_vertex:.2f})',
                xy=(x_vertex, y_vertex),
                xytext=(x_vertex, y_vertex - 8),
                fontsize=10 , ha='center')

    # --- Корни (пересечение с X) ---
    discriminant = b**2 - 4*a*c
    if discriminant >= 0:
        root1 = (-b + math.sqrt(discriminant)) / (2*a)
        root2 = (-b - math.sqrt(discriminant)) / (2*a)
        ax.plot([root1, root2], [0, 0], 'ro', label="Корни")
        ax.annotate(f'{root1:.2f}', xy=(root1,0), xytext=(root1,5), fontsize=10, color='red')
        ax.annotate(f'{root2:.2f}', xy=(root2,0), xytext=(root2,5), fontsize=10, color='red')
    else:
        ax.text(0, 50, "Корней нет", color='red', fontsize=12, ha='center')

    ax.legend()
    canvas.draw()

# сброс значений
def reset_plot():
    entry_a.delete(0, tk.END)
    entry_b.delete(0, tk.END)
    entry_c.delete(0, tk.END)
    entry_a.insert(0, "1")
    entry_b.insert(0, "0")
    entry_c.insert(0, "0")
    update_plot()

# окно приложения
root = tk.Tk()
root.title("График параболы с вершиной и корнями")

# сетка 6x6
for i in range(6):
    root.grid_rowconfigure(i, weight=1, minsize=50)
for j in range(6):
    root.grid_columnconfigure(j, weight=1, minsize=80)

# левая часть: метки и поля ввода
tk.Label(root, text="Переменная a:", font=("Arial", 12)).grid(row=0, column=0, sticky="e", padx=5, pady=5)
tk.Label(root, text="Переменная b:", font=("Arial", 12)).grid(row=1, column=0, sticky="e", padx=5, pady=5)
tk.Label(root, text="Переменная c:", font=("Arial", 12)).grid(row=2, column=0, sticky="e", padx=5, pady=5)

entry_a = tk.Entry(root, font=("Arial", 12))
entry_b = tk.Entry(root, font=("Arial", 12))
entry_c = tk.Entry(root, font=("Arial", 12))

entry_a.insert(0, "1")
entry_b.insert(0, "0")
entry_c.insert(0, "0")

entry_a.grid(row=0, column=1, sticky="we", padx=5, pady=5)
entry_b.grid(row=1, column=1, sticky="we", padx=5, pady=5)
entry_c.grid(row=2, column=1, sticky="we", padx=5, pady=5)

# кнопки
tk.Button(root, text="Построить", fg='white', bg="#090F46", font=("Arial", 11, "bold"), command=update_plot)\
    .grid(row=3, column=0, columnspan=1, sticky="we", padx=5, pady=5)
tk.Button(root, text="Сбросить", fg='white', bg="#46090E", font=("Arial", 11, "bold"), command=reset_plot)\
    .grid(row=3, column=1, columnspan=1, sticky="we", padx=5, pady=5)

# правая часть: текст с определением параболы
parabola_text = (
    "Парабола — график квадратичной функции y = ax² + bx + c.\n"
    "Свойства параболы:\n"
    "1. Вершина — минимум (a>0) или максимум (a<0).\n"
    "2. Направление ветвей определяется a.\n"
    "3. Ширина и крутизна зависят от |a|.\n"
    "4. Горизонтальное смещение — b.\n"
    "5. Вертикальное смещение — c.\n"
    "6. Ось симметрии: x = -b/(2a).\n"
    "7. Пересечение с осью Y: (0, c)."
)
tk.Label(root, text=parabola_text, justify="left", font=("Arial", 11), bg="white", relief="solid", padx=10, pady=10)\
    .grid(row=0, column=4, rowspan=6, sticky="n", padx=5, pady=5)

# график в центре
plt.style.use('seaborn-v0_8-whitegrid')
fig, ax = plt.subplots(figsize=(8, 6))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=0, column=2, rowspan=6, columnspan=2, sticky="nsew", padx=5, pady=5)

# первичная отрисовка
update_plot()
root.mainloop()
