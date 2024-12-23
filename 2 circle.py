### 2 Создать программу, которая рисует окружность с заданным пользователем радиусом
import matplotlib.pyplot as plt
import numpy as np


def bresenham_circle(radius):
    x = 0
    y = radius
    d = 3 - 2 * radius
    points = []

    def draw_circle_points(x, y):
        points.extend(
            [(x, y), (-x, y), (x, -y), (-x, -y), (y, x), (-y, x), (y, -x), (-y, -x)]
        )

    while x <= y:
        draw_circle_points(x, y)
        if d <= 0:
            d = d + 4 * x + 6
        else:
            d = d + 4 * (x - y) + 10
            y -= 1
        x += 1

    return points


def plot_circle(radius):
    points = bresenham_circle(radius)

    # Удаляем дубликаты и сортируем точки по углам
    unique_points = list(set(points))
    unique_points.sort(key=lambda p: np.arctan2(p[1], p[0]))

    # Добавляем первую точку в конец для замыкания контура
    unique_points.append(unique_points[0])

    # Разворачиваем список точек в x и y для построения графика
    x_coords = [point[0] for point in unique_points]
    y_coords = [point[1] for point in unique_points]

    # Рисуем
    plt.plot(x_coords, y_coords, color="black")
    plt.gca().set_aspect("equal", adjustable="box")
    plt.title(f"My MEGA GIPER ULTRA CIRCLE {radius}")
    plt.grid(True)
    plt.show()


# Enter
radius = int(input("R: "))
plot_circle(radius)
