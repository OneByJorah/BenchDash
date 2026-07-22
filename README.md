<div align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/Chart.js-FF6384?style=for-the-badge&logo=chart.js&logoColor=white">
  <img src="https://img.shields.io/badge/license-MIT-blue?style=for-the-badge">
</div>

<br>

<div align="center">
  <h1>BenchDash</h1>
  <p><strong>Automated LLM Benchmarking Platform</strong></p>
  <p>Auto-discover, test, rank, and visualize local LLMs on Ollama.</p>
  <p>
    <a href="#features">Features</a> •
    <a href="#quick-start">Quick Start</a> •
    <a href="#architecture">Architecture</a> •
    <a href="#contributing">Contributing</a>
  </p>
</div>

---

## Screenshot

![BenchDash Dashboard](docs/screenshot.png)
*LLM benchmarking dashboard with performance rankings and charts.*

## Features

- **Auto-Discovery** — Automatically discover available Ollama models.
- **Automated Testing** — Run standardized benchmarks on all models.
- **Performance Ranking** — Rank models by speed, quality, and resources.
- **Visualization** — Interactive charts for benchmark results.
- **History Tracking** — Compare results over time.
- **Resource Monitoring** — Track CPU/RAM/GPU usage during tests.
- **Custom Prompts** — Define your own benchmark prompts.
- **Export Results** — Export to CSV/JSON.

## Quick Start

```bash
git clone https://github.com/OneByJorah/BenchDash.git
cd BenchDash

pip install -r requirements.txt
python3 app.py
```

Open **http://localhost:5000** in your browser.

### Docker

```bash
docker compose up -d
```

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `OLLAMA_URL` | `http://localhost:11434` | Ollama API endpoint |
| `PORT` | `5000` | Dashboard port |
| `BENCHMARK_PROMPTS` | — | Custom benchmark prompts file |
| `RESULTS_DIR` | `./results` | Benchmark results storage |

## Architecture

```
Browser ──HTTP──▶ Flask App ──API──▶ Ollama
                    │
                    ├──▶ Benchmark Runner
                    ├──▶ Results Analyzer
                    ├──▶ Chart Generator
                    └──▶ SQLite (History)
```

## Project Structure

```
BenchDash/
├── app.py                 # Flask application
├── bench/
│   ├── __init__.py
│   ├── runner.py          # Benchmark execution
│   ├── analyzer.py        # Results analysis
│   └── prompts/           # Benchmark prompts
├── templates/             # HTML templates
├── static/                # CSS, JS, charts
├── results/               # Benchmark results
├── requirements.txt       # Python dependencies
└── README.md
```

## Benchmark Metrics

| Metric | Description |
|--------|-------------|
| **Tokens/sec** | Generation speed |
| **Time to First Token** | Response latency |
| **Quality Score** | Response quality rating |
| **Memory Usage** | RAM consumption |
| **VRAM Usage** | GPU memory (if applicable) |

## Contributing

Contributions are welcome. Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for community standards.

## Security

For security concerns, see [SECURITY.md](SECURITY.md). Please report vulnerabilities to **info@jorahone.com** — do not use public issues.

## License

MIT © Jhonattan L. Jimenez

---

<div align="center">
  <p>Automated LLM benchmarking for Ollama.</p>
  <p><a href="https://github.com/OneByJorah">@OneByJorah</a></p>
</div>
