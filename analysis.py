from typing import Hashable
from diktyonphi import Graph, Node
import heapq

def bfs(graph: Graph, start_id):
    visited = set()
    queue = [start_id]
    print(f"BFS od uzlu {start_id}:")

    while queue:
        current_id = queue.pop(0)
        if current_id in visited:
            continue
        visited.add(current_id)
        print(f"  {current_id}")
        node = graph.node(current_id)
        for neighbor_id in node.neighbor_ids:
            if neighbor_id not in visited:
                edge = node.to(neighbor_id)
                edge["color"] = "green"
                edge["penwidth"] = 2
                queue.append(neighbor_id)

def dfs(graph: Graph, start_id, visited=None):
    if visited is None:
        visited = set()
        print(f"DFS od uzlu {start_id}:")

    if start_id in visited:
        return
    visited.add(start_id)
    print(f"  {start_id}")
    node = graph.node(start_id)
    for neighbor_id in node.neighbor_ids:
        if neighbor_id not in visited:
            edge = node.to(neighbor_id)
            edge["color"] = "purple"
            edge["penwidth"] = 2
            dfs(graph, neighbor_id, visited)

def dijkstra_path(graph: Graph, start_id:Hashable, end_id:Hashable):
    print(f"Hledání nejkratší cesty z {start_id} do {end_id} pomocí Dijkstrova algoritmu:")
    distances = {node.id: float('inf') for node in graph}
    previous = {node.id: None for node in graph}
    distances[start_id] = 0

    queue = [(0, start_id)]

    while queue:
        current_dist, current_id = heapq.heappop(queue)
        if current_id == end_id:
            break
        node = graph.node(current_id)
        for neighbor_id in node.neighbor_ids:
            edge = node.to(neighbor_id)
            weight = edge._attrs.get("weight", 1)
            new_dist = current_dist + weight
            if new_dist < distances[neighbor_id]:
                distances[neighbor_id] = new_dist
                previous[neighbor_id] = current_id
                heapq.heappush(queue, (new_dist, neighbor_id))

    path = []
    current = end_id
    while current:
        path.insert(0, current)
        current = previous[current]

    if not path or path[0] != start_id:
        print("Cesta neexistuje.")
        return

    print("  → ".join(path))
    print(f"  Délka cesty: {distances[end_id]}")

    for i in range(len(path) - 1):
        src = graph.node(path[i])
        dst = graph.node(path[i+1])
        edge = src.to(dst)
        edge["color"] = "blue"
        edge["penwidth"] = 3
