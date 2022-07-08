import os
from dataclasses import dataclass
from os.path import abspath

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

@dataclass(frozen=True)
class Tile:
    """Class that is used to initialize the possible tiles to be added as grid elements"""
    image: int  # image reference variable
    adjacency_rules: tuple[tuple[int, float]]  # [Edge N, E, S, W][Valid Tiles][Tile_id, Weight]

Tiles = {
"""
    "Field": Tile(, adjacency_rules=(("Field", ""
                                                      ,
                                                      ,
                                                  ), (), (), ())) #  Field
"""
}

def load_images():
    base_path = os.path.dirname(__file__) + "\\resources\\"
    filepaths = os.listdir("resources")
    images = [pygame.image.load(base_path + img) for img in filepaths]
    return images
