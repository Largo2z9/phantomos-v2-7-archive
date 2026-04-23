#!/usr/bin/env python3
"""
checkpoint-resolver — UserPromptSubmit hook.

If the user's message resolves a staged workflow proposal (confirm/reject
pattern match on any brand's .workflow.json#/pending), promote or clear the
pending entry, append to history, set the checkpoint flag accordingly.

This is the ONLY path by which a workflow checkpoint becomes true. Agents
cannot self-mark, because checkpoint state is written from a UserPromptSubmit
hook whose input is the literal user text — not agent output.
"""
from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

CONFIRM_PATTERNS = [
    r"\boui\b", r"\byes\b", r"\byep\b", r"\bok\b", r"\bgo\b", r"\bconfirm(e|é|ed)?\b",
    r"\bvalide\b", r"\bparfait\b", r"\bexact\b", r"\bcorrect\b", r"\byup\b",
    r"✓", r"👍", r"\bc'est bon\b", r"\bc bon\b",
]
REJECT_PATTERNS = [
    r"\bnon\b", r"\bno\b", r"\bnope\b", r"\bskip\b", r"\bpas\b.*\b(bon|ok|ça)\b",
    r"\breject(e|ed)?\b", r"\bfaux\b", r"\bincorrect\b", r"\bmauvais\b", r"\bpas du tout\b",
]


def find_workspace_root(start: Path) -> Path | None:
    cur = start.resolve()
    for _ in range(8):
        if (cur / "brands").is_dir() and (cur / "resources").is_dir():
            return cur
        if cur.parent == cur:
            return None
        cur = cur.parent
    return None


def classify(text: str) -> str | None:
    lower = text.lower()
    for p in CONFIRM_PATTERNS:
        if re.search(p, lower):
            return "confirm"
    for p in REJECT_PATTERNS:
        if re.search(p, lower):
            return "reject"
    return None


def load_json(p: Path) -> dict:
    try:
        return json.loads(p.read_text())
    except Exception:
        return {}


def save_json(p: Path, data: dict) -> None:
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def resolve_brand(brand_dir: Path, prompt: str) -> str | None:
    wf_path = brand_dir / ".workflow.json"
    if not wf_path.exists():
        return None
    state = load_json(wf_path)
    pending = state.get("pending")
    if not pending:
        return None

    decision = classify(prompt)
    if decision is None:
        return None

    checkpoint = pending.get("checkpoint")
    product_slug = pending.get("product_slug")
    history_entry = {
        "resolved_at": datetime.utcnow().isoformat() + "Z",
        "checkpoint": checkpoint,
        "product_slug": product_slug,
        "summary": pending.get("summary"),
        "decision": decision,
        "operator_text": prompt.strip()[:500],
    }
    state.setdefault("history", []).append(history_entry)
    state["pending"] = None

    if decision == "confirm":
        if checkpoint == "confirmed_products":
            lst = state["checkpoints"].setdefault("confirmed_products", [])
            if product_slug and product_slug not in lst:
                lst.append(product_slug)
        else:
            state["checkpoints"][checkpoint] = True

    save_json(wf_path, state)
    return f"{decision}:{checkpoint}" + (f":{product_slug}" if product_slug else "")


def main() -> None:
    try:
        payload = json.loads(sys.stdin.read() or "{}")
    except json.JSONDecodeError:
        sys.exit(0)

    prompt = payload.get("prompt", "")
    if not prompt or len(prompt) > 2000:
        sys.exit(0)

    cwd = Path(payload.get("cwd") or os.getcwd())
    root = find_workspace_root(cwd)
    if root is None:
        sys.exit(0)

    brands_dir = root / "brands"
    if not brands_dir.is_dir():
        sys.exit(0)

    resolutions = []
    for brand_dir in brands_dir.iterdir():
        if not brand_dir.is_dir() or brand_dir.name.startswith("_"):
            continue
        r = resolve_brand(brand_dir, prompt)
        if r:
            resolutions.append(f"{brand_dir.name}:{r}")

    if resolutions:
        log = root / ".phantom"
        log.mkdir(exist_ok=True)
        with (log / "checkpoint-resolver.log").open("a") as f:
            f.write(json.dumps({
                "ts": datetime.utcnow().isoformat() + "Z",
                "resolutions": resolutions,
            }) + "\n")

    sys.exit(0)


if __name__ == "__main__":
    main()
