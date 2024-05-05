import statistics
import sys
from timeit import timeit
from memory_profiler import memory_usage
from pyamaze import maze, agent, textLabel, COLOR
from pyfiglet import figlet_format
import inquirer
from search_algorithms.a_star import a_star_algorithm
from search_algorithms.bfs import bfs_algorithm
from search_algorithms.dfs import dfs_algorithm
from mdp_algorithms.policy_iteration import policy_iteration_algorithm
from mdp_algorithms.value_iteration import value_iteration_algorithm

# Maze implementation library reference/credit: Pyamaze (https://pypi.org/project/pyamaze/)

# Print welcome banner!
print(figlet_format("Welcome to Prathamesh's Maze Solver for CS7IS2!", justify='center', width=140))

# Either run an individual algorithm or compare multiple algorithms
answer = inquirer.prompt([inquirer.List("wish", message="I want to", choices=["Run an individual algorithm",
                                                                              "Compare multiple algorithms", "Exit"]
                                        )])

# Run an individual algorithm
if answer["wish"] == "Run an individual algorithm":
    # 5 algorithm options
    answer = inquirer.prompt([inquirer.List("algorithm", message="I want to run the individual algorithm",
                                            choices=["A*", "Breadth-first search", "Depth-first search",
                                                     "Policy iteration", "Value iteration"]
                                            )])
    # Number of columns in the maze
    maze_columns = inquirer.prompt([inquirer.Text("number of columns for the maze",
                                                  message="How many columns do you want in the maze?",
                                                  validate=lambda _, c: c.isdigit() and int(c) > 0
                                                  )])
    # Number of rows in the maze
    maze_rows = inquirer.prompt([inquirer.Text("number of rows for the maze",
                                               message="How many rows do you want in the maze?",
                                               validate=lambda _, c: c.isdigit() and int(c) > 0
                                               )])

    # Number of iterations for measuring time taken
    iterations = inquirer.prompt([inquirer.Text("iterations",
                                                message="How many iterations do you want to run the algorithm for?",
                                                validate=lambda _, c: c.isdigit() and int(c) > 0
                                                )])

    # Create the maze
    maze = maze(int(maze_rows["number of rows for the maze"]), int(maze_columns["number of columns for the maze"]))
    maze.CreateMaze(loopPercent=50)

    # Calculate the search space and path after running the chosen algorithm while also tracking time and memory used
    memory_from_iterations = []
    search_space_from_iterations = []
    path_length_from_iterations = []

    average_memory = None
    average_search_space = None
    average_path_length = None
    maze_area_to_search = None
    path_to_target = None
    memory = None
    time_taken = None

    if answer["algorithm"] == "A*":
        for _ in range (int(iterations["iterations"])):
            memory, (maze_area_to_search, path_to_target) = memory_usage((a_star_algorithm, (maze,), {}),
                                                                         retval=True)
            memory_from_iterations.append(max(memory))
            search_space_from_iterations.append(len(maze_area_to_search) + 1)
            path_length_from_iterations.append(len(path_to_target) + 1)

        average_memory = statistics.mean(memory_from_iterations)
        average_search_space = statistics.mean(search_space_from_iterations)
        average_path_length = statistics.mean(path_length_from_iterations)
        time_taken = timeit(stmt='a_star_algorithm(maze)', number=int(iterations["iterations"]),
                            globals=globals())

    elif answer["algorithm"] == "Breadth-first search":
        for _ in range (int(iterations["iterations"])):
            memory, (maze_area_to_search, path_to_target) = memory_usage((bfs_algorithm, (maze,), {}),
                                                                         retval=True)
            memory_from_iterations.append(max(memory))
            search_space_from_iterations.append(len(maze_area_to_search) + 1)
            path_length_from_iterations.append(len(path_to_target) + 1)

        average_memory = statistics.mean(memory_from_iterations)
        average_search_space = statistics.mean(search_space_from_iterations)
        average_path_length = statistics.mean(path_length_from_iterations)
        time_taken = timeit(stmt='bfs_algorithm(maze)', number=int(iterations["iterations"]),
                            globals=globals())

    elif answer["algorithm"] == "Depth-first search":
        for _ in range (int(iterations["iterations"])):
            memory, (maze_area_to_search, path_to_target) = memory_usage((dfs_algorithm, (maze,), {}),
                                                                         retval=True)
            memory_from_iterations.append(max(memory))
            search_space_from_iterations.append(len(maze_area_to_search) + 1)
            path_length_from_iterations.append(len(path_to_target) + 1)

        average_memory = statistics.mean(memory_from_iterations)
        average_search_space = statistics.mean(search_space_from_iterations)
        average_path_length = statistics.mean(path_length_from_iterations)
        time_taken = timeit(stmt='dfs_algorithm(maze)', number=int(iterations["iterations"]),
                            globals=globals())

    elif answer["algorithm"] == "Policy iteration":
        for _ in range (int(iterations["iterations"])):
            memory, path_to_target = memory_usage((policy_iteration_algorithm, (maze,), {}),
                                                  retval=True)
            memory_from_iterations.append(max(memory))
            path_length_from_iterations.append(len(path_to_target) + 1)

        average_memory = statistics.mean(memory_from_iterations)
        average_path_length = statistics.mean(path_length_from_iterations)
        time_taken = timeit(stmt='policy_iteration_algorithm(maze)',
                            number=int(iterations["iterations"]),
                            globals=globals())

    elif answer["algorithm"] == "Value iteration":
        for _ in range (int(iterations["iterations"])):
            memory, path_to_target = memory_usage((value_iteration_algorithm, (maze,), {}),
                                                  retval=True)
            memory_from_iterations.append(max(memory))
            path_length_from_iterations.append(len(path_to_target) + 1)

        average_memory = statistics.mean(memory_from_iterations)
        average_path_length = statistics.mean(path_length_from_iterations)
        time_taken = timeit(stmt='value_iteration_algorithm(maze)',
                            number=int(iterations["iterations"]),
                            globals=globals())

    # Add title and labels to the maze to show memory and path information
    print(f"Average {answer['algorithm']} maximum memory usage: {average_memory} MiB")
    print(f"Average {answer['algorithm']} path length:", average_path_length)
    print(f"Average {answer['algorithm']} time taken: {time_taken} seconds")
    label = textLabel(maze, f"{answer['algorithm']} maximum memory used", f"{round(max(memory), 4)}MiB")
    label.lab.configure(bg="grey", fg="black", font=('Trebuchet MS', 15), relief="raised")
    label.lab.pack_configure(expand=False, anchor='s')
    label = textLabel(maze, f"{answer['algorithm']} path length", len(path_to_target) + 1)
    label.lab.configure(bg="grey", fg="black", font=('Trebuchet MS', 15), relief="raised")
    label.lab.pack_configure(expand=False, anchor='s')
    # MDP algorithms do not have a search space to be mentioned in the label
    if maze_area_to_search is not None:
        label = textLabel(maze, f"{answer['algorithm']} search space", len(maze_area_to_search) + 1)
        label.lab.configure(bg="grey", fg="black", font=('Trebuchet MS', 15), relief="raised")
        label.lab.pack_configure(expand=False, anchor='s')
    label = textLabel(maze, f"{answer['algorithm']} time taken", f"{round(time_taken, 4)}s")
    label.lab.configure(bg="grey", fg="black", font=('Trebuchet MS', 15), relief="raised")
    label.lab.pack_configure(expand=False, anchor='s')
    maze._win.title(f"{answer['algorithm']} algorithm solving a {maze_rows['number of rows for the maze']}x"
                    f"{maze_columns['number of columns for the maze']} maze (Path is cyan)")

    # Add agents to the maze to show the search space (for search algorithms only) and path of the algorithm
    search_space = agent(maze, footprints=True, shape='square', color=COLOR.yellow)

    # MDP algorithms do not have a search space to be an agent or label in the maze
    if maze_area_to_search is not None:
        maze._win.title(f"{answer['algorithm']} algorithm solving a {maze_rows['number of rows for the maze']}x"
                        f"{maze_columns['number of columns for the maze']} maze (Search space is yellow, "
                        f"path is cyan)")
        maze.tracePath({search_space: maze_area_to_search}, showMarked=True, delay=75)

    # All algorithms have a path to be an agent
    path = agent(maze, footprints=True, color=COLOR.cyan)
    maze.tracePath({path: path_to_target}, delay=75)

    # Run the maze
    maze.run()

# Run multiple algorithms
elif answer["wish"] == "Compare multiple algorithms":
    # Either compare between search algorithms, MDP algorithms, or between all of them together
    answer = inquirer.prompt([inquirer.List("algorithm_type",
                                            message="The type of algorithms I want to compare between are",
                                            choices=["Search algorithms (to each other)",
                                                     "MDP algorithms (to each other)",
                                                     "Search and MDP algorithms"]
                                            )])

    # Number of columns in the maze
    maze_columns = inquirer.prompt([inquirer.Text("number of columns for the maze",
                                                  message="How many columns do you want in the maze?",
                                                  validate=lambda _, c: c.isdigit() and int(c) > 0
                                                  )])

    # Number of rows in the maze
    maze_rows = inquirer.prompt([inquirer.Text("number of rows for the maze",
                                               message="How many rows do you want in the maze?",
                                               validate=lambda _, c: c.isdigit() and int(c) > 0
                                               )])

    # Number of iterations for measuring time taken
    iterations = inquirer.prompt([inquirer.Text("iterations",
                                                message="How many iterations do you want to run each algorithm for?",
                                                validate=lambda _, c: c.isdigit() and int(c) > 0
                                                )])

    # Create the maze
    maze = maze(int(maze_rows["number of rows for the maze"]), int(maze_columns["number of columns for the maze"]))
    maze.CreateMaze(loopPercent=50)

    memory_from_iterations = []
    search_space_from_iterations = []
    path_length_from_iterations = []
    average_memory = None
    average_search_space = None
    average_path_length = None
    a_star_maze_area_to_search = None
    dfs_maze_area_to_search = None
    bfs_maze_area_to_search = None
    a_star_path_to_target = None
    dfs_path_to_target = None
    bfs_path_to_target = None
    policy_iteration_path_to_target = None
    value_iteration_path_to_target = None
    policy_iteration_memory = None
    value_iteration_memory = None

    # Calculate the search space and path after running the chosen algorithm while also tracking the memory used

    if answer["algorithm_type"] == "Search algorithms (to each other)":
        # A star algorithm completion with memory and time taken being measured
        for _ in range(int(iterations["iterations"])):
            a_star_memory, (a_star_maze_area_to_search, a_star_path_to_target) = memory_usage((a_star_algorithm,
                                                                                               (maze,), {}),
                                                                                              retval=True)
            memory_from_iterations.append(max(a_star_memory))
            search_space_from_iterations.append(len(a_star_maze_area_to_search) + 1)
            path_length_from_iterations.append(len(a_star_path_to_target) + 1)

        average_memory = statistics.mean(memory_from_iterations)
        average_search_space = statistics.mean(search_space_from_iterations)
        average_path_length = statistics.mean(path_length_from_iterations)
        a_star_time_taken = timeit(stmt='a_star_algorithm(maze)', number=int(iterations["iterations"]),
                            globals=globals())

        print(f"Average A* maximum memory usage: {average_memory} MiB")
        print(f"Average A* path length: {average_path_length}")
        print(f"Average A* search space: {average_search_space}")
        print(f"Average A* time taken: {a_star_time_taken} seconds")

        memory_from_iterations = []
        search_space_from_iterations = []
        path_length_from_iterations = []

        # DFS algorithm completion with memory and time taken being measured
        for _ in range(int(iterations["iterations"])):
            dfs_memory, (dfs_maze_area_to_search, dfs_path_to_target) = memory_usage((dfs_algorithm,
                                                                                      (maze,), {}), retval=True)
            memory_from_iterations.append(max(dfs_memory))
            search_space_from_iterations.append(len(dfs_maze_area_to_search) + 1)
            path_length_from_iterations.append(len(dfs_path_to_target) + 1)

        average_memory = statistics.mean(memory_from_iterations)
        average_search_space = statistics.mean(search_space_from_iterations)
        average_path_length = statistics.mean(path_length_from_iterations)
        dfs_time_taken = timeit(stmt='dfs_algorithm(maze)', number=int(iterations["iterations"]),
                                globals=globals())

        print(f"Average DFS maximum memory usage: {average_memory} MiB")
        print(f"Average DFS path length: {average_path_length}")
        print(f"Average DFS search space: {average_search_space}")
        print(f"Average DFS time taken: {dfs_time_taken} seconds")

        memory_from_iterations = []
        search_space_from_iterations = []
        path_length_from_iterations = []

        # BFS algorithm completion with memory and time taken being measured
        for _ in range(int(iterations["iterations"])):
            bfs_memory, (bfs_maze_area_to_search, bfs_path_to_target) = memory_usage((bfs_algorithm,
                                                                                      (maze,), {}), retval=True)
            memory_from_iterations.append(max(bfs_memory))
            search_space_from_iterations.append(len(bfs_maze_area_to_search) + 1)
            path_length_from_iterations.append(len(bfs_path_to_target) + 1)

        average_memory = statistics.mean(memory_from_iterations)
        average_search_space = statistics.mean(search_space_from_iterations)
        average_path_length = statistics.mean(path_length_from_iterations)
        bfs_time_taken = timeit(stmt='bfs_algorithm(maze)', number=int(iterations["iterations"]),
                                globals=globals())

        print(f"Average BFS maximum memory usage: {average_memory} MiB")
        print(f"Average BFS path length: {average_path_length}")
        print(f"Average BFS search space: {average_search_space}")
        print(f"Average BFS time taken: {bfs_time_taken} seconds")

        # Add title and labels to the maze to show memory and path information
        label = textLabel(maze, 'A* search space', len(a_star_maze_area_to_search) + 1)
        label.lab.configure(bg="grey", fg="black", font=('Trebuchet MS', 11), relief="raised")
        label.lab.pack_configure(expand=False, anchor='s')
        label = textLabel(maze, 'DFS search space', len(dfs_maze_area_to_search) + 1)
        label.lab.configure(bg="grey", fg="black", font=('Trebuchet MS', 11), relief="raised")
        label.lab.pack_configure(expand=False, anchor='s')
        label = textLabel(maze, 'BFS search space', len(bfs_maze_area_to_search) + 1)
        label.lab.configure(bg="grey", fg="black", font=('Trebuchet MS', 11), relief="raised")
        label.lab.pack_configure(expand=False, anchor='s')
        label = textLabel(maze, 'A* path length', len(a_star_path_to_target) + 1)
        label.lab.configure(bg="grey", fg="black", font=('Trebuchet MS', 11), relief="raised")
        label.lab.pack_configure(expand=False, anchor='s')
        label = textLabel(maze, 'DFS path length', len(dfs_path_to_target) + 1)
        label.lab.configure(bg="grey", fg="black", font=('Trebuchet MS', 11), relief="raised")
        label.lab.pack_configure(expand=False, anchor='s')
        label = textLabel(maze, 'BFS path length', len(bfs_path_to_target) + 1)
        label.lab.configure(bg="grey", fg="black", font=('Trebuchet MS', 11), relief="raised")
        label.lab.pack_configure(expand=False, anchor='s')
        label = textLabel(maze, 'A* time taken', f"{round(a_star_time_taken, 4)}")
        label.lab.configure(bg="grey", fg="black", font=('Trebuchet MS', 11), relief="raised")
        label.lab.pack_configure(expand=False, anchor='s')
        label = textLabel(maze, 'DFS time taken', f"{round(dfs_time_taken, 4)}")
        label.lab.configure(bg="grey", fg="black", font=('Trebuchet MS', 11), relief="raised")
        label.lab.pack_configure(expand=False, anchor='s')
        label = textLabel(maze, 'BFS time taken', f"{round(bfs_time_taken, 4)}")
        label.lab.configure(bg="grey", fg="black", font=('Trebuchet MS', 11), relief="raised")
        label.lab.pack_configure(expand=False, anchor='s')
        maze._win.title(f"Search algorithms solving a {maze_rows['number of rows for the maze']}x"
                        f"{maze_columns['number of columns for the maze']} maze (A* is yellow, DFS is blue,"
                        f" BFS is red)")

        # Agents for each search algorithm
        a_star_path = agent(maze, footprints=True, color=COLOR.yellow)
        dfs_path = agent(maze, footprints=True, color=COLOR.blue)
        bfs_path = agent(maze, footprints=True, color=COLOR.red)

        # Create a trace of each agent
        maze.tracePath({a_star_path: a_star_path_to_target}, delay=75)
        maze.tracePath({dfs_path: dfs_path_to_target}, delay=75)
        maze.tracePath({bfs_path: bfs_path_to_target}, delay=75)

        # Run the maze
        maze.run()

    elif answer["algorithm_type"] == "MDP algorithms (to each other)":
        # Policy iteration algorithm completion with memory and time taken being measured
        for _ in range(int(iterations["iterations"])):
            policy_iteration_memory, policy_iteration_path_to_target = memory_usage((policy_iteration_algorithm,
                                                                                     (maze,), {}), retval=True)
            memory_from_iterations.append(max(policy_iteration_memory))
            path_length_from_iterations.append(len(policy_iteration_path_to_target) + 1)

        average_memory = statistics.mean(memory_from_iterations)
        average_path_length = statistics.mean(path_length_from_iterations)
        policy_iteration_time_taken = timeit(stmt='policy_iteration_algorithm(maze)',
                                             number=int(iterations["iterations"]),
                                             globals=globals())

        print(f"Average policy iteration maximum memory usage: {average_memory} MiB")
        print(f"Average policy iteration path length: {average_path_length}")
        print(f"Average policy iteration time taken: {policy_iteration_time_taken} seconds")

        memory_from_iterations = []
        path_length_from_iterations = []

        # Value iteration algorithm completion with memory and time taken being measured
        for _ in range(int(iterations["iterations"])):
            value_iteration_memory, value_iteration_path_to_target = memory_usage((value_iteration_algorithm,
                                                                                   (maze,), {}), retval=True)
            memory_from_iterations.append(max(value_iteration_memory))
            path_length_from_iterations.append(len(value_iteration_path_to_target) + 1)

        average_memory = statistics.mean(memory_from_iterations)
        average_path_length = statistics.mean(path_length_from_iterations)
        value_iteration_time_taken = timeit(stmt='value_iteration_algorithm(maze)',
                                            number=int(iterations["iterations"]),
                                            globals=globals())

        print(f"Average value iteration maximum memory usage: {average_memory} MiB")
        print(f"Average value iteration path length: {average_path_length}")
        print(f"Average value iteration time taken: {value_iteration_time_taken} seconds")

        # Add title and labels to the maze to show memory and path information
        label = textLabel(maze, f"Policy iteration maximum memory used",
                          f"{round(max(policy_iteration_memory), 4)} MiB")
        label.lab.configure(bg="grey", fg="black", font=('Trebuchet MS', 11), relief="raised")
        label.lab.pack_configure(expand=False, anchor='s')
        label = textLabel(maze, f"Value iteration maximum memory used",
                          f"{round(max(value_iteration_memory), 4)} MiB")
        label.lab.configure(bg="grey", fg="black", font=('Trebuchet MS', 11), relief="raised")
        label.lab.pack_configure(expand=False, anchor='s')
        label = textLabel(maze, 'Policy iteration path length', len(policy_iteration_path_to_target) + 1)
        label.lab.configure(bg="grey", fg="black", font=('Trebuchet MS', 11), relief="raised")
        label.lab.pack_configure(expand=False, anchor='s')
        label = textLabel(maze, 'Value iteration path length', len(value_iteration_path_to_target) + 1)
        label.lab.configure(bg="grey", fg="black", font=('Trebuchet MS', 11), relief="raised")
        label.lab.pack_configure(expand=False, anchor='s')
        label = textLabel(maze, 'Policy iteration time taken', f"{round(policy_iteration_time_taken, 4)}s")
        label.lab.configure(bg="grey", fg="black", font=('Trebuchet MS', 11), relief="raised")
        label.lab.pack_configure(expand=False, anchor='s')
        label = textLabel(maze, 'Value iteration time taken', f"{round(value_iteration_time_taken, 4)}s")
        label.lab.configure(bg="grey", fg="black", font=('Trebuchet MS', 11), relief="raised")
        label.lab.pack_configure(expand=False, anchor='s')
        maze._win.title(f"Search algorithms solving a {maze_rows['number of rows for the maze']}x"
                        f"{maze_columns['number of columns for the maze']} maze (Policy iteration is red, Value "
                        f"iteration is yellow)")

        # Agents for each search algorithm
        policy_iteration_path = agent(maze, footprints=True, color=COLOR.red)
        value_iteration_path = agent(maze, footprints=True, color=COLOR.yellow)

        # Create a trace of each agent
        maze.tracePath({policy_iteration_path: policy_iteration_path_to_target}, delay=75)
        maze.tracePath({value_iteration_path: value_iteration_path_to_target}, delay=75)

        # Run the maze
        maze.run()

    elif answer["algorithm_type"] == "Search and MDP algorithms":
        # A star algorithm completion with memory and time taken being measured
        for _ in range(int(iterations["iterations"])):
            a_star_memory, (a_star_maze_area_to_search, a_star_path_to_target) = memory_usage((a_star_algorithm,
                                                                                               (maze,), {}),
                                                                                              retval=True)
            memory_from_iterations.append(max(a_star_memory))
            search_space_from_iterations.append(len(a_star_maze_area_to_search) + 1)
            path_length_from_iterations.append(len(a_star_path_to_target) + 1)

        average_memory = statistics.mean(memory_from_iterations)
        average_search_space = statistics.mean(search_space_from_iterations)
        average_path_length = statistics.mean(path_length_from_iterations)
        a_star_time_taken = timeit(stmt='a_star_algorithm(maze)', number=int(iterations["iterations"]),
                                   globals=globals())

        print(f"Average A* maximum memory usage: {average_memory} MiB")
        print(f"Average A* path length: {average_path_length}")
        print(f"Average A* search space: {average_search_space}")
        print(f"Average A* time taken: {a_star_time_taken} seconds")

        memory_from_iterations = []
        search_space_from_iterations = []
        path_length_from_iterations = []

        # DFS algorithm completion with memory and time taken being measured
        for _ in range(int(iterations["iterations"])):
            dfs_memory, (dfs_maze_area_to_search, dfs_path_to_target) = memory_usage((dfs_algorithm,
                                                                                      (maze,), {}), retval=True)
            memory_from_iterations.append(max(dfs_memory))
            search_space_from_iterations.append(len(dfs_maze_area_to_search) + 1)
            path_length_from_iterations.append(len(dfs_path_to_target) + 1)

        average_memory = statistics.mean(memory_from_iterations)
        average_search_space = statistics.mean(search_space_from_iterations)
        average_path_length = statistics.mean(path_length_from_iterations)
        dfs_time_taken = timeit(stmt='dfs_algorithm(maze)', number=int(iterations["iterations"]),
                                globals=globals())

        print(f"Average DFS maximum memory usage: {average_memory} MiB")
        print(f"Average DFS path length: {average_path_length}")
        print(f"Average DFS search space: {average_search_space}")
        print(f"Average DFS time taken: {dfs_time_taken} seconds")

        memory_from_iterations = []
        search_space_from_iterations = []
        path_length_from_iterations = []

        # BFS algorithm completion with memory and time taken being measured
        for _ in range(int(iterations["iterations"])):
            bfs_memory, (bfs_maze_area_to_search, bfs_path_to_target) = memory_usage((bfs_algorithm,
                                                                                      (maze,), {}), retval=True)
            memory_from_iterations.append(max(bfs_memory))
            search_space_from_iterations.append(len(bfs_maze_area_to_search) + 1)
            path_length_from_iterations.append(len(bfs_path_to_target) + 1)

        average_memory = statistics.mean(memory_from_iterations)
        average_search_space = statistics.mean(search_space_from_iterations)
        average_path_length = statistics.mean(path_length_from_iterations)
        bfs_time_taken = timeit(stmt='bfs_algorithm(maze)', number=int(iterations["iterations"]),
                                globals=globals())

        print(f"Average BFS maximum memory usage: {average_memory} MiB")
        print(f"Average BFS path length: {average_path_length}")
        print(f"Average BFS search space: {average_search_space}")
        print(f"Average BFS time taken: {bfs_time_taken} seconds")

        memory_from_iterations = []
        search_space_from_iterations = []
        path_length_from_iterations = []

        # Policy iteration algorithm completion with memory and time taken being measured
        for _ in range(int(iterations["iterations"])):
            policy_iteration_memory, policy_iteration_path_to_target = memory_usage((policy_iteration_algorithm,
                                                                                     (maze,), {}), retval=True)
            memory_from_iterations.append(max(policy_iteration_memory))
            path_length_from_iterations.append(len(policy_iteration_path_to_target) + 1)

        average_memory = statistics.mean(memory_from_iterations)
        average_path_length = statistics.mean(path_length_from_iterations)
        policy_iteration_time_taken = timeit(stmt='policy_iteration_algorithm(maze)',
                                             number=int(iterations["iterations"]),
                                             globals=globals())

        print(f"Average policy iteration maximum memory usage: {average_memory} MiB")
        print(f"Average policy iteration path length: {average_path_length}")
        print(f"Average policy iteration time taken: {policy_iteration_time_taken} seconds")

        memory_from_iterations = []
        path_length_from_iterations = []

        # Value iteration algorithm completion with memory and time taken being measured
        for _ in range(int(iterations["iterations"])):
            value_iteration_memory, value_iteration_path_to_target = memory_usage((value_iteration_algorithm,
                                                                                   (maze,), {}), retval=True)
            memory_from_iterations.append(max(value_iteration_memory))
            path_length_from_iterations.append(len(value_iteration_path_to_target) + 1)

        average_memory = statistics.mean(memory_from_iterations)
        average_path_length = statistics.mean(path_length_from_iterations)
        value_iteration_time_taken = timeit(stmt='value_iteration_algorithm(maze)',
                                            number=int(iterations["iterations"]),
                                            globals=globals())

        print(f"Average value iteration maximum memory usage: {average_memory} MiB")
        print(f"Average value iteration path length: {average_path_length}")
        print(f"Average value iteration time taken: {value_iteration_time_taken} seconds")

        label = textLabel(maze, 'A* time taken', f"{round(a_star_time_taken, 4)}")
        label.lab.configure(bg="grey", fg="black", font=('Trebuchet MS', 15), relief="raised")
        label.lab.pack_configure(expand=False, anchor='s')
        label = textLabel(maze, 'DFS time taken', f"{round(dfs_time_taken, 4)}")
        label.lab.configure(bg="grey", fg="black", font=('Trebuchet MS', 15), relief="raised")
        label.lab.pack_configure(expand=False, anchor='s')
        label = textLabel(maze, 'BFS time taken', f"{round(bfs_time_taken, 4)}")
        label.lab.configure(bg="grey", fg="black", font=('Trebuchet MS', 15), relief="raised")
        label.lab.pack_configure(expand=False, anchor='s')
        maze._win.title(f"Search algorithms solving a {maze_rows['number of rows for the maze']}x"
                        f"{maze_columns['number of columns for the maze']} maze (A* is yellow, DFS is blue,"
                        f" BFS is red)")
        label = textLabel(maze, 'Policy iteration time taken', f"{round(policy_iteration_time_taken, 4)}s")
        label.lab.configure(bg="grey", fg="black", font=('Trebuchet MS', 15), relief="raised")
        label.lab.pack_configure(expand=False, anchor='s')
        label = textLabel(maze, 'Value iteration time taken', f"{round(value_iteration_time_taken, 4)}s")
        label.lab.configure(bg="grey", fg="black", font=('Trebuchet MS', 15), relief="raised")
        label.lab.pack_configure(expand=False, anchor='s')
        maze._win.title(f"Search algorithms solving a {maze_rows['number of rows for the maze']}x"
                        f"{maze_columns['number of columns for the maze']} maze (A* is blue, DFS is red, "
                        f"BFS is yellow, Policy iteration is green, Value iteration is white)")

        # Agents for each search algorithm
        a_star_path = agent(maze, footprints=True, color=COLOR.blue)
        dfs_path = agent(maze, footprints=True, color=COLOR.red)
        bfs_path = agent(maze, footprints=True, color=COLOR.yellow)
        policy_iteration_path = agent(maze, footprints=True, color=COLOR.green)
        value_iteration_path = agent(maze, footprints=True, color=COLOR.dark)

        # Create a trace of each agent
        maze.tracePath({a_star_path: a_star_path_to_target}, delay=75)
        maze.tracePath({dfs_path: dfs_path_to_target}, delay=75)
        maze.tracePath({bfs_path: bfs_path_to_target}, delay=75)
        maze.tracePath({policy_iteration_path: policy_iteration_path_to_target}, delay=75)
        maze.tracePath({value_iteration_path: value_iteration_path_to_target}, delay=75)

        # Run the maze
        maze.run()

# Exit the program!
elif answer["wish"] == "Exit":
    print(figlet_format("Goodbye!", justify='center', width=140))
    sys.exit()
