import networkx as nx
import matplotlib.pyplot as plt
from mock_results import triple_preference, triple_preference_gpt_35, triple_preference_gpt_4o, triple_preference_claude_35, triple_preference_claude_3
import math
from constants import MORAL_VALUES
from L_visualise_graphs import plot_pair_graph

# turn triples into tuples of edges
def visualise_triples(triple_preference):
    edges = {}
    nodes = MORAL_VALUES
    for triple, triple_values in triple_preference.items():
        triple_values.pop("neither")
        vals = sorted(triple_values.items(), key=lambda item: item[1])
        print(vals)
        triples = [x[0] for x in vals]
        A, B, C = triples
        edges[(A, B)] = triple_values[B] - triple_values[A]
        edges[(B, C)] = triple_values[C] - triple_values[B]
        edges[(A, C)] = triple_values[C] - triple_values[A]
    print(edges)
    return edges
    # print(len(edges), len(set(edges)), edges)
    # G = nx.DiGraph(list(set(edges)))
    # print(G)
    # OPTIONS = {
    #     "font_size": 8,
    #     "node_size": 1500,
    #     "node_color": "lightblue",
    #     "edgecolors": "black",
    #     "linewidths": 1.5,
    #     "width": 1.5,
    # }
    # node_coords = {node: (math.cos(math.radians(60)* (i%6)),4*math.sin(math.radians(60)* (i%6)) ) for i, node in enumerate(MORAL_VALUES)}
    # nx.draw_networkx(G, node_coords, **OPTIONS)
    #
    # # Set margins for the axes so that nodes aren't clipped
    # ax = plt.gca()
    # ax.margins(0.20)
    # plt.axis("off")
    # plt.show()

if __name__ == "__main__":
    plot_pair_graph(visualise_triples(triple_preference_gpt_35), output_filename="triple_preference_gpt_35.png")
    plot_pair_graph(visualise_triples(triple_preference_gpt_4o), output_filename="triple_preference_gpt_4o.png")
    plot_pair_graph(visualise_triples(triple_preference_claude_3), output_filename="triple_preference_claude_3.png")
    plot_pair_graph(visualise_triples(triple_preference_claude_35), output_filename="triple_preference_claude_35.png")


