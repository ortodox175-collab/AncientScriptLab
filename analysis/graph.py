from collections import defaultdict
from analysis.bigrams import build_bigrams


def build_graph(sequence):
    graph = defaultdict(lambda: defaultdict(int))

    for a, b in build_bigrams(sequence):
        graph[a][b] += 1

    return graph


def normalize_graph(graph):
    prob_graph = {}

    for node, edges in graph.items():
        total = sum(edges.values())

        prob_graph[node] = {
            k: v / total for k, v in edges.items()
        }

    return prob_graph
