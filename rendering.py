import pygame
import os
import generation
import tiles


def wfc(r, c, pixels):
    # Visuals setup
    os.environ["SDL_VIDEO_CENTERED"] = '1'

    black = (0, 0, 0)
    images = tiles.load_images(pixels)

    #  pygame setup
    size = (c * pixels, r * pixels)
    pygame.init()
    pygame.display.set_caption("Tile Map Generation")
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    fps = 5

    #  Data structure setup
    tile_grid = generation.TileGrid(c, r, pixels)

    # Running
    run = True
    keep_generating = True
    while run:
        clock.tick(fps)
        # Update the game
        if keep_generating: keep_generating = tile_grid.iterate()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # tile_grid.test()
                    # run = tile_grid.iterate()
                    keep_generating = not keep_generating
                elif event.key == pygame.K_BACKSPACE:
                    tile_grid.reset()
                    keep_generating = True
        screen.fill(black)
        tile_grid.update(surface=screen, images=images)
        pygame.display.update()
    pygame.quit()
