#!/usr/bin/env python3
"""
Stop hook — audit the last assistant turn for two tone/coherence violations.

Claude Code cannot intercept assistant text output before it renders, so hard
prevention is impossible. This hook does the next best thing: post-hoc audit
with a persistent log and a stderr line that surfaces on the next turn.

Audits:
1. Em-dash usage in operator-facing output. CLAUDE.md bans '—' in replies
   (policy: period, comma, or two sentences). Each occurrence logged.
2. Narrative claims about entity fields (spec.json, offers.json, profile.json,
   brand.json, compliance_gap, flagged CRITICAL, etc.) without a recent
   coherence_check event in `.phantom/context-engine-events.jsonl`. The class
   of bug caught on Nooance: agent said "I flagged compliance_gap CRITICAL"
   while the field was {}.

Writes:
- `.phantom/tone-audit.log` — one line per em-dash occurrence with a quote.
- `.phantom/coherence-audit.log` — one line per unchecked entity claim.

Stderr surfaces a single summary line if any violation occurred. Agent sees
this at next tool call and can self-correct.
"""
from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

EM_DASH = "—"

# Entity-field markers that imply the agent made a factual claim about a file.
ENTITY_MARKERS = (
    re.compile(r"\b(?:spec|offers|profile|brand|learnings|strategy)\.json\b", re.I),
    re.compile(r"\bcompliance_gap\b"),
    re.compile(r"\bflagg?ed\s+(?:as\s+)?(?:CRITICAL|P0|P1|MAJOR)\b", re.I),
    re.compile(r"\bstamped\s+(?:the\s+)?(?:field|value)\b", re.I),
)

LOG_LINE_MAX = 300


def find_workspace_root(start: Path) -> Path | None:
    cur = start.resolve()
    for _ in range(12):
        if (cur / "brands").is_dir() and (cur / ".skills").is_dir():
            return cur
        if cur.parent == cur:
            return None
        cur = cur.parent
    return None


def extract_last_assistant_text(transcript_path: Path) -> str:
    """Pull concatenated text content from the last assistant message in the
    transcript. Claude Code writes JSONL with one message per line."""
    if not transcript_path.is_file():
        return ""
    last_text = ""
    try:
        for line in transcript_path.read_text().splitlines():
            if not line.strip():
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            if entry.get("type") != "assistant":
                continue
            msg = entry.get("message") or {}
            content = msg.get("content") or []
            parts = []
            for block in content:
                if isinstance(block, dict) and block.get("type") == "text":
                    parts.append(block.get("text") or "")
            if parts:
                last_text = "\n".join(parts)
    except Exception:
        return ""
    return last_text


def count_em_dashes(text: str) -> list[str]:
    """Return one excerpt per em-dash, max 5 to avoid log bloat."""
    quotes = []
    for m in re.finditer(EM_DASH, text):
        start = max(0, m.start() - 40)
        end = min(len(text), m.end() + 40)
        excerpt = text[start:end].replace("\n", " ").strip()
        quotes.append(excerpt[:LOG_LINE_MAX])
        if len(quotes) >= 5:
            break
    return quotes


def recent_coherence_events(events_path: Path, window_seconds: int = 300) -> int:
    """Count coherence_check events in the last N seconds."""
    if not events_path.is_file():
        return 0
    cutoff = datetime.now(timezone.utc).timestamp() - window_seconds
    count = 0
    try:
        for line in events_path.read_text().splitlines():
            if "coherence_check" not in line:
                continue
            try:
                e = json.loads(line)
            except json.JSONDecodeError:
                continue
            ts = e.get("ts") or ""
            try:
                t = datetime.fromisoformat(ts.replace("Z", "+00:00")).timestamp()
            except Exception:
                continue
            if t >= cutoff:
                count += 1
    except Exception:
        return 0
    return count


def entity_claims(text: str) -> list[str]:
    """Return excerpts matching entity-field markers, deduplicated, max 5."""
    hits = []
    seen = set()
    for pattern in ENTITY_MARKERS:
        for m in pattern.finditer(text):
            start = max(0, m.start() - 40)
            end = min(len(text), m.end() + 40)
            excerpt = text[start:end].replace("\n", " ").strip()[:LOG_LINE_MAX]
            if excerpt in seen:
                continue
            seen.add(excerpt)
            hits.append(excerpt)
            if len(hits) >= 5:
                return hits
    return hits


def append_log(log_path: Path, kind: str, excerpts: list[str]) -> None:
    log_path.parent.mkdir(exist_ok=True)
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    with log_path.open("a") as f:
        for excerpt in excerpts:
            f.write(json.dumps({"ts": now, "kind": kind, "excerpt": excerpt}, ensure_ascii=False) + "\n")


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    if data.get("hook_event_name") not in ("Stop", "SubagentStop"):
        sys.exit(0)

    transcript_path = data.get("transcript_path")
    if not transcript_path:
        sys.exit(0)

    root_str = os.environ.get("CLAUDE_PROJECT_DIR")
    root = Path(root_str) if root_str else find_workspace_root(Path.cwd())
    if root is None:
        sys.exit(0)

    text = extract_last_assistant_text(Path(transcript_path))
    if not text:
        sys.exit(0)

    warnings = []

    em_dashes = count_em_dashes(text)
    if em_dashes:
        append_log(root / ".phantom" / "tone-audit.log", "em_dash", em_dashes)
        warnings.append(f"{len(em_dashes)} em-dash in operator reply (CLAUDE.md bans '—')")

    claims = entity_claims(text)
    if claims:
        recent = recent_coherence_events(root / ".phantom" / "context-engine-events.jsonl")
        if recent == 0:
            append_log(root / ".phantom" / "coherence-audit.log", "unchecked_entity_claim", claims)
            warnings.append(f"{len(claims)} entity-field claim without coherence_check — run validate-output-coherence before shipping such statements")

    if warnings:
        print("[turn-end-audit] " + " | ".join(warnings), file=sys.stderr)

    sys.exit(0)


if __name__ == "__main__":
    main()
