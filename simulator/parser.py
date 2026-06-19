from typing import Tuple
from simulator.models import Node, Grid

def parse_map(filepath: str) -> Grid:
    with open(filepath, 'r') as f:
        lines = [line.strip() for line in f.readlines()]

    # Split lines into terrain and elevation matrices
    terrain_lines = []
    elevation_lines = []
    
    parsing_terrain = False
    parsing_elevation = False
    
    for line in lines:
        if not line:
            continue
        if line.startswith("# Terrain Matrix"):
            parsing_terrain = True
            parsing_elevation = False
            continue
        elif line.startswith("# Elevation Matrix"):
            parsing_terrain = False
            parsing_elevation = True
            continue
            
        # Ignore other comments
        if line.startswith("#") and not (parsing_terrain or parsing_elevation):
            continue
            
        if parsing_terrain:
            terrain_lines.append(line)
        elif parsing_elevation:
            elevation_lines.append(line)

    if not terrain_lines or not elevation_lines:
        raise ValueError("Map file must contain both terrain and elevation matrices.")

    if len(terrain_lines) != len(elevation_lines):
        raise ValueError("Terrain and Elevation matrices must have the same height.")

    height = len(terrain_lines)
    
    terrain_matrix = []
    for line in terrain_lines:
        row = line.split()
        terrain_matrix.append(row)

    elevation_matrix = []
    for line in elevation_lines:
        row = [int(val) for val in line.split()]
        elevation_matrix.append(row)

    if len(terrain_matrix) == 0:
        raise ValueError("Matrices cannot be empty.")

    width = len(terrain_matrix[0])

    for y in range(height):
        if len(terrain_matrix[y]) != width or len(elevation_matrix[y]) != width:
            raise ValueError("Terrain and Elevation matrices must have the same dimensions and be rectangular.")

    nodes = []
    start_node = None
    goal_node = None

    for y in range(height):
        row_nodes = []
        for x in range(width):
            terrain = terrain_matrix[y][x]
            elevation = elevation_matrix[y][x]
            
            node = Node(x, y, terrain, elevation)
            row_nodes.append(node)
            
            if terrain == 'S':
                if start_node is not None:
                    raise ValueError("Multiple start nodes found.")
                start_node = node
            elif terrain == 'G':
                if goal_node is not None:
                    raise ValueError("Multiple goal nodes found.")
                goal_node = node
                
        nodes.append(row_nodes)

    if start_node is None or goal_node is None:
        raise ValueError("Map must contain exactly one Start (S) and one Goal (G).")

    return Grid(width, height, nodes, start_node, goal_node)
