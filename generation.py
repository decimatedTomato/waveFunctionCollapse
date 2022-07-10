import numpy as np

from typing import Optional
from dataclasses import dataclass
import random

from tiles import tiles


@dataclass()
class GridElement:
    """Class that is used to store the state of each element in the TileGrid"""
    tile_id: Optional[int] # Collapsed tiles have a tile_id != None
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
        Using numpy for the array may have been a mistake. It doesn't add much except for problems.
        Since I don't really understand dtypes that aren't numeric the ide doesn't suggest grid element attributes.
        """

    def entropy_of(self, x, y) -> int:
        """Returns the number of tiles that have valid borders with the tile of the 4 bordering grid elements"""
        return len(self.valid_neighbors(x, y))

    def valid_neighbors(self, x, y):
        # First add the existing adjacent edges into a list (using None if the adjacent tile is empty)
        adjacent_edges = []
        if y - 1 < 0 or self.grid_array[x, y - 1].tile_id is None:
            adjacent_edges.append(None)
        else:
            adjacent_edges.append(tiles[self.grid_array[x, y - 1].tile_id].adjacency_rules.South)

        if x + 1 > self.columns - 1 or self.grid_array[x + 1, y].tile_id is None:
            adjacent_edges.append(None)
        else:
            adjacent_edges.append(tiles[self.grid_array[x + 1, y].tile_id].adjacency_rules.West)

        if y + 1 > self.rows - 1 or self.grid_array[x, y + 1].tile_id is None:
            adjacent_edges.append(None)
        else:
            adjacent_edges.append(tiles[self.grid_array[x, y + 1].tile_id].adjacency_rules.North)

        if x - 1 < 0 or self.grid_array[x - 1, y].tile_id is None:
            adjacent_edges.append(None)
        else:
            adjacent_edges.append(tiles[self.grid_array[x - 1, y].tile_id].adjacency_rules.East)
        # Go through 4 adjacent tiles and create set of possible bordering Tiles
        valid_tiles = []
        for tile in tiles:
            valid_tile = True
            for direction, condition in enumerate(adjacent_edges):
                if condition is None:
                    continue
                # Check for failure to meet condition
                if condition != tile.adjacency_rules[direction]:
                    valid_tile = False
            if valid_tile:
                valid_tiles.append(tile)

        return valid_tiles

    def collapse_tile(self, element_pos: tuple[int, int]):
        """When this function is called on a specific tile a valid tile id is selected and it becomes collapsed"""
        element: GridElement = self.grid_array[element_pos]
        pot_tiles = self.valid_neighbors(element_pos[0], element_pos[1])
        r = random.randint(0, len(pot_tiles) - 1)  # Untested
        element.tile_id = r
        # Once I've changed the entropy propogation system from being recalculated every iteration
        # propogate() should be here


    def iterate(self) -> bool:
        """Chooses a tile with the lowest entropy, collapses that tile"""

        """
        How in the hell should this thing backtrack
        """
        min_entropy = None
        for i in range(self.rows):
            for j in range(self.columns):
                element: GridElement = self.grid_array[i, j]
                # Skip collapsed tiles
                if element.tile_id is not None:
                    continue
                # evaluate entropy for non-collapsed grid elements
                element.entropy = self.entropy_of(i, j)

                if min_entropy is None:
                    min_entropy = element.entropy
                    continue
                min_entropy = min(element.entropy, min_entropy)

        if min_entropy is None:
            print("Generation completed")
            return False

        # Now create a list of the lowest entropy grid elements
        pot_elements = []
        for i in range(self.rows):
            for j in range(self.columns):
                element: GridElement = self.grid_array[i, j]
                if element.entropy == min_entropy:
                    pot_elements.append((i, j))
        print(pot_elements)

        if min_entropy == 0:
            print("Impossible position found")
            return False

        # From the selected elements randomly choose one
        r = random.randint(0, len(pot_elements) - 1)
        # Into collapse_tile I pass the position of the tile to be collapsed
        self.collapse_tile(pot_elements[r])

        return True

    def test(self):
        self.grid_array[self.columns // 2, self.rows // 2].tile_id = 5
        print("Central:", self.entropy_of(self.columns // 2, self.rows // 2))
        print("North:", self.entropy_of(self.columns // 2, self.rows // 2 - 1))
        print("East:", self.entropy_of(self.columns // 2 + 1, self.rows // 2))
        print("South:", self.entropy_of(self.columns // 2, self.rows // 2 + 1))
        print("West:", self.entropy_of(self.columns // 2 - 1, self.rows // 2))

        self.collapse_tile((self.columns // 2, self.rows // 2))

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
