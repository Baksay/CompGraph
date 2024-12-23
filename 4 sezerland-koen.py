### 4 Реализация алгоритма Сезерленда-Коэна
import matplotlib.pyplot as plt

# Определяем коды регионов для отсечения
INSIDE = 0  # 0000
LEFT = 1    # 0001
RIGHT = 2   # 0010
BOTTOM = 4  # 0100
TOP = 8     # 1000

# Ф-ция для вычисления кода точки
def compute_code(x, y, x_min, y_min, x_max, y_max):
    code = INSIDE
    if x < x_min:    # Sleva ot okna
        code |= LEFT
    elif x > x_max:  # Sprava ot okna
        code |= RIGHT
    if y < y_min:    # Nizhe okna
        code |= BOTTOM
    elif y > y_max:  # Vyshe okna
        code |= TOP
    return code

# Алгоритм Сезерленда-Коэна для отсечения отрезков
def cohen_sutherland_clip(x1, y1, x2, y2, x_min, y_min, x_max, y_max):
    code1 = compute_code(x1, y1, x_min, y_min, x_max, y_max)
    code2 = compute_code(x2, y2, x_min, y_min, x_max, y_max)
    accept = False

    while True:
        if code1 == 0 and code2 == 0:  # Обе точки внутри окна
            accept = True
            break
        elif code1 & code2 != 0:  # Обе точки снаружи, отрезок вне окна
            break
        else:
            x, y = 0.0, 0.0
            # Выбираем точку снаружи
            if code1 != 0:
                code_out = code1
            else:
                code_out = code2

            # Пересечения с границами окна
            if code_out & TOP:
                x = x1 + (x2 - x1) * (y_max - y1) / (y2 - y1)
                y = y_max
            elif code_out & BOTTOM:
                x = x1 + (x2 - x1) * (y_min - y1) / (y2 - y1)
                y = y_min
            elif code_out & RIGHT:
                y = y1 + (y2 - y1) * (x_max - x1) / (x2 - x1)
                x = x_max
            elif code_out & LEFT:
                y = y1 + (y2 - y1) * (x_min - x1) / (x2 - x1)
                x = x_min

            # Заменим точку снаружи на точку пересечения и пересчитаем код
            if code_out == code1:
                x1, y1 = x, y
                code1 = compute_code(x1, y1, x_min, y_min, x_max, y_max)
            else:
                x2, y2 = x, y
                code2 = compute_code(x2, y2, x_min, y_min, x_max, y_max)

    if accept:
        return x1, y1, x2, y2
    else:
        return None

# Функция визуализации отсечения линии
def draw_plot(lines, x_min, y_min, x_max, y_max):
    fig, ax = plt.subplots()

    # Окно отсечения
    ax.plot([x_min, x_max, x_max, x_min, x_min],
            [y_min, y_min, y_max, y_max, y_min], 'k-', lw=2)

    # Отрезки до отсечения
    for line in lines:
        x1, y1, x2, y2 = line
        ax.plot([x1, x2], [y1, y2], 'r--', label='Do otsecheniya')

    # Отсечение
    for line in lines:
        result = cohen_sutherland_clip(*line, x_min, y_min, x_max, y_max)
        if result:
            x1, y1, x2, y2 = result
            ax.plot([x1, x2], [y1, y2], 'g-', lw=2, label='Posle otsecheniya')

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Otsechenie otrezkov algoritmom Sazerlenda-Koena')
    plt.grid(True)
    plt.show()

# Пример
if __name__ == "__main__":
    x_min, y_min = 10, 10
    x_max, y_max = 100, 100

    lines = [
        (5, 5, 120, 120),
        (50, 50, 60, 70),
        (70, 80, 120, 140),
        (10, 110, 110, 10),
        (0, 50, 200, 50)
    ]

    draw_plot(lines, x_min, y_min, x_max, y_max)