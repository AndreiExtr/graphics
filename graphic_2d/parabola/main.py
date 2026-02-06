import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math
from tkinter import filedialog


# -------------------- ИГРА --------------------

levels = [
    {
        "name": "Уровень 1: Попади в точку",
        "targets": [(2, 6)],
        "tolerance": 0.3
    },
    {
        "name": "Уровень 2: Две цели",
        "targets": [(-3, 5), (3, 5)],
        "tolerance": 0.3
    },
    {
        "name": "Уровень 3: Высокая цель",
        "targets": [(0, 8)],
        "tolerance": 0.3
    },
    {
        "name": "Уровень 4: Три вершины",
        "targets": [(0, -4),(-2, 6),(2, 6)],
        "tolerance": 0.3
    }
]
game_active = False
current_level = 0
# -------------------- ИГРА --------------------


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

    # ui параболы
    ax.plot(x, y, color="#a81010", linewidth=2, label="Парабола") # линия параболы
    ax.axhline(0, linewidth=1) # ось x
    ax.axvline(0, linewidth=1) # ось y

    # подписи осей
    ax.set_xlabel("x")
    ax.set_ylabel("y")

    # ui текста функции
    ax.set_title(f"y = {a}x² + {b}x + {c}", fontsize=14, pad=20)
    ax.set_ylim(-50, 100)
    ax.grid(True)

        # -------------------- ИГРА --------------------
        # ---------- цели уровня ----------
    if game_active:
        level = levels[current_level]
        for tx, ty in level["targets"]:
            ax.plot(tx, ty, "ro", markersize=10)
            ax.annotate("Цель", (tx, ty), xytext=(tx+0.5, ty+0.5))

    # -------------------- ИГРА --------------------


    # вершина
    xv = -b / (2 * a)
    yv = a * xv**2 + b * xv + c
    ax.plot(xv, yv, "bo", label="Вершина") # легенда
    ax.annotate(f"Вершина\n({xv:.2f}, {yv:.2f})", # подсказка текст вершины
                xy=(xv, yv),
                xytext=(xv, yv - 10),
                ha="center")

    # корни
    d = b**2 - 4*a*c
    if d >= 0:
        r1 = (-b + math.sqrt(d)) / (2*a)
        r2 = (-b - math.sqrt(d)) / (2*a)
        ax.plot([r1, r2], [0, 0], "go", label="Корни")
        ax.annotate(f'X1 = {r1:.2f}', xy=(r1,0), xytext=(r1,5), fontsize=10, color="#039C0F") # подсказка текст корня X1
        ax.annotate(f'X2 = {r2:.2f}', xy=(r2,0), xytext=(r2,5), fontsize=10, color="#039C0F") # подсказка текст корня X2
    else:
        ax.text(0, 40, "Корней нет", ha="center", color="red")

    # ---- Интервалы возрастания/убывания ----
    x_min, x_max = ax.get_xlim()
    if a > 0:
        # убывает слева, возрастает справа
        ax.axvspan(x_min, xv, color='red', alpha=0.1, label="Убывает")
        ax.axvspan(xv, x_max, color='green', alpha=0.1, label="Возрастает")
    else:
        # возрастает слева, убывает справа
        ax.axvspan(x_min, xv, color='green', alpha=0.1, label="Возрастает")
        ax.axvspan(xv, x_max, color='red', alpha=0.1, label="Убывает")

    #ax.legend() # обозначения на графике (по умолчанию справа сверху)

    # -------------------- ИГРА --------------------
    if game_active and check_win(x, y):
        ax.text(0.5, 0.9,
                f"{levels[current_level]['name']} пройден!",
                transform=ax.transAxes,
                fontsize=16,
                color="green",
                ha="center")
    # -------------------- ИГРА --------------------


    canvas.draw()


def check_win(x, y):
    level = levels[current_level]
    tol = level["tolerance"]

    for tx, ty in level["targets"]:
        # минимальное расстояние от параболы до цели
        dist = np.min(np.sqrt((x - tx)**2 + (y - ty)**2))
        if dist > tol:
            return False
    return True


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

main = ttk.Frame(root, padding=10) # отступ по краям основного интерфейса
main.grid(sticky="nsew")

main.columnconfigure(1, weight=1)
main.rowconfigure(0, weight=1)


# -------- левая панель --------
# родительский фрейм для двух блоков
left_frame = ttk.Frame(main)
left_frame.grid(row=0, column=0, rowspan=1, sticky="ns")  # весь правый столбец


# Блок 1: Коэффициенты
left = ttk.LabelFrame(left_frame, text="Коэффициенты", padding=10)
left.pack(fill="both", expand=True, pady=(5,0))

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

# кнопки
ttk.Button(left, text="Построить", command=update_plot)\
    .grid(row=3, column=0, columnspan=2, sticky="we", pady=(10, 5))

ttk.Button(left, text="Сбросить", command=reset_plot)\
    .grid(row=4, column=0, columnspan=2, sticky="we")

# сохранение графики
def save_plot_dialog():
    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG файл", "*.png"), ("PDF файл", "*.pdf"), ("SVG файл", "*.svg")],
        title="Сохранить график"
    )
    if file_path:
        fig.savefig(file_path, dpi=300)
        print(f"График сохранён в {file_path}")

ttk.Button(left, text="Сохранить", command=save_plot_dialog).grid(row=5, column=0, columnspan=2, sticky="we", pady=(5,0))


# Блок 2: Игра
left_game = ttk.LabelFrame(left_frame, text="Игра", padding=10)
left_game.pack(fill="both", expand=True, pady=(5,0))


left_game_text = tk.Text(
    left_game,
    width=35,
    height=10,
    wrap="word",
    bg="#f0f0f0",
    relief="flat"
)
left_game_text.insert("1.0",
    "С помощью одной параболы попадать\n"
    "в заданные точки (цели) и проходить\n"
    "уровни возрастающей сложности.\n"
)

left_game_text.config(state="disabled")
left_game_text.pack(fill="both", expand=True)

def start_game():
    global game_active, current_level
    game_active = True
    current_level = 0
    reset_plot()

def next_level():
    global current_level, game_active
    if not game_active:
        return

    if current_level < len(levels) - 1:
        current_level += 1
        reset_plot()
    else:
        game_active = False
        ax.text(0.5, 0.9, "ИГРА ПРОЙДЕНА!",
                transform=ax.transAxes,
                fontsize=18,
                color="blue",
                ha="center")
        canvas.draw()

def end_game():
    global game_active, current_level
    game_active = False
    reset_plot()


ttk.Button(left_game, text="Начать игру", command=start_game)\
    .pack(fill="x", pady=(0,5))


ttk.Button(left_game, text="Следующий уровень", command=next_level)\
    .pack(fill="x", pady=(0,5))

ttk.Button(left_game, text="Закончить игру", command=end_game)\
    .pack(fill="x")


# -------- центр: график --------
center = ttk.Frame(main)
center.grid(row=0, column=1, sticky="nsew", padx=10)

plt.style.use("seaborn-v0_8-whitegrid")
fig, ax = plt.subplots(figsize=(10, 5)) # размер графики
fig.patch.set_facecolor("#f0f0f0")

canvas = FigureCanvasTkAgg(fig, master=center)
canvas.get_tk_widget().pack(fill="both", expand=True)


# масштаб колесиком мыши
def on_scroll(event):

    MIN_RANGE = 0.5
    MAX_RANGE = 300

    # если мышь вне области графика — не масштабируется
    if event.xdata is None or event.ydata is None:
        return

    scale_factor = 0.9 if event.button == 'up' else 1.1 # скорость масштабирования

    x_min, x_max = ax.get_xlim()
    y_min, y_max = ax.get_ylim()

    x_center = event.xdata
    y_center = event.ydata

    new_x_min = x_center - (x_center - x_min) * scale_factor
    new_x_max = x_center + (x_max - x_center) * scale_factor

    new_y_min = y_center - (y_center - y_min) * scale_factor
    new_y_max = y_center + (y_max - y_center) * scale_factor

    # проверка диапазона
    if (new_x_max - new_x_min) < MIN_RANGE or (new_x_max - new_x_min) > MAX_RANGE:
        return
    if (new_y_max - new_y_min) < MIN_RANGE or (new_y_max - new_y_min) > MAX_RANGE:
        return

    ax.set_xlim(new_x_min, new_x_max)
    ax.set_ylim(new_y_min, new_y_max)

    canvas.draw_idle()

canvas.mpl_connect("scroll_event", on_scroll)


# -------- правая панель --------
# родительский фрейм для двух блоков
right_frame = ttk.Frame(main)
right_frame.grid(row=0, column=2, rowspan=1, sticky="ns")  # весь правый столбец

# ---- Блок 1: Справка ----
right_help = ttk.LabelFrame(right_frame, text="Справка", padding=10)
right_help.pack(fill="both", expand=True, pady=(0,5))  # отступ между блоками


text_help = tk.Text(
    right_help,
    width=35,
    height=10,
    wrap="word",
    bg="#f0f0f0",
    relief="flat"
)
text_help.insert("1.0",
    "Парабола — график функции y = ax² + bx + c.\n\n"
    "• Вершина — минимум (a > 0) или максимум (a < 0)\n"
    "• a определяет направление ветвей\n"
    "• |a| влияет на ширину\n"
    "• b сдвигает влево / вправо\n"
    "• c — пересечение с осью Y\n"
    "• Ось симметрии: x = -b / (2a)"
)
text_help.config(state="disabled")
text_help.pack(fill="both", expand=True)

# ---- Блок 2: Обозначения ----
right_legend = ttk.LabelFrame(right_frame, text="Обозначения", padding=10)
right_legend.pack(fill="both", expand=True, pady=(5,0))

text_legend = tk.Text(
    right_legend,
    width=35,
    height=10,
    wrap="word",
    bg="#f0f0f0",
    relief="flat"
)

# Вершина
frame_vertex = ttk.Frame(right_legend)
frame_vertex.pack(fill="x", pady=5)

canvas_vertex = tk.Canvas(frame_vertex, width=20, height=20, highlightthickness=0)
canvas_vertex.pack(side="left", padx=(0, 30))
canvas_vertex.create_oval(2, 2, 18, 18, fill="blue", outline="blue")

ttk.Label(frame_vertex, text="Вершина").pack(side="left") 

# Корни
frame_root = ttk.Frame(right_legend)
frame_root.pack(fill="x", pady=5)

canvas_root = tk.Canvas(frame_root, width=20, height=20, highlightthickness=0)
canvas_root.pack(side="left", padx=(0, 30))
canvas_root.create_oval(2, 2, 18, 18, fill="green", outline="green")

ttk.Label(frame_root, text="Корни").pack(side="left") 

# Возрастает
frame_up = ttk.Frame(right_legend)
frame_up.pack(fill="x", pady=5)

canvas_up = tk.Canvas(frame_up, width=40, height=20, bg="#dcf0dc", highlightthickness=0)
canvas_up.pack(side="left", padx=(0, 10))
canvas_up.create_rectangle(2, 2, 18, 18, fill="#dcf0dc", outline="")
ttk.Label(frame_up, text="Возрастает").pack(side="left")

# Убывает
frame_down = ttk.Frame(right_legend)
frame_down.pack(fill="x", pady=5)

canvas_down = tk.Canvas(frame_down, width=40, height=20, bg="#FFe5e5", highlightthickness=0)
canvas_down.pack(side="left", padx=(0, 10))
canvas_down.create_rectangle(2, 2, 18, 18, fill="#FFe5e5", outline="")

ttk.Label(frame_down, text="Убывает").pack(side="left")

# первичная отрисовка
update_plot()
root.mainloop()
