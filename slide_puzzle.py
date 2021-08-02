# TODO:
# check number of images inside the folder
# if there are more than one image ask the player to choose
# randomize the tiles and check if solvable
# game loop
#    check for player actions
#        mouse click or arrows pressed
#    handle events
#        check if tile can be moved
#        change status of tile moved tile
#        checke if player win
#    update screen
#        drawn board
#        drawn tiles animation

import os

import pygame as pg

from puzzle_sprites import PuzzleImage


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
    puzzle_image.update()
    puzzle_image.draw(screen)

    pg.display.update()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                raise SystemExit
        clock.tick(30)

if __name__ == "__main__":
    main()
