import os
import json
from threading import Lock
from typing import Optional, Dict
from app.config import settings

class MetadataStore:
    """Simple file‑based JSON store for file metadata.
    Thread‑safe for concurrent reads/writes using a lock.
    """

    def __init__(self, store_path: Optional[str] = None):
        self.store_path = store_path or settings.METADATA_STORE
        self._lock = Lock()
        # Ensure the file exists
        if not os.path.exists(self.store_path):
            with open(self.store_path, "w", encoding="utf-8") as f:
                json.dump({}, f)

    def _load_store(self) -> Dict:
        with open(self.store_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_store(self, data: Dict) -> None:
        with open(self.store_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, default=str)

    def get(self, file_id: str) -> Optional[Dict]:
        with self._lock:
            data = self._load_store()
            return data.get(file_id)

    def set(self, file_id: str, metadata: Dict) -> None:
        with self._lock:
            data = self._load_store()
            data[file_id] = metadata
            self._save_store(data)

    def list_all(self) -> Dict:
        with self._lock:
            return self._load_store()
