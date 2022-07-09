import pygame
import os
import generation
import tiles


def wfc(r, c):
    # Visuals setup
    os.environ["SDL_VIDEO_CENTERED"] = '1'
    scaler = 32
    height = scaler * r
    width = scaler * c

    black = (0, 0, 0)
    images = tiles.load_images()

    #  pygame setup
    size = (width, height)
    pygame.init()
    pygame.display.set_caption("Tile Map Generation")
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    fps = 1

    #  Data structure setup
    tile_grid = generation.TileGrid(width, height, scaler)

    # Running
    run = True
    dostuff = True
    while run:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_KP_ENTER:
                    tile_grid.iterate()
        # Update the game
        if dostuff:
            screen.fill(black)
            tile_grid.iterate()
            tile_grid.update(surface=screen, images=images)
            dostuff = False
        pygame.display.update()
    pygame.quit()
