# TODO:
# check number of images inside the folder
# if there are more than one image ask the player to choose
# game loop
#    update screen
#        drawn tiles animation

import os

import pygame as pg

from sprites import PuzzleImage


def get_images():
    """
    Returns a list of the names of each file that has a bmp extension.
    """
    return [
        os.path.join("resources", "graphics", name)
        for name in os.listdir(os.path.join("resources", "graphics"))
        if name[-3:].lower() in "bmp"
    ]


def main():
    pg.init()
    clock = pg.time.Clock()
    screen = pg.display.set_mode((400, 400), 0, 32)
    images = get_images()
    board_image = pg.image.load(images[0]).convert()
    puzzle_image = PuzzleImage(board_image, 4, 100)

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

        screen.fill((0, 0, 0))
        puzzle_image.update()
        puzzle_image.draw(screen)

        pg.display.update()
        clock.tick(30)


if __name__ == "__main__":
    main()
