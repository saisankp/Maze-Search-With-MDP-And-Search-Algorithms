# Maze implementation library reference/credit: Pyamaze (https://pypi.org/project/pyamaze/)

import random
from mdp_algorithms.utility_functions import valid_actions, set_initial_rewards, update_state_based_on_action


def value_iteration_algorithm(maze):
    path = []
    current_state = (maze.rows, maze.cols)
    path.append(current_state)
    potential_actions = {}
    decay = 0.9
    threshold = 0.005
    maze.rewards = {}

    # Set reward 1000 for the target state and -1 for non-target states
    set_initial_rewards(maze)

    # Iterate through all rows
    for row in range(1, maze.rows + 1):
        # Iterate through all columns
        for column in range(1, maze.cols + 1):
            present_square = (row, column)
            # Initialize no actions for the current square
            potential_actions[present_square] = []
            directions = {'North': 'N', 'East': 'E', 'South': 'S', 'West': 'W'}
            # Go to all directions
            for direction in directions.values():
                # If the present square has a valid path in the current direction, save it as a potential action
                if maze.maze_map[present_square][direction]:
                    potential_actions[present_square] = valid_actions((row, column), maze)

    # Set value function with 10000 for the target and -1 for non-target squares
    value_function = {}
    for square in maze.maze_map:
        if square == (1, 1):
            value_function[square] = 10000
        elif square in potential_actions.keys():
            value_function[square] = -1

    # Set initial policy by setting random policies for each cell
    policy = {}
    for potential_action in potential_actions.keys():
        policy[potential_action] = random.choice(potential_actions[potential_action])

    while True:
        max_change_in_value_function = 0
        # Iterate through all squares in the maze
        for state in maze.maze_map:
            updated_value = 0
            previous_value = value_function[state]
            # Iterate through all potential actions for the present square
            for action in potential_actions[state]:
                next_state = update_state_based_on_action(state, action)
                value = (maze.rewards[state] + (decay * value_function[tuple(next_state)]))
                # Check if the action is better
                if value > updated_value:
                    # If so, store this action and update the value
                    policy[state] = action
                    updated_value = value

            # Update the value of the current state
            value_function[state] = updated_value
            # Change in value function = absolute difference between new value - previous values for each state
            max_change_in_value_function = max(max_change_in_value_function,
                                               abs(previous_value - value_function[state]))
        # Break if we reach convergence
        if max_change_in_value_function < threshold:
            break

    # While the target is not reached yet, keep choosing the best action
    while current_state != (1, 1):
        action = policy[current_state]
        current_state = update_state_based_on_action(current_state, action)
        path.append(current_state)
    return path
