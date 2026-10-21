#!/usr/bin/env python3
"""Publish curated daily French lessons, without an AI API or external packages."""
import datetime as dt
import json
import os
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
queue = json.loads((ROOT / "automation/content-queue.json").read_text(encoding="utf-8"))
days = queue["days"]
assert len({d["day"] for d in days}) == len(days), "Duplicate day IDs"
assert len({w["word"].casefold() for d in days for w in d["vocabulary"]}) == sum(len(d["vocabulary"]) for d in days), "Duplicate vocabulary"
assert len({d["title"].casefold() for d in days}) == len(days), "Duplicate story titles"
for d in days:
    assert d["story"] and len(d["vocabulary"]) >= 3 and len(d["verbs"]) >= 2
today = dt.date.fromisoformat(os.environ.get("CONTENT_DATE", dt.datetime.now(ZoneInfo(queue["timezone"])).date().isoformat()))
elapsed = (today - dt.date.fromisoformat(queue["start_date"])).days + 1
released = [d for d in days if d["day"] <= elapsed]
output = {"last_checked": today.isoformat(), "released_count": len(released), "total_prepared": len(days), "lessons": released}
path = ROOT / "automation/published.json"
serialized = json.dumps(output, ensure_ascii=False, indent=2) + "\n"
if not path.exists() or path.read_text(encoding="utf-8") != serialized:
    path.write_text(serialized, encoding="utf-8")
    print(f"Published {len(released)}/{len(days)} lessons for {today}")
else:
    print("No changes")
if elapsed > len(days):
    print("WARNING: curated content queue exhausted; prepare more lessons.")
