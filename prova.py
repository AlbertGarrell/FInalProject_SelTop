# utils/prova.py

import networkx as nx
import random
from collections import defaultdict

def reduced_edge_lengths(G, y):
    red_lens = {}
    for u, v, data in G.edges(data=True):
        red_lens[(u, v)] = data['weight'] + y[u] - y[v]
    return red_lens

def build_G_minus(G, y):
    G_minus = nx.DiGraph()
    for u, v, data in G.edges(data=True):
        red_len = data['weight'] + y[u] - y[v]
        if red_len <= 0:
            G_minus.add_edge(u, v, weight=red_len)
    G_minus.add_nodes_from(G.nodes())
    return G_minus

def contract_scc(G_minus):
    sccs = list(nx.strongly_connected_components(G_minus))
    mapping = {}
    for i, scc in enumerate(sccs):
        for v in scc:
            mapping[v] = i
    H = nx.DiGraph()
    for u, v, data in G_minus.edges(data=True):
        cu, cv = mapping[u], mapping[v]
        if cu != cv:
            H.add_edge(cu, cv, weight=data['weight'])
    H.add_nodes_from(range(len(sccs)))
    return H, mapping, sccs

def round_re_duals(G, y_pred):
    y = y_pred.copy()
    last_neg_edges = None
    last_selected_sccs = None
    same_count = 0
    max_iters = 5

    for iter_count in range(1, max_iters + 1):
        print(f"\n=== Iteration {iter_count} ===")
        red_lens = reduced_edge_lengths(G, y)
        neg_edges = [(u, v) for (u, v), l in red_lens.items() if l < 0]
        print(f"Current duals y: {y}")
        print(f"Reduced edge lengths: {red_lens}")
        print(f"Negative edges: {neg_edges}")

        if not neg_edges:
            print("No negative edges... breaking the while.")
            break

        G_minus = build_G_minus(G, y)
        H, mapping, sccs = contract_scc(G_minus)
        print(f"SCCs: {sccs}")
        print(f"SCC mapping: {mapping}")
        x = 'X_aux'
        H.add_node(x)
        for i in range(len(sccs)):
            H.add_edge(x, i, weight=0)

        try:
            dists = nx.single_source_bellman_ford_path_length(H, x, weight='weight')
        except nx.NetworkXUnbounded:
            raise ValueError("Negative cycle detected in contracted graph during RPfRELD")

        layers = defaultdict(list)
        for i_scc, dist in dists.items():
            if i_scc == x:
                continue
            i = -dist
            layers[i].append(i_scc)
        
        # Debug print for layers
        print("Layer assignments:")
        for i, scc_list in layers.items():
            print(f"  Layer {i}: SCCs {scc_list}")

        if not layers:
            print("No layers found... breaking.")
            break

        i_star = max(layers, key=lambda k: len(layers[k]))
        print(f"i_star = {i_star}, layer with most SCCs: {layers[i_star]}")

        selected_sccs = set()
        for t in layers:
            if t >= i_star:
                selected_sccs.update(layers[t])

        print(f"Selected SCCs to decrement: {selected_sccs}")
        nodes_to_decrement = set()
        for idx, scc in enumerate(sccs):
            if idx in selected_sccs:
                print(f"  Decrementing duals for nodes: {list(scc)}")
                nodes_to_decrement.update(scc)

        # --------- PATCHED SECTION: only decrement one endpoint for each negative edge ---------
        actually_decrement = set(nodes_to_decrement)
        for u, v in neg_edges:
            # If both endpoints would be decremented, only decrement the source (u)
            if u in actually_decrement and v in actually_decrement:
                actually_decrement.remove(v)
        print(f"Final nodes to decrement this iteration: {actually_decrement}")

        # Defensive loop break if stuck (as before)
        if (neg_edges == last_neg_edges) and (selected_sccs == last_selected_sccs):
            same_count += 1
            print(f"Loop detected: negative edges and selected SCCs unchanged ({same_count} times).")
            if same_count >= max_iters:
                print(f"No progress after {max_iters} repeated iterations. Breaking loop.")
                break
        else:
            same_count = 0
        last_neg_edges = neg_edges.copy()
        last_selected_sccs = selected_sccs.copy()

        for v in actually_decrement:
            y[v] -= 1

    print(f"\nFinal duals y: {y}")
    return y

def reduced_edge_lengths_after(G, y):
    red_lens = reduced_edge_lengths(G, y)
    print("Reduced edge lengths after rounding:")
    for edge, val in red_lens.items():
        print(f"  Edge {edge}: reduced length = {val}")

def create_strongly_connected_gminus():
    G = nx.DiGraph()
    for i in range(5):
        G.add_edge(i, (i+1)%5, weight=-1)   # All edges negative, forms a 5-node cycle
    G.add_edge(0, 6, weight=5)
    G.add_edge(6, 7, weight=3)
    G.add_edge(7, 8, weight=2)
    return G

if __name__ == "__main__":
    print("\n=== Test: Rounding on Strongly Connected G_minus ===")
    G = create_strongly_connected_gminus()
    y_pred = {node: 0 for node in G.nodes}
    print("Edge weights:")
    for u, v, data in G.edges(data=True):
        print(f"  {u} → {v} (weight = {data['weight']})")
    y_feasible = round_re_duals(G, y_pred, max_iters=20)
    print("\nFeasible (rounded) duals:", y_feasible)
    reduced_edge_lengths_after(G, y_feasible)
