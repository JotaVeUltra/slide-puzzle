from pygame.sprite import Sprite, Group


class PuzzleImage(Group):
    """Container class for tiles"""

    def __init__(self, image_name, *sprites):  # board_size, stretch,
        super().__init__(*sprites)
        self.image_name = image_name
        self.tiles = []


class Tile(Sprite):
    """Sprite class of tiles"""

    def __init__(self, image):
        super().__init__()
