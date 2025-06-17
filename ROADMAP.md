# 🛣️ SampleMind AI – Roadmap

Dette dokumentet inneholder alle planlagte funksjoner, ideer, statusoppdateringer og milepæler for SampleMind AI. Vi bygger et AI-verktøy og system for organisering, analyse, eksport og import av samples til FL Studio på macOS.

---

## ✅ FASE 1 — Grunnstruktur og CLI-basert prototype (April - Mai 2025)

- [x] Sett opp prosjektstruktur og mappehierarki
- [x] Lag README.md og ROADMAP.md
- [x] Sett opp virtuell miljø og requirements.txt
- [ ] Implementer CLI-kommando for import av sample
- [ ] Lag `analyzer`-modul for BPM + key + mood med librosa
- [ ] Lag `organizer` som legger samples i mappestruktur basert på metadata
- [ ] Lag testdata og test CLI-verktøy lokalt

---

## 🧠 FASE 2 — AI og brukerflyt (Mai - Juni 2025)

- [ ] Utvid analyser med AI (genre classification, mood detection med transformers eller scikit-learn)
- [ ] Integrasjon med lokal database (SQLite eller TinyDB)
- [ ] CLI-kommandoer for tagging og søk
- [ ] Lag offline web-UI med drag & drop og waveform preview (bruk f.eks. Flask + HTMX)

---

## 🚀 FASE 3 — Plugin / App Integrasjon (Juli - August 2025)

- [ ] Utvikle enkel macOS-app (Electron eller Tauri)
- [ ] FL Studio integrasjon (f.eks. med MIDI-controllere eller automatisert sample loading)
- [ ] Sample pack generator
- [ ] Sample snapshot-system med prosjektlogg, notes og versjonering

---

## 🌍 FASE 4 — Community, eksport og deling (Høst 2025)

- [ ] System for eksport/import av sample packs med metadata
- [ ] Markdown-basert dokumentasjon for hver pakke
- [ ] Web-basert nedlasting eller deling av pack + metadata
- [ ] GitHub Action for å publisere sample packs som releases
- [ ] Få med community contributors (via GitHub Projects)

---

## 🧪 Ekstra ideer og AI-forslag (Backlog)

- AI-assistent som foreslår samples ut fra stemning eller skisse
- Lydbibliotek som matcher tempo og key automatisk
- Automatisert tagging av eldre samplebibliotek
- Smart kompressor/EQ suggestions via AI
- Audio fingerprint matching (unngå duplikater)
- Automatisk BPM-match til project-tempo
- Mood wheel UI for leting etter vibe
- Versjonskontroll for sample edits

---

## 🎯 Langsiktig mål (2026 →)

- SampleMind blir en AI-drevet DAW companion for alle som bruker FL Studio
- Full macOS og FL Studio integrasjon
- SampleMind Pro – med sky-integrasjon, kollaborasjon og AI-mastering
