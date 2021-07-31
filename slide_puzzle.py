# TODO:
# init pygame
# check number of images inside the folder
# if there are more than one image ask the player to choose
# load the image and split it in tiles by the BOARDSIZE² number
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


def get_images():
    """
    Returns a list of the names of each file that has a bmp extension.
    """
    return [
        name
        for name in os.listdir(os.path.join("resources", "graphics"))
        if name[-3:].lower() in "bmp"
    ]


def main():
    pass


if __name__ == "__main__":
    main()
