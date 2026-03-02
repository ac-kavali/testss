import sys

from setuptools.command.setopt import config_file

from tools import print_ascii_maze
from config import parse_config
from maze_generator import generate_maze, entry_exit_in_42
from path_finder import bfs


def maze_to_hex_string(grid: list[list[int]]) -> str:
    """
    Convert the maze grid to the output file format.
    One hex digit per cell, one row per line.

    Returns:
        A string where each line is one row of the maze (uppercase hex digits).
    """
    lines = []
    for row in grid:
        hex_row = ""  # empty string for this row
        for cell in row:
            hex_row += format(cell, 'X')  # add the hex representation to the string
        lines.append(hex_row)  # append the full string to lines
    return "\n".join(lines)


def create_entry_exit(grid, height , width):
    grid[0][0] &= ~1
    grid[height-1][width-1] &= ~4


if __name__ == "__main__":

    # Check That Just One Argument Given In Command Line.
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
        exit(1)

    WIDTH = config.width
    HEIGHT = config.height
    ENTRY = config.entry
    EXIT = config.exit
    PERFECT = config.perfect
    SEED= config.seed
    output_file = config.output_file

    maze_nature = "Perfect" if PERFECT else "Imperfect"

    if entry_exit_in_42(ENTRY, EXIT, WIDTH, HEIGHT):
        print("Error: Entry/Exit coordinates overlap with the '42' pattern "
              "(fully closed cells).Please choose different entry/exit coordinates.")
        exit(1)

    print(f"Generating {WIDTH}x{HEIGHT} {maze_nature} (seed={SEED})...\n")
    maze = generate_maze(WIDTH, HEIGHT, seed=SEED, perfect=PERFECT)

    print("=== ASCII view ===")
    print_ascii_maze(maze)

    print("\n=== Hex output (one row per line) ===")
    print(maze_to_hex_string(maze))

    print(f"\nPath of the maze:{bfs(maze, ENTRY, EXIT)}")
