import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math

# -------------------- логика --------------------
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

    ax.plot(x, y, color="#a81010", linewidth=2, label="Парабола")
    ax.axhline(0, linewidth=1)
    ax.axvline(0, linewidth=1)

    ax.set_title(f"y = {a}x² + {b}x + {c}", fontsize=14)
    ax.set_ylim(-50, 100)
    ax.grid(True)

    # вершина
    xv = -b / (2 * a)
    yv = a * xv**2 + b * xv + c
    ax.plot(xv, yv, "bo", label="Вершина")
    ax.annotate(f"Вершина\n({xv:.2f}, {yv:.2f})", # подсказка текст вершины
                xy=(xv, yv),
                xytext=(xv, yv - 10),
                ha="center")

    # корни
    d = b**2 - 4*a*c
    if d >= 0:
        r1 = (-b + math.sqrt(d)) / (2*a)
        r2 = (-b - math.sqrt(d)) / (2*a)
        ax.plot([r1, r2], [0, 0], "ro", label="Корни")
        ax.annotate(f'X1={r1:.2f}', xy=(r1,0), xytext=(r1,5), fontsize=10, color='red') # подсказка текст корня X1
        ax.annotate(f'X2={r2:.2f}', xy=(r2,0), xytext=(r2,5), fontsize=10, color='red') # подсказка текст корня X2
    else:
        ax.text(0, 40, "Корней нет", ha="center", color="red")

    ax.legend()
    canvas.draw()


# ----------------- Сброс данных -------------
def reset_plot():
    entry_a.delete(0, tk.END)
    entry_b.delete(0, tk.END)
    entry_c.delete(0, tk.END)

    entry_a.insert(0, "1")
    entry_b.insert(0, "0")
    entry_c.insert(0, "0")

    update_plot()


# -------------------- UI --------------------
root = tk.Tk()
root.title("Парабола")
root.geometry("1100x600")

root.option_add("*Font", ("Segoe UI", 10))

# основная сетка
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

main = ttk.Frame(root, padding=10)
main.grid(sticky="nsew")

main.columnconfigure(1, weight=1)
main.rowconfigure(0, weight=1)

# -------- левая панель --------
left = ttk.LabelFrame(main, text="Коэффициенты", padding=10)
left.grid(row=0, column=0, sticky="ns")

ttk.Label(left, text="a").grid(row=0, column=0, sticky="w", pady=5)
ttk.Label(left, text="b").grid(row=1, column=0, sticky="w", pady=5)
ttk.Label(left, text="c").grid(row=2, column=0, sticky="w", pady=5)

entry_a = ttk.Entry(left, width=6, justify="center")
entry_b = ttk.Entry(left, width=6, justify="center")
entry_c = ttk.Entry(left, width=6, justify="center")

entry_a.grid(row=0, column=1, padx=5)
entry_b.grid(row=1, column=1, padx=5)
entry_c.grid(row=2, column=1, padx=5)

entry_a.insert(0, "1")
entry_b.insert(0, "0")
entry_c.insert(0, "0")

ttk.Button(left, text="Построить", command=update_plot)\
    .grid(row=3, column=0, columnspan=2, sticky="we", pady=(10, 5))

ttk.Button(left, text="Сбросить", command=reset_plot)\
    .grid(row=4, column=0, columnspan=2, sticky="we")

# -------- центр: график --------
center = ttk.Frame(main)
center.grid(row=0, column=1, sticky="nsew", padx=10)

plt.style.use("seaborn-v0_8-whitegrid")
fig, ax = plt.subplots(figsize=(10, 5)) # размер графики
fig.patch.set_facecolor("#f8f9fa")

canvas = FigureCanvasTkAgg(fig, master=center)
canvas.get_tk_widget().pack(fill="both", expand=True)

# -------- правая панель --------
right = ttk.LabelFrame(main, text="Справка", padding=10)
right.grid(row=0, column=2, sticky="ns")

text = tk.Text(
    right,
    width=35,
    height=18,
    wrap="word",
    bg="#f0f0f0",
    relief="flat"
)


text.insert(
    "1.0",
    "Парабола — график функции y = ax² + bx + c.\n\n"
    "• Вершина — минимум (a > 0) или максимум (a < 0)\n"
    "• a определяет направление ветвей\n"
    "• |a| влияет на ширину\n"
    "• b сдвигает влево / вправо\n"
    "• c — пересечение с осью Y\n"
    "• Ось симметрии: x = -b / (2a)"
)

text.config(state="disabled")
text.pack()

# первичная отрисовка
update_plot()
root.mainloop()
