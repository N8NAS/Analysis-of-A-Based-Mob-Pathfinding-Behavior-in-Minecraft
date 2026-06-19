import math
from typing import List, Tuple, Dict, Optional

class Node:
    def __init__(self, x: int, y: int, terrain_type: str, elevation: int):
        self.x = x
        self.y = y
        self.terrain_type = terrain_type
        self.elevation = elevation

    def get_terrain_penalty(self) -> float:
        penalties = {
            'S': 0.0,
            'G': 0.0,
            '.': 0.0,
            'W': 8.0,
            'F': 16.0,
            'M': 8.0,
            'L': 32.0,
            '#': float('inf')
        }
        return penalties.get(self.terrain_type, 0.0)

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f"Node({self.x}, {self.y}, {self.terrain_type}, e={self.elevation})"


class Grid:
    def __init__(self, width: int, height: int, nodes: List[List[Node]], start_node: Node, goal_node: Node):
        self.width = width
        self.height = height
        self.nodes = nodes
        self.start_node = start_node
        self.goal_node = goal_node

    def get_node(self, x: int, y: int) -> Optional[Node]:
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.nodes[y][x]
        return None

    def get_neighbors(self, node: Node) -> List[Tuple[Node, float]]:
        neighbors = []
        
        directions = [
            (0, -1, False),
            (0, 1, False),
            (1, 0, False),
            (-1, 0, False),
            (1, -1, True),
            (-1, -1, True),
            (1, 1, True),
            (-1, 1, True)
        ]

        for dx, dy, is_diagonal in directions:
            nx, ny = node.x + dx, node.y + dy
            neighbor = self.get_node(nx, ny)
            
            if neighbor is None or neighbor.terrain_type == '#':
                continue

            delta_y = neighbor.elevation - node.elevation
            elevation_penalty = 0.0
            
            if delta_y > 1:
                continue
            elif delta_y < -3:
                continue
            elif delta_y == 1:
                elevation_penalty = 1.0
            elif 0 >= delta_y >= -3:
                elevation_penalty = 0.0

            terrain_penalty = neighbor.get_terrain_penalty()
            
            adjacency_penalty = 0.0
            if neighbor.terrain_type not in ['L', '#']:
                for adx, ady, _ in directions:
                    adj_node = self.get_node(nx + adx, ny + ady)
                    if adj_node and adj_node.terrain_type == 'L':
                        adjacency_penalty = 8.0
                        break
            
            base_cost = 1.414 if is_diagonal else 1.0
            
            total_cost = base_cost + terrain_penalty + elevation_penalty + adjacency_penalty
            neighbors.append((neighbor, total_cost))
            
        return neighbors
