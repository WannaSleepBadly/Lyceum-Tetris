import pygame


W, H = 10, 15
TILE = 45
GAME_RES = W * TILE, H * TILE  # Игровое разрешение
fps = 60

pygame.init()
game_sc = pygame.display.set_mode(GAME_RES)
clock = pygame.time.Clock()

grid = [pygame.Rect(x * TILE, y * TILE, TILE, TILE) for x in range(W) for y in range(H)]  # Доска

while True:
    game_sc.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    [pygame.draw.rect(game_sc, (255, 255, 255), i_rect, 1) for i_rect in grid]  # Отрисовка доски
    pygame.display.flip()
    clock.tick(fps)
