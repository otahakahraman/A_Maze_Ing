*This project has been created as part of the 42 curriculum by okahrama, btop.*

# A-Maze-ing

## Description

A-Maze-ing generates a maze from a configuration file, writes it in hexadecimal wall-bit format, and displays it in an interactive terminal view. It supports perfect mazes and braided mazes with extra routes, a 42 pattern, and a shortest-path solution.

## Instructions

Requirements: Python 3.10 or newer. The application has no third-party runtime dependencies.

From the repository root, run:

```bash
python a_maze_ing.py config.txt
```

Use `--no-visualize` to generate and save the maze without opening the interactive view:

```bash
python a_maze_ing.py config.txt --no-visualize
```

The visualizer accepts `s` to show or hide the solution, `c` to change wall color, and `q` to quit. The generated file is written to the path specified by `OUTPUT_FILE`.

Build the reusable `mazegen-*` wheel at the repository root with:

```bash
python -m pip install build
python -m build --wheel --outdir .
```

## Configuration

The config file uses one `KEY=VALUE` setting per line. All settings are required:

```text
WIDTH=11
HEIGHT=21
SEED=42
ENTRY=(0,0)
EXIT_COORD=(10,20)
OUTPUT_FILE=masze.txt
PERFECT=false
```

- `WIDTH`, `HEIGHT`: maze dimensions in cells.
- `SEED`: integer seed for repeatable generation.
- `ENTRY`, `EXIT_COORD`: zero-based `(x,y)` cell coordinates, inside the grid and different from each other.
- `OUTPUT_FILE`: destination filename for the generated maze.
- `PERFECT`: `true` creates a maze with a unique route structure; `false` opens additional passages to add loops.

The 42 pattern is applied when the grid is large enough to contain it. For Pac-Man analysis, use a grid with clear space around the pattern (at least 9 by 7 in the tested layouts) and place the entry and exit on open cells.

## Maze generation algorithm

The generator uses randomized depth-first search with an explicit stack (iterative backtracking). It starts at the entry, chooses a random unvisited neighbour, removes the shared wall, and backtracks when it reaches a cell with no unvisited neighbours. A seeded random number generator makes a configuration reproducible. In non-perfect mode, additional walls are removed to create loops, then fully open 3 by 3 areas are scanned and one internal passage is closed in each detected area.

Depth-first backtracking is compact, easy to adapt to a grid, and naturally produces a connected maze with no loops before extra passages are added. Breadth-first search is used separately to find a shortest route from entry to exit.

## Reusable generator module

The standalone module is [`mazegen.py`](mazegen.py) and is included in the pip-installable `mazegen-a-maze-ing` distribution. It has no project-specific imports or third-party runtime dependencies.

```python
from mazegen import MazeGenerator

generator = MazeGenerator(width=20, height=15, seed=42)
generator.generator(x=0, y=0, perfect=False)

maze = generator.grid  # rows of integer wall masks
solution = generator.find_short_path((0, 0), (19, 14))  # N/E/S/W string
```

Change `width`, `height`, and `seed` to customize the maze. The grid is the in-memory structure, not the exported text file: each cell is an integer whose N/E/S/W wall bits are 1/2/4/8. The solution is a shortest route from entry to exit. `maze_generator/generator.py` re-exports the same class for the main application.

## Team and project management

- **okahrama**: maze generation, 42 pattern, integration, and debugging.
- **btop**: configuration parsing and terminal visualization.

We planned to build the project in stages: parse and validate configuration, generate and export a maze, then add visualization and validation. During development, we refined the 42 placement and added checks for Pac-Man playability and oversized open areas. Splitting parsing, generation, writing, and display into modules worked well. Future work could improve automated regression coverage across more sizes and seeds.

Tools used: Python, Git, the terminal, setuptools/build, and the maze analyzer during development.

## Resources 

- [Python documentation](https://docs.python.org/3/)
- [Python `random` documentation](https://docs.python.org/3/library/random.html)
- [Python `collections.deque` documentation](https://docs.python.org/3/library/collections.html#collections.deque)
- [Depth-first search](https://en.wikipedia.org/wiki/Depth-first_search) and [breadth-first search](https://en.wikipedia.org/wiki/Breadth-first_search)

## AI Usage
ChatGPT/Codex and Claude AI were used to explain Python concepts, suggest and review debugging changes in configuration parsing, maze generation, output, and validation, and help draft this README. The team reviewed and integrated suggestions. AI did not replace the team's implementation decisions or final verification.
