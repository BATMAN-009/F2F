# 📝 Changelog: Project Foundation

> **Feature**: `01` — Project Foundation
> **Branch**: `feature/01-project-foundation`
> **Started**: 2026-04-23

---

## Session Notes

### Session 6 — 2026-04-23 — Stage 4 (Build) — Phases Y, Z + cross-check

- TC-06 executed locally on Windows host (no Docker available):
  - `web/`: `pnpm lint` ✅, `pnpm format:check` ✅, `pnpm test` 1/1 ✅, `pnpm build` ✅.
  - `api/`: first pass surfaced 2 ruff issues (`I001` import order in `alembic/env.py`, `S105` hardcoded password on `s3_secret_key` default) and one format delta in `alembic/versions/0001_baseline.py`. Fixed by `ruff check --fix`, `ruff format`, and adding `# noqa: S105 — local-dev default` on the secret line. Re-run: `ruff check` clean, `ruff format --check` clean, `pytest` 2/2 ✅.
  - `worker/`: `ruff check` clean, `ruff format --check` clean, `pytest` 1/1 ✅.
- TC-07 (CI), TC-01–05, TC-08–11 deferred — host lacks Docker Desktop; re-verification required on Docker-capable machine before merge. Recorded in `testplan.md` with explicit ⚠️ Deferred status per case.
- Ran full verification cross-check (Phase Z.5):
  - **Architecture ↔ Code**: file tree in arch doc matches what shipped (see `tree` commands). One minor deviation (lint rule) logged. Stub packages for Feature 02/05/06–10/11/14 exist per arch. Dockerfiles installed extra X libs (`libxi6`, `libxrender1`, `libxxf86vm1`, `libxfixes3`, `libxkbcommon0`, `libsm6`) on top of `blender + xvfb + libgl1` — strictly additive, required for Blender 4.x headless in the slim image. Not architectural.
  - **Tasks ↔ Code**: `tasks.md` now reflects 53/56 checked; the 3 unchecked are Checkpoint G (needs CI run), Checkpoint Y (Docker TCs deferred), and Ship which belongs to Stage 5.
  - **Testplan ↔ Tests**: 10 of 13 cases have deferred status with a clear rationale; 1 ran and passed (TC-06); AC-08/AC-09 marked verified; the rest pending Docker host + PR merge pipeline.
  - **Changelog ↔ Session**: this entry plus sessions 3.5, 4, 5 cover every commit on the feature branch.
  - **Dependencies ↔ Architecture**: `api/pyproject.toml`, `worker/pyproject.toml`, `web/package.json` all strictly within arch-specified package sets; no unapproved additions.
- Updated `docs/project-changelog.md` `[Unreleased] > Added` with a Feature #01 summary (pending merge).
- Stopped at: end of Phase Z. Ready for Stage 5 Ship once Docker-side TCs and CI are green.

### Session 5 — 2026-04-23 — Stage 4 (Build) — Phases E, F, G, H

- Phase E: Blender add-on stub (`addons/blender/f2f_addon/__init__.py` with `bl_info` + no-op `register`/`unregister`; README pointing to Feature 13) and Maya placeholder README (reserved for v1.1).
- Phase F: three Dockerfiles (`api`, `worker` with apt Blender + xvfb + libgl1 + extra X libs, `web` on node:20-slim via corepack pnpm), `infra/minio/create-buckets.sh` (mc alias retry + `mb --ignore-existing`), `docker-compose.yml` with seven services (db · redis · minio · createbuckets · api · worker · web), named volumes `db_data` / `minio_data`, healthchecks on db/redis/minio/api, `depends_on: condition: service_healthy` where meaningful. Added `infra/scripts/dev.ps1` and `dev.sh` wrappers (`up`/`down`/`logs`/`migrate`/`shell`).
- Phase G: `.github/workflows/ci.yml` with six jobs (`lint-web`, `test-web`, `lint-api`, `test-api`, `lint-worker`, `test-worker`) using `actions/setup-node@v4` (node 20) + `pnpm/action-setup@v4` (pnpm 9.15.0) + `actions/setup-python@v5` (3.12) + `astral-sh/setup-uv@v3` (with cache). Triggers `push` on `feature/**` / `hotfix/**` and `pull_request` on `main`. Concurrency group cancels superseded runs.
- Phase H: expanded README `Getting Started` with real working commands (`cp .env.example .env`, `docker compose up -d --build`, `alembic upgrade head`, `/tasks/ping` smoke), added `Development Workflow` (per-service commands: web / api / worker), `CI` section, and `Troubleshooting` (bucket timing, worker image size, pnpm first-boot, port conflicts, health interpretation).
- YAML sanity-checked `docker-compose.yml` (Python `yaml.safe_load` parses the expected 7 services + 2 volumes). `docker compose config` not runnable in this shell — Checkpoint F compose-level validation marked ✅ on the strength of the YAML parse + hand-review against architecture.
- Checkpoint G's "all 6 jobs pass on GitHub" remains unchecked until the branch is pushed and CI runs.
- Stopped at: end of Phase H. Next: Phase Y (testplan execution), Phase Z (cleanup + full cross-check).

### Session 4 — 2026-04-23 — Stage 4 (Build) — Phase D: Web scaffold

- Committed Next.js 14 scaffold under `web/` (package.json, tsconfig, Tailwind, ESLint, Prettier, Vitest configs).
- App shell: `app/layout.tsx`, `app/page.tsx` (landing), `components/HealthBadge.tsx` (calls `/healthz`), `lib/api.ts` (fetch wrapper), `app/globals.css` (Tailwind directives).
- Smoke test `tests/smoke.test.ts` wired with Vitest + jsdom.
- Added placeholder `public/favicon.ico` (minimal 78-byte ICO).
- Ran `pnpm install` (pnpm 9.15.0, Node 24) — committed `pnpm-lock.yaml`.
- `pnpm format:check` clean; `pnpm lint` clean; `pnpm test` green; `pnpm build` succeeds (static).
- **Deviation (minor)**: Removed `@typescript-eslint/no-unused-vars` override from `web/.eslintrc.json` (plugin not bundled with `eslint-config-next@14`); logged in Deviations table below.
- Stopped at: end of Phase D. Next: Phase E (Blender add-on scaffold).

### Session 3.5 — 2026-04-23 — Stage 4 (Build) — Phases A, B, C

- Phase A (`c4953e9`): `.editorconfig`, `.gitattributes`, `.env.example` per architecture.
- Phase B (`c5b66a1`): FastAPI scaffold — `/healthz`, `/tasks/ping`, `alembic` baseline, stub packages (ledger / manufacturability / mcp / providers / pipeline / models / schemas), conftest + `test_health`. `uv sync` / `ruff` / `pytest` all green.
- Phase C (`e8c483f`): Celery worker — `celery_app.py`, `tasks.ping` (graceful Blender absence), `blender_scripts/smoke.py`, eager-mode `test_ping`. `uv sync` / `ruff` / `pytest` all green.

### Session 3 — 2026-04-23 — Stage 3 (Plan)

- Wrote `tasks.md` with 8 phases (A–H) + testing (Y) + cleanup (Z), 56 tasks total.
- Wrote `testplan.md` with 11 AC, 11 test cases, edge/security/perf sections.
- Initialized this changelog.

### Session 2 — 2026-04-23 — Stage 2 (Design)

- Wrote `architecture.md`: full file tree (~60 new files), docker-compose service table with healthchecks, three Dockerfile specs, CI workflow (6 jobs), complete `.env.example`, security + trade-offs sections.
- Architecture FINALIZED.

### Session 1 — 2026-04-23 — Stage 1 (Discuss)

- Drafted `discussion.md`: problem framing, scope (scaffolding only), 4 user stories, 12 functional + 4 non-functional requirements.
- Raised 8 open questions; user answered all:
  1. Versions: Node 20 LTS / pnpm 9 / Python 3.12 / latest Blender apt.
  2. CI is advisory — no branch protection.
  3. Tailwind CSS enabled in `web/` from the start.
  4. MinIO bucket `f2f-assets` auto-provisioned by a `createbuckets` sidecar.
  5. Custom Blender image built on `python:3.12-slim` + apt Blender + xvfb + libgl1.
  6. Skip OpenTelemetry in Feature 01; revisit v1.1.
  7. Commit `.env.example` with safe local defaults; keep `.env` gitignored.
  8. License TBD — leave out of this feature.
- Marked discussion 🟢 COMPLETE. Committed `d648772`.

---

## Deviations from Plan

| Date | Deviation | Rationale |
|---|---|---|
| 2026-04-23 | Removed `@typescript-eslint/no-unused-vars` rule override from `web/.eslintrc.json` | `eslint-config-next@14` does not bundle `@typescript-eslint/eslint-plugin`; the rule is undefined at lint time. `next/core-web-vitals` already enforces unused-var checks via its own pipeline. Minor amendment — architecture intent preserved. |

---

## Final Summary

_Filled at Stage 5 / 6._
