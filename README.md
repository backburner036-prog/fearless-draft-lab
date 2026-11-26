# Fearless Draft Lab

A League of Legends draft simulator with **Fearless Draft** rules, opponent
pick/ban tendencies, and live win-rate impact — built for coaches' pre-match
preparation.

Entry for **Cloud9 x JetBrains: Sky's The Limit Hackathon 2026** (Category 2:
LoL Macro Scouting & Draft Management System).

- Devpost: https://cloud9.devpost.com/
- Submission deadline: 12 Jan 2027 11:00 PT (13 Jan 2027 02:00 WIB)

## What it does (planned)

1. **Interactive draft simulator** — pick/ban phases, blue/red side, BO3/BO5
   series tracking.
2. **Fearless Draft mode** — champions picked in earlier games of a series are
   locked out of later games, with the champion pool visibly shrinking in
   Game 3 / Game 5.
3. **Opponent tendency panel** — pick/ban rates per champion, first-pick
   tendencies, role pools, derived from pro-match data.
4. **Live win-rate impact** — predicted win % that updates with every
   pick/ban.
5. **"How to Win" insights** — data-backed counter-strategy suggestions
   (e.g. "Opponent picks Sejuani 70% in Game 1 — ban her and their Fearless
   Game 2 win-rate drops 15%").

## Built with JetBrains

- WebStorm + JetBrains Air + AI Coding Agent Junie (tooling write-up in
  `AI_SHOWCASE.md` once the build lands).

## Data

Tendency data is derived from the official GRID starter data for this
hackathon (https://github.com/cloud9esports/stl-hackathon-2026-grid-starter).
**The GRID data files are NOT included in this repository** — they are
licensed only for building the hackathon project and must never be
redistributed. Clone the starter repo next to this project and point the
build at it via `STL_DATA_DIR` (see `.gitignore`).

## Status

Scaffold only — build in progress (Week 1: data + design).
