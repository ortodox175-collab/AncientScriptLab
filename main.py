from core.corpus import Corpus
from analysis.entropy import entropy

def main():
    corpus = Corpus()

    print("AncientScriptLab v1.0")

    # ПУСТОЙ СТАРТ
    print("Initial records:", len(corpus))

    # ТЕСТ МАТЕМАТИКИ
    test_seq = [1, 2, 2, 3, 3, 3, 4]
    print("Test entropy:", entropy(test_seq))

    # РОНГО-РОНГО (пока файл НЕ подключён — просто подготовка)
    print("Rongorongo importer ready")

if __name__ == "__main__":
    main()
