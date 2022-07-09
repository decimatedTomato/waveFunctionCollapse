import os
from dataclasses import dataclass
from enum import auto, IntEnum
from typing import NamedTuple

import pygame


# Edge Types
# F: Field, M: Mountain
# North/South: left right
# East/West: top bottom
class Edge(IntEnum):
    FF = auto()
    FM = auto()
    MF = auto()
    MM = auto()


class Edges(NamedTuple):
    North: int
    East: int
    South: int
    West: int


@dataclass()
class Tile:
    """Class that is used to initialize the possible tiles to be added as grid elements"""
    img_filepath: str
    adjacency_rules: NamedTuple
    image: pygame.Surface = None
    # I would like this class to be frozen (immutable) but then how could I add the images.
    # Maybe the images should use a dict or list index to correspond to Tiles instead


tiles = [Tile('Field-BL Corner Mountain.png', Edges(Edge.MM, Edge.MM, Edge.FM, Edge.MF)),
         Tile('Field-BL Mountain-TR.png', Edges(Edge.MM, Edge.MM, Edge.FF, Edge.FF)),
         Tile('Field-BR Corner Mountain.png', Edges(Edge.MM, Edge.MF, Edge.MF, Edge.MM)),
         Tile('Field-L Mountain-R.png', Edges(Edge.FM, Edge.MM, Edge.FM, Edge.FF)),
         Tile('Field-T Mountain-B.png', Edges(Edge.FF, Edge.FM, Edge.MM, Edge.FM)),
         Tile('Field-TL Corner Mountain.png', Edges(Edge.FM, Edge.MM, Edge.MM, Edge.FM)),
         Tile('Field-TL Mountain-BR.png', Edges(Edge.FF, Edge.MM, Edge.MM, Edge.FF)),
         Tile('Field-TR Corner Mountain.png', Edges(Edge.MF, Edge.FM, Edge.MM, Edge.MM)),
         Tile('Field.png', Edges(Edge.FF, Edge.FF, Edge.FF, Edge.FF)),
         Tile('Mountain-BL Field-TR.png', Edges(Edge.FF, Edge.FF, Edge.MM, Edge.MM)),
         Tile('Mountain-L Field-R.png', Edges(Edge.MF, Edge.FF, Edge.MF, Edge.MM)),
         Tile('Mountain-T Field_B.png', Edges(Edge.MM, Edge.MF, Edge.FF, Edge.MF)),
         Tile('Mountain-TL Field-BR.png', Edges(Edge.MM, Edge.FF, Edge.FF, Edge.MM)),
         Tile('Mountain.png', Edges(Edge.MM, Edge.MM, Edge.MM, Edge.MM))]


def load_images():
    base_path = os.path.dirname(__file__) + "\\resources\\"
    filepaths = os.listdir("resources")
    images = []

    for image_filepath in filepaths:
        filepath_found = False
        for tile in tiles:
            if tile.img_filepath == image_filepath:
                tile.image = pygame.image.load(base_path + image_filepath)
                images.append(tile.image)
                filepath_found = True
        if not filepath_found:
            print(f"filepath {image_filepath} not found")

    return images