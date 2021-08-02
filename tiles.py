from random import shuffle


def count_inversions(array, blank):
    """Returns the number of inversions in a list ignoring the blank value."""
    count = 0
    for i, tile1 in enumerate(array[:-1]):
        if tile1 is not blank:
            for tile2 in array[i + 1 :]:
                if tile2 is not blank:
                    if tile1 > tile2:
                        count += 1
    return count


def find_blank_position(grid, blank):
    """Returns the number of row, from bottom, that contains the blank value."""
    for i, row in enumerate(grid[::-1]):
        if blank in row:
            return i + 1


def check_solvability(grid, blank=0):
    """Checks if a given instance of the slide puzzle is solvable."""
    array = [inner for outer in grid for inner in outer]
    inversions = count_inversions(array, blank)
    if len(grid) % 2:
        return not inversions % 2
    blank_pos = find_blank_position(grid, blank)
    return blank_pos % 2 != inversions % 2


def as_grid(array, board_size):
    """Convert a 1D array into a 2D array with given board size."""
    return [array[i : i + board_size] for i in range(0, len(array), board_size)]


def get_positions_dict(board_size):
    """Returns a dictionary with the positions of each tile in the puzzle."""
    number_of_tiles = board_size ** 2
    current_tile = 1
    positions = {}
    for y in range(board_size):
        for x in range(board_size):
            positions[current_tile] = (x, y)
            current_tile += 1
            if current_tile == number_of_tiles:
                current_tile = 0  # blank tile
    return positions


def randomize_tiles_positions(board_size):
    """Returns a random list of tiles positions."""
    positions = get_positions_dict(board_size)
    keys = list(positions.keys())
    while True:
        shuffle(keys)
        if check_solvability(as_grid(keys, board_size)):
            return keys
