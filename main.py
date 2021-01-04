import pygame


W, H = 10, 15
TILE = 45
GAME_RES = W * TILE, H * TILE  # Игровое разрешение


pygame.init()
game_sc = pygame.display.set_mode(GAME_RES)
clock = pygame.time.Clock()

while True:
    game_sc.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    pygame.display.flip()
    clock.tick()