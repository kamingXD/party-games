#!/usr/bin/env python3
"""Build one self-contained HTML file for Pages and offline use."""
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
pack = json.loads((root / "data/game-pack.json").read_text(encoding="utf-8"))
if len(pack["words"]) != 4 or any(len(w["items"]) != 20 for w in pack["words"]):
    raise ValueError("Expected four teams with 20 words each")
if len(pack["mandatory"]) != 40 or len(pack["buzzer"]) != 20:
    raise ValueError("Expected 40 mandatory and 20 shared buzzer questions")
for team in "ABCD":
    if sum(q["team"] == team for q in pack["mandatory"]) != 10:
        raise ValueError(f"Expected ten mandatory questions for {team}")
questions = pack["mandatory"] + pack["buzzer"]
if len({q["id"] for q in questions}) != len(questions):
    raise ValueError("Question IDs must be unique")
for q in questions:
    if len(q["choices"]) != 4 or q["answer"] != q["choices"][q["answerIndex"]]:
        raise ValueError(f"Invalid answer choices for {q['id']}")
serialized = json.dumps(pack, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")
template = (root / "src/app.template.html").read_text(encoding="utf-8")
if template.count("__GAME_DATA__") != 1:
    raise ValueError("Template must contain exactly one data marker")
notes = json.loads((root / "notes/red-black-ocamp.json").read_text(encoding="utf-8"))
if len(notes) != 50:
    raise ValueError("Expected fifty red/black prompts")
notes_json = json.dumps(notes, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")
base = template.replace("__GAME_DATA__", serialized).replace("__NOTES_DATA__", notes_json)
(root / "docs").mkdir(exist_ok=True)
for filename, config in [("index.html", {"enabled": True, "api": "https://party-game-scoreboard.kaming-pong-work.chatgpt.site/api/party/state"}), ("offline.html", {"enabled": False})]:
    html = base.replace("__SYNC_CONFIG__", json.dumps(config, separators=(",", ":")))
    output = root / "docs" / filename
    output.write_text(html, encoding="utf-8")
    print(f"Built {output}: {len(html.encode('utf-8')):,} bytes")
(root / "docs/.nojekyll").touch()
