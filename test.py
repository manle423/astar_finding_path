import random
import itertools
import matplotlib.pyplot as plt
import networkx as nx


class Node:
    def __init__(self, id=0, adjacent_nodes=None, position=(0, 0), color=None):
        if adjacent_nodes is None:
            adjacent_nodes = []
        self.id = id
        self.adjacent_nodes = adjacent_nodes
        self.adjacent_colors = {adjacent_node.color for adjacent_node in adjacent_nodes}
        self.color = color
        self.level = len(adjacent_nodes)
        self.position = position
        self.has_edge = False

    def decrease_adjacent_levels(self):
        for node in self.adjacent_nodes:
            node.level -= 1


# check if 2 adjacent nodes has the same color
def is_valid_coloring(graph, coloring):
    for u, v in graph.edges():
        if coloring[u] == coloring[v]:
            return False
    return True


def greedy_coloring(graph):
    coloring = {}
    for node in graph.nodes():
        # get the colors of adjacent nodes
        adjacent_colors = {coloring.get(neighbor) for neighbor in graph.neighbors(node)}
        # find a color (from color 0, then color 1,...) that is not in adjacent_colors
        coloring[node] = next(color for color in itertools.count() if color not in adjacent_colors)
    return coloring


# number of nodes
n_nodes = 10

# create a graph with nodes
G = nx.Graph()
G.add_nodes_from(range(n_nodes))

# draw edges between nodes
for i in range(n_nodes):
    # đảm bảo không xét cạnh ngược lại và đỉnh ko tự nối chính nó
    for j in range(i + 1, n_nodes):
        if random.random() < 0.4:
            G.add_edge(i, j)

coloring_result = greedy_coloring(G)

print("Coloring: ", coloring_result)
print("Valid:", is_valid_coloring(G, coloring_result))
print("K:", len(set(coloring_result.values())))
print(len(G.nodes) == len(coloring_result))

# vẽ đồ thị lên màn hình
color_map = [coloring_result[node] for node in G.nodes]
print("Color map:", color_map)
nx.draw(G, node_color=color_map, with_labels=True, font_weight="bold")
plt.show()
