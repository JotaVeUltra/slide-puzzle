import pygame as pg

from tiles import get_positions_dict, randomize_tiles_positions


class PuzzleImage(pg.sprite.Group):
    """Container class for tiles"""

    def __init__(self, board_image, board_size=4, tile_size=100, *sprites):
        super().__init__(*sprites)
        self.board_size = board_size
        self.state = "playing"
        tiles_positions = randomize_tiles_positions(board_size)
        postions_dict = get_positions_dict(board_size)
        x, y = 0, 0
        for tile in tiles_positions:
            tile_image = pg.Surface((tile_size, tile_size))
            current_position = postions_dict[tile]
            if current_position == (board_size - 1, board_size - 1):
                self.blank_position = (x, y)
            else:
                tile_image.blit(
                    board_image,
                    (0, 0),
                    (
                        tile_size * current_position[0],
                        tile_size * current_position[1],
                        tile_size,
                        tile_size,
                    ),
                )
                self.add(
                    Tile(
                        tile_image,
                        tile_size,
                        original_position=postions_dict[tile],
                        position=(x, y),
                    )
                )
            x += 1
            if x == board_size:
                x = 0
                y += 1

    def draw(self, surface):
        """Draw all tiles on the surface"""
        super().draw(surface)
        if self.state == "won":
            myfont = pg.font.SysFont(pg.font.get_default_font(), 60)
            textsurface = myfont.render("Won", False, (255, 0, 0))
            surface.blit(
                textsurface,
                (
                    surface.get_width() / 2 - textsurface.get_width() / 2,
                    surface.get_height() / 2,
                ),
            )

    def update(self, *args):
        """Update the state of the puzzle"""
        super().update(*args)
        won = True
        for sprite in self.sprites():
            sprite.update(*args)
            if sprite.position != sprite.original_position:
                won = False
        if won:
            self.state = "won"

    def get_tile(self, x, y):
        """Return the tile at the given position"""
        for tile in self.sprites():
            if tile.position == (x, y):
                return tile
        return None

    def move_tile(self, direction):
        """Move the tile in the given direction"""
        if self.state == "playing":
            x, y = self.blank_position
            if direction == "up":
                tile = self.get_tile(x, y + 1)
            elif direction == "down":
                tile = self.get_tile(x, y - 1)
            if direction == "left":
                tile = self.get_tile(x + 1, y)
            if direction == "right":
                tile = self.get_tile(x - 1, y)
            if tile:
                tile.position, self.blank_position = self.blank_position, tile.position

    def try_move(self, tile):
        """Try to move tiles in row or column"""
        clicked_position = tile.position
        if self.state == "playing":
            x, y = self.blank_position
            if tile.position[0] == x or tile.position[1] == y:
                while self.blank_position != clicked_position:
                    if tile.position[0] < x:
                        self.move_tile("right")
                    elif tile.position[0] > x:
                        self.move_tile("left")
                    elif tile.position[1] < y:
                        self.move_tile("down")
                    elif tile.position[1] > y:
                        self.move_tile("up")


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
        """Update the position of the tile"""
        self.rect = pg.Rect(
            self.position[0] * self.size,
            self.position[1] * self.size,
            self.size,
            self.size,
        )
