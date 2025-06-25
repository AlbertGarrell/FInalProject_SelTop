from typing import Dict, Tuple, Any
import networkx as nx

def bellman_ford(graph: nx.DiGraph, source: Any) -> Tuple[Dict[Any, float], Dict[Any, Any]]:
    """
    Bellman-Ford algorithm to compute shortest paths from a source node.

    Parameters:
        graph (nx.DiGraph): A directed graph with edge weights.
        source (Any): The source node.

    Returns:
        dist (Dict[Any, float]): Shortest distances from the source.
        pred (Dict[Any, Any]): Predecessor of each node in the path.
        
    Raises:
        ValueError: If a negative-weight cycle is detected.
    """
    dist = {node: float('inf') for node in graph.nodes}
    pred = {node: None for node in graph.nodes}
    dist[source] = 0

    # Relax edges repeatedly
    for _ in range(len(graph.nodes) - 1): # The shortest path between any two nodes in a graph can have at most |V| − 1 edges
        for u, v, data in graph.edges(data=True):
            weight = data.get('weight', 1) # Default weight is 1 if not specified
            if dist[u] + weight < dist[v]:
                dist[v] = dist[u] + weight
                pred[v] = u

    # Check for negative-weight cycles
    for u, v, data in graph.edges(data=True):
        weight = data.get('weight', 1) # Default weight is 1 if not specified
        if dist[u] + weight < dist[v]:
            raise ValueError("Graph contains a negative-weight cycle")

    return dist, pred
