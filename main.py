import pygame


W, H = 10, 15
tile = 45
game_resolution = W * tile, H * tile  # Игровое разрешение
fps = 60

pygame.init()
game_sc = pygame.display.set_mode(game_resolution)
clock = pygame.time.Clock()

grid = [pygame.Rect(x * tile, y * tile, tile, tile) for x in range(W) for y in range(H)]  # Доска

figure_positions = [  # координаты плиток, из которых состоят фигуры
    [(0, 0), (-2, 0), (-1, 0), (1, 0)],  # (на чертеже) Красная линия
    [(0, 0), (-1, -1), (-1, 0), (0, -1)],  # (на чертеже) Оранжевый квадрат
    [(0, 0), (-1, -1), (0, -1), (0, 1)],  # (на чертеже) Жёлтая абракадабра
    [(0, 0), (-1, -1), (-1, 0), (0, 1)],  # (на чертеже) Зелёная абракадабра
    [(0, 0), (0, -1), (-1, 0), (0, 1)]  # (на чертеже) Голубая абракадабра
]

figures = [[pygame.Rect(x + W // 2, y + 1, 1, 1) for x, y in figure_position] for figure_position in figure_positions]  # Сами фигуры
figure_rect = pygame.Rect(0, 0, tile - 2, tile - 2)  # Плитка
figure = figures[4]  # Текущая фигура

while True:
    game_sc.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    [pygame.draw.rect(game_sc, (255, 255, 255), i_rect, 1) for i_rect in grid]  # Отрисовка доски
    for i in range(4):
        figure_rect.x = figure[i].x * tile
        figure_rect.y = figure[i].y * tile
        pygame.draw.rect(game_sc, (255, 255, 255), figure_rect)

    pygame.display.flip()
    clock.tick(fps)
