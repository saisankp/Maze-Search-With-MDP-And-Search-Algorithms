# Maze implementation library reference/credit: Pyamaze (https://pypi.org/project/pyamaze/)

from queue import PriorityQueue
from search_algorithms.utility_functions import set_neighbouring_square, construct_path_from_dictionary


# A star algorithm implementation using manhattan heuristic
def a_star_algorithm(maze):
    # Set the (x,y) coordinates of the starting square
    initial_maze_square = (maze.rows, maze.cols)
    # Before we start, lets keep track of explored squares and how we got there
    explored_squares = {}
    # Use a priority queue to keep track of nodes to explore
    nodes_to_explore = PriorityQueue()
    nodes_to_explore.put((manhattan_distance(initial_maze_square, (1, 1)),
                          manhattan_distance(initial_maze_square, (1, 1)), initial_maze_square))
    # G-score is the cost from the start
    g_score = dict.fromkeys(maze.grid, float('inf'))
    g_score[initial_maze_square] = 0
    # F-Score is the cost from the start + estimated cost (i.e. heuristic with manhattan distance)
    f_score = dict.fromkeys(maze.grid, float('inf'))
    f_score[initial_maze_square] = manhattan_distance(initial_maze_square, (1, 1))
    # Start with initial maze square!
    maze_area_to_search = [initial_maze_square]
    # Keep looping until we have explored everything necessary
    while not nodes_to_explore.empty():
        # Get the 3rd element in tuple (i.e. square we are presently at)
        _, _, present_square = nodes_to_explore.get()
        # Add the current cell to the search space
        maze_area_to_search.append(present_square)
        # If we reached the target, break out of the loop!
        if present_square == (1, 1):
            break
        # Pyamaze takes single letter representations of each cardinal direction
        directions = {'North': 'N', 'East': 'E', 'South': 'S', 'West': 'W'}
        # Otherwise, explore potentially neighbouring squares and update G-Score/F-Score if a better path is found
        for direction in directions.values():
            if maze.maze_map[present_square][direction]:
                # Set the neighbouring square (x,y) based on the direction and the square we are presenting at
                neighbouring_square = set_neighbouring_square(direction, present_square)
                # Set a temporary G-Score and F-Score
                tentative_g_score = g_score[present_square]
                tentative_f_score = tentative_g_score + manhattan_distance(neighbouring_square, (1, 1))
                # If the tentative F-score (total estimated cost) for reaching 'neighbouring_square' is lower, update!
                if tentative_f_score < f_score[neighbouring_square]:
                    explored_squares[neighbouring_square] = present_square
                    f_score[neighbouring_square] = tentative_f_score
                    g_score[neighbouring_square] = tentative_g_score
                    nodes_to_explore.put((tentative_f_score,
                                          manhattan_distance(neighbouring_square, (1, 1)),
                                          neighbouring_square))
    # Construct the path from the start to the target square
    path_to_target = construct_path_from_dictionary(initial_maze_square, explored_squares)
    return maze_area_to_search, path_to_target


# Manhattan distance between 2 points for the heuristic (instead of Euclidean distance which would underestimate it)
def manhattan_distance(starting_maze_square, ending_maze_square):
    return abs(starting_maze_square[0] - ending_maze_square[0]) + abs(starting_maze_square[1] - ending_maze_square[1])
