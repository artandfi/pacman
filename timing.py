from cProfile import Profile
from pstats import Stats, SortKey
from maze import Maze
from solver import MazeSolverAStar, MazeSolverGreedy


def profile(solver):
    print(type(solver).__name__)

    with Profile() as profile:
        solver.solve()
    
    stats = Stats(profile)
    stats.sort_stats(SortKey.TIME)
    print(stats.get_print_list([32]))


def main():
    maze = Maze(50, 50)
    maze.generate()
    solver_a_star = MazeSolverAStar(maze)
    solver_greedy = MazeSolverGreedy(maze)

    profile(solver_a_star)
    profile(solver_greedy)


if __name__ == "__main__":
    main()
