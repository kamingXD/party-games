# Party Games

Four teams of three. Cantonese party controls, editable questions, shared scores and fifty original red/black discussion prompts.

## Hosting

- GitHub Pages: `https://kamingxd.github.io/party-games/`.
- Audience: append `#audience`; host: append `#host` and enter the existing host PIN.
- Shared score service: `https://party-game-scoreboard.kaming-pong-work.chatgpt.site/api/party/state`, backed by persistent D1 storage.
- The service accepts CORS requests from the specific GitHub Pages origin. Only PIN-authenticated requests can update state. The PIN remains in tab memory and is never committed or placed in a URL.
- Viewers refresh every three seconds. Scores and per-question grading history are shared. Timer and question-bank edits remain local to the host browser.
- Writes use a database revision check; concurrent hosts cannot silently overwrite each other. Failed/uncertain writes reload authoritative state before the host retries.

## Rules and content

- Big TV: twenty words per team, five-minute default, correct +10.
- Mandatory: ten four-choice questions per team, correct +10, wrong 0; supplementary attempts use the same scores.
- Buzzer: one shared twenty-question list; first correct +20, supplementary correct +10, wrong −10.
- Bank: 24 contemporary culture/context questions and 36 original troll/logic questions. Historical culture event questions focus on 2023–2025; sources and explanations are included.
- `notes/red-black-ocamp.md`: fifty original nonsexual, deeper yes/no discussion prompts, with optional follow-ups in five themes. The same notes are available in the host UI.

## Build and edit

```sh
python3 scripts/build.py
```

- `src/app.template.html`: interface and controls.
- `data/game-pack.json`: canonical question bank.
- `notes/red-black-ocamp.json`: canonical discussion prompts.
- `docs/index.html`: online version.
- `docs/offline.html`: standalone offline version, with no runtime network requests.

Use the question editor for text, choices, answer key, explanations, categories and words. Browser edits do not update GitHub automatically. Export JSON, replace `data/game-pack.json`, rebuild, then commit and push to publish permanent changes. Download updated HTML for a portable offline copy.

Scores and grading history are preserved when editing questions. Reset them before a new event when appropriate. Online storage and offline browser storage are separate; the online game does not upload previously stored offline scores automatically.

## Privacy and access

The public static HTML contains questions and answer keys. Audience mode hides host controls; score-write authorization is enforced by the separate service. Do not put private participant notes or secrets in the public question bank. Discussion notes do not record participant responses.

## Deployment

GitHub Pages publishes the `main` branch `/docs` folder. `.nojekyll` bypasses Jekyll. The D1 score service is deployed separately through Sites; its existing score table is preserved and a new `party_sessions` table stores the shared session.
