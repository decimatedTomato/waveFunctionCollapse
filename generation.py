import numpy as np
import pygame

import random
from dataclasses import dataclass


from tiles import Tile, tiles

@dataclass()
class GridElement:
    """Class that is used to store the state of each element in the TileGrid"""
    tile_id: int
    entropy: int
    is_collapsed: bool = False


class TileGrid:
    """Class that is used to perform transformations"""

    def __init__(self, width, height, scaler):
        # Visual
        self.width: int = width
        self.height: int = height
        self.scaler: int = scaler
        self.columns: int = int(height / scaler)
        self.rows: int = int(width / scaler)

        # Logic
        self.size: tuple[int, int] = (self.rows, self.columns)
        self.grid_array = np.ndarray(shape=self.size, dtype=GridElement)

    def calculate_entropy(self, x, y):
        """UNIMPLEMENTED"""
        current_grid_element = self.grid_array[x, y]
        valid_tile = {}
        # Go through 4 adjacent tiles and create set of possible bordering Tiles
        if self.grid_array[x + 1, y] is not None:  # is within range
            pass
        return len(valid_tile)

    def collapse_tile(self):
        """When this function is called on a specific tile a valid tile id is selected and it becomes collapsed"""
        pass

    def iterate(self):
        min_entropy = None
        for i in range(self.rows):
            for j in range(self.columns):
                if self.grid_array[i, j].is_collapsed is False:
                    if min_entropy is None:
                        min_entropy = self.calculate_entropy(i, j)

    def update(self, images, surface):
        for x in range(self.rows):
            for y in range(self.columns):



                x_pos = x * self.scaler
                y_pos = y * self.scaler
                r = random.randint(0, 13)
                surface.blit(images[r], (x_pos, y_pos))