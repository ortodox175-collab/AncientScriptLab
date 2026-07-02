from core.corpus import Corpus

from analysis.entropy import entropy
from analysis.frequency import frequency, top_symbols
from analysis.bigrams import top_bigrams
from analysis.graph import build_graph, normalize_graph

from analysis.embeddings import (
    build_cooccurrence,
    compute_pmi,
    build_embeddings
)

from analysis.clustering import kmeans, print_clusters
from analysis.latent import latent_structure, print_latent

from generation.markov import (
    choose_start,
    generate_v3,
    build_context_model,
    generate_v31,
    structure_score
)


def main():
    corpus = Corpus()

    print("AncientScriptLab v5 → v7 FULL SYSTEM\n")

    corpus.load_rongorongo("data/raw/rongorongo.txt")

    seq = corpus.all_sequences("Rongorongo")
    freq = frequency(seq)

    print("Records:", len(corpus.records))
    print("Total symbols:", len(seq))
    print("Entropy:", entropy(seq))

    # =========================
    # GRAPH (v2-v4)
    # =========================
    graph = build_graph(seq)
    prob_graph = normalize_graph(graph)

    start = choose_start(seq, freq)
    gen = generate_v3(prob_graph, start)

    print("\nGenerated (v3):")
    print(gen)

    # =========================
    # v3.1
    # =========================
    context_model = build_context_model(seq, order=2)
    gen2 = generate_v31(context_model, gen)

    print("\nGenerated (v3.1):")
    print(gen2)

    # =========================
    # v4 score
    # =========================
    print("\nStructure score:", round(structure_score(gen2), 3))

    # =========================
    # v5 embeddings
    # =========================
    co = build_cooccurrence(seq)
    pmi = compute_pmi(co)
    vectors = build_embeddings(pmi)

    print("\nEmbeddings size:", len(vectors))

    # =========================
    # v6 clustering
    # =========================
    clusters = kmeans(vectors, k=3)
    print_clusters(clusters)

    # =========================
    # v7 latent structure
    # =========================
    latent = latent_structure(seq)
    print_latent(latent)


if __name__ == "__main__":
    main()
