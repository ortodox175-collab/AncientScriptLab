from dataclasses import dataclass
from pathlib import Path
import json


@dataclass(slots=True)
class DatasetInfo:

    name: str

    version: str

    source: str

    parser: str

    filename: str

    sha256: str = ""

    description: str = ""


class DatasetRegistry:

    """
    Registry of scientific datasets.

    Stores only metadata.

    Does NOT download datasets.
    """

    def __init__(self):

        self.datasets = {}

    def register(self, info: DatasetInfo):

        self.datasets[info.name] = info

    def get(self, name):

        return self.datasets.get(name)

    def exists(self, name):

        return name in self.datasets

    def names(self):

        return sorted(self.datasets.keys())

    def summary(self):

        return {
            "datasets": len(self.datasets)
        }

    def save(self, filename):

        data = {}

        for name, ds in self.datasets.items():

            data[name] = {

                "version": ds.version,

                "source": ds.source,

                "parser": ds.parser,

                "filename": ds.filename,

                "sha256": ds.sha256,

                "description": ds.description

            }

        Path(filename).write_text(

            json.dumps(data, indent=4),

            encoding="utf-8"

        )

    def load(self, filename):

        self.datasets.clear()

        path = Path(filename)

        if not path.exists():

            return

        data = json.loads(

            path.read_text(

                encoding="utf-8"

            )

        )

        for name, item in data.items():

            self.register(

                DatasetInfo(

                    name=name,

                    version=item["version"],

                    source=item["source"],

                    parser=item["parser"],

                    filename=item["filename"],

                    sha256=item.get("sha256", ""),

                    description=item.get("description", "")

                )

            )

