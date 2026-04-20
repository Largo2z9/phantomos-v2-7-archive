#!/usr/bin/env python3
"""
Builds .skills/_manifest.json from all SKILL.md frontmatters.

The manifest is a single JSON file the agent reads at session start instead
of scanning 29+ SKILL.md files. Regenerated on any skill add/rename/edit.

Usage:
    python3 .skills/build-manifest.py

Run from workspace-template root or from anywhere (resolves paths relative
to this script's location).
"""

import json
import re
import sys
from pathlib import Path
from datetime import datetime, timezone

SCRIPT_DIR = Path(__file__).resolve().parent
SKILLS_DIR = SCRIPT_DIR / "skills"
OUTPUT = SCRIPT_DIR / "_manifest.json"


def parse_frontmatter(text):
    """Extract YAML frontmatter between --- delimiters. Returns dict or None."""
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        return None
    block = m.group(1)

    data = {}
    current_key = None
    current_list = None
    buffer_multiline = None
    buffer_key = None

    for raw in block.split("\n"):
        line = raw.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue

        # Multi-line folded scalar `key: >`
        if buffer_multiline is not None:
            if re.match(r"^[A-Za-z_][A-Za-z0-9_]*:", line) and not line.startswith(" "):
                data[buffer_key] = buffer_multiline.strip()
                buffer_multiline = None
                buffer_key = None
            else:
                buffer_multiline += " " + line.strip()
                continue

        m_kv = re.match(r"^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$", line)
        if m_kv:
            k, v = m_kv.group(1), m_kv.group(2).strip()
            current_key = k
            current_list = None
            if v == ">" or v == "|":
                buffer_multiline = ""
                buffer_key = k
                continue
            if v.startswith("[") and v.endswith("]"):
                data[k] = [x.strip() for x in v[1:-1].split(",") if x.strip()]
                continue
            if v == "":
                data[k] = {}
                current_list = None
                continue
            if v.lower() in ("true", "false"):
                data[k] = v.lower() == "true"
                continue
            data[k] = v.strip('"').strip("'")
        elif line.startswith("  ") and current_key and isinstance(data.get(current_key), dict):
            m_nested = re.match(r"^\s+([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$", line)
            if m_nested:
                k, v = m_nested.group(1), m_nested.group(2).strip()
                if v.startswith("[") and v.endswith("]"):
                    data[current_key][k] = [x.strip() for x in v[1:-1].split(",") if x.strip()]
                elif v.lower() in ("true", "false"):
                    data[current_key][k] = v.lower() == "true"
                else:
                    data[current_key][k] = v.strip('"').strip("'")

    if buffer_multiline is not None and buffer_key:
        data[buffer_key] = buffer_multiline.strip()

    return data


TRIGGER_FR_RE = re.compile(r"FR\s*:\s*(.+?)(?=\bEN\s*:|$)", re.DOTALL | re.IGNORECASE)
TRIGGER_EN_RE = re.compile(r"EN\s*:\s*(.+?)$", re.DOTALL | re.IGNORECASE)
QUOTED_RE = re.compile(r'"([^"]+)"')


def extract_triggers(description):
    """Pull FR and EN trigger phrases from the description text."""
    fr_match = TRIGGER_FR_RE.search(description or "")
    en_match = TRIGGER_EN_RE.search(description or "")
    fr = QUOTED_RE.findall(fr_match.group(1)) if fr_match else []
    en = QUOTED_RE.findall(en_match.group(1)) if en_match else []
    return {"fr": fr, "en": en}


def build_manifest():
    entries = []
    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        if not skill_dir.is_dir() or skill_dir.name.startswith("_"):
            continue
        if skill_dir.name == "custom":
            continue
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            continue
        try:
            text = skill_file.read_text(encoding="utf-8")
        except Exception as e:
            print(f"WARN: {skill_file}: {e}", file=sys.stderr)
            continue
        fm = parse_frontmatter(text)
        if not fm:
            print(f"WARN: no frontmatter in {skill_file}", file=sys.stderr)
            continue

        perm = fm.get("permissions", {}) if isinstance(fm.get("permissions"), dict) else {}
        disamb = fm.get("disambiguates_against", {}) if isinstance(fm.get("disambiguates_against"), dict) else {}
        entry = {
            "name": fm.get("name", skill_dir.name),
            "type": fm.get("type", "unknown"),
            "model": fm.get("recommended_model", "sonnet"),
            "subagent_safe": perm.get("subagent_safe", False),
            "mode": perm.get("mode", "direct"),
            "triggers": extract_triggers(fm.get("description", "")),
            "disambiguates_against": disamb,
            "path": f".skills/skills/{skill_dir.name}/SKILL.md",
        }
        entries.append(entry)

    manifest = {
        "_version": "1.0",
        "_generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "_count": len(entries),
        "skills": entries,
    }
    OUTPUT.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT} with {len(entries)} skills")


if __name__ == "__main__":
    build_manifest()
