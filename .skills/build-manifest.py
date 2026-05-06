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

try:
    import yaml
except ImportError:
    print(
        "ERROR: PyYAML required. Install with: pip3 install --user pyyaml",
        file=sys.stderr,
    )
    sys.exit(1)

SCRIPT_DIR = Path(__file__).resolve().parent
SKILLS_DIR = SCRIPT_DIR / "skills"
OUTPUT = SCRIPT_DIR / "_manifest.json"

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
FLOW_SEQ_RE = re.compile(r"(\[)([^\[\]\n]*)(\])")


def _quote_flow_items_with_braces(match):
    """Coerce unquoted flow sequence items that contain `{` into quoted strings.

    Backward compat shim: pre-PyYAML legacy SKILL.md files stored values like
    `writes: [brands/{slug}/products/{slug}/spec.json via write_to_context]`
    where the unquoted `{slug}` would be parsed by PyYAML as a nested flow
    mapping and fail. The legacy regex parser tolerated this. We tolerate it
    here too by quoting any flow-sequence item containing a brace, before
    handing the block to yaml.safe_load.
    """
    open_b, body, close_b = match.group(1), match.group(2), match.group(3)
    parts = [p.strip() for p in body.split(",")]
    fixed = []
    for p in parts:
        if not p:
            continue
        if "{" in p and not (p.startswith('"') or p.startswith("'")):
            # escape any embedded double quote, then wrap
            p_escaped = p.replace('"', '\\"')
            fixed.append(f'"{p_escaped}"')
        else:
            fixed.append(p)
    return open_b + ", ".join(fixed) + close_b


def _preprocess_frontmatter(block):
    """Apply backward compat shims before yaml.safe_load."""
    return FLOW_SEQ_RE.sub(_quote_flow_items_with_braces, block)


def parse_frontmatter(text, skill_name=None):
    """Strict YAML parse of frontmatter between --- delimiters.

    Returns dict on success, None if no frontmatter or yaml error.
    YAML errors are logged with skill name and the skill is skipped
    (manifest build continues for the remaining skills).
    """
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None
    block = _preprocess_frontmatter(m.group(1))
    try:
        data = yaml.safe_load(block)
    except yaml.YAMLError as e:
        label = skill_name or "<unknown>"
        print(f"WARN: yaml parse error in {label}: {e}", file=sys.stderr)
        return None
    if not isinstance(data, dict):
        return None
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
        fm = parse_frontmatter(text, skill_name=skill_dir.name)
        if not fm:
            print(f"WARN: no frontmatter or invalid yaml in {skill_file}", file=sys.stderr)
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
