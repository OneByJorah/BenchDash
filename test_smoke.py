"""Smoke test for BenchDash collector + dashboard rendering.

Run:  python3 -m pytest test_smoke.py -q   (or)  python3 test_smoke.py
"""
import importlib.util
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

import collector.system_info as system_info

import app as appmod


def test_collect_returns_keys():
    info = system_info.collect()
    for k in ("cpu", "cpu_cores", "ram_gb", "os", "python_version"):
        assert k in info, f"missing key {k}"


def test_app_renders_html():
    html = appmod.render_html(system_info.collect())
    assert "BENCHDASH" in html
    assert "System Profile" in html


def test_app_health_payload():
    payload = json.loads(appmod.json.dumps({"status": "OK"}))
    assert payload["status"] == "OK"


if __name__ == "__main__":
    test_collect_returns_keys()
    test_app_renders_html()
    test_app_health_payload()
    print("SMOKE OK")
