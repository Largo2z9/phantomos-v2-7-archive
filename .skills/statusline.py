#!/usr/bin/env python3
"""
PhantomOS status line for Claude Code.

Reads the active brand state and outputs a single line for the terminal status bar.
Format: "🟢 {brand_slug} · L{level} · {tests_count} tests · last {time_ago}"

Install: add to ~/.claude/settings.json under "statusLine" key:
    {
      "statusLine": {
        "type": "command",
        "command": "python3 /path/to/workspace-template/.skills/statusline.py"
      }
    }

Reads from cwd. If cwd is not a PhantomOS workspace, outputs nothing (silent).
Designed to be fast (< 50ms): reads only _snapshot.md and status.json, no full scan.
"""
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path


def find_workspace_root() -> Path | None:
    """Walk up from cwd looking for a PhantomOS workspace marker."""
    cwd = Path.cwd()
    for parent in [cwd, *cwd.parents]:
        if (parent / "_version.json").exists() and (parent / "brands").exists():
            return parent
    return None


def get_active_brand_slug(root: Path) -> str | None:
    """Read session-state.md to find the active brand. Fallback: only brand if N=1."""
    session_state = root / "session-state.md"
    if session_state.exists():
        content = session_state.read_text(errors="ignore")
        # Look for "active_brand: {slug}" or first heading mentioning a brand
        for line in content.splitlines()[:50]:
            if "active_brand" in line.lower() or "brand actif" in line.lower():
                parts = line.split(":")
                if len(parts) >= 2:
                    slug = parts[1].strip().strip('"`*[]')
                    if slug:
                        return slug
    # Fallback: only brand if N=1
    brands_dir = root / "brands"
    if brands_dir.exists():
        brands = [d.name for d in brands_dir.iterdir() if d.is_dir() and not d.name.startswith("_")]
        if len(brands) == 1:
            return brands[0]
    return None


def get_context_level(root: Path, slug: str) -> int:
    """Read status.json wedge_complete to determine context level L1/L2/L3."""
    status_file = root / "brands" / slug / "status.json"
    if not status_file.exists():
        return 0
    try:
        data = json.loads(status_file.read_text())
        # Heuristique: niveau = somme des completeness_scores >= 0.7
        scores = data.get("completeness_scores", {})
        if not scores:
            return 1 if data.get("wedge_complete") else 0
        completed = sum(1 for v in scores.values() if isinstance(v, (int, float)) and v >= 0.7)
        if completed >= 5:
            return 3
        elif completed >= 3:
            return 2
        else:
            return 1
    except Exception:
        return 0


def get_active_tests_count(root: Path, slug: str) -> int:
    """Count active tests in learnings.json (type=test-result, status absent or inconclusive/fatigued)."""
    learnings_file = root / "brands" / slug / "learnings.json"
    if not learnings_file.exists():
        return 0
    try:
        data = json.loads(learnings_file.read_text())
        entries = data.get("entries", [])
        active = 0
        for e in entries:
            if e.get("type") != "test-result":
                continue
            test = e.get("test_result", {})
            status = test.get("status", "")
            if status in ("", "inconclusive", "fatigued"):
                active += 1
        return active
    except Exception:
        return 0


def get_last_session_time_ago(root: Path) -> str:
    """Read session-state.md mtime as proxy for last session."""
    session_state = root / "session-state.md"
    if not session_state.exists():
        return "?"
    try:
        mtime = datetime.fromtimestamp(session_state.stat().st_mtime, tz=timezone.utc)
        delta = datetime.now(tz=timezone.utc) - mtime
        seconds = delta.total_seconds()
        if seconds < 3600:
            return f"{int(seconds // 60)}m"
        elif seconds < 86400:
            return f"{int(seconds // 3600)}h"
        else:
            return f"{int(seconds // 86400)}d"
    except Exception:
        return "?"


def get_status_icon(level: int, tests: int) -> str:
    """Status icon based on level and activity."""
    if level >= 2 and tests > 0:
        return "🟢"
    elif level >= 1:
        return "🟡"
    else:
        return "⚪"


def main():
    root = find_workspace_root()
    if not root:
        # Not in a PhantomOS workspace, silent
        sys.exit(0)

    slug = get_active_brand_slug(root)
    if not slug:
        # No brand active or multiple brands without active selection
        print("⚪ phantomos · no active brand")
        return

    level = get_context_level(root, slug)
    tests = get_active_tests_count(root, slug)
    time_ago = get_last_session_time_ago(root)
    icon = get_status_icon(level, tests)

    if tests > 0:
        print(f"{icon} {slug} · L{level} · {tests} tests · last {time_ago}")
    else:
        print(f"{icon} {slug} · L{level} · last {time_ago}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        # Statusline must never break the terminal. Silent failure.
        sys.exit(0)
