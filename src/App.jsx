import champions from './data/champions.json'
import cloud9 from './data/cloud9-kia.json'
import meta from './data/meta.json'
import TendencyPanel from './components/TendencyPanel.jsx'
import './App.css'

function Stat({ label, value, sub }) {
  return (
    <div className="stat">
      <div className="stat-value">{value}</div>
      <div className="stat-label">{label}</div>
      {sub ? <div className="stat-sub">{sub}</div> : null}
    </div>
  )
}

function App() {
  return (
    <div className="app">
      <header className="app-header">
        <div className="logo-mark">FDL</div>
        <div>
          <h1>Fearless Draft Lab</h1>
          <p className="subtitle">
            LoL draft simulator with Fearless Draft rules, opponent tendencies
            and live win-rate impact — Cloud9 x JetBrains: Sky&apos;s The Limit
            Hackathon 2026, Category 2.
          </p>
        </div>
        <span className="badge">Week 1 — data + stack</span>
      </header>

      <section className="stats" aria-label="Dataset summary">
        <Stat
          label="LoL games analysed"
          value={meta.total_lol_games.toLocaleString('en-US')}
          sub={`${meta.date_range[0].slice(0, 10)} → ${meta.date_range[1].slice(0, 10)}`}
        />
        <Stat
          label="Champions seen"
          value={meta.champions_seen}
          sub={`${meta.patch_count} patches (${meta.patches[0]} – ${meta.patches[meta.patches.length - 1]})`}
        />
        <Stat
          label="Cloud9 Kia record"
          value={`${meta.cloud9_kia.wins}W–${meta.cloud9_kia.games - meta.cloud9_kia.wins}L`}
          sub={`win rate ${(meta.cloud9_kia.win_rate * 100).toFixed(1)}% over ${meta.cloud9_kia.games} games`}
        />
        <Stat
          label="Series games"
          value={`G1 ${meta.games_by_game_number['1']} · G5 ${meta.games_by_game_number['5']}`}
          sub="Fearless pool shrinks from Game 3 on — see Game 5 data"
        />
      </section>

      <main>
        <TendencyPanel champions={champions} cloud9={cloud9} />
      </main>

      <footer className="app-footer">
        <p>
          Tendency data: aggregate statistics derived from the official GRID
          starter meta CSVs for this hackathon. Raw GRID data is NOT in this
          repository. Draft engine, Fearless mode and live win-rate impact land
          in Weeks 2–4.
        </p>
        <p>
          Built with React 19.3.1 + Vite 8.4.0 · Node ≥ 20 · Data regenerated
          with <code>python3 scripts/extract-tendencies.py</code>
        </p>
      </footer>
    </div>
  )
}

export default App
