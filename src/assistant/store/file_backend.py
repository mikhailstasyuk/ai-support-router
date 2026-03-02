import json
import os
from pathlib import Path
from typing import Any


class FileBackend:
    def __init__(self, base_dir: str = "data/mock") -> None:
        self.base = Path(base_dir)
        self.base.mkdir(parents=True, exist_ok=True)

    def _path(self, domain: str) -> Path:
        return self.base / f"{domain}.json"

    def read(self, domain: str) -> list[dict[str, Any]]:
        path = self._path(domain)
        if not path.exists():
            return []
        try:
            with path.open("r", encoding="utf-8") as fh:
                data = json.load(fh)
        except (json.JSONDecodeError, OSError):
            # Keep runtime deterministic even if a concurrent write or manual edit left invalid JSON.
            return []
        return data if isinstance(data, list) else []

    def write(self, domain: str, records: list[dict[str, Any]]) -> None:
        path = self._path(domain)
        temp_path = path.with_suffix(f"{path.suffix}.tmp")
        with temp_path.open("w", encoding="utf-8") as fh:
            json.dump(records, fh, indent=2)
            fh.flush()
            os.fsync(fh.fileno())
        temp_path.replace(path)

    def upsert(self, domain: str, record_id: str, payload: dict[str, Any], id_field: str = "id") -> dict[str, Any]:
        records = self.read(domain)
        for idx, record in enumerate(records):
            if record.get(id_field) == record_id:
                records[idx] = {**record, **payload}
                self.write(domain, records)
                return records[idx]
        merged = {id_field: record_id, **payload}
        records.append(merged)
        self.write(domain, records)
        return merged

    def delete(self, domain: str, record_id: str, id_field: str = "id") -> bool:
        records = self.read(domain)
        updated = [record for record in records if record.get(id_field) != record_id]
        changed = len(updated) != len(records)
        if changed:
            self.write(domain, updated)
        return changed
