# Maze implementation library reference/credit: Pyamaze (https://pypi.org/project/pyamaze/)

# Get valid actions from current coordinates
def valid_actions(coordinates, maze):
    actions = maze.maze_map[(coordinates[0], coordinates[1])]
    valid_actions_to_take = []
    for direction, valid in actions.items():
        if valid:
            valid_actions_to_take.append(direction)
    return valid_actions_to_take


# Update a state/square based on an action
def update_state_based_on_action(state, action):
    if action == 'N':
        updated_state = (state[0] - 1, state[1])
    elif action == 'E':
        updated_state = (state[0], state[1] + 1)
    elif action == 'S':
        updated_state = (state[0] + 1, state[1])
    elif action == 'W':
        updated_state = (state[0], state[1] - 1)
    else:
        # Unknown action supplied, so default to original state
        updated_state = state
    return updated_state


# Set initial rewards where the target square has a reward of 1000 and non target squares have -1
def set_initial_rewards(maze):
    for state in maze.maze_map:
        if state == (1, 1):
            maze.rewards[state] = 1000
        else:
            maze.rewards[state] = -1
