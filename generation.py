import numpy as np

from typing import Optional
from dataclasses import dataclass
import random

from tiles import tiles


@dataclass(frozen=True)
class Choice:
    """Class that is used to record all of the random decisions the program makes"""
    tile_options: Optional[list[int]]
    grid_options: Optional[list[tuple[int, int]]]
    # options are listed in order that will be attempted

@dataclass()
class GridElement:
    """Class that is used to store the state of each element in the TileGrid"""
    tile_id: Optional[int]  # Collapsed tiles have a tile_id != None
    entropy: int = len(tiles)


class TileGrid:
    """Class that is used to preserve the grid state and modify it"""

    def __init__(self, columns, rows, pixels):
        # Visual
        self.pixels: int = pixels
        self.columns: int = columns
        self.rows: int = rows

        # Grid
        self.size: tuple[int, int] = (self.rows, self.columns)
        self.grid_array: np.ndarray[GridElement] = np.ndarray(shape=self.size, dtype=object)
        """Using numpy for the array may have been a mistake. It doesn't add much except for problems.
        Since I don't really understand dtypes that aren't numeric the ide doesn't suggest grid element attributes."""
        for x in range(self.columns):
            for y in range(self.rows):
                self.grid_array[x, y] = GridElement(None)

        """ For every random choice the list of choices and the attempted choices should be saved.
        This feels like it's going to run into memory issues very quickly.
        But how else should I do it? """
        self.last_pos: tuple[int, int]
        self.history: list[Choice] = []  # field(default_factory=list)
        self.decisions: int = 0

    def entropy_of(self, pos: tuple[int, int]) -> int:
        """Returns the number of tiles that have valid borders with the tile of the 4 bordering grid elements"""
        return len(self.valid_neighbors(pos))

    def valid_neighbors(self, pos: tuple[int, int]):
        # First add the existing adjacent edges into a list (using None if the adjacent tile is empty)
        x, y = pos
        adjacent_edges = []
        if y - 1 < 0 or self.grid_array[x, y - 1].tile_id is None:
            adjacent_edges.append(None)
        else:
            adjacent_edges.append(tiles[self.grid_array[x, y - 1].tile_id].constraints.South)

        if x + 1 > self.columns - 1 or self.grid_array[x + 1, y].tile_id is None:
            adjacent_edges.append(None)
        else:
            adjacent_edges.append(tiles[self.grid_array[x + 1, y].tile_id].constraints.West)

        if y + 1 > self.rows - 1 or self.grid_array[x, y + 1].tile_id is None:
            adjacent_edges.append(None)
        else:
            adjacent_edges.append(tiles[self.grid_array[x, y + 1].tile_id].constraints.North)

        if x - 1 < 0 or self.grid_array[x - 1, y].tile_id is None:
            adjacent_edges.append(None)
        else:
            adjacent_edges.append(tiles[self.grid_array[x - 1, y].tile_id].constraints.East)
        # Go through 4 adjacent tiles and create set of possible bordering Tiles
        valid_tiles = []
        for tile in tiles:
            valid_tile = True
            for direction, condition in enumerate(adjacent_edges):
                if condition is None:
                    continue
                # Check for failure to meet condition
                if condition != tile.constraints[direction]:
                    valid_tile = False
            if valid_tile:
                valid_tiles.append(tile)

        return valid_tiles

    def recollapse_tile(self, chosen_id: int, chosen_pos: tuple[int, int]):
        element: GridElement = self.grid_array[chosen_pos]
        element.tile_id = chosen_id
        self.propogate_change(chosen_pos)
        self.last_pos = chosen_pos
        self.decisions += 1

    def backtrack(self):
        """This function removes the most recently changed tile and resets the entropy of its neighbors"""
        pos = self.last_pos
        print("pos:", pos)
        print("tile options", self.history[-1].tile_options)
        element = self.grid_array[pos]
        element.tile_id = None
        element.entropy = self.entropy_of(pos)
        self.propogate_change(pos)
        self.decisions -= 1

    def collapse_tile(self, element_pos: tuple[int, int]):
        """When this function is called on a specific tile a valid tile id is selected and it becomes collapsed"""
        element: GridElement = self.grid_array[element_pos]
        pot_tiles = self.valid_neighbors(element_pos)
        options = [tiles.index(pot_tile) for pot_tile in pot_tiles]
        random.shuffle(options)
        if len(options) == 1:
            print(f"for tile: {element_pos} there is only 1 option")
        else:
            print("Multiple options", options)
        element.tile_id = options.pop()
        self.propogate_change(element_pos)
        self.history.append(Choice(tile_options=options, grid_options=[element_pos]))
        self.last_pos = element_pos
        self.decisions += 1

    def propogate_change(self, pos: tuple[int, int]):
        x, y = pos
        if not y - 1 < 0:
            self.grid_array[x, y - 1].entropy = self.entropy_of((x, y - 1))
        if not x + 1 > self.columns - 1:
            self.grid_array[x + 1, y].entropy = self.entropy_of((x + 1, y))
        if not y + 1 > self.rows - 1:
            self.grid_array[x, y + 1].entropy = self.entropy_of((x, y + 1))
        if not x - 1 < 0:
            self.grid_array[x - 1, y].entropy = self.entropy_of((x - 1, y))

    def iterate(self) -> bool:
        """Chooses a tile with the lowest entropy, collapses that tile"""

        # If this decision point has been reached through backtracking, instead utilize the history
        if self.decisions < len(self.history):
            choice = self.history.pop()
            if not choice.grid_options:
                print("No tile nor grid options left")
                return False
            if choice.tile_options:
                # I need to handle the case where it was later decided that the most recent tile placement should
                # be reconsidered
                self.recollapse_tile(choice.tile_options.pop(), choice.grid_options[0])
                self.history.append(Choice(choice.tile_options, choice.grid_options))
                return True
            print("All tile options of selected grid element coordinates have been exhausted. Good Luck!")
            self.collapse_tile(choice.grid_options.pop())
            self.history.append(Choice(grid_options=choice.grid_options, tile_options=None))
            self.decisions += 1
            return True

        # General case where decision is being evaluated for the first time
        min_entropy = None
        for i in range(self.columns):
            for j in range(self.rows):
                element: GridElement = self.grid_array[i, j]

                # Skip collapsed elements
                if element.tile_id is not None:
                    continue

                # Undo unsolvable tiles
                if element.entropy == 0:
                    self.backtrack()
                    return True

                if min_entropy is None:
                    min_entropy = element.entropy
                    continue
                min_entropy = min(element.entropy, min_entropy)

        if min_entropy is None:
            print("Generation completed")
            return False
        if min_entropy == 0:
            print("Unreachable code reached")
            return False

        # Create a list of the lowest entropy grid element coordinates
        pot_elements = []
        for i in range(self.columns):
            for j in range(self.rows):
                element: GridElement = self.grid_array[i, j]
                if element.tile_id is not None:
                    continue
                if element.entropy == min_entropy:
                    pot_elements.append((i, j))
        random.shuffle(pot_elements)
        self.collapse_tile(pot_elements.pop())
        self.history.append(Choice(grid_options=pot_elements, tile_options=None))
        self.decisions += 1
        return True

    def print_state(self):
        # Print out the tile_id and entropy of every tile,
        for j in range(self.rows):
            for i in range(self.columns):
                ele: GridElement = self.grid_array[i, j]
                e = ele.entropy
                t = ele.tile_id
                print(f"[{e},{'  ' if t is None else f'{t}'.zfill(2)}]", end='')
            print()
        print()

    def update(self, surface, images):
        """This function should render all of the collapsed wavelengths every frame"""
        for x in range(self.columns):
            for y in range(self.rows):
                element: GridElement = self.grid_array[x, y]
                if element.tile_id is None:
                    continue
                x_pos = x * self.pixels
                y_pos = y * self.pixels
                surface.blit(images[element.tile_id], (x_pos, y_pos))

    def recalculate_entropy(self):
        """No longer necessary, inefficient solution to track the entropy of all tiles"""
        for i in range(self.columns):
            for j in range(self.rows):
                self.grid_array[i, j].entropy = self.entropy_of((i, j))

    def reset(self):
        for x in range(self.columns):
            for y in range(self.rows):
                self.grid_array[x, y] = GridElement(None)
        self.recalculate_entropy()
