import numpy as np

from typing import Optional
import random
from dataclasses import dataclass

from tiles import tiles

@dataclass()
class GridElement:
    """Class that is used to store the state of each element in the TileGrid"""
    tile_id: Optional[int]
    entropy: int = len(tiles)


class TileGrid:
    """Class that is used to preserve the grid state and modify it"""

    def __init__(self, width, height, scaler):
        # Visual
        self.width: int = width
        self.height: int = height
        self.scaler: int = scaler
        self.columns: int = int(height / scaler)
        self.rows: int = int(width / scaler)

        # Grid
        self.size: tuple[int, int] = (self.rows, self.columns)
        self.grid_array: np.ndarray[GridElement] = np.ndarray(shape=self.size, dtype=object)
        for x in range(self.rows):
            for y in range(self.columns):
                self.grid_array[x, y] = GridElement(None)
        """
        #basic_grid_element = GridElement(None)
        #self.grid_array.fill(basic_grid_element)
        # I don't understand it, it could easily break when I try to modify the values, and the code is ugly
        # But for now that's ok
        # I was so right about it not working
        """

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
        central_grid_element = self.grid_array[self.columns // 2, self.rows // 2]
        central_grid_element.tile_id = 5
        # min_entropy = None
        # for i in range(self.rows):
        #     for j in range(self.columns):
        #         if self.grid_array[i, j].is_collapsed is False:
        #             if min_entropy is None:
        #                 min_entropy = self.calculate_entropy(i, j)

    def update(self, surface, images):
        """This function should render all of the collapsed wavelengths every frame"""
        for x in range(self.rows):
            for y in range(self.columns):
                element: GridElement = self.grid_array[x, y]
                if element.tile_id is None:
                    continue
                x_pos = x * self.scaler
                y_pos = y * self.scaler
                surface.blit(images[element.tile_id], (x_pos, y_pos))