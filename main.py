from core.corpus import Corpus

from analysis.entropy import entropy
from analysis.frequency import frequency, top_symbols
from analysis.length import (
    average_length,
    min_length,
    max_length,
)
from analysis.bigrams import top_bigrams


def main():
    corpus = Corpus()

    print("AncientScriptLab v2.3 (BIGRAM ANALYSIS)\n")

    corpus.load_rongorongo("data/raw/rongorongo.txt")

    seq = corpus.all_sequences("Rongorongo")

    print("Script: Rongorongo\n")

    print("Records:", len(corpus.records))
    print("Total symbols:", len(seq))
    print("Unique symbols:", len(frequency(seq)))

    print("Average record length:", round(average_length(corpus.records), 2))
    print("Shortest record:", min_length(corpus.records))
    print("Longest record:", max_length(corpus.records))

    print("Entropy:", entropy(seq))

    print("\nTop symbols:")
    for symbol, count in top_symbols(seq, 10):
        print(f"{symbol} : {count}")

    print("\nTop bigrams:")
    for (a, b), count in top_bigrams(seq, 10):
        print(f"{a}-{b} : {count}")


if __name__ == "__main__":
    main()
