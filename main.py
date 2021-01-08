import os
import sys
import pygame
from copy import deepcopy
from random import choice


width, height = 10, 15
tile = 45
game_resolution = width * tile, height * tile  # Игровое разрешение
fps = 60
res = 950, 700

game_background = pygame.image.load('image/background_4.jpg')
background = pygame.image.load('image/background_2.jpg')
pygame.init()
pygame.font.init()
fancy_font = pygame.font.SysFont('Monotype Corsiva', 120)
small_fancy_font = pygame.font.SysFont('Monotype Corsiva', 100)
show_record, show_score = small_fancy_font.render('Record:', False, (255, 255, 255)),\
                          small_fancy_font.render('Score:', False, (255, 255, 255))
title = fancy_font.render('TETRIS', False, (255, 255, 255))
screen = pygame.display.set_mode(res)
game_screen = pygame.Surface(game_resolution)
clock = pygame.time.Clock()

grid = [pygame.Rect(x * tile, y * tile, tile, tile) for x in range(width) for y in range(height)]  # Доска

colors = [(255, 181, 232), (255, 153, 153), (255, 102, 102), (255, 102, 153),  # Цвета для фигур
          (255, 0, 102), (255, 204, 255), (255, 0, 255), (204, 102, 255), (204, 0, 255),
          (153, 51, 255), (153, 102, 255), (204, 204, 255), (102, 0, 255), (51, 51, 255),
          (51, 102, 255), (0, 102, 255), (153, 204, 255), (0, 204, 255), (204, 255, 255),
          (102, 255, 255), (153, 255, 204), (51, 255, 204)]
color = choice(colors)

figure_positions = [  # координаты плиток, из которых состоят фигуры
    [(0, 0), (-2, 0), (-1, 0), (1, 0)],  # (на чертеже) Красная линия
    [(0, 0), (-1, -1), (-1, 0), (0, -1)],  # (на чертеже) Оранжевый квадрат
    [(0, 0), (-1, -1), (0, -1), (0, 1)],  # (на чертеже) Жёлтая абракадабра
    [(0, 0), (-1, -1), (-1, 0), (0, 1)],  # (на чертеже) Зелёная абракадабра
    [(0, 0), (0, -1), (-1, 0), (0, 1)]  # (на чертеже) Голубая абракадабра
]

figures = [[pygame.Rect(x + width // 2, y + 1, 1, 1) for x, y in figure_position]
           for figure_position in figure_positions]  # Сами фигуры
figure_rect = pygame.Rect(0, 0, tile - 2, tile - 2)  # Плитка
figure = deepcopy(choice(figures))  # Текущая фигура
field = [[0 for _ in range(width)] for i in range(height)]  # Карта поля

count, count_speed = 0, 60  # Счетчик и скорость, с которой он изменяется(для падения)


def check_borders():  # Проверка границ
    if figure[i].x < 0 or figure[i].x > width - 1 or \
            figure[i].y > height - 1 or field[figure[i].y][figure[i].x] != 0:
        return False
    return True


def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


while True:
    screen.blit(background, (0, 0))
    screen.blit(game_screen, (10, 10))
    game_screen.blit(game_background, (0, 0))
    screen.blit(title, (515, 10))
    screen.blit(show_score, (510, 275))
    screen.blit(show_record, (510, 470))
    change_x = 0  # Изменение х координаты фигуры на столько-то клеток
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                change_x = -1  # На 1 клетку влево
            if event.key == pygame.K_RIGHT:
                change_x = 1  # На 1 клетку вправо
            if event.key == pygame.K_DOWN:
                pass
            if event.key == pygame.K_UP:
                pass

    old_figure = deepcopy(figure)  # Копия на случай, если фигура будет выходить за границы
    for i in range(4):  # Непосредственно изменение х координаты каждой плитки фигуры
        figure[i].x += change_x
        if not check_borders():
            figure = deepcopy(old_figure)
            break

    count += count_speed  # Обновление счетчика
    if count > 2000:  # Задаем скорость падения
        count = 0
        old_figure = deepcopy(figure)
        for i in range(4):  # Изменение у коордиаты всех плиток
            figure[i].y += 1
            if not check_borders():
                for c in range(4):
                    field[old_figure[c].y][old_figure[c].x] = color  # Отмечаем на поле, что
                    # данная клетка занята таким цветом
                figure, color = deepcopy(choice(figures)), choice(colors)
                break

    line = height - 1  # Последняя строка поля
    for i in range(height - 1, -1, -1):  # Проходимся по всему полю
        full_count = 0  # Счетчик заполненных плиток
        for j in range(width):
            if field[i][j] != 0:
                full_count += 1
            field[line][j] = field[i][j]  # Заполненная линия заменяется на ту, что над ней
        if full_count < width:
            line -= 1

    [pygame.draw.rect(game_screen, (255, 255, 255), i_rect, 1) for i_rect in grid]  # Отрисовка доски

    for i in range(4):  # Отрисовка фигуры
        figure_rect.x = figure[i].x * tile
        figure_rect.y = figure[i].y * tile
        pygame.draw.rect(game_screen, color, figure_rect)

    for y, raw in enumerate(field):  # Отрисовка тех фигур, которые уже упали на доску (поля)
        for x, col in enumerate(raw):
            if col != 0:
                figure_rect.x = x * tile
                figure_rect.y = y * tile
                pygame.draw.rect(game_screen, col, figure_rect)

    pygame.display.flip()
    clock.tick(fps)