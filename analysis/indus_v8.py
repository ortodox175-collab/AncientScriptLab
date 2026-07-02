from collections import defaultdict, Counter
import math


class IndusEncoder:
    def __init__(self):
        self.sign_to_id = {}
        self.id_to_sign = {}
        self.next_id = 0

    def encode_sequence(self, sequence):
        encoded = []
        for s in sequence:
            if s not in self.sign_to_id:
                self.sign_to_id[s] = self.next_id
                self.id_to_sign[self.next_id] = s
                self.next_id += 1
            encoded.append(self.sign_to_id[s])
        return encoded


class IndusGraph:
    def __init__(self):
        self.edges = defaultdict(Counter)
        self.node_freq = Counter()

    def add_sequence(self, seq):
        for i, s in enumerate(seq):
            self.node_freq[s] += 1
            if i < len(seq) - 1:
                self.edges[s][seq[i + 1]] += 1

    def normalize(self):
        self.prob = {}
        for a, targets in self.edges.items():
            total = sum(targets.values())
            self.prob[a] = {b: v / total for b, v in targets.items()}


class SignProfile:
    def __init__(self):
        self.start_pos = Counter()
        self.end_pos = Counter()
        self.total = Counter()
        self.positions = defaultdict(list)

    def update(self, seq):
        for i, s in enumerate(seq):
            self.total[s] += 1
            self.positions[s].append(i)

        if seq:
            self.start_pos[seq[0]] += 1
            self.end_pos[seq[-1]] += 1

    def compute_features(self, sign_id):
        freq = self.total[sign_id]

        pos_start = self.start_pos[sign_id] / freq if freq else 0
        pos_end = self.end_pos[sign_id] / freq if freq else 0

        positions = self.positions[sign_id]
        avg_pos = sum(positions) / len(positions) if positions else 0

        return {
            "freq": freq,
            "start_ratio": pos_start,
            "end_ratio": pos_end,
            "avg_position": avg_pos
        }


class ContextModel:
    def __init__(self):
        self.left = defaultdict(Counter)
        self.right = defaultdict(Counter)

    def update(self, seq):
        for i in range(len(seq)):
            if i > 0:
                self.left[seq[i]][seq[i - 1]] += 1
            if i < len(seq) - 1:
                self.right[seq[i]][seq[i + 1]] += 1

    def context_entropy(self, sign_id):
        def entropy(counter):
            total = sum(counter.values())
            if total == 0:
                return 0
            return -sum((v / total) * math.log(v / total + 1e-9)
                        for v in counter.values())

        return {
            "left_entropy": entropy(self.left[sign_id]),
            "right_entropy": entropy(self.right[sign_id])
        }


class IndusSystemV8:
    def __init__(self):
        self.encoder = IndusEncoder()
        self.graph = IndusGraph()
        self.profile = SignProfile()
        self.context = ContextModel()

    def ingest(self, corpus):
        for seq in corpus:
            self.graph.add_sequence(seq)
            self.profile.update(seq)
            self.context.update(seq)

        self.graph.normalize()

    def get_sign_features(self, sign_id):
        features = {}
        features.update(self.profile.compute_features(sign_id))
        features.update(self.context.context_entropy(sign_id))
        return features

    def summary(self):
        return {
            "symbols": len(self.profile.total),
            "nodes": len(self.graph.node_freq),
        }
