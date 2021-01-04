import pygame
from copy import deepcopy


width, height = 10, 15
tile = 45
game_resolution = width * tile, height * tile  # Игровое разрешение
fps = 60

pygame.init()
game_sc = pygame.display.set_mode(game_resolution)
clock = pygame.time.Clock()

grid = [pygame.Rect(x * tile, y * tile, tile, tile) for x in range(width) for y in range(height)]  # Доска

figure_positions = [  # координаты плиток, из которых состоят фигуры
    [(0, 0), (-2, 0), (-1, 0), (1, 0)],  # (на чертеже) Красная линия
    [(0, 0), (-1, -1), (-1, 0), (0, -1)],  # (на чертеже) Оранжевый квадрат
    [(0, 0), (-1, -1), (0, -1), (0, 1)],  # (на чертеже) Жёлтая абракадабра
    [(0, 0), (-1, -1), (-1, 0), (0, 1)],  # (на чертеже) Зелёная абракадабра
    [(0, 0), (0, -1), (-1, 0), (0, 1)]  # (на чертеже) Голубая абракадабра
]

figures = [[pygame.Rect(x + width // 2, y + 1, 1, 1) for x, y in figure_position] for figure_position in figure_positions]  # Сами фигуры
figure_rect = pygame.Rect(0, 0, tile - 2, tile - 2)  # Плитка
figure = figures[4]  # Текущая фигура


def check_borders():  # Проверка границ при движении фигуры влево-вправо
    if figure[i].x < 0 or figure[i].x > width - 1:
        return False
    return True


while True:
    game_sc.fill((0, 0, 0))
    change_x = 0  # Изменение х координаты фигуры на столько-то клеток

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                change_x = -1  # На 1 клетку влево
            if event.key == pygame.K_RIGHT:
                change_x = 1  # На 1 клетку вправо

        old_figure = deepcopy(figure)  # Копия на случай, если фигура будет выходить за границы
        for i in range(4):  # Непосредственно изменение координат каждой клетки фигуры
            figure[i].x += change_x
            if not check_borders():
                figure = old_figure
                break

    [pygame.draw.rect(game_sc, (255, 255, 255), i_rect, 1) for i_rect in grid]  # Отрисовка доски

    for i in range(4):  # Отрисовка фигуры
        figure_rect.x = figure[i].x * tile
        figure_rect.y = figure[i].y * tile
        pygame.draw.rect(game_sc, (255, 255, 255), figure_rect)

    pygame.display.flip()
    clock.tick(fps)
