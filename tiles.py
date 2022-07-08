import os
from dataclasses import dataclass
from enum import auto, IntEnum
from typing import NamedTuple

import pygame

"""
Steps:
Load the images in /resources
Display the first image from this list
Turn list into a dict comprehension that creates the format
"name"(without file extension): "image with said name"
Put all of the adjacency rules of the 14 Tiles into the Tiles dictionary
for now Ill use format
"name": adjacency_rules
Later I can figure out how to move all of this into the dataclass
"""


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


@dataclass(frozen=True)
class Tile:
    """Class that is used to initialize the possible tiles to be added as grid elements"""
    image: str
    adjacency_rules: NamedTuple


tiles = [Tile('Field.png', Edges(Edge.FF, Edge.FF, Edge.FF, Edge.FF)),
         Tile('Field-BL Corner Mountain.png', Edges(Edge.MM, Edge.MM, Edge.FM, Edge.MF)),
         Tile('Field-BL Mountain-TR.png', Edges(Edge.MM, Edge.MM, Edge.FF, Edge.FF)),
         Tile('Field-BR Corner Mountain.png', Edges(Edge.MM, Edge.MF, Edge.MF, Edge.MM)),
         Tile('Field-L Mountain-R.png', Edges(Edge.FM, Edge.MM, Edge.FM, Edge.FF)),
         Tile('Field-T Mountain-B.png', Edges(Edge.FF, Edge.FM, Edge.MM, Edge.FM)),
         Tile('Field-TL Corner Mountain.png', Edges(Edge.FM, Edge.MM, Edge.MM, Edge.FM)),
         Tile('Field-TL Mountain-BR.png', Edges(Edge.FF, Edge.MM, Edge.MM, Edge.FF)),
         Tile('Field-TR Corner Mountain.png', Edges(Edge.MF, Edge.FM, Edge.MM, Edge.MM)),
         Tile('Mountain.png', Edges(Edge.MM, Edge.MM, Edge.MM, Edge.MM)),
         Tile('Mountain-BL Field-TR.png', Edges(Edge.FF, Edge.FF, Edge.MM, Edge.MM)),
         Tile('Mountain-L Field-R.png', Edges(Edge.MF, Edge.FF, Edge.MF, Edge.MM)),
         Tile('Mountain-T Field_B.png', Edges(Edge.MM, Edge.MF, Edge.FF, Edge.MF)),
         Tile('Mountain-TL Field-BR.png', Edges(Edge.MM, Edge.FF, Edge.FF, Edge.MM))]


def load_images():
    base_path = os.path.dirname(__file__) + "\\resources\\"
    filepaths = os.listdir("resources")
    images = [pygame.image.load(base_path + img) for img in filepaths]
    print(filepaths)
    return images
