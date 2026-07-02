from pathlib import Path

from datasets.indus.schema import (
    IndusCorpus,
    IndusInscription,
)


def load_mahadevan_txt(path):

    """
    Universal loader for Mahadevan corpus.

    Expected format:

    M0001 342 120 17 91
    M0002 201 11 44
    ...

    One inscription per line.
    """

    corpus = IndusCorpus(
        name="Mahadevan",
        version="1.0"
    )

    path = Path(path)

    for line in path.read_text(
        encoding="utf-8"
    ).splitlines():

        line = line.strip()

        if not line:
            continue

        if line.startswith("#"):
            continue

        parts = line.split()

        inscription_id = parts[0]

        signs = [int(x) for x in parts[1:]]

        corpus.add(

            IndusInscription(

                inscription_id=inscription_id,

                signs=signs,

                source="Mahadevan"

            )

        )

    return corpus
