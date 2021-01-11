# Фон заставки by Ashlinaa, игры - by ryllcat21, музыка - Wii Shop Channel
import sys
import pygame
from copy import deepcopy
from random import choice
# import os  Нужно для музыки


width, height = 10, 15
tile = 45
game_resolution = width * tile, height * tile  # Игровое разрешение
fps = 60
res = 950, 700

game_background = pygame.image.load('image/background_4.jpg')
background = pygame.image.load('image/background_2.jpg')
pygame.init()
#  pygame.mixer.music.load('Wii-Shop-Channel.ogg')  Не работает пока что, F
#  pygame.mixer.music.play(loops=-1)
pygame.font.init()
pygame.display.set_caption('Пастельный Тетрис')
fancy_font = pygame.font.SysFont('Monotype Corsiva', 120)
small_fancy_font = pygame.font.SysFont('Monotype Corsiva', 100)
show_record_text, show_score_text = small_fancy_font.render('Record:', False, (255, 255, 255)), \
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

count, count_speed, limit = 0, 60, 2000  # Счетчик, скорость, с которой он изменяется и предел(для падения)


def get_record():
    global record
    try:
        with open('records.txt', 'r', encoding='utf-8') as f:
            record = int(f.readline())
    except FileNotFoundError:
        with open('records.txt', 'w', encoding='utf-8') as f:
            f.write('0')


def start_screen():  # Заставка
    intro_text = ["                Добро пожаловать в TETRIS!", "",
                  "Управление",
                  "→ и ← для перемещения фигуры вправо и влево,",
                  "↑ для вращения и ↓ для ускоренного падения", "", "",
                  "    Для начала игры нажмите любую клавишу!"]
    fon = pygame.transform.scale(pygame.image.load('image/background_3.jpg'), res)
    screen.blit(fon, (0, 0))
    text_coord = 50
    for ss_line in intro_text:
        font = pygame.font.SysFont('Monotype Corsiva', 50)
        string_rendered = font.render(ss_line, True, (255, 255, 255))
        shade_string = font.render(ss_line, True, (189, 134, 240))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(shade_string, intro_rect)
        intro_rect.y -= 5
        screen.blit(string_rendered, intro_rect)
        intro_rect.y += 5

    while True:
        for ss_event in pygame.event.get():
            if ss_event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif ss_event.type == pygame.KEYDOWN or \
                    ss_event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(fps)


def end_screen(count_1, record_1):  # Конец игры
    intro_text = ["                      Конец игры!", "",
                  f"Ваш счет: {count_1}",
                  f"Ваш рекорд: {record_1}", "",
                  "Для начала игры нажмите", "любую клавишу!"]
    fon = pygame.transform.scale(pygame.image.load('image/background_1.png'), res)
    screen.blit(fon, (0, 0))
    text_coord = 50
    for ss_line in intro_text:
        font = pygame.font.SysFont('Monotype Corsiva', 70)
        string_rendered = font.render(ss_line, True, (255, 255, 255))
        shade_string = font.render(ss_line, True, (189, 134, 240))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(shade_string, intro_rect)
        intro_rect.y -= 5
        screen.blit(string_rendered, intro_rect)
        intro_rect.y += 5

    while True:
        for end_event in pygame.event.get():
            if end_event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif end_event.type == pygame.KEYDOWN or \
                    end_event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(fps)


def check_borders():  # Проверка границ
    if figure[i].x < 0 or figure[i].x > width - 1 or \
            figure[i].y > height - 1 or field[figure[i].y][figure[i].x] != 0:
        return False
    return True


def update_record():
    global record
    if score > record:  # Обновление рекорда
        with open('records.txt', 'w', encoding='utf-8') as f:
            f.write(str(score))
        record = score


score, record = 0, 0
get_record()
start_screen()
while True:
    screen.blit(background, (0, 0))
    screen.blit(game_screen, (10, 10))
    game_screen.blit(game_background, (0, 0))
    screen.blit(title, (515, 10))
    screen.blit(show_score_text, (510, 275))
    screen.blit(show_record_text, (510, 400))
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
                limit = 70  # Ускоренное падение
            if event.key == pygame.K_UP:  # Вращение
                center = figure[0]  # Центр вращения(отмечен на чертеже)
                old_figure = deepcopy(figure)
                for i in range(4):
                    x = figure[i].y - center.y
                    y = figure[i].x - center.x
                    figure[i].x = center.x - x
                    figure[i].y = center.y + y
                    if not check_borders():
                        figure = deepcopy(old_figure)
                        break

    old_figure = deepcopy(figure)  # Копия на случай, если фигура будет выходить за границы
    for i in range(4):  # Непосредственно изменение х координаты каждой плитки фигуры
        figure[i].x += change_x
        if not check_borders():
            figure = deepcopy(old_figure)
            break

    count += count_speed  # Обновление счетчика
    if count > limit:  # Задаем скорость падения
        count = 0
        old_figure = deepcopy(figure)
        for i in range(4):  # Изменение у коордиаты всех плиток
            figure[i].y += 1
            if not check_borders():
                for c in range(4):
                    field[old_figure[c].y][old_figure[c].x] = color  # Отмечаем на поле, что
                    # данная клетка занята таким цветом
                limit = 2000
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
        else:
            score += 10

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

    show_score = small_fancy_font.render(str(score), False, (255, 255, 255))  # Показ счета
    screen.blit(show_score, (720, 280))
    update_record()
    show_record = small_fancy_font.render(str(record), False, (255, 255, 255))  # Показ рекорда
    screen.blit(show_record, (775, 405))

    for i in range(width):
        if field[0][i] != 0:  # Конец игры
            field = [[0 for _ in range(width)] for i in range(height)]  # Обнуление поля
            count = 0  # Обнуление "падения"
            update_record()
            for rect in grid:  # Заполнение доски белыми квадратиками
                pygame.draw.rect(game_screen, (255, 255, 255), rect)
                screen.blit(game_screen, (10, 10))
                pygame.display.flip()
                clock.tick(200)
            end_screen(score, record)
            score = 0  # Обнуление счета

    pygame.display.flip()
    clock.tick(fps)
