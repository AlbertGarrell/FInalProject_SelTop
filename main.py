from graphs.graph_generator import generate_random_graph, generate_grid_graph, create_simple_graph
from algorithms.bellman_ford import bellman_ford
from graphs.graph_generator import create_bigger_toy_graph
from utils.rounding import round_re_duals, reduced_edge_lengths
import networkx as nx
import matplotlib.pyplot as plt
from utils.rounding import round_re_duals, reduced_edge_lengths, reduced_edge_lengths_after
from graphs.graph_generator import create_layered_toy_graph

def visualize_graph_with_paths(G, predecessors, source):
    pos = nx.spring_layout(G)
    edge_labels = nx.get_edge_attributes(G, 'weight')

    # Build list of edges in shortest paths (source to each reachable node)
    path_edges = []
    for target in G.nodes:
        if target == source or predecessors[target] is None:
            continue
        current = target
        while current != source and predecessors[current] is not None:
            path_edges.append((predecessors[current], current))
            current = predecessors[current]

    # Draw full graph
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', arrows=True)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    # Highlight shortest paths
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2.5, arrows=True)

    plt.title("Graph with Highlighted Shortest Paths")
    plt.show()


def test_rounding_on_simple_graph():
    print("\n=== Test: Rounding on Simple Toy Graph ===")
    G = create_simple_graph()
    y_pred = {node: 0 for node in G.nodes}

    print("Initial predicted duals:", y_pred)
    print("Edge weights:")
    for u, v, data in G.edges(data=True):
        print(f"  {u} → {v} (weight = {data['weight']})")

    y_feasible = round_re_duals(G, y_pred)
    print("Feasible (rounded) duals:", y_feasible)

    red_lens = reduced_edge_lengths(G, y_feasible)
    print("Reduced edge lengths after rounding:")
    for edge, val in red_lens.items():
        print(f"  Edge {edge}: reduced length = {val}")


def test_rounding_on_bigger_toy_graph():
    print("\n=== Test: Rounding on Bigger Toy Graph ===")
    G = create_bigger_toy_graph()
    y_pred = {node: 0 for node in G.nodes}

    print("Initial predicted duals:", y_pred)
    print("Edge weights:")
    for u, v, data in G.edges(data=True):
        print(f"  {u} → {v} (weight = {data['weight']})")

    y_feasible = round_re_duals(G, y_pred)
    print("Feasible (rounded) duals:", y_feasible)

    red_lens = reduced_edge_lengths(G, y_feasible)
    print("Reduced edge lengths after rounding:")
    for edge, val in red_lens.items():
        print(f"  Edge {edge}: reduced length = {val}")


def test_rounding_on_layered_toy_graph():
    print("\n=== Test: Rounding on Layered Toy Graph ===")
    G = create_layered_toy_graph()
    y_pred = {node: 0 for node in G.nodes}
    print("Initial predicted duals:", y_pred)
    print("Edge weights:")
    for u, v, data in G.edges(data=True):
        print(f"  {u} → {v} (weight = {data['weight']})")
    y_feasible = round_re_duals(G, y_pred)
    print("\nFeasible (rounded) duals:", y_feasible)
    reduced_edge_lengths_after(G, y_feasible)


def test_rounding_on_random_graph():
    print("\n=== Test: Rounding on Layered Toy Graph ===")
    G = generate_random_graph()
    y_pred = {node: 0 for node in G.nodes}
    print("Initial predicted duals:", y_pred)
    print("Edge weights:")
    for u, v, data in G.edges(data=True):
        print(f"  {u} → {v} (weight = {data['weight']})")
    y_feasible = round_re_duals(G, y_pred)
    print("\nFeasible (rounded) duals:", y_feasible)
    reduced_edge_lengths_after(G, y_feasible)


def test_bellman_ford_on_generated_graph():
    # Choose graph type
    G = generate_random_graph(n_nodes=8, edge_prob=0.4, weight_range=(-5, 10))
    # G = generate_grid_graph(3, 3, weight_range=(1, 5))

    source = 0

    print("🔧 Generated graph:")
    for u, v, data in G.edges(data=True):
        print(f"  {u} → {v} (weight = {data['weight']})")

    try:
        distances, predecessors = bellman_ford(G, source)
        print(f"\n🚀 Source node: {source}")
        print("\n📏 Shortest distances:")
        for node, dist in distances.items():
            print(f"  {source} → {node} = {dist}")

        print("\n🧭 Predecessors:")
        for node, pred in predecessors.items():
            print(f"  {node} ← {pred}")

        visualize_graph_with_paths(G, predecessors, source)

    except ValueError as e:
        print("❌ Error:", e)

if __name__ == "__main__":
    print("\n" + "="*40 + "\n")
    test_rounding_on_random_graph()