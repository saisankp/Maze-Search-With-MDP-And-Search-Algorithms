# Maze implementation library reference/credit: Pyamaze (https://pypi.org/project/pyamaze/)

from search_algorithms.utility_functions import set_neighbouring_square, construct_path_from_dictionary


# Breadth first search algorithm implementation
def bfs_algorithm(maze):
    # Set the (x,y) coordinates of the starting square
    initial_maze_square = (maze.rows, maze.cols)
    # Start with empty search space
    maze_area_to_search = []
    # Before we start, lets keep track of explored squares and how we got there
    explored_squares = {}
    # Start off with the initial square as the next square that is discovered
    subsequent_squares = [initial_maze_square]
    discovered_squares = [initial_maze_square]
    # Keep looping until we have explored everything necessary
    while len(subsequent_squares) > 0:
        # Remove the first element off the list of the next squares we are going to
        present_square = subsequent_squares[0]
        del subsequent_squares[0]
        # If we reached the target, break out of the loop!
        if present_square == (1, 1):
            break
        # Pyamaze takes single letter representations of each cardinal direction
        directions = {'North': 'N', 'East': 'E', 'South': 'S', 'West': 'W'}
        # Otherwise, explore potentially neighbouring squares
        for direction in directions.values():
            if maze.maze_map[present_square][direction]:
                # Set the neighbouring square (x,y) based on the direction and the square we are presenting at
                neighbouring_square = set_neighbouring_square(direction, present_square)
                # If the neighbouring square has already been explored, ignore it
                if neighbouring_square in discovered_squares:
                    continue
                # Add the neighbour to the list of explored squares
                maze_area_to_search.append(neighbouring_square)
                # Add neighbour to the list of squares to explore next
                subsequent_squares.append(neighbouring_square)
                # Add neighbour to the list of discovered squares
                discovered_squares.append(neighbouring_square)
                # Update the BFS path between the (relationship between the neighbour and the present square)
                explored_squares[neighbouring_square] = present_square
    # Construct the path from the start to the target square
    path_to_target = construct_path_from_dictionary(initial_maze_square, explored_squares)
    return maze_area_to_search, path_to_target
