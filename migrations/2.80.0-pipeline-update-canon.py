#!/usr/bin/env python3
"""
Migration v2.80.0 · pipeline update canon

Type · additive
Ships · NEW slash commands /update + /version + NEW doctrine
update-distribution-discipline + NEW migrations framework.

Backward compat strict · aucune transformation opérateur state.
Cross-reference doctrine · docs/system/update-distribution-doctrine.md
"""

import argparse
import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple


# === METADATA ===
MIGRATION_VERSION = "2.80.0"
MIGRATION_DESCRIPTION = (
    "NEW pipeline update canon · /update + /version + doctrine + migrations framework"
)
MIGRATION_TYPE = "additive"

WORKSPACE_ROOT = Path.cwd()

# Additive migration · zero operator file modified.
# Backup scope · _version.json only (only file rewritten on update).
AFFECTED_FILES: List[str] = [
    "_version.json",
]


def check_required() -> Tuple[bool, str]:
    """
    Pre-conditions · _version.json present and current version < 2.80.0.
    """
    version_file = WORKSPACE_ROOT / "_version.json"
    if not version_file.exists():
        return False, "_version.json missing"

    with open(version_file) as f:
        current = json.load(f).get("template_version", "")

    if not current:
        return False, "template_version field missing in _version.json"

    # Idempotence · already on or past 2.80.0
    if _semver_gte(current, MIGRATION_VERSION):
        return False, f"already on v{current} (>= v{MIGRATION_VERSION})"

    return True, f"ready · current v{current} → target v{MIGRATION_VERSION}"


def run_transformation(dry_run: bool = False) -> None:
    """
    Additive migration · zero operator data transformation.
    Canon files (slash commands, doctrine, migrations framework) ship via
    rsync from canonical workspace-template, not via this script.
    This script only logs the additive surface and validates presence
    post-rsync.
    """
    if dry_run:
        print(f"[DRY] would log additive surface · {MIGRATION_DESCRIPTION}")
        return

    print("→ Additive migration · NEW canon shipped via rsync · no data transformation")
    print("→ NEW slash command · /update")
    print("→ NEW slash command · /version")
    print("→ NEW doctrine · docs/system/update-distribution-doctrine.md")
    print("→ NEW framework · migrations/ (README + _template.py)")


def validate_state() -> Tuple[bool, str]:
    """
    Verify v2.80.0 canon files are present post-rsync.
    """
    required_files = [
        WORKSPACE_ROOT / ".claude" / "commands" / "update.md",
        WORKSPACE_ROOT / ".claude" / "commands" / "version.md",
        WORKSPACE_ROOT / "docs" / "system" / "update-distribution-doctrine.md",
        WORKSPACE_ROOT / "migrations" / "_template.py",
        WORKSPACE_ROOT / "migrations" / "README.md",
    ]
    missing = [
        str(f.relative_to(WORKSPACE_ROOT)) for f in required_files if not f.exists()
    ]
    if missing:
        return False, f"missing files · {missing}"
    return True, "v2.80.0 canon shipped · all files present"


def rollback() -> bool:
    """
    Rollback additive migration · restore _version.json from backup and
    leave NEW canon files in place (rollback to v2.79.x means _version.json
    states the prior version; NEW files become inert no-ops).
    """
    backup_root = WORKSPACE_ROOT / "_archive" / "migrations"
    if not backup_root.exists():
        print(f"✗ No backup folder · {backup_root}")
        return False

    backups = sorted(backup_root.glob(f"pre-v{MIGRATION_VERSION}-*"))
    if not backups:
        print(f"✗ No backup found for v{MIGRATION_VERSION}")
        return False

    latest_backup = backups[-1]
    print(f"→ Found backup · {latest_backup.relative_to(WORKSPACE_ROOT)}")

    version_backup = latest_backup / "_version.json"
    if not version_backup.exists():
        print("✗ _version.json missing in backup")
        return False

    shutil.copy2(version_backup, WORKSPACE_ROOT / "_version.json")
    print("✓ Restored _version.json from backup")
    print("⚠ NEW canon files (commands · doctrine · migrations) left in place · inert")
    return True


def _semver_gte(a: str, b: str) -> bool:
    """Return True if version a >= version b (semver compare on first 3 parts)."""
    def parse(v: str) -> Tuple[int, ...]:
        parts = v.split(".")[:3]
        try:
            return tuple(int(p) for p in parts)
        except ValueError:
            return (0, 0, 0)

    return parse(a) >= parse(b)


def _backup_affected_files() -> Optional[Path]:
    if not AFFECTED_FILES:
        print("○ No affected files declared · skipping backup")
        return None

    backup_dir = (
        WORKSPACE_ROOT
        / "_archive"
        / "migrations"
        / f"pre-v{MIGRATION_VERSION}-{datetime.now().strftime('%Y-%m-%d')}"
    )
    backup_dir.mkdir(parents=True, exist_ok=True)

    backed_up = 0
    for rel_path in AFFECTED_FILES:
        src = WORKSPACE_ROOT / rel_path
        if not src.exists():
            continue
        dst = backup_dir / rel_path
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        backed_up += 1

    print(f"→ Backup · {backup_dir.relative_to(WORKSPACE_ROOT)} ({backed_up} item(s))")
    return backup_dir


def main() -> int:
    parser = argparse.ArgumentParser(
        description=f"Migration v{MIGRATION_VERSION} · {MIGRATION_DESCRIPTION}"
    )
    parser.add_argument("--apply", action="store_true", help="Apply migration")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check pre-conditions, no apply",
    )
    parser.add_argument(
        "--rollback",
        action="store_true",
        help="Revert this migration from backup",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview without applying",
    )
    args = parser.parse_args()

    if args.check:
        ready, reason = check_required()
        status = "✓" if ready else "✗"
        print(f"{status} Pre-conditions · {reason}")
        return 0 if ready else 1

    if args.rollback:
        return 0 if rollback() else 1

    if args.apply or args.dry_run:
        ready, reason = check_required()
        if not ready:
            print(f"✗ Pre-conditions failed · {reason}")
            return 1
        print(f"✓ Pre-conditions · {reason}")

        if not args.dry_run:
            _backup_affected_files()

        run_transformation(dry_run=args.dry_run)

        if args.dry_run:
            print(f"[DRY] Migration v{MIGRATION_VERSION} preview complete")
            return 0

        valid, reason = validate_state()
        status = "✓" if valid else "✗"
        print(f"{status} Post-migration state · {reason}")
        return 0 if valid else 1

    parser.print_help()
    return 1


if __name__ == "__main__":
    exit(main())
