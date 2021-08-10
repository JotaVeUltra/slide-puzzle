import pygame as pg

from tiles import get_positions_dict, randomize_tiles_positions


class PuzzleImage(pg.sprite.Group):
    """Container class for tiles"""

    def __init__(self, board_image, board_size=4, screen_size=400, *sprites):
        super().__init__(*sprites)
        self.board_size = board_size
        self.state = "playing"
        tiles_positions = randomize_tiles_positions(board_size)
        t_size = screen_size / board_size
        postions_dict = get_positions_dict(board_size)
        x, y = 0, 0
        for tile in tiles_positions:
            tile_image = pg.Surface((t_size, t_size))
            tile_pos = postions_dict[tile]
            if tile_pos == (board_size - 1, board_size - 1):
                self.blank_position = (x, y)
            else:
                tile_rect = (t_size * tile_pos[0], t_size * tile_pos[1], t_size, t_size)
                tile_image.blit(board_image, (0, 0), tile_rect)
                self.add(Tile(tile_image, t_size, postions_dict[tile], (x, y)))
            x += 1
            if x == board_size:
                x = 0
                y += 1

    def draw(self, surface):
        """Draw all tiles on the surface"""
        super().draw(surface)
        if self.state == "won":
            myfont = pg.font.SysFont("Arial", 60)
            textsurface = myfont.render("Win", False, (255, 0, 0))
            x = surface.get_width() / 2 - textsurface.get_width() / 2
            y = surface.get_height() / 2
            surface.blit(textsurface, (x, y))

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
        super().update(*args)
        self.rect = pg.Rect(
            self.position[0] * self.size,
            self.position[1] * self.size,
            self.size,
            self.size,
        )


class ThumbnailGroup(pg.sprite.Group):
    """Container class for thumbnails"""

    def __init__(self, images, *sprites):
        super().__init__(*sprites)
        x, y = 0, 0
        while len(images):
            self.add(Thumbnail(images.pop(), (x, y), 0))
            x += 1
            if x == 4:
                x = 0
                y += 1
        self.scroll_position = 0
        self.max_scroll_position = max(0, y - 4)


class Thumbnail(pg.sprite.Sprite):
    """Sprite class of thumbnails"""

    def __init__(self, image, position, scroll, *groups):
        super().__init__(*groups)
        self.full_image = image
        self.image = pg.transform.scale(image, (80, 80))
        self.rect = pg.Rect(0, 0, 80, 80)
        self.position = position
        self.scroll = scroll

    def update(self, scroll_position, *args):
        """Update the position of the thumbnail"""
        super().update(*args)
        self.scroll = scroll_position
        self.rect.x = 10 + 92 * self.position[0]
        self.rect.y = 10 + 92 * (self.position[1] - self.scroll)


class Scroll(pg.sprite.Sprite):
    """Sprite class of scroll"""

    def __init__(self, max_scroll, *groups) -> None:
        super().__init__(*groups)
        self.max_scroll = max_scroll
        self.height = 380 / max_scroll
        self.at = 0
        self.rect = pg.Rect(380, 10, 15, self.height)

    def up(self):
        """Scroll up"""
        self.at = max(self.at - 1, 0)
        self.rect.y = 10 + (self.at * self.height)

    def down(self):
        """Scroll down"""
        self.at = min(self.at + 1, self.max_scroll - 1)
        self.rect.y = 10 + (self.at * self.height)

    def draw(self, surface):
        """Draw the scroll"""
        pg.draw.rect(surface, (255, 255, 255), self.rect)
