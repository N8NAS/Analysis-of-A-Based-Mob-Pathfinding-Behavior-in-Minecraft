# Analysis-of-A--Based-Mob-Pathfinding-Behavior-in-Minecraft
Python Algorithm Comparison Program

This program is a pathfinding simulator that emulates grid movement mechanics similar to the game Minecraft. It is designed to test, visualize, and compare the performance of four classic pathfinding algorithms.

## Overview

The simulator evaluates the pathfinding performance from a Start point (`S`) to a Goal point (`G`) based on realistic grid parameters. 
The map is constructed using two layers of matrices:
1. **Terrain Matrix:** Defines the type of terrain being traversed.
2. **Elevation Matrix:** Defines the elevation (height) of the blocks, which introduces time penalties for jumping and prevents the "zombie" from jumping too high or falling too far.

Different block types have unique obstacles and movement costs:
- `.` (Grass/Dirt) / `S` (Start) / `G` (Goal): Normal terrain.
- `W` (Water): Slows down movement.
- `F` (Fire): Incurs a high cost penalty if stepped on directly.
- `L` (Lava): Has the highest cost penalty, and also spreads **heat** (an adjacency danger penalty) if the agent walks right next to it.
- `M` (Mud): Slows down the agent's movement speed.
- `#` (Wall/Bedrock): An absolute obstacle that **cannot be passed**.

The movement simulation also calculates traversal time by mimicking the actual chase speed of a Minecraft Zombie.

The algorithms tested and compared in this simulator are:
1. **A* (A-Star)**
2. **Dijkstra**
3. **BFS (Breadth-First Search)**
4. **GBFS (Greedy Best-First Search)**

## Prerequisites

Before running the program, ensure your system has **Python 3.x** installed along with the `matplotlib` visualization library.
You can install it via the terminal or Command Prompt using the following command:

```bash
pip install matplotlib
```

## How to Run

Open your terminal and navigate to the project directory. To run the simulation, execute the `main.py` file using the `--map` argument followed by the text file name of the map.

**Example Commands:**

```bash
# Run the basic obstacle map
python main.py --map clear.txt

# Run the U-shaped map
python main.py --map U.txt

# Run the branching graph-like map
python main.py --map GraphLike.txt

# Run the complex maze map
python main.py --map maze.txt
```

## Outputs

Once the program finishes running, it will generate the following outputs:
1. **Terminal Table**: Directly prints a performance comparison table of each algorithm (including Nodes Expanded, Total Cost, Path Length, Execution Time, and Estimated Traversal Time).
2. **Summary Text File (`comparison_[mapname].txt`)**: Exports the terminal comparison table into a `.txt` file for documentation.
3. **Visual Graphs (`result_[Algorithm]_[mapname].png`)**: The program automatically draws and saves the resulting path visuals as PNG images.
   - The area evaluated by the algorithm is highlighted in semi-transparent light blue.
   - The final successful path is highlighted with a thick semi-transparent lime green line, keeping the original terrain visible underneath.

## Contributor

Nathan Adhika Santosa/13524041
