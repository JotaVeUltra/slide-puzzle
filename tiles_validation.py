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
