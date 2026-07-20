# Changelog

## [1.0.0] - 2026-07-20

### Added
- Real HTTP dashboard (`app.py`) — stdlib `http.server`, dark/amber ops UI.
- CLI entrypoint (`benchdash.py`) — `collect` / `show` commands.
- JSON API: `/api/summary`, `/api/results`, `/api/health`.
- Assert-based smoke test (`test_smoke.py`).
- Working Dockerfile (Alpine, non-root, HEALTHCHECK) and docker-compose.yml.
- Real screenshots under `docs/screenshots/`.

### Changed
- Collector now reports structured root-disk usage instead of a placeholder.
- README rewritten to describe only implemented, verified functionality.
