#!/usr/bin/env python3
"""
export-session.py
Parse a Claude Code session JSONL and write a clean markdown transcript.

Modes:
  --current             Export the current session (most recent .jsonl in the project folder).
  --pick                List the N most recent sessions and prompt the operator to choose.
  --session <id|date>   Export a specific session by ID (UUID) or date (YYYY-MM-DD prefix match).
  --since <duration>    Export every session newer than the given duration (e.g. "1 week", "3 days").
                        Useful for batch archival.
  --to <path>           Output directory (default: ./_sessions-archive/).
  --workspace <path>    Workspace root (default: cwd). Used to compute the Claude Code project key.
  --no-thinking         Strip the assistant thinking blocks from the output (default: include them).
  --list                List recent sessions and exit, do not export.

Output format: markdown with chronological turns. Each turn is labelled (user / assistant / tool /
thinking) and includes timestamp + model where available. Tool calls and tool results are inlined
in fenced blocks for readability. The output filename is YYYY-MM-DD-<slug>.md where slug is derived
from the first user message.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

CLAUDE_PROJECTS_ROOT = Path.home() / ".claude" / "projects"


def workspace_to_project_key(workspace_path: Path) -> str:
    """Claude Code stores sessions under ~/.claude/projects/<escaped-path>/.
    The escaping replaces / with - and prepends a -.
    Example: /Users/foo/dev/bar -> -Users-foo-dev-bar
    """
    abs_path = str(workspace_path.resolve())
    return abs_path.replace("/", "-")


def find_project_dir(workspace_path: Path) -> Path | None:
    key = workspace_to_project_key(workspace_path)
    candidate = CLAUDE_PROJECTS_ROOT / key
    if candidate.is_dir():
        return candidate
    return None


def list_session_files(project_dir: Path) -> list[Path]:
    if not project_dir.is_dir():
        return []
    files = [p for p in project_dir.iterdir() if p.suffix == ".jsonl"]
    files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return files


def parse_session_meta(jsonl_path: Path) -> dict:
    """Read the first few lines of a JSONL session and extract metadata.
    Returns: {session_id, started_at, first_user_message, model, turn_count}
    """
    session_id = jsonl_path.stem
    started_at = None
    first_user_message = ""
    model = ""
    turn_count = 0

    try:
        with open(jsonl_path, encoding="utf-8") as f:
            for line in f:
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue
                ts = entry.get("timestamp")
                if ts and started_at is None:
                    started_at = ts
                role = entry.get("role") or entry.get("type")
                if role == "user" and not first_user_message:
                    content = entry.get("content") or entry.get("message", {}).get("content", "")
                    if isinstance(content, list):
                        for block in content:
                            if isinstance(block, dict) and block.get("type") == "text":
                                first_user_message = block.get("text", "")[:200]
                                break
                            if isinstance(block, str):
                                first_user_message = block[:200]
                                break
                    elif isinstance(content, str):
                        first_user_message = content[:200]
                if not model:
                    model = (
                        entry.get("model")
                        or entry.get("message", {}).get("model")
                        or ""
                    )
                if role in ("user", "assistant"):
                    turn_count += 1
    except OSError:
        pass

    return {
        "session_id": session_id,
        "started_at": started_at or "",
        "first_user_message": first_user_message.strip().replace("\n", " "),
        "model": model,
        "turn_count": turn_count,
        "path": str(jsonl_path),
        "mtime": datetime.fromtimestamp(jsonl_path.stat().st_mtime, tz=timezone.utc).isoformat(),
    }


def slugify(text: str, max_len: int = 60) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"\s+", "-", text).strip("-")
    if not text:
        return "session"
    return text[:max_len].rstrip("-")


def render_block(block) -> str:
    """Render a content block (text / tool_use / tool_result / thinking) to markdown."""
    if isinstance(block, str):
        return block.strip()
    if not isinstance(block, dict):
        return ""

    btype = block.get("type")

    if btype == "text":
        return (block.get("text") or "").strip()

    if btype == "thinking":
        thinking = (block.get("thinking") or "").strip()
        if not thinking:
            return ""
        return f"> _thinking_\n>\n> {thinking.replace(chr(10), chr(10) + '> ')}"

    if btype == "tool_use":
        name = block.get("name", "tool")
        tool_input = block.get("input", {})
        try:
            input_str = json.dumps(tool_input, indent=2, ensure_ascii=False)
        except (TypeError, ValueError):
            input_str = str(tool_input)
        return f"**Tool call** · `{name}`\n\n```json\n{input_str}\n```"

    if btype == "tool_result":
        content = block.get("content", "")
        if isinstance(content, list):
            content = "\n".join(render_block(c) for c in content if c)
        elif not isinstance(content, str):
            content = str(content)
        truncated = content[:2000]
        suffix = " ... [truncated]" if len(content) > 2000 else ""
        return f"**Tool result**\n\n```\n{truncated}{suffix}\n```"

    return ""


def render_session(jsonl_path: Path, include_thinking: bool = True) -> tuple[str, dict]:
    """Render a JSONL session to markdown. Returns (markdown_string, meta_dict)."""
    meta = parse_session_meta(jsonl_path)
    lines = []
    lines.append(f"# Session · {meta['session_id'][:8]}")
    lines.append("")
    lines.append(f"- **Started**: {meta['started_at'] or meta['mtime']}")
    lines.append(f"- **Model**: {meta['model'] or 'unknown'}")
    lines.append(f"- **Turns**: {meta['turn_count']}")
    lines.append(f"- **First message**: {meta['first_user_message'] or '(empty)'}")
    lines.append("")
    lines.append("---")
    lines.append("")

    with open(jsonl_path, encoding="utf-8") as f:
        for line in f:
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue

            role = entry.get("role") or entry.get("type")
            ts = entry.get("timestamp", "")
            if role not in ("user", "assistant"):
                continue

            content = entry.get("content")
            if content is None:
                msg = entry.get("message", {})
                content = msg.get("content")
                if not role and msg.get("role"):
                    role = msg["role"]

            if not content:
                continue

            label = "User" if role == "user" else "Assistant"
            lines.append(f"## {label}{' · ' + ts if ts else ''}")
            lines.append("")

            if isinstance(content, str):
                lines.append(content.strip())
                lines.append("")
            elif isinstance(content, list):
                for block in content:
                    btype = block.get("type") if isinstance(block, dict) else None
                    if btype == "thinking" and not include_thinking:
                        continue
                    rendered = render_block(block)
                    if rendered:
                        lines.append(rendered)
                        lines.append("")

            lines.append("---")
            lines.append("")

    return "\n".join(lines), meta


def parse_duration(spec: str) -> timedelta:
    """Parse '1 week', '3 days', '12 hours' into a timedelta."""
    spec = spec.strip().lower()
    m = re.match(r"^(\d+)\s*(second|seconds|minute|minutes|hour|hours|day|days|week|weeks)$", spec)
    if not m:
        raise ValueError(f"Invalid duration: {spec}")
    n = int(m.group(1))
    unit = m.group(2).rstrip("s")
    return {
        "second": timedelta(seconds=n),
        "minute": timedelta(minutes=n),
        "hour": timedelta(hours=n),
        "day": timedelta(days=n),
        "week": timedelta(weeks=n),
    }[unit]


def pick_session_interactive(sessions: list[Path]) -> Path | None:
    """Print the N most recent sessions and prompt the operator for a choice."""
    if not sessions:
        print("No sessions found.", file=sys.stderr)
        return None

    print("Recent sessions:\n")
    metas = []
    for i, path in enumerate(sessions[:20], start=1):
        meta = parse_session_meta(path)
        metas.append(meta)
        ts = meta["mtime"][:16].replace("T", " ")
        msg = meta["first_user_message"] or "(empty)"
        if len(msg) > 70:
            msg = msg[:70] + "..."
        model = meta["model"] or "?"
        turns = meta["turn_count"]
        print(f"  {i:2}. [{ts}] {msg}")
        print(f"      model={model} turns={turns} id={meta['session_id'][:8]}")

    print("")
    try:
        choice = input("Pick a number (1-20), or q to quit: ").strip()
    except (EOFError, KeyboardInterrupt):
        return None
    if choice.lower() in ("q", "quit", ""):
        return None
    try:
        idx = int(choice) - 1
        return sessions[idx]
    except (ValueError, IndexError):
        print(f"Invalid choice: {choice}", file=sys.stderr)
        return None


def filter_session_by_spec(sessions: list[Path], spec: str) -> Path | None:
    """Match a session by UUID prefix or YYYY-MM-DD date prefix."""
    spec = spec.strip()
    for path in sessions:
        if path.stem.startswith(spec):
            return path
    if re.match(r"^\d{4}-\d{2}-\d{2}", spec):
        for path in sessions:
            mtime_iso = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).isoformat()
            if mtime_iso.startswith(spec):
                return path
    spec_l = spec.lower()
    for path in sessions:
        meta = parse_session_meta(path)
        if spec_l in meta["first_user_message"].lower():
            return meta and Path(meta["path"])
    return None


def export_one(jsonl_path: Path, output_dir: Path, include_thinking: bool) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    md, meta = render_session(jsonl_path, include_thinking=include_thinking)

    started = meta.get("started_at") or meta.get("mtime")
    date_prefix = (started[:10] if started else datetime.utcnow().strftime("%Y-%m-%d"))
    slug = slugify(meta["first_user_message"] or "session")
    filename = f"{date_prefix}-{slug}.md"
    out_path = output_dir / filename

    counter = 1
    while out_path.exists():
        counter += 1
        out_path = output_dir / f"{date_prefix}-{slug}-{counter}.md"

    out_path.write_text(md, encoding="utf-8")
    return out_path


def main():
    parser = argparse.ArgumentParser(description="Export a Claude Code session to markdown.")
    parser.add_argument("--current", action="store_true", help="Export the most recent session.")
    parser.add_argument("--pick", action="store_true", help="Interactive pick from recent sessions.")
    parser.add_argument("--session", help="Session UUID prefix, date prefix, or topic substring.")
    parser.add_argument("--since", help='Batch export sessions newer than duration, e.g. "1 week".')
    parser.add_argument("--list", action="store_true", help="List recent sessions and exit.")
    parser.add_argument("--to", default="./_sessions-archive", help="Output directory.")
    parser.add_argument("--workspace", default=os.getcwd(), help="Workspace root.")
    parser.add_argument("--no-thinking", action="store_true", help="Strip thinking blocks.")
    args = parser.parse_args()

    workspace_path = Path(args.workspace).resolve()
    project_dir = find_project_dir(workspace_path)
    if project_dir is None:
        print(f"No Claude Code project folder found for workspace: {workspace_path}", file=sys.stderr)
        print(f"Looked under: {CLAUDE_PROJECTS_ROOT / workspace_to_project_key(workspace_path)}", file=sys.stderr)
        sys.exit(1)

    sessions = list_session_files(project_dir)
    if not sessions:
        print(f"No session files found in {project_dir}", file=sys.stderr)
        sys.exit(1)

    output_dir = Path(args.to)
    if not output_dir.is_absolute():
        output_dir = workspace_path / output_dir

    include_thinking = not args.no_thinking

    if args.list:
        print(f"Sessions in {project_dir}:\n")
        for path in sessions[:30]:
            meta = parse_session_meta(path)
            ts = meta["mtime"][:16].replace("T", " ")
            msg = (meta["first_user_message"] or "(empty)")[:80]
            print(f"[{ts}] turns={meta['turn_count']:3} model={meta['model'] or '?':12} {msg}")
        return

    targets: list[Path] = []

    if args.since:
        try:
            delta = parse_duration(args.since)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(2)
        cutoff = datetime.now(timezone.utc) - delta
        for path in sessions:
            mtime = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
            if mtime >= cutoff:
                targets.append(path)
        if not targets:
            print(f"No sessions newer than {args.since}", file=sys.stderr)
            sys.exit(0)
    elif args.session:
        match = filter_session_by_spec(sessions, args.session)
        if match is None:
            print(f"No session matched: {args.session}", file=sys.stderr)
            sys.exit(1)
        targets = [match]
    elif args.pick:
        match = pick_session_interactive(sessions)
        if match is None:
            print("Cancelled.", file=sys.stderr)
            sys.exit(0)
        targets = [match]
    elif args.current:
        targets = [sessions[0]]
    else:
        if len(sessions) > 1:
            match = pick_session_interactive(sessions)
            if match is None:
                print("Cancelled.", file=sys.stderr)
                sys.exit(0)
            targets = [match]
        else:
            targets = [sessions[0]]

    print(f"Exporting {len(targets)} session(s) to {output_dir}")
    for jsonl_path in targets:
        out_path = export_one(jsonl_path, output_dir, include_thinking)
        print(f"  ✓ {out_path}")

    print("\nDone.")


if __name__ == "__main__":
    main()
