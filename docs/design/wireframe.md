# Fearless Draft Lab — Design Wireframe & Spesifikasi UI

**Proyek:** Fearless Draft Lab — entry Cloud9 x JetBrains Sky's The Limit Hackathon 2026,
Kategori 2 (LoL Macro Scouting & Draft Management System)
**Desainer:** Gusdur (Mission Control) · **Minggu 1:** 27 Nov–3 Des 2026
**Mockup interaktif:** [`mockup.html`](./mockup.html) — buka di browser, semua layar + state bisa diklik.
**Stack target:** React + Vite (Habibie, Minggu 2–3) — semua komponen di bawah dipetakan ke komponen React di §7.

> **Aset orisinal:** semua visual di mockup ini dibuat dari CSS/SVG murni (monogram huruf +
> bentuk geometris). TIDAK ada artwork, logo, atau aset Riot/Cloud9. Nama champion dipakai
> sebagai label data saja (fakta permainan), tile champion memakai monogram orisinal.
> Logo "FDL" di mockup adalah mark orisinal (heksagon + huruf F).

---

## 1. Ringkasan layar

| # | Layar / state | Isi utama | Status di mockup |
|---|---|---|---|
| S0 | **Setup (empty state)** | Pilih sisi (Blue/Red), lawan (preset: Cloud9 Kia dll.), format seri BO3/BO5, toggle Fearless | Layar awal mockup |
| S1 | **Draft utama — fase Ban/Pick** | Board Blue vs Red, grid champion, stepper fase, timer | Layar utama mockup |
| S2 | **Panel tendensi lawan** | Pick/ban rate per champion, first-pick, pool per role, sample size | Sidebar kanan (selalu terlihat) |
| S3 | **Indikator win-rate live** | Bar Blue vs Red + delta per pick/ban, angka % | Di atas board + sidebar |
| S4 | **Mode Fearless — pool menyusut** | Tab Game 1/2/3, champion terkunci per game, counter pool tersisa | Panel Fearless (sidebar) + tile terkunci di grid |
| S5 | **Akhir draft (end state)** | Ringkasan komposisi kedua tim, win-rate final, kartu "How to Win", aksi lanjut | Overlay/panel akhir di mockup |

Alur: S0 → S1 (20 langkah draft) → S5 → "Next Game" (Fearless: champion yang
sudah ter-pick terkunci, kembali ke S1 Game 2 dengan pool menyusut) → … → seri selesai.

Urutan draft (format standar LoL, dipakai mockup + engine):
`Ban B,R,B,R,B,R → Pick B,R,R,B,B,R → Ban R,B,R,B → Pick R,B,B,R`
= 10 ban + 10 pick. Giliran aktif selalu ditandai di board + stepper.

---

## 2. Palet warna

Nuansa Cloud9 (biru/hitam) tanpa memakai aset merek mereka.

| Token | Hex | Pakai untuk |
|---|---|---|
| `--c9-blue` | `#0090D4` | Aksen utama, CTA, link, sorot Blue side |
| `--c9-sky` | `#4FC3F7` | Aksen terang, hover, garis aktif |
| `--navy-950` | `#060B14` | Background halaman |
| `--navy-900` | `#0A1424` | Background panel gelap |
| `--navy-800` | `#0E1B30` | Background kartu / panel |
| `--navy-700` | `#16263F` | Background kartu hover / input |
| `--line` | `#1E3355` | Border, divider |
| `--line-strong` | `#2C4A73` | Border aktif |
| `--text` | `#EAF2FB` | Teks utama |
| `--muted` | `#8FA6C2` | Teks sekunder, label |
| `--faint` | `#5B7391` | Teks tersier, placeholder |
| `--blue-team` | `#2E9BFF` | Blue side (pick, bar, badge) |
| `--red-team` | `#FF4D5E` | Red side (pick, bar, badge) |
| `--gold` | `#FFC857` | Peringatan Fearless, insight, highlight |
| `--green` | `#34D399` | Win-rate naik, status OK |
| `--danger` | `#FF4D5E` | Ban, win-rate turun, error |

Aturan: teks di atas `--c9-blue` / `--blue-team` memakai `#06121F` (gelap) atau putih
tebal; kontras teks utama terhadap `--navy-800` ≥ 7:1. Jangan pakai warna tim
lain (ungu/hijau) untuk menandai sisi — hanya biru vs merah.

---

## 3. Tipografi

| Peran | Font | Ukuran / bobot | Keterangan |
|---|---|---|---|
| Display / judul layar | **Chakra Petch** 700 | 28–32 px, uppercase, letter-spacing 0.04em | Judul board, angka win-rate besar |
| Judul panel / label | **Chakra Petch** 600 | 13–15 px, uppercase, ls 0.08em | Header panel, nama fase |
| Teks tubuh | **Inter** 400/500 | 13–14 px, line-height 1.5 | Deskripsi, insight, tabel |
| Angka / data | **JetBrains Mono** 500/700 | 12–20 px | Win-rate, pick-rate, timer (angka tabular, tidak goyang) |
| Nama champion | **Inter** 600 | 12 px | Di kartu champion |

Semua font gratis (Google Fonts, OFL) — boleh di-bundle atau pakai system fallback
(`system-ui, sans-serif`) bila offline. Mockup memakai stack ini dengan fallback sistem.

---

## 4. Layout grid

- **Canvas:** max-width 1440 px, padding luar 24 px, background `--navy-950`.
- **Grid utama draft:** 12 kolom, gutter 16 px.
  - Kolom 1–3 (kiri): board Blue side — 5 slot pick vertikal + bar ban.
  - Kolom 4–9 (tengah): champion grid + search + filter role.
  - Kolom 10–12 (kanan): sidebar — win-rate, tendensi lawan, Fearless tracker.
- **Header:** tinggi 56 px — logo FDL, nama seri/lawan, tab Game, toggle Fearless, timer fase.
- **Phase bar:** di bawah header, tinggi 40 px — stepper 4 fase + giliran aktif + tombol aksi.
- **Responsif:** < 1100 px sidebar pindah ke bawah grid; < 760 px board Blue/Red jadi
  dua kolom berdampingan di atas grid (layout 1 kolom, prioritas: board → grid → sidebar).
- **Radius:** kartu 10 px, tombol 8 px, chip 999 px. **Shadow:** `0 8px 24px rgba(0,0,0,.45)`
  untuk panel terangkat; tanpa shadow untuk kartu datar (pakai border 1 px `--line`).

---

## 5. Komponen

### 5.1 ChampionCard (grid tengah)
- Ukuran: rasio 1:1, min 72 px. Isi: monogram 2 huruf (inisial champion) di atas
  bentuk geometris per role + nama + role + pick-rate kecil.
- Warna latar monogram per role (bukan per champion, supaya orisinal):
  Top `#7C5CFF`, Jungle `#22B07D`, Mid `#E8A33D`, ADC `#E5484D`, Support `#3E9BFF`.
- **State:**
  | State | Tampilan |
  |---|---|
  | Default | Border `--line`, latar `--navy-800` |
  | Hover | Border `--c9-sky`, latar `--navy-700`, naik 2 px, cursor pointer |
  | Selected (klik sekali, konfirmasi) | Outline 2 px `--c9-blue` + glow |
  | Picked Blue / Red | Border tebal sisi tim + badge "BLUE"/"RED" + monogram redup 40% |
  | Banned | Grayscale + overlay diagonal merah + ikon ✕, tidak bisa diklik |
  | Fearless-locked | Grayscale + ikon gembok 🔒 + label "LOCKED G1", tidak bisa diklik |
  | Disabled (bukan giliran / filter tidak cocok) | Opacity 0.35, tidak bisa diklik |

### 5.2 PickSlot & BanSlot (board kiri/kanan)
- PickSlot: 64×64 px, monogram + nama + role; slot kosong = garis putus-putus +
  label role ("TOP", "JNG", "MID", "ADC", "SUP") + nomor urut.
- BanSlot: 40×40 px, 5 per sisi dalam satu baris; ban terisi = monogram kecil +
  overlay ✕ merah; slot kosong = kotak garis putus-putus.
- Slot giliran aktif: border berdenyut (`--c9-sky`, animasi 1,2 dtk) + label
  "YOUR PICK" / "ENEMY BAN" di atasnya.

### 5.3 WinRateMeter
- Bar horizontal terbagi Blue vs Red (lebar ∝ win%), angka besar di kedua ujung
  (JetBrains Mono 20 px), delta "+3,2%" di tengah dengan panah ▲/▼ + warna hijau/merah.
- Di bawah bar: log 3 perubahan terakhir ("Pick Azir → Blue +2,1%").
- Update: animasi lebar bar 400 ms ease-out setiap pick/ban.

### 5.4 TendencyPanel (sidebar kanan)
- Baris per champion: monogram kecil + nama + bar pick-rate (lebar ∝ %) + angka %.
- Seksi: **Top Picks** (5 besar), **First Pick** (3 besar + %), **Role Pool**
  (per role: 3 champion teratas lawan), **Sample** ("n = 142 game, patch 26.x").
- Baris yang champion-nya sudah di-ban/di-pick ikut berubah state (coret/redup).
- Insight card "How to Win" di bawah: latar `--gold` 10% + border kiri emas,
  1–2 kalimat aksi ("Ban Sejuani — lawan first-pick 70% di Game 1").

### 5.5 FearlessTracker (sidebar kanan, bawah)
- Tab Game 1 / 2 / 3(/4/5): tab aktif = game berjalan; tab selesai = skor + ikon ✓.
- Counter pool: "Pool tersisa: 148 / 168 champion" + progress bar menyusut per game.
- Daftar champion terkunci per game (chip kecil + gembok); klik chip → sorot
  kartunya di grid (scroll + outline emas).

### 5.6 Tombol & aksi
- **Primary** (Confirm Pick/Ban): latar `--c9-blue`, teks gelap tebal, radius 8 px.
- **Ghost** (Reset Draft, Change Side): border `--line-strong`, teks `--text`.
- **Danger** (Forfeit / Reset Series): teks `--red-team`, border merah tipis.
- Semua tombol: hover +8% brightness, disabled opacity 0.4, fokus keyboard
  outline `--c9-sky` 2 px (aksesibilitas: semua aksi bisa keyboard).

### 5.7 PhaseStepper
- 4 segmen: Ban 1 → Pick 1 → Ban 2 → Pick 2; segmen selesai = centang + biru,
  aktif = biru terang + label giliran, berikut = redup. Timer fase 30 dtk
  (countdown, habis = auto-pick rekomendasi tertinggi — ditandai "AUTO").

---

## 6. Perilaku tiap state (ringkas)

| State layar | Yang terlihat | Aksi tersedia |
|---|---|---|
| **S0 Setup (kosong)** | Form setup di tengah: pilih sisi, lawan, BO3/BO5, toggle Fearless, tombol "Start Draft" | Semua field bisa diubah; belum ada board |
| **S1 Draft berjalan** | Board + grid + sidebar aktif; giliran + timer jalan | Klik champion → pilih → Confirm; Undo (1 langkah); filter role/search |
| **S1 lawan giliran (simulasi)** | Banner "Enemy is picking…" + grid terkunci 1,2 dtk lalu lawan auto-pick | Tunggu / Skip sim (tombol "Simulate enemy") |
| **S4 Fearless antar-game** | Pool menyusut, chip terkunci, tab game pindah | "Start Game 2" (pool sudah disaring) |
| **S5 Draft selesai** | Overlay ringkasan: komposisi 5v5, win-rate final, 3 insight, tombol aksi | Next Game / Export (salin teks) / New Draft / Back to Setup |
| **Seri selesai** | Banner pemenang seri + rekap per game | Export full report / New Series |

**Aturan interaksi yang mengikat:**
1. Champion yang sudah di-pick/di-ban/di-lock TIDAK PERNAH bisa diklik lagi
   (bukan cuma pesan error — tombolnya mati).
2. Setiap aksi mengubah win-rate secara langsung + tercatat di log (maks 3 baris).
3. Filter role + search tidak pernah menyembunyikan state champion (yang terkunci
   tetap terlihat, hanya redup) — pelatih harus melihat pool yang hilang.
4. Semua angka memakai format konsisten: win-rate 1 desimal + "%", pick-rate
   tanpa desimal + "%", timer `MM:SS`.

---

## 7. Pemetaan ke komponen React (untuk Habibie, Minggu 2–3)

| Komponen desain | File React (saran) | State / props utama |
|---|---|---|
| App shell + header | `src/App.jsx` | `series`, `game`, `fearlessOn` |
| SetupScreen (S0) | `src/components/SetupScreen.jsx` | `onStart({side, opponent, format, fearless})` |
| DraftBoard | `src/components/DraftBoard.jsx` | `picks`, `bans`, `turn`, `phase` |
| PickSlot / BanSlot | `src/components/Slots.jsx` | `champion?`, `role`, `active` |
| ChampionGrid + filter | `src/components/ChampionGrid.jsx` | `champions`, `filter`, `onSelect` |
| ChampionCard | `src/components/ChampionCard.jsx` | `champion`, `state` (enum §5.1) |
| WinRateMeter | `src/components/WinRateMeter.jsx` | `blueWinPct`, `deltaLog[]` |
| TendencyPanel | `src/components/TendencyPanel.jsx` | `tendencies`, `sampleSize` |
| FearlessTracker | `src/components/FearlessTracker.jsx` | `lockedByGame`, `poolRemaining` |
| PhaseStepper | `src/components/PhaseStepper.jsx` | `phase`, `turn`, `timerSecs` |
| DraftSummary (S5) | `src/components/DraftSummary.jsx` | `picks`, `bans`, `winPct`, `insights[]` |
| Data (mock → API) | `src/data/champions.js`, `src/data/tendencies.js` | ganti mock dengan output ekstraksi GRID |

**Catatan implementasi:** mockup ini memakai data dummy deterministik (bukan data
GRID asli — data GRID tidak boleh di-commit). Nilai win-rate di mockup dihitung
dari skor "power" tiap champion + sinergi sederhana; model asli (Minggu 4)
menggantikan fungsi `winRateImpact()` tanpa mengubah komponen.

---

## 8. Checklist kriteria juri yang dijawab desain ini

- **Design:** sistem visual konsisten (token di §2–3), hierarki jelas (board →
  grid → sidebar), state lengkap dan tidak ambigu.
- **Technological Implementation:** mockup interaktif membuktikan alur draft +
  Fearless sebelum engine jadi; komponen dipetakan 1:1 ke React.
- **Potential Impact:** layout meniru alat pelatih pro (board di kiri, data di kanan)
  — bisa dipakai langsung di ruang latihan.
- **Quality of the Idea:** Fearless divisualisasikan sebagai pool yang menyusut
  (bukan sekadar daftar larangan) — inti formatnya kelihatan dalam 5 detik.
- **Presentation:** mockup bisa dibuka juri tanpa build; semua teks Bahasa Inggris
  di UI (sesuai syarat submit), dokumen ini dwibahasa seperlunya.
