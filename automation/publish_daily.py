#!/usr/bin/env python3
"""Publish one unused curated French lesson per Vietnam day. Never edit index032.html."""
import datetime as dt
import html
import json
from pathlib import Path
from zoneinfo import ZoneInfo

root = Path(__file__).resolve().parent.parent
data = json.loads((root / "automation" / "content-bank.json").read_text(encoding="utf-8"))
entries = data["entries"]
ids = [e["id"] for e in entries]
assert len(ids) == len(set(ids)), "Duplicate lesson IDs"
required = {"id", "theme", "word", "type", "ipa", "vi", "example", "story", "verb", "present", "passe_compose", "imparfait"}
assert all(required.issubset(e) and all(str(e[k]).strip() for k in required) for e in entries)
state_path = root / "automation" / "published.json"
state = json.loads(state_path.read_text(encoding="utf-8")) if state_path.exists() else {"published": []}
published = state["published"]
assert len(published) == len(set(published)), "Duplicate published IDs"
today = dt.datetime.now(ZoneInfo("Asia/Ho_Chi_Minh")).date().isoformat()
if state.get("last_date") == today:
    print("Already published for", today)
    raise SystemExit(0)
entry = next((e for e in entries if e["id"] not in published), None)
if entry is None:
    print("Content bank exhausted; refusing to repeat old lessons.")
    raise SystemExit(1)
esc = lambda value: html.escape(str(value), quote=True)
page = f"""<!doctype html>
<html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Bài tiếng Pháp ngày {today}</title>
<style>body{{font-family:system-ui,sans-serif;max-width:700px;margin:auto;padding:20px;line-height:1.65;background:#f7f9fc;color:#203447}}article{{background:white;padding:20px;border-radius:14px;margin:15px 0;border:1px solid #dce4ed}}h1{{font-size:1.5rem}}h2{{font-size:1.2rem}}a{{color:#145e8a}}.fr{{font-size:1.12rem}}</style></head>
<body><nav><a href="index032.html">← Ứng dụng học chính (bản 032)</a></nav>
<h1>Bài tiếng Pháp ngày {today}</h1><p>Chủ đề: {esc(entry["theme"])} · A1–A2 · Ôn passé composé và imparfait</p>
<article><h2>1. Từ vựng</h2><p class="fr"><b>{esc(entry["word"])}</b> — {esc(entry["ipa"])}</p>
<p>{esc(entry["type"])} · {esc(entry["vi"])}</p><p lang="fr" class="fr">{esc(entry["example"])}</p></article>
<article><h2>2. Đọc hiểu</h2><p lang="fr" class="fr">{esc(entry["story"])}</p></article>
<article><h2>3. Động từ: {esc(entry["verb"])}</h2>
<p>Présent: <span lang="fr">{esc(entry["present"])}</span></p>
<p>Passé composé: <span lang="fr">{esc(entry["passe_compose"])}</span></p>
<p>Imparfait: <span lang="fr">{esc(entry["imparfait"])}</span></p></article>
<p>Kho bài có giới hạn, không tự tạo bằng AI. Khi dùng hết bài đã chuẩn bị, quy trình dừng thay vì lặp nội dung.</p>
</body></html>"""
(root / "contenu-du-jour.html").write_text(page, encoding="utf-8")
published.append(entry["id"])
state.update({"published": published, "last_date": today, "latest_id": entry["id"]})
state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("Published", entry["id"], "for", today)
