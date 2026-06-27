from core.corpus import Corpus
from analysis.entropy import entropy

def main():
    corpus = Corpus()

    print("AncientScriptLab v1.0")
    print("Records:", len(corpus))

    # тестовая проверка (без корпуса пока)
    test_seq = [1, 2, 2, 3, 3, 3, 4]
    print("Test entropy:", entropy(test_seq))

if __name__ == "__main__":
    main()
