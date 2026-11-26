/* TendencyPanel — S2 from the design wireframe (docs/design/wireframe.md).
 * Week 1: read-only tables from the extracted aggregate JSON.
 * Weeks 2-4: this panel becomes the live sidebar next to the draft board. */

function pct(x) {
  return `${(x * 100).toFixed(1)}%`
}

function ChampTable({ rows, limit = 10, showWins = true }) {
  return (
    <table className="champ-table">
      <thead>
        <tr>
          <th>#</th>
          <th>Champion</th>
          <th>Picks</th>
          <th>Pick rate</th>
          {showWins ? <th>Win rate</th> : null}
        </tr>
      </thead>
      <tbody>
        {rows.slice(0, limit).map((r, i) => (
          <tr key={r.champion}>
            <td>{i + 1}</td>
            <td className="champ-name">{r.champion}</td>
            <td>{r.picks}</td>
            <td>{pct(r.pick_rate)}</td>
            {showWins ? (
              <td className={r.win_rate >= 0.55 ? 'wr-high' : r.win_rate <= 0.45 ? 'wr-low' : ''}>
                {pct(r.win_rate)}
                {r.low_sample ? ' *' : ''}
              </td>
            ) : null}
          </tr>
        ))}
      </tbody>
    </table>
  )
}

function TendencyPanel({ champions, cloud9 }) {
  return (
    <section className="tendency-panel" aria-label="Opponent tendency panel">
      <h2>Opponent tendencies</h2>
      <p className="panel-note">
        Pick = champion played in a game (max once per game, so pick rate =
        share of games). Win rate = share of those games won. * = fewer than
        10 picks (low sample).
      </p>

      <div className="panel-grid">
        <div className="panel-card">
          <h3>Most picked — all teams</h3>
          <ChampTable rows={champions} limit={15} />
        </div>

        <div className="panel-card">
          <h3>Cloud9 Kia — champion pool</h3>
          <p className="panel-sub">
            {cloud9.games} games · {cloud9.wins}W–
            {cloud9.games - cloud9.wins}L · win rate{' '}
            {pct(cloud9.win_rate)}
          </p>
          <ChampTable rows={cloud9.champion_pool} limit={15} />
        </div>
      </div>

      <div className="panel-card">
        <h3>Cloud9 Kia — champion pool per player</h3>
        <div className="player-grid">
          {cloud9.player_pools.map((p) => (
            <div key={p.player} className="player-card">
              <div className="player-head">
                <strong>{p.player}</strong>
                <span>
                  {p.games}G · {p.wins}W · {pct(p.win_rate)} ·{' '}
                  {p.champions_played} champs
                </span>
              </div>
              <div className="player-pool">
                {p.pool.slice(0, 5).map((c) => (
                  <span key={c.champion} className="pool-chip">
                    {c.champion} ({c.picks}, {pct(c.win_rate)})
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="panel-card">
        <h3>Cloud9 Kia — most-faced opponents</h3>
        <table className="champ-table">
          <thead>
            <tr>
              <th>Opponent</th>
              <th>Games</th>
              <th>C9 win rate vs</th>
              <th>Their most-picked vs C9</th>
              <th>C9 most-picked vs them</th>
            </tr>
          </thead>
          <tbody>
            {cloud9.opponents.slice(0, 8).map((o) => (
              <tr key={o.team}>
                <td className="champ-name">{o.team}</td>
                <td>{o.games_vs_c9}</td>
                <td>{pct(o.c9_win_rate_vs)}</td>
                <td>
                  {o.their_top_picks_vs_c9
                    .map((c) => `${c.champion} (${c.picks})`)
                    .join(', ')}
                </td>
                <td>
                  {o.c9_top_picks_vs_them
                    .map((c) => `${c.champion} (${c.picks})`)
                    .join(', ')}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  )
}

export default TendencyPanel
