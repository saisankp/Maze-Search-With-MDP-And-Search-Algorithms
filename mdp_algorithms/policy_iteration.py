# Maze implementation library reference/credit: Pyamaze (https://pypi.org/project/pyamaze/)

from mdp_algorithms.utility_functions import valid_actions, update_state_based_on_action, set_initial_rewards


def policy_iteration_algorithm(maze):
    path = []
    current_state = (maze.rows, maze.cols)
    path.append(current_state)
    value_function = {}
    discount_factor = 0.9
    maze.rewards = {}

    # Set value function as 0 for all states
    for state in maze.maze_map:
        value_function[state] = 0

    # Set reward 1000 for the target state and -1 for non-target states
    set_initial_rewards(maze)

    # Complete policy iteration to find the optimal policy
    policy = policy_improvement(maze, value_function, discount_factor)

    # While the target is not reached yet, keep choosing the best action
    while current_state != (1, 1):
        action = max(policy[current_state], key=policy[current_state].get)
        current_state = update_state_based_on_action(current_state, action)
        path.append(current_state)
    return path


# Converge towards an optimal policy by refining it
def policy_improvement(maze, value_function, discount_factor):
    # Initialize a policy where each state has various actions with equal probability
    current_policy = initialize_policy_for_each_state(maze)
    # Find optimal policy
    while True:
        # Track if the policy changes during policy improvement
        policy_has_changed_during_improvement = True
        # Evaluate the current policy
        policy_evaluation(current_policy, maze, value_function, discount_factor, threshold=0.001)
        # Iterate over all states in the maze
        for state in maze.maze_map.keys():
            # Keep track of action values
            expected_values_of_all_actions = {}
            # Keep track of previous action
            action_chosen_by_policy_before_update = max(current_policy[state], key=current_policy[state].get)
            # Iterate through all valid actions
            for action in valid_actions(state, maze):
                next_state = update_state_based_on_action(state, action)
                # If this state is not valid in the maze, use the current state (agent stays in same position)
                if next_state not in maze.maze_map:
                    next_state = state
                # Calculate value of a action at this next state
                expected_values_of_all_actions[action] = (maze.rewards.get(next_state, 0) +
                                                          discount_factor * value_function[next_state])
            # Calculate the best possible action
            action_with_highest_expected_value = max(expected_values_of_all_actions,
                                                     key=expected_values_of_all_actions.get)
            # If the action is the best action, set its probability to 1, or 0 otherwise
            for action in current_policy[state]:
                if action == action_with_highest_expected_value:
                    current_policy[state][action] = 1
                else:
                    current_policy[state][action] = 0
            # Update if the policy has changed to a better one
            if action_chosen_by_policy_before_update != action_with_highest_expected_value:
                policy_has_changed_during_improvement = False
        # Break if the policy has improved
        if policy_has_changed_during_improvement:
            break
    return current_policy


# Initialize a policy where each state has various actions with equal probability
def initialize_policy_for_each_state(maze):
    current_policy = {}
    for state in maze.maze_map.keys():
        current_policy[state] = {}
        # Start with uniform policy (set initial probabilities to be equal)
        for action in valid_actions(state, maze):
            # Set each action to have a probability of 1/total number of valid actions (to have equal probability)
            current_policy[state][action] = 1.0 / len(valid_actions(state, maze))
    return current_policy


# Evaluate the value function until convergence
def policy_evaluation(policy, maze, value_function, discount_factor, threshold):
    while True:
        max_change_in_value_function = 0
        for state in maze.maze_map.keys():
            estimated_state_value = 0
            # Iterate over all actions and their probabilities in the policy
            for action, probability_of_action in policy[state].items():
                next_state = update_state_based_on_action(state, action)
                # If this state is not valid in the maze, use the current state (agent stays in same position)
                if next_state not in maze.maze_map:
                    next_state = state
                # Use Bellman equation for state value estimation
                estimated_state_value = (estimated_state_value + probability_of_action *
                                         (maze.rewards.get(next_state, 0) + discount_factor *
                                          value_function[next_state]))
            # Change in value function = absolute difference between new value - previous values for each state
            max_change_in_value_function = max(max_change_in_value_function,
                                               abs(estimated_state_value - value_function[state]))
            value_function[state] = estimated_state_value
        # Break if we reach convergence
        if max_change_in_value_function < threshold:
            break
