#!/usr/bin/env python3
"""Extract draft-tendency aggregates for Fearless Draft Lab (Week 1).

Reads the GRID starter *meta* CSVs (small files, no .zst decompression) from a
separate clone next to this repo and writes AGGREGATE JSON into src/data/.

Aggregate, derived numbers are safe to commit. The raw GRID files themselves
must NEVER be committed (see .gitignore + the leak check before every push).

Usage:
    python3 scripts/extract-tendencies.py [--meta-dir DIR] [--out-dir DIR]

Defaults: --meta-dir = $STL_DATA_DIR/meta, else
../cloud9-grid-data/meta (the sparse GRID clone next to this repo).
--out-dir defaults to src/data/.

Inputs (meta CSVs): games.csv, rosters.csv, teams.csv, players.csv.
A pick = one active roster row (champion, player, team, game).
A win  = the picker's team_id == games.winner_team_id.
"""

import argparse
import csv
import json
import os
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone

CLOUD9_KIA_ID = "47351"
CLOUD9_KIA_NAME = "Cloud9 Kia"

MIN_PICKS_OVERALL = 10  # champions below this are still listed, flagged low-sample


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def rate(n, d):
    return round(n / d, 4) if d else 0.0


def champion_table(picks, wins, total_games, label=""):
    """picks/wins: Counter champion -> count. Returns sorted list of dicts."""
    rows = []
    for champ in picks:
        p = picks[champ]
        w = wins.get(champ, 0)
        rows.append(
            {
                "champion": champ,
                "picks": p,
                "wins": w,
                "pick_rate": rate(p, total_games),
                "win_rate": rate(w, p),
                "low_sample": p < MIN_PICKS_OVERALL,
            }
        )
    rows.sort(key=lambda r: (-r["picks"], -r["win_rate"], r["champion"]))
    return rows


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--meta-dir", default=None)
    ap.add_argument("--out-dir", default=None)
    args = ap.parse_args()

    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    meta_dir = (
        args.meta_dir
        or os.path.join(os.environ.get("STL_DATA_DIR", ""), "meta")
        if os.environ.get("STL_DATA_DIR")
        else os.path.join(os.path.dirname(repo_root), "cloud9-grid-data", "meta")
    )
    out_dir = args.out_dir or os.path.join(repo_root, "src", "data")
    os.makedirs(out_dir, exist_ok=True)

    for name in ("games.csv", "rosters.csv", "teams.csv", "players.csv"):
        p = os.path.join(meta_dir, name)
        if not os.path.isfile(p):
            print(f"ERROR: missing {p} (set --meta-dir or STL_DATA_DIR)", file=sys.stderr)
            return 1

    games = [g for g in read_csv(os.path.join(meta_dir, "games.csv"))
             if g["title"] == "lol" and g.get("finished") == "True"]
    rosters = [r for r in read_csv(os.path.join(meta_dir, "rosters.csv"))
               if r["title"] == "lol" and r.get("participation_status") == "active"]
    teams = {t["team_id"]: t["name"] for t in read_csv(os.path.join(meta_dir, "teams.csv"))
             if t["title"] == "lol"}
    players = {p["player_id"]: p["name"] for p in read_csv(os.path.join(meta_dir, "players.csv"))
               if p["title"] == "lol"}

    game_by_id = {g["game_id"]: g for g in games}
    total_games = len(games)
    patches = sorted({g["patch"] for g in games if g.get("patch")})
    dates = [g["started_at"] for g in games if g.get("started_at")]
    c9_games = [g for g in games
                if g["team1_id"] == CLOUD9_KIA_ID or g["team2_id"] == CLOUD9_KIA_ID]
    c9_wins = sum(1 for g in c9_games if g["winner_team_id"] == CLOUD9_KIA_ID)

    # --- overall champion picks / wins -------------------------------------
    picks_all, wins_all = Counter(), Counter()
    picks_by_game_no = defaultdict(Counter)
    wins_by_game_no = defaultdict(Counter)
    games_by_no = Counter()
    for g in games:
        games_by_no[int(g["game_number"])] += 1

    # --- per-team + per-player ---------------------------------------------
    picks_team = defaultdict(Counter)   # team_id -> champion -> picks
    wins_team = defaultdict(Counter)
    games_team = Counter()
    picks_player = defaultdict(Counter)  # player_id -> champion -> picks
    wins_player = defaultdict(Counter)
    games_player = Counter()
    c9_opponents = Counter()             # opponent team_id -> games vs C9
    c9_opp_wins = Counter()              # opponent team_id -> C9 wins vs them
    picks_vs_c9 = defaultdict(Counter)   # opponent team_id -> champion -> picks vs C9
    wins_vs_c9 = defaultdict(Counter)    # opponent team_id -> champion -> wins vs C9
    picks_c9_vs = defaultdict(Counter)   # opponent team_id -> C9 champion picks
    wins_c9_vs = defaultdict(Counter)    # opponent team_id -> C9 champion wins

    for r in rosters:
        g = game_by_id.get(r["game_id"])
        if g is None:
            continue
        champ = r["character_name"]
        tid, pid = r["team_id"], r["player_id"]
        won = tid == g["winner_team_id"]
        gno = int(g["game_number"])
        picks_all[champ] += 1
        wins_all[champ] += won
        picks_by_game_no[gno][champ] += 1
        wins_by_game_no[gno][champ] += won
        picks_team[tid][champ] += 1
        wins_team[tid][champ] += won
        picks_player[pid][champ] += 1
        wins_player[pid][champ] += won
        if g["team1_id"] == CLOUD9_KIA_ID or g["team2_id"] == CLOUD9_KIA_ID:
            opp = (g["team2_id"] if g["team1_id"] == CLOUD9_KIA_ID
                   else g["team1_id"])
            if tid == CLOUD9_KIA_ID:
                picks_c9_vs[opp][champ] += 1
                wins_c9_vs[opp][champ] += won
            elif tid == opp:
                picks_vs_c9[opp][champ] += 1
                wins_vs_c9[opp][champ] += won

    for g in games:
        for tid in (g["team1_id"], g["team2_id"]):
            games_team[tid] += 1
        if g["team1_id"] == CLOUD9_KIA_ID or g["team2_id"] == CLOUD9_KIA_ID:
            opp = g["team2_id"] if g["team1_id"] == CLOUD9_KIA_ID else g["team1_id"]
            c9_opponents[opp] += 1
            if g["winner_team_id"] == CLOUD9_KIA_ID:
                c9_opp_wins[opp] += 1

    generated = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    source_note = (
        "Aggregate statistics derived from the Cloud9 x JetBrains Sky's The Limit "
        "2026 GRID starter meta CSVs (games.csv + rosters.csv). Raw GRID data is NOT "
        "in this repository. A pick = one active roster row; a win = the picker's "
        "team won the game. Champions can be picked at most once per game, so "
        "pick_rate = games with that pick / total games."
    )
    meta = {
        "generated_at_utc": generated,
        "source": source_note,
        "total_lol_games": total_games,
        "total_roster_rows": len(rosters),
        "champions_seen": len(picks_all),
        "teams_seen": len(games_team),
        "patches": patches,
        "patch_count": len(patches),
        "date_range": [min(dates), max(dates)] if dates else [],
        "games_by_game_number": {str(k): games_by_no[k] for k in sorted(games_by_no)},
        "cloud9_kia": {
            "team_id": CLOUD9_KIA_ID,
            "games": len(c9_games),
            "wins": c9_wins,
            "win_rate": rate(c9_wins, len(c9_games)),
        },
    }

    champions = champion_table(picks_all, wins_all, total_games)
    by_game_no = {
        str(gno): champion_table(picks_by_game_no[gno], wins_by_game_no[gno],
                                 games_by_no[gno])
        for gno in sorted(games_by_no)
    }

    # --- Cloud9 Kia profile -------------------------------------------------
    # Players who ever played for C9 Kia in these rosters.
    c9_pids = sorted({r["player_id"] for r in rosters
                      if r["team_id"] == CLOUD9_KIA_ID})
    player_pools = []
    for pid in c9_pids:
        # games played per player = distinct games in rosters for that player+C9
        gp = len({r["game_id"] for r in rosters
                  if r["player_id"] == pid and r["team_id"] == CLOUD9_KIA_ID})
        # wins: one roster row per player per game, so row count == games won.
        wp = sum(1 for r in rosters
                 if r["player_id"] == pid and r["team_id"] == CLOUD9_KIA_ID
                 and game_by_id.get(r["game_id"], {}).get("winner_team_id") == CLOUD9_KIA_ID)
        pool = champion_table(picks_player[pid], wins_player[pid], gp)
        player_pools.append({
            "player_id": pid,
            "player": players.get(pid, pid),
            "games": gp,
            "wins": wp,
            "win_rate": rate(wp, gp),
            "champions_played": len(pool),
            "pool": pool,
        })
    player_pools.sort(key=lambda p: (-p["games"], p["player"]))

    opponents = []
    for opp_id, n in c9_opponents.most_common():
        opponents.append({
            "team_id": opp_id,
            "team": teams.get(opp_id, opp_id),
            "games_vs_c9": n,
            "c9_wins_vs": c9_opp_wins.get(opp_id, 0),
            "c9_win_rate_vs": rate(c9_opp_wins.get(opp_id, 0), n),
            "their_top_picks_vs_c9": champion_table(
                picks_vs_c9[opp_id], wins_vs_c9[opp_id], n)[:5],
            "c9_top_picks_vs_them": champion_table(
                picks_c9_vs[opp_id], wins_c9_vs[opp_id], n)[:5],
        })

    c9 = {
        "team_id": CLOUD9_KIA_ID,
        "team": CLOUD9_KIA_NAME,
        "games": len(c9_games),
        "wins": c9_wins,
        "win_rate": rate(c9_wins, len(c9_games)),
        "champion_pool": champion_table(picks_team[CLOUD9_KIA_ID],
                                        wins_team[CLOUD9_KIA_ID], len(c9_games)),
        "player_pools": player_pools,
        "opponents": opponents,
    }

    # --- top-team table (context: who plays most) ---------------------------
    top_teams = []
    for tid, n in games_team.most_common(15):
        w = sum(1 for g in games
                if tid in (g["team1_id"], g["team2_id"])
                and g["winner_team_id"] == tid)
        top_teams.append({
            "team_id": tid, "team": teams.get(tid, tid), "games": n,
            "wins": w, "win_rate": rate(w, n),
            "top_picks": champion_table(picks_team[tid], wins_team[tid], n)[:5],
        })

    def dump(name, obj):
        path = os.path.join(out_dir, name)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(obj, f, indent=2, ensure_ascii=False)
            f.write("\n")
        print(f"wrote {path} ({os.path.getsize(path)} bytes)")

    dump("meta.json", meta)
    dump("champions.json", champions)
    dump("champions-by-game-number.json", by_game_no)
    dump("cloud9-kia.json", c9)
    dump("top-teams.json", top_teams)

    print(f"OK: {total_games} LoL games, {len(picks_all)} champions, "
          f"C9 Kia {c9_wins}W-{len(c9_games) - c9_wins}L "
          f"({rate(c9_wins, len(c9_games)) * 100:.1f}%)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
