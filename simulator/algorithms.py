import math
import heapq
from collections import deque
from typing import List, Tuple, Dict, Optional
from simulator.models import Node, Grid

class Pathfinder:
    def find_path(self, grid: Grid) -> Tuple[Optional[List[Tuple[int, int]]], float, int]:
        """
        Finds a path from grid.start_node to grid.goal_node.
        Returns a tuple: (path_coordinates, total_cost, nodes_expanded).
        If no path is found, returns (None, 0.0, nodes_expanded).
        """
        raise NotImplementedError

def euclidean_distance(n1: Node, n2: Node) -> float:
    return math.sqrt((n1.x - n2.x)**2 + (n1.y - n2.y)**2)

class AStar(Pathfinder):
    def __init__(self, use_heuristic: bool = True):
        self.use_heuristic = use_heuristic

    def find_path(self, grid: Grid) -> Tuple[Optional[List[Tuple[int, int]]], float, int]:
        self.expanded_nodes = []
        open_set = []
        heapq.heappush(open_set, (0.0, 0, grid.start_node)) # (f_score, tie_breaker, node)
        
        came_from: Dict[Node, Tuple[Node, float]] = {} # node -> (parent_node, cost_from_parent)
        
        g_score: Dict[Node, float] = {grid.start_node: 0.0}
        f_score: Dict[Node, float] = {grid.start_node: self._h(grid.start_node, grid.goal_node)}
        
        tie_breaker = 0
        nodes_expanded = 0
        
        while open_set:
            _, _, current = heapq.heappop(open_set)
            nodes_expanded += 1
            self.expanded_nodes.append((current.x, current.y))
            
            if current == grid.goal_node:
                path, cost = self._reconstruct_path(came_from, current)
                return path, cost, nodes_expanded
                
            for neighbor, cost in grid.get_neighbors(current):
                tentative_g_score = g_score[current] + cost
                
                if tentative_g_score < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = (current, cost)
                    g_score[neighbor] = tentative_g_score
                    f = tentative_g_score + self._h(neighbor, grid.goal_node)
                    f_score[neighbor] = f
                    
                    tie_breaker += 1
                    heapq.heappush(open_set, (f, tie_breaker, neighbor))
                    
        return None, 0.0, nodes_expanded

    def _h(self, node: Node, goal: Node) -> float:
        if self.use_heuristic:
            return euclidean_distance(node, goal)
        return 0.0

    def _reconstruct_path(self, came_from: Dict[Node, Tuple[Node, float]], current: Node) -> Tuple[List[Tuple[int, int]], float]:
        path = [(current.x, current.y)]
        total_cost = 0.0
        
        while current in came_from:
            parent, cost_from_parent = came_from[current]
            total_cost += cost_from_parent
            current = parent
            path.append((current.x, current.y))
            
        path.reverse()
        return path, total_cost

class Dijkstra(AStar):
    def __init__(self):
        super().__init__(use_heuristic=False)

class BFS(Pathfinder):
    def find_path(self, grid: Grid) -> Tuple[Optional[List[Tuple[int, int]]], float, int]:
        self.expanded_nodes = []
        queue = deque([grid.start_node])
        came_from: Dict[Node, Tuple[Node, float]] = {}
        visited = set([grid.start_node])
        nodes_expanded = 0
        
        while queue:
            current = queue.popleft()
            nodes_expanded += 1
            self.expanded_nodes.append((current.x, current.y))
            
            if current == grid.goal_node:
                path, cost = self._reconstruct_path(came_from, current)
                return path, cost, nodes_expanded
                
            for neighbor, cost in grid.get_neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    came_from[neighbor] = (current, cost)
                    queue.append(neighbor)
                    
        return None, 0.0, nodes_expanded

    def _reconstruct_path(self, came_from: Dict[Node, Tuple[Node, float]], current: Node) -> Tuple[List[Tuple[int, int]], float]:
        path = [(current.x, current.y)]
        total_cost = 0.0
        
        while current in came_from:
            parent, cost_from_parent = came_from[current]
            total_cost += cost_from_parent
            current = parent
            path.append((current.x, current.y))
            
        path.reverse()
        return path, total_cost

class GBFS(Pathfinder):
    def find_path(self, grid: Grid) -> Tuple[Optional[List[Tuple[int, int]]], float, int]:
        self.expanded_nodes = []
        open_set = []
        heapq.heappush(open_set, (self._h(grid.start_node, grid.goal_node), 0, grid.start_node))
        
        came_from: Dict[Node, Tuple[Node, float]] = {}
        visited = set([grid.start_node])
        
        tie_breaker = 0
        nodes_expanded = 0
        
        while open_set:
            _, _, current = heapq.heappop(open_set)
            nodes_expanded += 1
            self.expanded_nodes.append((current.x, current.y))
            
            if current == grid.goal_node:
                path, cost = self._reconstruct_path(came_from, current)
                return path, cost, nodes_expanded
                
            for neighbor, cost in grid.get_neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    came_from[neighbor] = (current, cost)
                    tie_breaker += 1
                    heapq.heappush(open_set, (self._h(neighbor, grid.goal_node), tie_breaker, neighbor))
                    
        return None, 0.0, nodes_expanded

    def _h(self, node: Node, goal: Node) -> float:
        return euclidean_distance(node, goal)

    def _reconstruct_path(self, came_from: Dict[Node, Tuple[Node, float]], current: Node) -> Tuple[List[Tuple[int, int]], float]:
        path = [(current.x, current.y)]
        total_cost = 0.0
        
        while current in came_from:
            parent, cost_from_parent = came_from[current]
            total_cost += cost_from_parent
            current = parent
            path.append((current.x, current.y))
            
        path.reverse()
        return path, total_cost
