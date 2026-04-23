# 📋 Project Changelog

> **Project**: F2F (working title)
> **Format**: Based on [Keep a Changelog](https://keepachangelog.com/)
> **Last Updated**: 2026-04-23

---

## [Unreleased]

### Added
- *(no shipped features yet — first feature is `01-project-foundation`)*
- **Feature #01 — Project Foundation** _(pending merge)_ — Monorepo scaffold:
  `api/` (FastAPI + `/healthz` + `/tasks/ping` + Alembic baseline + stub
  packages for ledger/manufacturability/mcp/providers/pipeline/models/schemas),
  `worker/` (Celery + Blender-ready ping task), `web/` (Next.js 14 +
  TypeScript + Tailwind + Vitest + `HealthBadge`), `addons/` (Blender add-on
  stub + Maya placeholder), `infra/docker/` (3 Dockerfiles), `docker-compose.yml`
  (db + redis + minio + createbuckets + api + worker + web with healthchecks
  and named volumes), MinIO bucket sidecar, `.github/workflows/ci.yml` (6
  advisory jobs), README getting-started + troubleshooting.

### Changed
- **Roadmap expansion (2026-04-23)** — v1.0 expanded from 14 to 15 features:
  **Design Ledger** folded into Feature 02, new **Manufacturability Analysis**
  inserted as Feature 11 (between Export and AR), **MCP server** folded into
  Feature 14 (Public API), ledger viewer added to Feature 15 (History UI).
  AR / Blender add-on / API / History renumbered to 12–15.
  Scheduled for v1.1/v1.2: Decision Engine (unifies Pillars 2+3), Parametric
  Variants, Iterative Refinement, Multi-Provider Racing, Evaluation Harness,
  OpenTelemetry, Depth/LiDAR input, Version Tree UI, Live Multiplayer Viewer,
  QR Passport, Reprint/Remix.

### Fixed

### Removed

---

<!--
Once features start shipping, copy this block per release/milestone:

## [X.Y.Z] — YYYY-MM-DD

### Added
- **Feature #XX — Feature Name** — Brief description

### Changed
- **Feature #XX — Feature Name** — Brief description

### Fixed
- **Hotfix — Description** — What was fixed and why

### Removed
- **Feature #XX — Feature Name** — What was removed and why
-->
