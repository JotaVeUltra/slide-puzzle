import pygame as pg


class PuzzleImage(pg.sprite.Group):
    """Container class for tiles"""

    def __init__(self, board_image, board_size=4, tile_size=100, *sprites):
        super().__init__(*sprites)
        for y in range(board_size):
            for x in range(board_size):
                tile_image = pg.Surface((tile_size, tile_size))
                tile_image.blit(
                    board_image,
                    (0, 0),
                    (tile_size * x, tile_size * y, tile_size, tile_size),
                )
                self.add(Tile(tile_image, tile_size, (x, y)))


class Tile(pg.sprite.Sprite):
    """Sprite class of tiles"""

    def __init__(self, image, size, position, *groups):
        super().__init__(*groups)
        self.image = image
        self.rect = self.image.get_rect()
        self.size = size
        self.position = position

    def update(self, *args):
        self.rect = self.position[0] * self.size, self.position[1] * self.size
