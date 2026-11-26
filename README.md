# Fearless Draft Lab

A League of Legends draft simulator with **Fearless Draft** rules, opponent
pick/ban tendencies, and live win-rate impact — built for coaches' pre-match
preparation.

Entry for **Cloud9 x JetBrains: Sky's The Limit Hackathon 2026** (Category 2:
LoL Macro Scouting & Draft Management System).

- Devpost: https://cloud9.devpost.com/
- Submission deadline: 12 Jan 2027 11:00 PT (13 Jan 2027 02:00 WIB)

## What it does

1. **Interactive draft simulator** — pick/ban phases, blue/red side, BO3/BO5
   series tracking. *(Weeks 2–3)*
2. **Fearless Draft mode** — champions picked in earlier games of a series are
   locked out of later games, with the champion pool visibly shrinking in
   Game 3 / Game 5. *(Weeks 2–3)*
3. **Opponent tendency panel** — pick/ban rates per champion, first-pick
   tendencies, role pools, derived from pro-match data. *(Week 1 — live)*
4. **Live win-rate impact** — predicted win % that updates with every
   pick/ban. *(Week 4)*
5. **"How to Win" insights** — data-backed counter-strategy suggestions
   (e.g. "Opponent picks Sejuani 70% in Game 1 — ban her and their Fearless
   Game 2 win-rate drops 15%"). *(Week 4)*

## Stack (locked, Week 1)

| Tool | Version |
| --- | --- |
| Node.js | ≥ 20 (tested 24.22.1) |
| React | 19.3.1 (exact) |
| React DOM | 19.3.1 (exact) |
| Vite | 8.4.0 (exact) |
| @vitejs/plugin-react | 6.3.0 (exact) |
| oxlint | 1.95.0 (exact, `npm run lint`) |
| Python (extraction only) | 3.12, stdlib only — no extra packages |

All versions are pinned exact in `package.json` and `package-lock.json`.

## Run it

```bash
npm install
npm run dev      # dev server, http://localhost:5173
npm run build    # production build into dist/
npm run preview  # serve the production build
npm run extract  # regenerate src/data/*.json from the GRID meta CSVs
npm run lint     # oxlint
```

## Data

Tendency data is derived from the official GRID starter data for this
hackathon (https://github.com/cloud9esports/stl-hackathon-2026-grid-starter).
**The GRID data files are NOT included in this repository** — they are
licensed only for building the hackathon project and must never be
redistributed. Clone the starter repo next to this project and point the
build at it via `STL_DATA_DIR` (see `.gitignore`).

### Data pipeline (Week 1)

`scripts/extract-tendencies.py` reads only the small `meta/` CSVs
(`games.csv`, `rosters.csv`, `teams.csv`, `players.csv`) — no `.zst` file is
ever decompressed — and writes aggregate JSON into `src/data/`:

| File | Contents |
| --- | --- |
| `meta.json` | Totals, patch list, date range, Cloud9 Kia record |
| `champions.json` | Pick rate + win rate per champion (all teams) |
| `champions-by-game-number.json` | Same, split by series game 1–5 (Fearless relevance) |
| `cloud9-kia.json` | C9 Kia champion pool, per-player pools, most-faced opponents |
| `top-teams.json` | 15 most active teams + their top picks |

Definitions: a pick = one active roster row; a win = the picker's team won
the game. A champion can be picked at most once per game, so pick rate =
games with that pick / total games.

Current snapshot (26 Nov 2026): **1,739 finished LoL games** (15 Jan 2025 –
13 Oct 2026, 28 patches, 156 champions, 45 teams). Cloud9 Kia:
**90W–52L (63.4%)** over 142 games. Most picked overall: Xin Zhao 28.8%,
Rumble 27.5%, Ezreal 24.3%. Cloud9 Kia's most picked: Corki (24, 75% WR),
Ezreal (22), Renekton (21).

## Built with JetBrains

- WebStorm + JetBrains Air + AI Coding Agent Junie (tooling write-up in
  `AI_SHOWCASE.md` once the build lands). Trial codes arrive ~3 Dec 2026;
  until then the build uses the WebStorm trial/EAP. The `.idea/`, `.junie/`
  and `.air/` folders will be committed as proof of JetBrains usage.

## Status

Week 1 done: stack locked + builds, tendency extraction from GRID meta CSVs,
opponent tendency panel live in the app. Next: draft engine + Fearless mode
(Weeks 2–3, see `docs/design/wireframe.md` for the component map).
