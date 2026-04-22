# 💬 Discussion: Project Foundation

> **Feature**: `01` — Project Foundation
> **Status**: � COMPLETE
> **Branch**: `feature/01-project-foundation`
> **Depends On**: — (first feature)
> **Date Started**: 2026-04-23
> **Date Completed**: 2026-04-23

---

## Summary

Lay the monorepo foundation so every subsequent feature has a clean, consistent
place to land. This feature produces **no product functionality** — it produces a
repo layout, local docker-compose dev environment, lint/format/test tooling, a smoke
CI workflow, and a documented developer setup. After this ships, a new contributor
(human or AI) can clone F2F, run `docker compose up`, and see all services healthy.

---

## Lessons from Previous Features

No prior features — this is #01. Decisions to carry forward from the project-init
discussion (not features, but relevant precedent):

- **Design Ledger is a cross-cutting principle** — Feature 02 will add the tables,
  but Feature 01's data-layer scaffolding (SQLAlchemy + Alembic wiring) must not
  preclude an append-only event-log pattern. No premature decisions here; just
  awareness.
- **MCP server is a v1.0 deliverable** — no action in Feature 01, but the `api/app/mcp/`
  directory will be created empty-with-README so the slot is reserved.

---

## Functional Requirements

The foundation is "done" when all of the following are true from a fresh clone:

- **FR-01** — `docker compose up -d` brings up PostgreSQL 16, Redis 7, MinIO, api
  (FastAPI), worker (Celery + Blender headless), and web (Next.js) — all healthy.
- **FR-02** — `http://localhost:8000/healthz` returns `200 {"status":"ok"}`.
- **FR-02b** — `http://localhost:8000/docs` serves the FastAPI auto-OpenAPI UI.
- **FR-03** — `http://localhost:3000` loads a minimal Next.js landing page that
  successfully calls `/healthz` via the API client and renders the result.
- **FR-04** — `http://localhost:9001` serves the MinIO console; the
  `f2f-assets` bucket exists (provisioned at startup).
- **FR-05** — Celery worker is connected to Redis; a trivial `ping` task returns
  `"pong"` when invoked (visible via a `/tasks/ping` debug endpoint on the API).
- **FR-06** — Blender headless is invokable from the worker container: the worker
  image contains `blender`, and `blender --version` runs inside it.
- **FR-07** — Alembic is wired; `alembic upgrade head` runs cleanly with a single
  empty baseline migration.
- **FR-08** — Linters/formatters pass on an empty codebase:
  - Python: `ruff check .` and `ruff format --check .` both clean in `api/` and `worker/`
  - TypeScript: `pnpm lint` and `pnpm format:check` both clean in `web/`
- **FR-09** — Test runners execute a single placeholder test on each side:
  - `pytest` in `api/` and `worker/` — one passing test each
  - `vitest run` in `web/` — one passing test
- **FR-10** — A GitHub Actions workflow runs lint + tests on every push to any
  `feature/**` branch and on PRs to `main`. It must pass on the Feature 01 PR
  itself.
- **FR-11** — The Blender add-on directory exists with a valid (but empty-of-logic)
  add-on manifest so future features can plug in.
- **FR-12** — Environment variables are defined via a committed `.env.example`; the
  docker-compose stack reads `.env` for overrides; missing-variable behavior is
  documented in the README.

---

## Current State / Reference

### What Exists

- Project-init docs (`docs/mastery.md`, `docs/mastery-compact.md`,
  `docs/project-discussion.md`, `docs/project-context.md`, `docs/project-roadmap.md`,
  `docs/project-changelog.md`, `AGENTS.md`, `README.md`, `.gitignore`).
- Git repo on GitHub at `BATMAN-009/F2F`, default branch `main`.
- No source code. No `web/`, `api/`, `worker/`, `addons/`, or `infra/` directories yet.

### What Works Well (to preserve)

- Mastery framework layout — `docs/` is canonical; `AGENTS.md` at project root.
- Branch-per-feature with human-approved merges — working cleanly (PR #1 was merged
  this way).

### What Needs Improvement

- None applicable — greenfield.

---

## Proposed Approach

Scaffold six top-level directories and a `docker-compose.yml` that wires everything
together. Each sub-stack gets the minimum viable skeleton; no business logic.

### Scaffolded directories

| Directory | Contents |
|---|---|
| `web/` | Next.js 14 App Router + TypeScript + Tailwind + `next-themes`; `/` page that calls `/healthz`; ESLint + Prettier; Vitest + a `smoke.test.ts`; `pnpm` lockfile |
| `api/` | FastAPI + SQLAlchemy 2 + Alembic + pydantic-settings; `/healthz` + `/tasks/ping`; Ruff; pytest + `test_healthz.py`; `pyproject.toml` with `uv`-friendly layout |
| `worker/` | Celery app + `tasks.ping` + Blender invocation smoke; Ruff; pytest + `test_ping.py`; `pyproject.toml` |
| `addons/blender/f2f_addon/` | Minimal `__init__.py` with a valid `bl_info` and an empty "F2F" operator stub |
| `infra/docker/` | `Dockerfile.api`, `Dockerfile.worker` (Blender-based), `Dockerfile.web` |
| `infra/scripts/` | `dev.ps1` / `dev.sh` helpers for `up`, `down`, `logs`, `migrate` |

### docker-compose services

| Service | Image / Build | Ports | Purpose |
|---|---|---|---|
| `db` | `postgres:16-alpine` | 5432 | PostgreSQL |
| `redis` | `redis:7-alpine` | 6379 | Celery broker + result backend |
| `minio` | `minio/minio:latest` | 9000 / 9001 | S3-compatible storage + console |
| `createbuckets` | `minio/mc:latest` | — | One-shot: create `f2f-assets` bucket |
| `api` | build `infra/docker/Dockerfile.api` | 8000 | FastAPI |
| `worker` | build `infra/docker/Dockerfile.worker` | — | Celery + Blender headless |
| `web` | build `infra/docker/Dockerfile.web` | 3000 | Next.js dev server |

### CI skeleton

Single `.github/workflows/ci.yml`:
- Jobs: `lint-web`, `test-web`, `lint-py` (api + worker), `test-py` (api + worker)
- Triggers: push to `feature/**`, PR to `main`
- No deploy, no release automation yet (v1.1+ concern)

---

## Dependencies

| Dependency | Type | Status |
|---|---|---|
| Docker Desktop | Tool (local) | User must have installed |
| Node.js 20 + pnpm | Tool (local) | User must have installed |
| Python 3.12 + uv | Tool (local) | User appears to be installing uv (terminal context) |
| GitHub Actions | Infra | Free tier sufficient for v1.0 |
| `postgres:16-alpine` | Container image | Public |
| `redis:7-alpine` | Container image | Public |
| `minio/minio`, `minio/mc` | Container images | Public |
| Blender 4.x | Installed inside worker image | Base: `linuxserver/blender` or `nytimes/blender` (TBD in Stage 2) |

---

## Research & Prior Art

N/A — every piece of this stack is well-understood. Any stage 2 research
(e.g., which Blender Docker base image is smallest & most stable) belongs in
Stage 2 (architecture) not here.

---

## Open Questions — RESOLVED

- [x] **Q1 — Versions**: **Node 20 LTS, pnpm 9, Python 3.12** (recommended defaults).
- [x] **Q2 — CI**: **Include GitHub Actions CI**, no branch protection (advisory).
- [x] **Q3 — Tailwind**: **Yes**, Tailwind CSS from day one in `web/`.
- [x] **Q4 — MinIO bucket provisioning**: **Yes**, automate via a `createbuckets`
  one-shot service in `docker-compose.yml`.
- [x] **Q5 — Blender base image**: **Build our own** on `python:3.12-slim` + apt
  Blender. Smaller, fully owned.
- [x] **Q6 — OTEL in Feature 01**: **Skip entirely** — revisit in v1.1.
- [x] **Q7 — `.env.example`**: **Yes**, include placeholder `TRIPO_API_KEY=` and all
  other v1.0 env vars from `project-context.md`.
- [x] **Q8 — License**: **TBD** — decide when publicizing.

---

## Decisions Made

| Date | Decision | Rationale |
|---|---|---|
| 2026-04-23 | Feature 01 scope = scaffolding only; zero business logic | Keeps feature shippable fast; every subsequent feature starts from a known-good floor |
| 2026-04-23 | Reserve `api/app/ledger/`, `api/app/manufacturability/`, `api/app/mcp/` as empty stubs | So Features 02, 11, 14 plug in without restructuring |
| 2026-04-23 | Local-only (docker-compose) — no cloud touches in Feature 01 | Matches v1.0 internal-demo scope |
| 2026-04-23 | Versions: Node 20 LTS, pnpm 9, Python 3.12 | Current LTS / stable across all tooling |
| 2026-04-23 | GitHub Actions CI included in Feature 01, branch protection off | Lint+tests on PRs without locking emergency merges |
| 2026-04-23 | Tailwind CSS included in `web/` from day one | Avoids a future CSS retrofit; Next.js default companion |
| 2026-04-23 | MinIO `f2f-assets` bucket auto-provisioned via `createbuckets` one-shot service | Zero-friction clone → `up` → working |
| 2026-04-23 | Blender base image = custom build on `python:3.12-slim` + apt Blender | Smaller (~1.2 GB), fully owned, no external maintenance dependency |
| 2026-04-23 | OTEL/Jaeger skipped in Feature 01; scheduled for v1.1 | Keep Stage 2 tight |
| 2026-04-23 | `.env.example` committed with all v1.0 vars (incl. placeholder `TRIPO_API_KEY=`) | Day-1 developer visibility |
| 2026-04-23 | License = TBD | Internal demo; decide on publicization |

---

## Discussion Complete ✅

**Summary**: Feature 01 scaffolds the F2F monorepo — `web/`, `api/`, `worker/`,
`addons/blender/`, `infra/` — and wires a local docker-compose stack (PostgreSQL,
Redis, MinIO + auto-created bucket, FastAPI api, Celery+Blender worker, Next.js
web). It delivers no product functionality; it delivers a known-good, lint-clean,
test-green foundation that every subsequent v1.0 feature plugs into. Stubs for
`ledger/`, `manufacturability/`, and `mcp/` are reserved inside `api/app/` so
Features 02, 11, and 14 add code without restructuring. GitHub Actions CI runs lint
+ tests on `feature/**` pushes and PRs to `main`, advisory (no branch protection).

**Completed**: 2026-04-23
**Next**: Create architecture doc → `architecture.md`
