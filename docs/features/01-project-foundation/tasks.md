# ✅ Tasks: Project Foundation

> **Feature**: `01` — Project Foundation
> **Architecture**: [`architecture.md`](architecture.md)
> **Branch**: `feature/01-project-foundation`
> **Status**: 🔴 NOT STARTED
> **Progress**: 0/56 tasks complete

---

## Pre-Flight

- [x] Discussion doc marked COMPLETE (2026-04-23)
- [x] Architecture doc FINALIZED (2026-04-23)
- [x] Feature branch created from main (`feature/01-project-foundation`)
- [x] No dependent features (Feature 01 is first)

---

## Phase A — Repo Hygiene

> Top-level config files that every subsequent phase depends on.

- [ ] **A.1** — Create `.editorconfig` (LF, UTF-8, 2-space indent for TS/JSON/YAML, 4-space for Python, final newline)
- [ ] **A.2** — Create `.gitattributes` (`* text=auto eol=lf`; binary flags for common image/mesh extensions)
- [ ] **A.3** — Create `.env.example` per architecture doc
- [ ] **A.4** — Verify `.env` and `.env.*` (except `.env.example`) are already in root `.gitignore` (confirmed from project-init commit)
- [ ] 📍 **Checkpoint A** — Files exist; `.env.example` matches the architecture table exactly

---

## Phase B — API Service (Python / FastAPI)

> The pipeline orchestration service. Ships with `/healthz` and `/tasks/ping` only.

- [ ] **B.1** — Create `api/pyproject.toml` with dependencies: `fastapi`, `uvicorn[standard]`, `sqlalchemy>=2`, `psycopg[binary]`, `alembic`, `celery`, `redis`, `pydantic-settings`, `boto3`, `httpx`; dev: `pytest`, `pytest-asyncio`, `ruff`
- [ ] **B.2** — Create `api/ruff.toml` per architecture
- [ ] **B.3** — Create `api/app/__init__.py`, `api/app/config.py` (pydantic-settings `Settings` class), `api/app/db.py` (SQLAlchemy engine + `SessionLocal` + `DeclarativeBase`)
- [ ] **B.4** — Create `api/app/celery_app.py` (Celery client configured with `REDIS_URL`; no tasks registered here — just dispatch)
- [ ] **B.5** — Create `api/app/routes/__init__.py`, `api/app/routes/health.py` with `GET /healthz` that checks DB (`SELECT 1`) and Redis (`PING`) and returns status JSON
- [ ] **B.6** — Create `api/app/routes/tasks.py` with `GET /tasks/ping` (dispatches) and `GET /tasks/ping/{task_id}` (returns result)
- [ ] **B.7** — Create `api/app/main.py`: FastAPI app, register routers, CORS for `http://localhost:3000`
- [ ] **B.8** — Create stub packages + README markers: `api/app/ledger/`, `api/app/manufacturability/`, `api/app/mcp/`, `api/app/providers/`, `api/app/pipeline/`, `api/app/models/`, `api/app/schemas/`
- [ ] **B.9** — Create `api/alembic.ini`, `api/alembic/env.py`, `api/alembic/script.py.mako`, `api/alembic/versions/0001_baseline.py` (empty `upgrade`/`downgrade`)
- [ ] **B.10** — Create `api/tests/__init__.py`, `api/tests/conftest.py` (TestClient fixture), `api/tests/test_health.py` (asserts `GET /healthz` returns 200 and has `status` key)
- [ ] **B.11** — Run `uv sync` in `api/` to generate `uv.lock`; commit the lockfile
- [ ] **B.12** — Run `ruff check .` and `ruff format --check .` in `api/` → fix anything until clean
- [ ] **B.13** — Run `pytest` in `api/` → ensure `test_health` passes (monkey-patch DB/Redis to up for this test)
- [ ] 📍 **Checkpoint B** — `uv run pytest` green; `ruff check .` green; `ruff format --check .` green

---

## Phase C — Worker Service (Python / Celery + Blender)

- [ ] **C.1** — Create `worker/pyproject.toml` with dependencies: `celery`, `redis`, `pydantic-settings`; dev: `pytest`, `ruff`
- [ ] **C.2** — Create `worker/ruff.toml` (identical to api's)
- [ ] **C.3** — Create `worker/worker/__init__.py`, `worker/worker/config.py`, `worker/worker/celery_app.py` (Celery app; broker+backend from `REDIS_URL`; autodiscover `worker.tasks`)
- [ ] **C.4** — Create `worker/worker/tasks/__init__.py`, `worker/worker/tasks/ping.py` — `@app.task(name="tasks.ping")` that runs `blender --version`, returns `f"pong | {blender_version}"`. Gracefully handle absence of Blender (return `"pong | blender: unavailable"`) so the test suite runs without Blender installed on the host.
- [ ] **C.5** — Create `worker/blender_scripts/smoke.py` — hello-world script runnable via `blender -b -P smoke.py` (prints a known string)
- [ ] **C.6** — Create `worker/tests/test_ping.py` — invokes `ping` synchronously via `.apply()` (eager mode) and asserts result starts with `"pong"`
- [ ] **C.7** — Run `uv sync` in `worker/`; commit lockfile
- [ ] **C.8** — Run `ruff check .` and `ruff format --check .` in `worker/` → fix until clean
- [ ] **C.9** — Run `pytest` in `worker/` → green
- [ ] 📍 **Checkpoint C** — All worker checks green without requiring Blender on host

---

## Phase D — Web Service (Next.js 14 + TS + Tailwind)

- [ ] **D.1** — Scaffold `web/` with `package.json` (name `@f2f/web`, private, scripts: `dev`, `build`, `start`, `lint`, `format`, `format:check`, `test`, `test:watch`), engines `node>=20`, packageManager `pnpm@9.x`
- [ ] **D.2** — Add deps: `next@14`, `react@18`, `react-dom@18`, `tailwindcss`, `postcss`, `autoprefixer`
- [ ] **D.3** — Add dev deps: `typescript`, `@types/node`, `@types/react`, `@types/react-dom`, `eslint`, `eslint-config-next`, `eslint-config-prettier`, `prettier`, `vitest`, `@vitejs/plugin-react`, `jsdom`, `@testing-library/react`, `@testing-library/jest-dom`
- [ ] **D.4** — Create `tsconfig.json`, `next.config.mjs`, `tailwind.config.ts` (content globs for `app/**`, `components/**`), `postcss.config.mjs`, `.eslintrc.json`, `.prettierrc`, `vitest.config.ts` (jsdom env)
- [ ] **D.5** — Create `app/globals.css` with `@tailwind base; @tailwind components; @tailwind utilities;`
- [ ] **D.6** — Create `app/layout.tsx` (HTML shell, imports globals.css), `app/page.tsx` (centered landing with title + `<HealthBadge />`)
- [ ] **D.7** — Create `lib/api.ts` — `apiFetch(path)` using `process.env.NEXT_PUBLIC_API_BASE`
- [ ] **D.8** — Create `components/HealthBadge.tsx` — client component, calls `/healthz`, renders colored dot + status
- [ ] **D.9** — Create `tests/smoke.test.ts` — trivial passing test (`expect(1 + 1).toBe(2)`) so Vitest is wired
- [ ] **D.10** — Create `public/favicon.ico` (placeholder 16×16 solid-color PNG renamed, or tiny blank ICO)
- [ ] **D.11** — Run `pnpm install` in `web/`; commit `pnpm-lock.yaml`
- [ ] **D.12** — Run `pnpm lint` → clean; `pnpm format:check` → clean; `pnpm test` → green
- [ ] 📍 **Checkpoint D** — `pnpm build` succeeds (static build smoke)

---

## Phase E — Blender Add-on Scaffold

- [ ] **E.1** — Create `addons/blender/f2f_addon/__init__.py` with valid `bl_info` and empty `register()` / `unregister()` stubs
- [ ] **E.2** — Create `addons/blender/f2f_addon/README.md` — note this is reserved for Feature 13
- [ ] **E.3** — Create `addons/maya/README.md` — note this is reserved for v1.1
- [ ] 📍 **Checkpoint E** — Folder layout matches architecture tree

---

## Phase F — Infra & docker-compose

- [ ] **F.1** — Create `infra/docker/Dockerfile.api` per architecture (python:3.12-slim, uv, copy api/, `uv sync`, uvicorn CMD)
- [ ] **F.2** — Create `infra/docker/Dockerfile.worker` (python:3.12-slim, uv, apt blender+xvfb+libgl1, copy worker/, `uv sync`, celery CMD)
- [ ] **F.3** — Create `infra/docker/Dockerfile.web` (node:20-slim, corepack enable pnpm, copy web/, pnpm install, dev CMD)
- [ ] **F.4** — Create `infra/minio/create-buckets.sh` — uses `mc` to configure alias and `mb --ignore-existing` the `f2f-assets` bucket
- [ ] **F.5** — Create `docker-compose.yml` per architecture service table, including healthchecks and `depends_on` with `condition: service_healthy`
- [ ] **F.6** — Create `infra/scripts/dev.ps1` and `infra/scripts/dev.sh` — thin wrappers: `up`, `down`, `logs [svc]`, `migrate`, `shell [svc]`
- [ ] 📍 **Checkpoint F** — `docker compose config` validates with no errors

---

## Phase G — CI

- [ ] **G.1** — Create `.github/workflows/ci.yml` with 6 jobs per architecture (lint-web, test-web, lint-api, test-api, lint-worker, test-worker)
- [ ] **G.2** — Triggers: `push` on `feature/**` and `hotfix/**`; `pull_request` on `main`
- [ ] **G.3** — Use `actions/setup-node@v4` (node 20) and `actions/setup-python@v5` (python 3.12); install `uv` via `astral-sh/setup-uv@v3`; install `pnpm` via `pnpm/action-setup@v4` (version 9)
- [ ] **G.4** — Cache dependencies (`pnpm store`, `uv cache`)
- [ ] 📍 **Checkpoint G** — After push, all 6 jobs appear and pass on GitHub

---

## Phase H — Documentation Updates

- [ ] **H.1** — Update top-level `README.md` "Getting Started" section with real working commands: clone → `cp .env.example .env` → `docker compose up -d` → `alembic upgrade head` → open URLs
- [ ] **H.2** — Update `README.md` "Development Workflow" section: how to run tests locally per service, how to lint, how to invoke CI manually
- [ ] **H.3** — Add a "Troubleshooting" subsection noting: MinIO bucket creation timing, Blender image size, first-boot `pnpm install` time
- [ ] 📍 **Checkpoint H** — A first-time reader can go from clone to working stack using only README

---

## Phase Y — Testing (run the test plan)

> Full test plan at [`testplan.md`](testplan.md).

- [ ] **Y.1** — TC-01 happy path: fresh clone + `docker compose up -d` + open all 3 URLs
- [ ] **Y.2** — TC-02 `/healthz` reports `db: up`, `redis: up`
- [ ] **Y.3** — TC-03 `/tasks/ping` round-trip returns `pong | Blender ...`
- [ ] **Y.4** — TC-04 MinIO bucket `f2f-assets` exists after startup
- [ ] **Y.5** — TC-05 `alembic upgrade head` succeeds on a fresh DB
- [ ] **Y.6** — TC-06 Each service's lint + unit tests pass locally
- [ ] **Y.7** — TC-07 CI workflow green on the PR for this feature
- [ ] **Y.8** — TC-08 Stopping the stack (`docker compose down`) is clean; restarting it preserves DB and MinIO state
- [ ] **Y.9** — TC-09 (negative) Missing `TRIPO_API_KEY` does NOT break Feature 01 services (used from Feature 05)
- [ ] **Y.10** — TC-10 (negative) API gracefully reports `db: down` when PostgreSQL is stopped
- [ ] 📍 **Checkpoint Y** — All test cases pass; `testplan.md` summary filled in

---

## Phase Z — Documentation & Cleanup

- [ ] **Z.1** — Inline comments only where logic is non-obvious (Alembic env.py, docker healthcheck gotchas)
- [ ] **Z.2** — Update `docs/features/01-project-foundation/changelog.md` with final session note + deviations from plan
- [ ] **Z.3** — Update `docs/project-roadmap.md`: mark Feature 01 as 🟢 Complete after merge
- [ ] **Z.4** — Update `docs/project-changelog.md` `[Unreleased] > Added`: "Feature #01 — Project Foundation"
- [ ] **Z.5** — Perform **full verification cross-check** per Mastery rules (architecture ↔ code, tasks ↔ code, testplan ↔ tests, changelog ↔ session, dependencies ↔ architecture); log result in feature changelog
- [ ] 📍 **Checkpoint Z** — Self-review all diffs on `feature/01-project-foundation` branch

---

## Ship 🚀

- [ ] All phases complete
- [ ] Final commit with descriptive message
- [ ] Push to feature branch
- [ ] Open PR; CI green
- [ ] Human approval received
- [ ] Merge to main (no-ff)
- [ ] Push main
- [ ] `[Unreleased] > Added` entry in `project-changelog.md`
- [ ] **Keep** the feature branch — do not delete
- [ ] Create review doc → `review.md` (Stage 6)
