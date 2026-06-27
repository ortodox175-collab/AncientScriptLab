from core.corpus import Corpus
from analysis.entropy import entropy
from analysis.frequency import top_symbols, frequency


def main():
    corpus = Corpus()

    print("AncientScriptLab v2.1 (FREQUENCY ANALYSIS)")

    corpus.load_rongorongo("data/raw/rongorongo.txt")

    print("Records:", len(corpus.records))

    seq = corpus.all_sequences("Rongorongo")

    print("Total symbols:", len(seq))

    print("Entropy:", entropy(seq))

    print("\nTop symbols:")
    for sym, cnt in top_symbols(seq, 10):
        print(sym, ":", cnt)

    print("\nUnique symbols:", len(frequency(seq)))


if __name__ == "__main__":
    main()
