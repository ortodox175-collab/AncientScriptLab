from core.corpus import Corpus
from analysis.entropy import entropy


def main():
    corpus = Corpus()

    print("AncientScriptLab v2.0")

    # универсальная загрузка (НЕ rongorongo-specific)
    corpus.load_generic("data/raw/rongorongo.json", "Rongorongo")

    print("Records:", len(corpus.records))

    seq = corpus.all_sequences("Rongorongo")

    print("Total symbols:", len(seq))
    print("Entropy:", entropy(seq))


if __name__ == "__main__":
    main()
