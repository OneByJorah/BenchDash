<div align="center">

![BenchDash](docs/assets/banner.svg)

# BenchDash

**Automated benchmarking platform for local LLMs on Ollama**

[![License: MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://python.org)
[![Ollama](https://img.shields.io/badge/Ollama-0.5%2B-black?logo=ollama)](https://ollama.ai)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-orange.svg)](CONTRIBUTING.md)
[![GitHub stars](https://img.shields.io/github/stars/OneByJorah/BenchDash?style=flat&logo=github)](https://github.com/OneByJorah/BenchDash/stargazers)
[![CodeQL](https://img.shields.io/github/actions/workflow/status/OneByJorah/BenchDash/codeql.yml?branch=main&label=CodeQL&logo=github)](https://github.com/OneByJorah/BenchDash/actions)
[![Dashboard](https://img.shields.io/badge/dashboard-live-38bdf8?logo=html5)](index.html)

</div>

---

> **⚠️ Project status:** BenchDash is in early development (design-first). Currently implemented: the **system telemetry collector** (`collector/system_info.py`) and the **standalone dashboard UI** (`index.html`, running on sample data). The benchmark engine, scoring, persistence, scheduler, notifications, and Flask backend described below are **planned, not yet implemented**. See [INTENT.md](INTENT.md) for the full design.

<p align="center">
  <img src="docs/assets/screenshot.png" alt="BenchDash Dashboard Preview" width="90%">
  <br>
  <sub><i>BenchDash dashboard (sample data) — leaderboard, performance charts, system stats</i><br>
  Screenshot: headless Chromium capture of the static UI served locally; charts render bundled sample data.</sub>
</p>

---

## Implemented

- **Standalone Dashboard UI** — Chart.js-powered single-file page with leaderboards, radar charts, speed metrics, and success-rate breakdown
- **System Telemetry Collector** — Collects CPU, RAM, GPU, VRAM, CUDA, driver, OS, kernel, Python/Ollama/Docker versions to `system_info.json`

## Planned

- **Auto-Discovery** — Automatically discover all Ollama models on the host
- **Multi-Dimension Benchmarks** — 13+ test categories: knowledge, code, math, reasoning, creativity, conversation, vision, generation, game dev, error resilience, consistency, context stress
- **Multi-Agent Modes** — Compare models via raw Ollama API, Hermes Agent, and Claude Code
- **System Telemetry per Run** — Attach GPU/VRAM/CUDA metrics to every benchmark run
- **History Tracking** — SQLite persistence with per-model JSON exports for trend analysis
- **Scoring System** — Discrete-tier scoring (0.1–1.0) with per-category and overall leaderboards
- **Export** — Results to CSV, JSON, and Markdown report formats
- **Scheduling** — Cron-style daily/weekly/monthly automated benchmarks
- **Notifications** — Telegram integration for run completion alerts

## Quick Start

### Dashboard UI

The standalone dashboard (`index.html`) requires no server and no dependencies — just open it in a browser, or serve it:

```bash
python3 -m http.server 8080
```

Open **http://localhost:8080**. The page currently renders bundled sample data.

### System Telemetry Collector

```bash
python3 collector/system_info.py
```

Writes a hardware/software report to `system_info.json` (CPU, RAM, GPU/VRAM via `nvidia-smi`, CUDA, drivers, OS, versions).

## Configuration

Environment variables consumed by the upcoming backend (see `.env.example`; currently informational):

| Variable | Default | Description |
|---|---|---|
| `OLLAMA_HOST` | `host.docker.internal:11434` | Ollama API endpoint |
| `DASHBOARD_PORT` | `8081` | Dashboard port |
| `DASHBOARD_HOST` | `0.0.0.0` | Dashboard bind address |
| `BENCH_SKIP_MEDIA` | `0` | Skip image/audio/video tests when set to `1` |

## Target Architecture

```
                    ┌─────────────────┐
                    │   Browser / UI   │
                    └────────┬────────┘
                             │ HTTP
                    ┌────────▼────────┐
                    │   Flask App     │
                    │  (app.py)       │
                    └───┬────┬────┬───┘
                        │    │    │
               ┌────────┤    │    ├──────────┐
               ▼             ▼               ▼
        ┌──────────┐  ┌──────────┐  ┌──────────────┐
        │Benchmark │  │  Results │  │   Scheduler  │
        │  Runner  │  │ Analyzer │  │  (cron-ish)  │
        └────┬─────┘  └────┬─────┘  └──────────────┘
             │             │
             ▼             ▼
        ┌──────────┐  ┌──────────┐
        │  Ollama  │  │  SQLite  │
        │   API    │  │  / JSON  │
        └──────────┘  └──────────┘
```

*Not yet implemented — target architecture for the benchmarking backend.*

## Project Structure

```
BenchDash/
├── index.html                  # Standalone dashboard UI (sample data)
├── collector/
│   └── system_info.py          # System telemetry collector
├── docs/
│   ├── assets/                 # Banner + dashboard screenshot
│   └── screenshots/            # Additional UI captures
├── .github/                    # CI (CodeQL), issue templates, Dependabot
├── Dockerfile                  # Container definition (backend pending)
├── docker-compose.yml          # Service scaffolding (backend pending)
└── README.md
```

## Planned Benchmark Metrics

| Metric | Description |
|---|---|
| **Tokens/sec** | Generation speed |
| **Time to First Token** | Response latency |
| **Quality Score** | Response quality rating (0.1–1.0) |
| **Memory Usage** | RAM consumption (GB) |
| **VRAM Usage** | GPU memory (if applicable) |
| **Success Rate** | Percentage of successful completions |

## Roadmap

- [x] System telemetry collector
- [x] Standalone dashboard UI
- [ ] Benchmark runner engine
- [ ] Multi-agent mode comparison
- [ ] Real-time streaming results
- [ ] Telegram notifications
- [ ] Historical trend charts

See [ROADMAP.md](ROADMAP.md) for full details.

## Contributing

Contributions are welcome. Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for community standards.

## Security

For security concerns, see [SECURITY.md](SECURITY.md). Report vulnerabilities to **security@jorahone.com**.

## License

[MIT](LICENSE) © Jhonattan L. Jimenez (OneByJorah)

---

<p align="center">
  Built with 🌴 by <a href="https://github.com/OneByJorah">OneByJorah</a> ·
  <a href="https://jorahone.com">jorahone.com</a>
</p>
