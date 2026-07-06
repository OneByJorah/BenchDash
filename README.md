<div align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/Ollama-000?style=for-the-badge&logo=ollama&logoColor=white">
  <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white">
  <img src="https://img.shields.io/badge/Chart.js-FF6384?style=for-the-badge&logo=chartdotjs&logoColor=white">
  <img src="https://img.shields.io/badge/Status-Design%20Document-yellow?style=for-the-badge">
</div>

> **⚠️ Status: Design Document** — This repository describes a planned benchmarking platform. Currently only `collector/system_info.py` is implemented. The Quick Start commands below document the design vision; they will produce `FileNotFoundError` until the modules are built. See the [Architecture](#-architecture) section for the full design.

<br>

<div align="center">
  <h1>🧪 Ollama Benchmark Dashboard</h1>
  <p><strong>A comprehensive, automated benchmarking platform for local LLMs running on Ollama</strong></p>
  <p>Auto-discover models → Run multi-dimensional tests → Rank & score → Visualize results</p>

  <p>
    <a href="#-features">Features</a> •
    <a href="#-quick-start">Quick Start</a> •
    <a href="#-architecture">Architecture</a> •
    <a href="#-test-categories">Tests</a> •
    <a href="#-dashboard">Dashboard</a> •
    <a href="#-scoring">Scoring</a> •
    <a href="#-export">Export</a>
  </p>
</div>

---

## 📸 Screenshot

This is a CLI/backend-only tool. No screenshots available.

## ✨ Features

- **Automated Model Discovery** — Detects all Ollama models on your host and runs benchmarks smallest → largest
- **Multi-Dimensional Testing** — 13+ test categories covering knowledge, reasoning, coding, creativity, conversation, stress, and more
- **Multi-Agent Support** — Benchmark models via:
  - **Direct** — Direct Ollama API calls (baseline)
  - **Hermes Agent** — Hermes CLI agent with tool access
  - **Claude Code** — Claude Code via Ollama proxy endpoint
- **Performance Metrics** — Tokens/sec, latency, CPU/GPU load, VRAM/RAM usage, temperature monitoring
- **Real-Time Dashboard** — Self-contained HTTP server with Chart.js visualizations
- **SQLite Persistence** — All results stored in SQLite + JSON for querying and export
- **Ranking & Scoring** — Per-category scoring, bonus awards, and overall leaderboard
- **Multiple Export Formats** — CSV, JSON, Markdown report generation
- **Scheduling** — Built-in cron-style scheduler for daily/weekly/monthly runs
- **Notifications** — Telegram integration for run completions and alerts

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- [Ollama](https://ollama.ai) installed and running (local or remote)
- One or more Ollama models pulled locally

### Installation

```bash
# Clone the repo
git clone https://github.com/OneByJorah/ollama-benchmark-dashboard.git
cd ollama-benchmark-dashboard

# No pip dependencies required — uses Python stdlib + Ollama API
# The dashboard uses Chart.js loaded via CDN
```

### Run a Full Benchmark

```bash
# Run the full benchmark pipeline (discovery → tests → ranking → report)
python3 orchestrator.py
```

### Run a Specific Model

```bash
# Test a single model with specific agent mode
python3 run_benchmark.py --mode direct --model gemma2:9b

# Available modes: direct, hermes-agent, claude-code
# Use --task to run just one task by ID
# Use --skip-media to skip image/audio/video tasks
```

### Run for a Single Model (Alternative)

```bash
python3 run_one_model.py --model gemma2:9b --mode direct
```

### Start the Dashboard

```bash
# Start the real-time benchmark dashboard
python3 dashboard_server.py

# Custom host/port
DASHBOARD_PORT=3000 DASHBOARD_HOST=127.0.0.1 python3 dashboard_server.py
```

Then open **http://localhost:8081** (or **http://127.0.0.1:8081**) in your browser.

> **Note:** The default `DASHBOARD_HOST=0.0.0.0` binds to all interfaces. For local-only access, set `DASHBOARD_HOST=127.0.0.1`.

## 🏗️ Architecture

```
ollama-benchmark-dashboard/
├── orchestrator.py              # Main runner: discovery → benchmarks → ranking → reporting
├── run_benchmark.py             # Alternative runner with agent mode support (direct/hermes/claude)
├── run_one_model.py             # Single model benchmark script
├── dashboard_server.py          # HTTP dashboard server with API endpoints
├── benchmark_meta.json          # Model list, task definitions, aliases
├── models.json                  # Discovered Ollama models
├── system_info.json             # Hardware & software system report
│
├── collector/                   # Data collection modules
│   ├── model_discovery.py       # Auto-detect Ollama models via CLI
│   ├── system_info.py           # CPU/RAM/GPU/VRAM/CUDA/OS collection
│   ├── performance.py           # Tokens/sec, latency, resource monitoring
│   └── stress.py                # Context window stress testing
│
├── tests/                       # Benchmark test modules (13 categories)
│   ├── knowledge.py             # World knowledge & fact retrieval
│   ├── programming.py           # Code generation & problem solving
│   ├── networking.py            # Network/IT knowledge
│   ├── math.py                  # Mathematical reasoning
│   ├── creative.py              # Creative writing & generation
│   ├── image.py                 # Image generation tasks
│   ├── audio.py                 # Audio generation tasks
│   ├── video.py                 # Video generation tasks
│   ├── vision.py                # Vision/understanding tasks
│   ├── game.py                  # HTML5 game development
│   ├── conversation.py          # 100-turn memory & context retention
│   ├── errors.py                # Malformed input resilience
│   └── consistency.py           # 10x identical prompt variance
│
├── ranking/                     # Scoring & ranking
│   ├── scorer.py                # Category + overall score computation
│   └── bonus.py                 # Best-in-class bonus awards
│
├── db/                          # SQLite database layer
│   ├── schema.sql               # Database schema
│   └── benchmark.py             # CRUD operations
│
├── exports/                     # Report exports
│   ├── csv_export.py            # CSV format export
│   ├── json_export.py           # JSON format export
│   └── markdown_export.py       # Markdown report generation
│
├── scheduler/                   # Automated scheduling
│   └── cron.py                  # Daily/weekly/monthly triggers
│
├── notifications/               # Alert integrations
│   └── telegram.py              # Telegram bot notifications
│
├── static/                      # Dashboard frontend
│   └── index.html               # Single-page dashboard with Chart.js
│
├── results/                     # Per-run JSON result files
├── outputs/                     # Generated artifacts (images, audio, etc.)
├── benchmark.db                 # SQLite results database
├── leaderboard.json             # Computed ranking leaderboard
├── benchmark.csv                # CSV export of results
├── benchmark.json               # JSON export of results
└── report.md                    # Markdown summary report
```

## 🧪 Test Categories

| Category | Description | What It Measures |
|----------|-------------|-----------------|
| **🧠 Knowledge** | Factual retrieval across domains | Accuracy, depth, breadth |
| **💻 Programming** | Code generation & algorithms | Correctness, efficiency |
| **🌐 Networking** | Network/IT infrastructure knowledge | Technical accuracy |
| **🔢 Math** | Mathematical problem solving | Reasoning, precision |
| **🎨 Creative** | Creative writing within constraints | Style, structure, brevity |
| **📷 Image** | Image generation capability | Visual output quality |
| **🎵 Audio** | Audio/sound generation | Audio file production |
| **🎬 Video** | Video/animation generation | Motion graphics output |
| **🎮 Game** | HTML5 game development | Interactivity, game logic |
| **💬 Conversation** | 100-turn memory & context retention | Long-context coherence |
| **⚠️ Errors** | Malformed input resilience | Robustness, error handling |
| **🎯 Consistency** | 10x identical prompt variance | Output stability |
| **🏋️ Stress** | Context window scaling | Performance under load |

## 📊 Dashboard

The built-in dashboard provides:

- **Summary Cards** — Total runs, average score, success rate, best model
- **4 Interactive Charts** — Score by model/mode, success rates, category radar, tokens/sec
- **Model Summary Table** — Per-model aggregated metrics with sorting
- **Detailed Results Table** — Every test run with scoring, duration, and notes
- **Filter Controls** — Filter by mode (Direct/Hermes/Claude), model, and category
- **Auto-Refresh** — Polls every 10 seconds for new data
- **Dark Theme** — Cyberpunk-inspired dark UI with glow effects

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` or `/index.html` | GET | Dashboard UI |
| `/api/results` | GET | All results + meta data |
| `/api/summary` | GET | Aggregated summary statistics |
| `/api/run` | POST | Queue a new benchmark run |

## 🏆 Scoring System

Each test is scored from **0.1 to 1.0** across discrete tiers:

- **1.0** — Excellent (score ≥ 0.75)
- **0.7** — Good (score ≥ 0.45)
- **0.4** — Fair (score ≥ 0.2)
- **0.1** — Poor (below threshold)

Scoring considers:
- Response length & relevance
- File outputs (for media tasks)
- Code correctness & structure
- Step-by-step reasoning
- HTML/JS interactivity (games)

**Bonus categories** award extra recognition for top performers in coding, networking, creativity, and more.

## 📤 Export Formats

```bash
# All exports are generated automatically after each orchestrator run

# JSON export
cat benchmark.json

# CSV export (import into spreadsheets)
cat benchmark.csv

# Markdown report (human-readable summary)
cat report.md
```

## ⚙️ Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OLLAMA_HOST` | `127.0.0.1:11434` | Ollama API host |
| `DASHBOARD_PORT` | `8081` | Dashboard HTTP server port |
| `DASHBOARD_HOST` | `0.0.0.0` | Dashboard bind address |
| `BENCH_SKIP_MEDIA` | `0` | Set to `1` to skip image/audio/video tests |

### Task Configuration

Edit `benchmark_meta.json` to:
- Add/remove models from the benchmark list
- Customize test tasks, prompts, and categories
- Configure model aliases for result file naming

## 🔔 Notifications

Telegram integration is available in `notifications/telegram.py`:

```bash
export TELEGRAM_BOT_TOKEN="your-bot-token"
export TELEGRAM_CHAT_ID="your-chat-id"
```

The scheduler in `scheduler/cron.py` supports automated daily, weekly, or monthly benchmark runs with notification delivery.

## 📋 Output Structure

Results are stored in two locations:

1. **SQLite Database** (`benchmark.db`) — Structured queryable data
   - `runs` — Benchmark run metadata
   - `results` — Per-test results with scores
   - `performance` — System metrics per model
   - `errors` — Error logs

2. **JSON Files** (`results/`) — Per-model, per-mode detailed results
   ```
   results/
   ├── model__direct__gemma2-9b.json
   ├── model__hermes-agent__gemma2-9b.json
   ├── model__direct__llava-13b.json
   ├── conversation__gemma2-9b.json
   ├── stress__gemma2-9b.json
   └── ...
   ```

## 🛠️ Development

```bash
# Test imports
python3 -c "import sys; sys.path.insert(0,'.'); from collector import *; from db import *; from ranking import *; from exports import *"

# Run a quick test with one model (direct mode only)
python3 run_benchmark.py --mode direct --model gemma2:9b --task 2 --skip-media
```

## 📄 License

MIT © Jhonattan L. Jimenez

---

<div align="center">
  <p>Built with ❤️ for the open-source AI community</p>
  <p>
    <a href="https://github.com/OneByJorah">@OneByJorah</a> •
    <a href="https://codebuff.com">Codebuff</a>
  </p>
</div>
