from core.corpus import Corpus
from analysis.entropy import entropy

def main():
    corpus = Corpus()

    print("AncientScriptLab v1.0")

    # ЗАГРУЗКА РОНГО-РОНГО
    corpus.load_rongorongo("data/raw/rongorongo.txt")

    print("Records:", len(corpus.records))

    # ОБЪЕДИНЁННАЯ ПОСЛЕДОВАТЕЛЬНОСТЬ
    seq = corpus.all_sequences("Rongorongo")

    print("Total symbols:", len(seq))
    print("Entropy:", entropy(seq))

if __name__ == "__main__":
    main()
