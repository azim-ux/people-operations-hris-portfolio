#!/usr/bin/env python3
"""Register the career workspace as an Obsidian vault with a recoverable backup."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import tempfile
import time
from pathlib import Path


VAULT = Path(__file__).resolve().parents[1]
REGISTRY = Path.home() / "Library/Application Support/obsidian/obsidian.json"
BACKUP = VAULT / "99_Archive/02_System_Metadata/Obsidian_Registry_Before_Career_Vault_2026-08-05.json"


def main() -> None:
    if not (VAULT / ".obsidian").is_dir():
        raise SystemExit(f"Vault marker missing: {VAULT / '.obsidian'}")
    if not REGISTRY.is_file():
        raise SystemExit(f"Obsidian registry missing: {REGISTRY}")

    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    vaults = data.setdefault("vaults", {})

    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    if not BACKUP.exists():
        shutil.copy2(REGISTRY, BACKUP)

    vault_id = next(
        (key for key, value in vaults.items() if Path(value.get("path", "")) == VAULT),
        hashlib.sha256(str(VAULT).encode("utf-8")).hexdigest()[:16],
    )
    for value in vaults.values():
        value["open"] = False
    vaults[vault_id] = {
        "path": str(VAULT),
        "ts": int(time.time() * 1000),
        "open": True,
    }

    REGISTRY.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix="obsidian-registry-", suffix=".json", dir=REGISTRY.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(data, handle, separators=(",", ":"))
            handle.write("\n")
        os.replace(temporary_name, REGISTRY)
    finally:
        if os.path.exists(temporary_name):
            os.unlink(temporary_name)

    print(vault_id)
    print(REGISTRY)
    print(BACKUP)


if __name__ == "__main__":
    main()
