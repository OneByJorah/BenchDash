#!/usr/bin/env python3
"""
BenchDash — local system benchmark/inventory dashboard.

Serves a live view of the host's hardware/software profile collected by
``collector/system_info.py``. Pure Python stdlib: ``http.server`` + ``json``.
No external dependencies.

Usage:
    python3 app.py                 # serve on 0.0.0.0:8081
    DASHBOARD_PORT=3000 python3 app.py
"""
import functools
import json
import mimetypes
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

import collector.system_info as system_info

ROOT = Path(__file__).resolve().parent
STATIC = ROOT / "static"
DATA = ROOT / "system_info.json"

BG = "#0d0d0c"
AMBER = "#FFB300"


def ensure_data():
    """Make sure a data file exists (collect once if missing)."""
    if not DATA.exists():
        system_info.save()


def load_info():
    ensure_data()
    try:
        return json.loads(DATA.read_text())
    except Exception:
        return {}


def row(label, value):
    v = value if value not in (None, "", "N/A") else "—"
    return f"<tr><td class='k'>{label}</td><td class='v'>{v}</td></tr>"


def render_html(info):
    i = info or {}
    status = "OPERATIONAL" if i.get("cpu") else "DEGRADED"
    cpu = i.get("cpu") or "—"
    cores = i.get("cpu_cores") or "—"
    ram = i.get("ram_gb") if i.get("ram_gb") is not None else "—"
    gpu = i.get("gpu") or "no GPU detected"
    rows = "".join([
        row("OS", f"{i.get('os','—')} {i.get('os_release','')}".strip()),
        row("Kernel", i.get("kernel")),
        row("CPU Model", cpu),
        row("CPU Cores", cores),
        row("RAM", f"{ram} GB" if isinstance(ram, (int, float)) else ram),
        row("GPU", gpu),
        row("VRAM", f"{i.get('vram_total_mb')} MB" if i.get("vram_total_mb") else None),
        row("CUDA", i.get("cuda_version")),
        row("Driver", i.get("driver_version")),
        row("Python", i.get("python_version")),
        row("Ollama", i.get("ollama_version")),
        row("Docker", i.get("docker_version")),
        row("Storage", f"{i['storage']['used']} / {i['storage']['size']} on {i['storage']['mount']}" if i.get("storage") else None),
        row("PCIe", i.get("pcie_info")),
    ])
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>BenchDash</title>
<style>
  :root{{--bg:{BG};--amber:{AMBER};}}
  *{{box-sizing:border-box}}
  body{{margin:0;background:var(--bg);color:#e8e8e6;font-family:'JetBrains Mono',ui-monospace,Menlo,Consolas,monospace}}
  header{{padding:18px 24px;border-bottom:1px solid #2a2a28;display:flex;align-items:center;gap:14px}}
  .logo{{color:var(--amber);font-weight:700;font-size:20px;letter-spacing:1px}}
  .dot{{width:10px;height:10px;border-radius:50%;background:#3ad17a;box-shadow:0 0 10px #3ad17a}}
  .status{{margin-left:auto;font-size:12px;color:var(--amber);border:1px solid var(--amber);padding:3px 10px;border-radius:3px}}
  main{{padding:24px;max-width:960px;margin:0 auto}}
  h2{{color:var(--amber);font-size:14px;text-transform:uppercase;letter-spacing:2px;margin:28px 0 10px}}
  table{{width:100%;border-collapse:collapse;font-size:13px}}
  td{{padding:9px 12px;border-bottom:1px solid #1d1d1b}}
  td.k{{color:#8a8a86;width:220px}}
  td.v{{color:#f2f2f0}}
  .grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin-top:10px}}
  .card{{background:#161614;border:1px solid #2a2a28;border-radius:6px;padding:14px}}
  .card .n{{color:var(--amber);font-size:20px;font-weight:700}}
  .card .l{{color:#8a8a86;font-size:11px;text-transform:uppercase;letter-spacing:1px;margin-top:4px}}
  footer{{padding:18px 24px;color:#5a5a56;font-size:11px;border-top:1px solid #1d1d1b;margin-top:30px}}
</style></head>
<body>
<header>
  <span class="dot"></span>
  <span class="logo">BENCHDASH</span>
  <span class="status">{status}</span>
</header>
<main>
  <h2>System Profile</h2>
  <table>{rows}</table>
  <h2>Quick Stats</h2>
  <div class="grid">
    <div class="card"><div class="n">{cores}</div><div class="l">CPU Cores</div></div>
    <div class="card"><div class="n">{ram}</div><div class="l">RAM (GB)</div></div>
    <div class="card"><div class="n">{i.get('docker_version','—')}</div><div class="l">Docker</div></div>
    <div class="card"><div class="n">{i.get('python_version','—')}</div><div class="l">Python</div></div>
  </div>
  <p style="color:#5a5a56;font-size:12px;margin-top:24px">
    Source: <code>collector/system_info.py</code> · data file: <code>system_info.json</code>
  </p>
</main>
<footer>BenchDash · JorahOne LLC · {status}</footer>
</body></html>"""


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="text/html; charset=utf-8"):
        data = body.encode("utf-8") if isinstance(body, str) else body
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        path = urlparse(self.path).path
        if path in ("/", "/index.html"):
            self._send(200, render_html(load_info()))
            return
        if path == "/api/summary" or path == "/api/results":
            self._send(200, json.dumps(load_info(), indent=2), "application/json")
            return
        if path == "/api/health":
            self._send(200, json.dumps({"status": "OK"}), "application/json")
            return
        if path.startswith("/static/"):
            rel = path[len("/static/"):]
            fp = (STATIC / rel).resolve()
            if STATIC in fp.parents and fp.exists():
                ctype = mimetypes.guess_type(fp)[0] or "application/octet-stream"
                self._send(200, fp.read_bytes(), ctype)
                return
        self._send(404, "Not Found")

    def log_message(self, *args):
        pass


def main():
    host = os.environ.get("DASHBOARD_HOST", "0.0.0.0")
    port = int(os.environ.get("DASHBOARD_PORT", "8081"))
    ensure_data()
    srv = ThreadingHTTPServer((host, port), Handler)
    print(f"[benchdash] OPERATIONAL on http://{host}:{port}")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        srv.shutdown()


if __name__ == "__main__":
    main()
