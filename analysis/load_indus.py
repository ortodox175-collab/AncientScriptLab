def load_indus_corpus(path="data/indus/corpus.txt"):
    corpus = []

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            seq = [int(x) for x in line.split()]
            corpus.append(seq)

    return corpus
