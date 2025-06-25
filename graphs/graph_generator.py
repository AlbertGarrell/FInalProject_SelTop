import networkx as nx
import random

def create_simple_graph():
    """
    Creates a toy graph:
        s → a (2)
        s → b (4)
        a → b (-3)
    Returns:
        G (nx.DiGraph): The graph
    """
    G = nx.DiGraph()
    G.add_edge('s', 'a', weight=2)
    G.add_edge('s', 'b', weight=4)
    G.add_edge('a', 'b', weight=-3)
    return G

def create_bigger_toy_graph():
    """
    Creates a directed graph with 5 nodes and some negative edges, but no negative cycles.
    Structure:
        0 → 1 (weight = 2)
        1 → 2 (weight = -3)
        2 → 3 (weight = 2)
        3 → 4 (weight = -1)
        4 → 2 (weight = 1)
        0 → 3 (weight = 4)
    Returns:
        G (nx.DiGraph): The graph
    """
    G = nx.DiGraph()
    G.add_edge(0, 1, weight=2)
    G.add_edge(1, 2, weight=-3)
    G.add_edge(2, 3, weight=2)
    G.add_edge(3, 4, weight=-1)
    G.add_edge(4, 2, weight=1)
    G.add_edge(0, 3, weight=4)
    return G

def create_layered_toy_graph():
    G = nx.DiGraph()
    G.add_edge(0, 1, weight=2)
    G.add_edge(1, 2, weight=-3)
    G.add_edge(2, 3, weight=2)
    G.add_edge(1, 3, weight=2)
    G.add_edge(3, 4, weight=4)
    G.add_edge(3, 5, weight=1)
    G.add_edge(4, 5, weight=-4)
    G.add_edge(5, 1, weight=1)
    return G


def generate_random_graph(n_nodes: int = 400, edge_prob: float = 0.1, weight_range=(-10, 10), allow_negative_cycles=False) -> nx.DiGraph:
    """
    Generate a random directed graph with optional negative weights.

    Parameters:
        n_nodes (int): Number of nodes in the graph
        edge_prob (float): Probability that an edge exists between any pair
        weight_range (tuple): Range of weights (inclusive)
        allow_negative_cycles (bool): Whether to allow negative-weight cycles

    Returns:
        G (nx.DiGraph): Generated graph
    """
    G = nx.DiGraph()
    G.add_nodes_from(range(n_nodes))

    for u in range(n_nodes):
        for v in range(n_nodes):
            if u != v and random.random() < edge_prob: 
                weight = random.randint(*weight_range) # The * operator unpacks the tuple
                G.add_edge(u, v, weight=weight)

    if not allow_negative_cycles:
        # Remove negative cycles by breaking strongly connected components with negative total weight
        try:
            nx.find_cycle(G)  # will throw if no cycle
            # optional: implement a proper cycle removal method
        except nx.exception.NetworkXNoCycle:
            pass  # all good

    return G

def generate_grid_graph(rows: int, cols: int, weight_range=(1, 10)) -> nx.DiGraph:
    """
    Generate a 2D grid graph with directional edges (right and down).

    Parameters:
        rows (int): Number of rows
        cols (int): Number of columns
        weight_range (tuple): Range of weights for edges

    Returns:
        G (nx.DiGraph): Directed grid graph
    """
    G = nx.DiGraph()
    for i in range(rows):
        for j in range(cols):
            node = i * cols + j
            if j < cols - 1:
                G.add_edge(node, node + 1, weight=random.randint(*weight_range))
            if i < rows - 1:
                G.add_edge(node, node + cols, weight=random.randint(*weight_range))
    return G
