import math
import os

import pygame as pg

from sprites import PuzzleImage, Scroll, ThumbnailGroup


clock = pg.time.Clock()


def button(screen, position, text):
    """
    Draw a button with text on the screen
    """
    font = pg.font.SysFont("Arial", 50)
    text_render = font.render(text, 1, (150, 200, 150))
    x, y, w, h = text_render.get_rect()
    x, y = position
    pg.draw.line(screen, (150, 150, 150), (x, y), (x + w, y), 5)
    pg.draw.line(screen, (150, 150, 150), (x, y - 2), (x, y + h), 5)
    pg.draw.line(screen, (50, 50, 50), (x, y + h), (x + w, y + h), 5)
    pg.draw.line(screen, (50, 50, 50), (x + w, y + h), [x + w, y], 5)
    pg.draw.rect(screen, (100, 100, 100), (x, y, w, h))
    return screen.blit(text_render, (x, y))


def get_images():
    """
    Returns a list of the images in the folder
    """
    return [
        os.path.join("images", name)
        for name in os.listdir(os.path.join("images"))
        if name[-3:].lower() in ["bmp", "png", "jpg"]
    ]


def select_board_size(screen):
    """
    Returns the size of the board
    """
    global clock

    screen.fill((0, 0, 0))
    b1 = button(screen, (100, 50), "2x2")
    b2 = button(screen, (200, 50), "3x3")
    b3 = button(screen, (100, 150), "4x4")
    b4 = button(screen, (200, 150), "5x5")
    b5 = button(screen, (100, 150), "6x6")
    b6 = button(screen, (200, 150), "7x7")
    b7 = button(screen, (100, 250), "8x8")
    b8 = button(screen, (200, 250), "9x9")

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                raise SystemExit
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if b1.collidepoint(pg.mouse.get_pos()):
                    return 2
                if b2.collidepoint(pg.mouse.get_pos()):
                    return 3
                if b3.collidepoint(pg.mouse.get_pos()):
                    return 4
                if b4.collidepoint(pg.mouse.get_pos()):
                    return 5
                if b5.collidepoint(pg.mouse.get_pos()):
                    return 6
                if b6.collidepoint(pg.mouse.get_pos()):
                    return 7
                if b7.collidepoint(pg.mouse.get_pos()):
                    return 8
                if b8.collidepoint(pg.mouse.get_pos()):
                    return 9

        pg.display.update()
        clock.tick(30)


def select_image_menu(screen, images):
    """
    Returns the selected image
    """
    global clock

    scroll = Scroll(math.ceil((len(images) / 4) - 3))
    menu = ThumbnailGroup(images[:])

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                raise SystemExit
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                for thumb in menu.sprites():
                    if thumb.rect.collidepoint((pg.mouse.get_pos())):
                        return pg.transform.scale(thumb.full_image, (400, 400))
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 4:
                    scroll.up()
                if event.button == 5:
                    scroll.down()

        screen.fill((0, 0, 0))
        menu.update(scroll.at)
        menu.draw(screen)
        scroll.draw(screen)

        pg.display.update()
        clock.tick(30)


def main():
    pg.init()
    global clock
    screen = pg.display.set_mode((400, 400), 0, 32)
    pg.display.set_caption("Slide Puzzle")

    images = [pg.image.load(image).convert() for image in get_images()]

    board_image = select_image_menu(screen, images)
    board_size = select_board_size(screen)
    puzzle_image = PuzzleImage(board_image, board_size)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                raise SystemExit
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                for tile in puzzle_image.sprites():
                    if tile.rect.collidepoint((pg.mouse.get_pos())):
                        puzzle_image.try_move(tile)
                        break
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    puzzle_image.move_tile("up")
                if event.key == pg.K_DOWN:
                    puzzle_image.move_tile("down")
                if event.key == pg.K_LEFT:
                    puzzle_image.move_tile("left")
                if event.key == pg.K_RIGHT:
                    puzzle_image.move_tile("right")
                if event.key == pg.K_ESCAPE:
                    board_image = select_image_menu(screen, images)
                    board_size = select_board_size(screen)
                    puzzle_image = PuzzleImage(board_image, board_size)

        screen.fill((0, 0, 0))
        puzzle_image.update()
        puzzle_image.draw(screen)

        pg.display.update()
        clock.tick(30)


if __name__ == "__main__":
    main()
