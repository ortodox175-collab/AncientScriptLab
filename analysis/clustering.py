from collections import defaultdict
import random
from analysis.embeddings import cosine


# =========================
# K-MEANS (простая версия)
# =========================

def kmeans(vectors, k=3, iterations=10):
    symbols = list(vectors.keys())

    centroids = random.sample(symbols, k)
    clusters = {i: [] for i in range(k)}

    for _ in range(iterations):

        clusters = {i: [] for i in range(k)}

        # assignment step
        for s in symbols:
            best = 0
            best_score = -1

            for i, c in enumerate(centroids):
                score = cosine(vectors[s], vectors[c])
                if score > best_score:
                    best_score = score
                    best = i

            clusters[best].append(s)

        # update step
        new_centroids = []

        for i in range(k):
            if not clusters[i]:
                continue

            new_centroids.append(clusters[i][0])

        centroids = new_centroids

    return clusters


def print_clusters(clusters):
    for i, c in clusters.items():
        print(f"\nCluster {i}:")
        print(c)
