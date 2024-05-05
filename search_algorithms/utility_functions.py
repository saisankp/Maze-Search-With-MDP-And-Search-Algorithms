# Maze implementation library reference/credit: Pyamaze (https://pypi.org/project/pyamaze/)

# Set the neighbouring squares depending on the cardinal directions provided
def set_neighbouring_square(direction, present_square):
    neighbouring_square = None
    if direction == 'N':
        neighbouring_square = (present_square[0] - 1, present_square[1])
    elif direction == 'E':
        neighbouring_square = (present_square[0], present_square[1] + 1)
    elif direction == 'S':
        neighbouring_square = (present_square[0] + 1, present_square[1])
    elif direction == 'W':
        neighbouring_square = (present_square[0], present_square[1] - 1)
    return neighbouring_square


# Construct the path from the dictionary of explored squares
def construct_path_from_dictionary(initial_maze_square, explored_squares):
    square = (1, 1)
    path_to_target = {}
    while square != initial_maze_square:
        path_to_target[explored_squares[square]] = square
        square = explored_squares[square]
    return path_to_target
