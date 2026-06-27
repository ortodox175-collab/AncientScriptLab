from core.record import TextRecord
import json

class ImportEngine:

    def load_generic_json(self, path, script_name):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        records = []

        for item in data:
            records.append(
                TextRecord(
                    script=script_name,
                    text_id=item["text_id"],
                    sequence=item["sequence"],
                    metadata=item.get("metadata", {})
                )
            )

        return records
