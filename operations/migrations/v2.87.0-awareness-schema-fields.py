#!/usr/bin/env python3
"""
Migration v2.87.0 · awareness.json schema v1.0 → v1.1

Adds NEW fields canon v2.81+ + v2.87.0 que tour.md écrit en cours d'exécution ·
- tour_entry_door (enum A/B/C/D · null default · NEW v2.81 splitter 4 portes)
- first_deliverable_built (boolean · null default · NEW v2.81 M5b)
- first_deliverable_skill (string · null default · NEW v2.81 M5b)
- first_deliverable_validated_corrections (integer · 0 default · NEW v2.81 M5b)
- paths_skipped (array · [] default · NEW v2.87 tour exit)

Idempotent · re-run safe · backup horodaté avant patch.

Usage ·
    python3 operations/migrations/v2.87.0-awareness-schema-fields.py [workspace_path]

Default workspace_path = current dir.
"""

import json
import shutil
import sys
from datetime import datetime
from pathlib import Path


def migrate_awareness(workspace_path: Path) -> dict:
    awareness_path = workspace_path / "operator" / "awareness.json"

    if not awareness_path.exists():
        return {"status": "skip", "reason": "awareness.json absent · fresh workspace use template"}

    with awareness_path.open("r") as f:
        data = json.load(f)

    current_version = data.get("_version", "1.0")

    if current_version == "1.1":
        return {"status": "skip", "reason": "already v1.1 · idempotent"}

    if current_version != "1.0":
        return {"status": "error", "reason": f"unexpected version {current_version}"}

    backup_path = awareness_path.with_suffix(f".bak.{datetime.now().strftime('%Y-%m-%d')}")
    shutil.copy2(awareness_path, backup_path)

    data["_version"] = "1.1"

    data.setdefault("_field_types", {}).update({
        "tour_entry_door": "stated",
        "paths_skipped": "derived",
        "first_deliverable_built": "derived",
        "first_deliverable_skill": "derived",
        "first_deliverable_validated_corrections": "derived",
    })

    data.setdefault("tour_entry_door", None)
    data.setdefault("paths_skipped", [])
    data.setdefault("first_deliverable_built", None)
    data.setdefault("first_deliverable_skill", None)
    data.setdefault("first_deliverable_validated_corrections", 0)

    if data.get("first_skill_built") is False:
        data["first_skill_built"] = None

    ordered_keys = [
        "_version", "_schema", "_field_types",
        "tour_status", "tour_entry_door", "tour_last_run", "sessions_count",
        "concepts_introduced", "paths_explored", "paths_skipped",
        "first_deliverable_built", "first_deliverable_skill",
        "first_deliverable_validated_corrections",
        "first_skill_offered", "first_skill_built", "first_brand_validated",
    ]
    ordered_data = {k: data[k] for k in ordered_keys if k in data}
    for k, v in data.items():
        if k not in ordered_data:
            ordered_data[k] = v

    with awareness_path.open("w") as f:
        json.dump(ordered_data, f, indent=2, ensure_ascii=False)
        f.write("\n")

    return {
        "status": "migrated",
        "from_version": "1.0",
        "to_version": "1.1",
        "backup": str(backup_path.name),
        "fields_added": [
            "tour_entry_door", "paths_skipped",
            "first_deliverable_built", "first_deliverable_skill",
            "first_deliverable_validated_corrections",
        ],
    }


if __name__ == "__main__":
    workspace = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    result = migrate_awareness(workspace)
    print(json.dumps(result, indent=2))
    sys.exit(0 if result["status"] in ("migrated", "skip") else 1)
