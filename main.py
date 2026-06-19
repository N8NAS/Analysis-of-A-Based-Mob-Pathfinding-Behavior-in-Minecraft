import time
import argparse
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from simulator.parser import parse_map
from simulator.algorithms import AStar, Dijkstra, BFS, GBFS

def draw_grid(grid, path, expanded_nodes, algorithm_name, execution_time_ms, nodes_expanded, path_cost, map_name):
    color_map = {
        '.': 'white',
        '#': 'black',
        'W': 'blue',
        'F': 'orange',
        'M': 'darkred',
        'L': 'red',
        'S': 'green',
        'G': 'yellow'
    }
    
    fig, ax = plt.subplots(figsize=(max(5, grid.width * 0.5), max(5, grid.height * 0.5)))
    ax.set_xlim(0, grid.width)
    ax.set_ylim(0, grid.height)
    ax.set_aspect('equal')
    ax.invert_yaxis()
    
    for y in range(grid.height):
        for x in range(grid.width):
            node = grid.nodes[y][x]
            color = color_map.get(node.terrain_type, 'white')
            rect = patches.Rectangle((x, y), 1, 1, linewidth=0.5, edgecolor='gray', facecolor=color)
            ax.add_patch(rect)
            
    if expanded_nodes:
        for ex, ey in expanded_nodes:
            if (ex, ey) != (grid.start_node.x, grid.start_node.y) and (ex, ey) != (grid.goal_node.x, grid.goal_node.y):
                terrain_color = color_map.get(grid.nodes[ey][ex].terrain_type, 'white')
                rect = patches.Rectangle((ex, ey), 1, 1, linewidth=0.5, edgecolor='gray', facecolor='lightblue', alpha=0.5)
                ax.add_patch(rect)
                rect2 = patches.Rectangle((ex, ey), 1, 1, linewidth=0.5, edgecolor='gray', facecolor=terrain_color, alpha=0.5)
                ax.add_patch(rect2)

    path_len = 0
    if path:
        path_len = len(path)
        for px, py in path:
            if (px, py) != (grid.start_node.x, grid.start_node.y) and (px, py) != (grid.goal_node.x, grid.goal_node.y):
                terrain_color = color_map.get(grid.nodes[py][px].terrain_type, 'white')
                rect = patches.Rectangle((px, py), 1, 1, linewidth=0.5, edgecolor='gray', facecolor='lime', alpha=0.5)
                ax.add_patch(rect)
                rect2 = patches.Rectangle((px, py), 1, 1, linewidth=0.5, edgecolor='gray', facecolor=terrain_color, alpha=0.5)
                ax.add_patch(rect2)
                
    title = f"{algorithm_name} | Time: {execution_time_ms:.4f}ms | Expanded: {nodes_expanded} | Cost: {path_cost:.4f} | Length: {path_len}"
    plt.title(title)
    
    base_map_name = os.path.basename(map_name)
    safe_algo_name = algorithm_name.replace('*', 'Star')
    filename = f"result_{safe_algo_name}_{base_map_name}.png"
    plt.savefig(filename, bbox_inches='tight')
    plt.close()

ZOMBIE_BASE_SPEED = 2.0

TERRAIN_SPEED_MULTIPLIER = {
    '.': 1.0,
    'S': 1.0,
    'G': 1.0,
    'W': 0.2,
    'F': 0.5,
    'M': 0.7,
    'L': 0.3,
}

def calculate_traversal_time(path, grid):
    if not path or len(path) < 2:
        return 0.0

    total_time_seconds = 0.0

    for i in range(len(path) - 1):
        x1, y1 = path[i]
        x2, y2 = path[i+1]
        
        node_A = grid.nodes[y1][x1]
        node_B = grid.nodes[y2][x2]
        
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        
        distance = 1.414 if dx != 0 and dy != 0 else 1.0
        
        effective_speed = ZOMBIE_BASE_SPEED * TERRAIN_SPEED_MULTIPLIER.get(node_B.terrain_type, 1.0)
        step_time = distance / effective_speed
        
        delta_elevation = node_B.elevation - node_A.elevation
        if delta_elevation == 1:
            step_time += 0.25
            
        total_time_seconds += step_time

    traversal_time_ms = total_time_seconds * 1000.0
    return traversal_time_ms

def run_benchmark(algorithm_name, algorithm_instance, grid, map_name):
    print(f"--- Running {algorithm_name} ---")
    
    start_time = time.perf_counter()
    path, cost, nodes_expanded = algorithm_instance.find_path(grid)
    end_time = time.perf_counter()
    
    execution_time_ms = (end_time - start_time) * 1000
    traversal_time_ms = calculate_traversal_time(path, grid) if path else 0.0
    time_to_target_ms = execution_time_ms + traversal_time_ms
    
    print(f"Execution Time:   {execution_time_ms:.4f} ms")
    if path:
        print(f"Path Cost:        {cost:.4f}")
        print(f"Path Length:      {len(path)} nodes")
        print(f"Nodes Expanded:   {nodes_expanded}")
        print(f"Traversal Time:   {traversal_time_ms:.4f} ms")
        print(f"Time to Target:   {time_to_target_ms:.4f} ms")
        print(f"Final Path Coordinates: {path}")
    else:
        print("Result: No valid path found.")
        print(f"Nodes Expanded:   {nodes_expanded}")
        print(f"Traversal Time:   {traversal_time_ms:.4f} ms")
        print(f"Time to Target:   {time_to_target_ms:.4f} ms")
    print("-" * 40 + "\n")
    
    expanded_nodes_list = getattr(algorithm_instance, 'expanded_nodes', [])
    draw_grid(grid, path, expanded_nodes_list, algorithm_name, execution_time_ms, nodes_expanded, cost, map_name)
    
    path_len = len(path) if path else 0
    return {
        'name': algorithm_name,
        'expanded': nodes_expanded,
        'cost': cost,
        'length': path_len,
        'exec_time': execution_time_ms,
        'traversal': traversal_time_ms,
        'target_time': time_to_target_ms
    }

def main():
    parser = argparse.ArgumentParser(description="Minecraft Pathfinding Simulator")
    parser.add_argument("--map", type=str, default="map.txt", help="Path to the map file")
    args = parser.parse_args()

    print(f"Loading map from {args.map}...")
    try:
        grid = parse_map(args.map)
    except Exception as e:
        print(f"Error loading map: {e}")
        return

    print(f"Grid loaded: {grid.width}x{grid.height}")
    print(f"Start Node: {grid.start_node}")
    print(f"Goal Node: {grid.goal_node}")
    print("\n" + "=" * 40 + "\n")

    algorithms = [
        ("A*", AStar()),
        ("Dijkstra", Dijkstra()),
        ("BFS", BFS()),
        ("GBFS", GBFS())
    ]

    results = []
    for name, algo in algorithms:
        res = run_benchmark(name, algo, grid, args.map)
        results.append(res)
        
    print("\n" + "=" * 100)
    print("ALGORITHM COMPARISON SUMMARY")
    print("=" * 100)
    print(f"{'Algorithm':<12} | {'Nodes Expanded':<16} | {'Path Cost':<12} | {'Path Length':<13} | {'Exec Time (ms)':<16} | {'Traversal (ms)':<16} | {'Time to Target (ms)'}")
    print("-" * 100)
    for r in results:
        print(f"{r['name']:<12} | {r['expanded']:<16} | {r['cost']:<12.4f} | {r['length']:<13} | {r['exec_time']:<16.4f} | {r['traversal']:<16.4f} | {r['target_time']:.4f}")
    print("=" * 100)

    map_basename = os.path.basename(args.map)
    map_name_no_ext, _ = os.path.splitext(map_basename)
    filename = f"comparison_{map_name_no_ext}.txt"
    with open(filename, 'w') as f:
        f.write("=" * 100 + "\n")
        f.write("ALGORITHM COMPARISON SUMMARY\n")
        f.write("=" * 100 + "\n")
        f.write(f"{'Algorithm':<12} | {'Nodes Expanded':<16} | {'Path Cost':<12} | {'Path Length':<13} | {'Exec Time (ms)':<16} | {'Traversal (ms)':<16} | {'Time to Target (ms)'}\n")
        f.write("-" * 100 + "\n")
        for r in results:
            f.write(f"{r['name']:<12} | {r['expanded']:<16} | {r['cost']:<12.4f} | {r['length']:<13} | {r['exec_time']:<16.4f} | {r['traversal']:<16.4f} | {r['target_time']:.4f}\n")
        f.write("=" * 100 + "\n")

if __name__ == "__main__":
    main()
