"""
This is the main program of the a-maze-ing project
"""
import sys

from print_maze import print_ascii_maze
from config import parse_config
from maze_generator import generate_maze
from path_finder import bfs

# The Function That Manage The Interactive Menu
def main_menu(maze, ENTRY, EXIT, output_file):
    print_ascii_maze(maze)
    path = bfs(maze, ENTRY, EXIT)
    print(f"\nPath of the maze: {path}")
    str_path = "".join(path)
    organize_output_file(
        maze,
        output_file,
        str_path,
        ENTRY,
        EXIT
    )
    while True:
        print("\n=== Main Menu ===")
        print("1. Re-generate a new maze")
        print("2. Show/Hide path from entry to exit")
        print("3. Rotate maze colors")
        print("4. Quit")

        try:
            choice = input("Enter your choice (1-3): ").strip()
        except BaseException :
            print("\nDetected Key Enterruption Exiting gracefully...")
            exit(0)

        if choice == "1":
            print("Maze re-generation started...")
            maze = generate_maze() # here is the maze 2d list of ints represented
            # print_maze(maze) do your fucking work here
        elif choice == "2":
            pass # also this is your fucking work
        elif choice == "3":
            pass
            # also this is your fucking role idiot
        elif choice == "4":
            print("Goodbye!") # let me do this.
            break
        else:
            print("Invalid choice. Try again.")

# Create The Output File With Required Elements (maze hex, entry, exit, )
def organize_output_file(
    grid: list[list[int]],
    output_file: str,
    path: str,
    entry: tuple[int, int],
    exit_: tuple[int, int],
) -> None:
    content = ""

    for row in grid:
        for column in row:
            content += format(column, "X")
        content += "\n"

    try:
        with open(output_file, "w") as file:
            file.write(content)
            file.write(f"\n{entry[0]},{entry[1]}\n")
            file.write(f"{exit_[0]},{exit_[1]}\n")
            file.write(path)
    except PermissionError:
        print("You don't have permission to write to this file.")


def create_entry_exit(grid, height, width):
    grid[0][0] &= ~1
    grid[height - 1][width - 1] &= ~4


if __name__ == "__main__":

    # Check that just one argument is given in command line.
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)

    try:
        config_file = sys.argv[1]
    except IndexError:
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)

    try:
        config = parse_config(config_file)
    except Exception as e:
        print(f"Config error: {e}")
        sys.exit(1)

    WIDTH = config.width
    HEIGHT = config.height
    ENTRY = config.entry
    EXIT = config.exit
    PERFECT = config.perfect
    SEED = config.seed
    output_file = config.output_file

    maze_nature = "Perfect" if PERFECT else "Imperfect"


    print(f"Generating {WIDTH}x{HEIGHT} {maze_nature} (seed={SEED})...\n")
    maze = generate_maze(WIDTH, HEIGHT, seed=SEED, perfect=PERFECT)
    main_menu(maze, ENTRY, EXIT, output_file)