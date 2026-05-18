#!/usr/bin/env python3
"""
Migration template canon · v2.80.0+

Pattern · 4 méthodes obligatoires (check_required · run_transformation · validate_state · rollback).
Cross-reference doctrine · docs/system/update-distribution-discipline.md

Usage ·
  python3 migrations/{version}-{slug}.py --check
  python3 migrations/{version}-{slug}.py --dry-run
  python3 migrations/{version}-{slug}.py --apply
  python3 migrations/{version}-{slug}.py --rollback

Copy this file to migrations/{version}-{slug}.py and fill in the TODOs.
"""

import argparse
import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple


# === METADATA ===
MIGRATION_VERSION = "X.Y.Z"  # target version · ex 2.80.0
MIGRATION_DESCRIPTION = "describe transform here"
MIGRATION_TYPE = "transform"  # additive | transform | deprecate

WORKSPACE_ROOT = Path.cwd()

# Files this migration will modify (used for backup scope).
# Override per migration · list relative paths from WORKSPACE_ROOT.
AFFECTED_FILES: List[str] = [
    # "brands/example/spec.yaml",
]


def check_required() -> Tuple[bool, str]:
    """
    Pre-conditions to apply this migration. Idempotent.
    Returns (ready, reason).
    """
    version_file = WORKSPACE_ROOT / "_version.json"
    if not version_file.exists():
        return False, "_version.json missing"

    with open(version_file) as f:
        current = json.load(f).get("template_version", "")

    # Idempotence guard · already on target
    if current == MIGRATION_VERSION:
        return False, f"already on v{current}"

    # TODO · add custom precondition checks here
    # Example · verify specific files exist before transformation

    return True, f"current v{current} → target v{MIGRATION_VERSION}"


def run_transformation(dry_run: bool = False) -> None:
    """
    Apply the migration. MUST be idempotent.
    """
    if dry_run:
        print(f"[DRY] would transform · {MIGRATION_DESCRIPTION}")
        return

    # TODO · custom transformation logic here
    # Example pattern · iterate affected files, detect already-transformed
    # state, skip if so, otherwise apply transform.
    print(f"→ Applying transformation · {MIGRATION_DESCRIPTION}")


def validate_state() -> Tuple[bool, str]:
    """
    Verify post-migration state is canonical. Pure read, no side effects.
    Returns (valid, reason).
    """
    # TODO · custom validation logic
    # Example · check that expected files exist, expected schema present.
    return True, "state validated"


def rollback() -> bool:
    """
    Revert this migration by restoring from automatic backup.
    Backup path · _archive/migrations/pre-v{version}-{date}/
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
    print(f"→ Restoring from {latest_backup.relative_to(WORKSPACE_ROOT)}")

    # TODO · custom restore logic per migration
    # Default pattern · copy backup files back to WORKSPACE_ROOT preserving
    # relative paths.
    restored = 0
    for src in latest_backup.rglob("*"):
        if src.is_file():
            rel = src.relative_to(latest_backup)
            dst = WORKSPACE_ROOT / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            restored += 1

    print(f"✓ Restored {restored} file(s) from backup")
    return True


def _backup_affected_files() -> Optional[Path]:
    """
    Create backup of AFFECTED_FILES at _archive/migrations/pre-v{version}-{date}/.
    Returns backup directory path, or None if nothing to back up.
    """
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
        if src.is_file():
            shutil.copy2(src, dst)
            backed_up += 1
        elif src.is_dir():
            shutil.copytree(src, dst, dirs_exist_ok=True)
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
