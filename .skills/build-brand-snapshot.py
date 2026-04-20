#!/usr/bin/env python3
"""
Builds brands/{slug}/_snapshot.md from a brand's JSON files.

The snapshot is a 1-2KB plaintext digest the agent reads at session start
instead of reading brand.json + every product + every audience + offers +
strategy separately. Cache-friendly, compose-free.

Usage:
    python3 .skills/build-brand-snapshot.py {brand_slug}
    python3 .skills/build-brand-snapshot.py --all

Run from workspace-template root.
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timezone

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
BRANDS = ROOT / "brands"


def load_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def short(s, n=120):
    if not s:
        return "—"
    s = str(s).replace("\n", " ").strip()
    return s if len(s) <= n else s[: n - 1] + "…"


def build_snapshot(brand_dir):
    slug = brand_dir.name
    brand = load_json(brand_dir / "brand.json") or {}
    strategy = load_json(brand_dir / "strategy.json") or {}

    lines = [f"# {slug} — snapshot", ""]

    # Identity
    identity = brand.get("identity", {})
    lines.append("## Identity")
    lines.append(f"- Name: {short(identity.get('name') or identity.get('brand_name'))}")
    lines.append(f"- Tagline: {short(identity.get('tagline') or identity.get('positioning_statement'))}")
    lines.append(f"- Sector: {short(identity.get('sector') or brand.get('sector'))}")
    lines.append(f"- Language: {short(identity.get('language'))}")
    tone = brand.get("tone_of_voice", {}) or brand.get("voice", {})
    if tone:
        lines.append(f"- Tone essentials: {short(tone.get('essence') or tone.get('register') or tone.get('signature'))}")
    lines.append("")

    # Products
    products_dir = brand_dir / "products"
    products = []
    if products_dir.exists():
        for p in sorted(products_dir.iterdir()):
            if p.is_dir() and not p.name.startswith("_"):
                spec = load_json(p / "spec.json") or {}
                pid = spec.get("identity", {})
                products.append({
                    "slug": p.name,
                    "name": pid.get("product_name") or pid.get("name") or p.name,
                    "price": (spec.get("pricing", {}) or {}).get("price_display") or (spec.get("pricing", {}) or {}).get("base_price"),
                    "hero": pid.get("hero") or pid.get("is_hero"),
                })
    lines.append(f"## Products ({len(products)})")
    for p in products[:10]:
        hero_mark = " ★" if p["hero"] else ""
        price = f" — {p['price']}" if p["price"] else ""
        lines.append(f"- {p['slug']}{hero_mark}{price}")
    if len(products) > 10:
        lines.append(f"- … +{len(products) - 10} more")
    lines.append("")

    # Audiences
    audiences_dir = brand_dir / "audiences"
    audiences = []
    if audiences_dir.exists():
        for a in sorted(audiences_dir.iterdir()):
            if a.is_dir() and not a.name.startswith("_"):
                profile = load_json(a / "profile.json") or {}
                pid = profile.get("identity", {})
                pains = (profile.get("psychology", {}) or {}).get("pain_points", []) or profile.get("pain_points", [])
                audiences.append({
                    "slug": a.name,
                    "label": pid.get("label") or pid.get("name") or a.name,
                    "primary": pid.get("primary") or pid.get("is_primary"),
                    "pains": [p.get("label") if isinstance(p, dict) else str(p) for p in pains[:2]],
                })
    lines.append(f"## Audiences ({len(audiences)})")
    for a in audiences[:6]:
        primary_mark = " ★" if a["primary"] else ""
        lines.append(f"- {a['slug']}{primary_mark}: {short(a['label'], 60)}")
        if a["pains"]:
            lines.append(f"  Top pains: {', '.join(short(p, 40) for p in a['pains'])}")
    if len(audiences) > 6:
        lines.append(f"- … +{len(audiences) - 6} more")
    lines.append("")

    # Offers
    offers_count = 0
    offer_types = {}
    if products_dir.exists():
        for p in products_dir.iterdir():
            if p.is_dir() and not p.name.startswith("_"):
                offers_doc = load_json(p / "offers.json") or {}
                offers = offers_doc.get("offers", []) if isinstance(offers_doc, dict) else []
                for off in offers:
                    if isinstance(off, dict) and off.get("active", True) is not False:
                        offers_count += 1
                        t = off.get("type") or "other"
                        offer_types[t] = offer_types.get(t, 0) + 1
    lines.append(f"## Offers active: {offers_count}")
    if offer_types:
        breakdown = ", ".join(f"{k}:{v}" for k, v in sorted(offer_types.items()))
        lines.append(f"- By type: {breakdown}")
    lines.append("")

    # Strategy
    if strategy:
        focus = strategy.get("current_focus") or strategy.get("monthly_focus") or (strategy.get("goals", {}) or {}).get("current")
        lines.append("## Strategy")
        lines.append(f"- Current focus: {short(focus)}")
        if strategy.get("targets"):
            t = strategy["targets"] if isinstance(strategy["targets"], str) else short(json.dumps(strategy["targets"]), 100)
            lines.append(f"- Targets: {t}")
        lines.append("")

    # Pending / status
    status = load_json(brand_dir / "status.json") or {}
    if status:
        lines.append("## Status")
        lines.append(f"- Wedge complete: {status.get('wedge_complete', False)}")
        level = status.get("context_level") or status.get("level")
        if level:
            lines.append(f"- Context level: {level}")
        lines.append("")

    lines.append(f"_Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}_")
    lines.append(f"_Refresh: python3 .skills/build-brand-snapshot.py {slug}_")

    (brand_dir / "_snapshot.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return len(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 .skills/build-brand-snapshot.py {slug} | --all", file=sys.stderr)
        sys.exit(1)
    arg = sys.argv[1]
    if arg == "--all":
        for d in sorted(BRANDS.iterdir()):
            if d.is_dir() and not d.name.startswith("_"):
                n = build_snapshot(d)
                print(f"{d.name}: {n} lines")
    else:
        d = BRANDS / arg
        if not d.exists():
            print(f"brand not found: {d}", file=sys.stderr)
            sys.exit(1)
        n = build_snapshot(d)
        print(f"{arg}: {n} lines")


if __name__ == "__main__":
    main()
