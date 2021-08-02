import pygame as pg

from tiles import randomize_tiles_positions


class PuzzleImage(pg.sprite.Group):
    """Container class for tiles"""

    def __init__(self, board_image, board_size=4, tile_size=100, *sprites):
        super().__init__(*sprites)
        self.board_size = board_size
        tiles_positions = randomize_tiles_positions(board_size)
        for y in range(board_size):
            for x in range(board_size):
                tile_image = pg.Surface((tile_size, tile_size))
                tile_image.blit(
                    board_image,
                    (0, 0),
                    (tile_size * x, tile_size * y, tile_size, tile_size),
                )
                if (x, y) != (board_size - 1, board_size - 1):
                    self.add(
                        Tile(tile_image, tile_size, (x, y), tiles_positions.pop(0))
                    )
        self.blank_position = tiles_positions.pop(0)


class Tile(pg.sprite.Sprite):
    """Sprite class of tiles"""

    def __init__(self, image, size, original_position, position, *groups):
        super().__init__(*groups)
        self.image = image
        self.rect = self.image.get_rect()
        self.size = size
        self.original_position = original_position
        self.position = position

    def update(self, *args):
        self.rect = self.position[0] * self.size, self.position[1] * self.size
