# 🏗️ Architecture: Project Foundation

> **Feature**: `01` — Project Foundation
> **Discussion**: [`discussion.md`](discussion.md)
> **Status**: 🟢 FINALIZED
> **Date**: 2026-04-23

---

## Overview

Create the F2F monorepo layout with six top-level service/tooling folders and a
docker-compose stack that brings the full local dev environment up with a single
command. This feature produces no business logic — only scaffolding, wiring, and
smoke-level plumbing. Every subsequent v1.0 feature (#02–#15) plugs into slots
defined here.

---

## File Structure

Every file to create. Nothing is modified (repo is near-empty beyond docs).

```
F2F/
├── .editorconfig                                   # NEW
├── .env.example                                    # NEW
├── .gitattributes                                  # NEW (LF for text, binary flags)
├── .github/
│   └── workflows/
│       └── ci.yml                                  # NEW
├── docker-compose.yml                              # NEW
│
├── infra/
│   ├── docker/
│   │   ├── Dockerfile.api                          # NEW
│   │   ├── Dockerfile.web                          # NEW
│   │   └── Dockerfile.worker                       # NEW
│   ├── minio/
│   │   └── create-buckets.sh                       # NEW
│   └── scripts/
│       ├── dev.ps1                                 # NEW
│       └── dev.sh                                  # NEW
│
├── api/
│   ├── pyproject.toml                              # NEW
│   ├── uv.lock                                     # NEW (generated)
│   ├── ruff.toml                                   # NEW
│   ├── alembic.ini                                 # NEW
│   ├── alembic/
│   │   ├── env.py                                  # NEW
│   │   ├── script.py.mako                          # NEW
│   │   └── versions/
│   │       └── 0001_baseline.py                    # NEW (empty baseline)
│   ├── app/
│   │   ├── __init__.py                             # NEW
│   │   ├── main.py                                 # NEW (FastAPI app + routes)
│   │   ├── config.py                               # NEW (pydantic-settings)
│   │   ├── db.py                                   # NEW (SQLAlchemy engine + session)
│   │   ├── celery_app.py                           # NEW (Celery client for dispatch)
│   │   ├── routes/
│   │   │   ├── __init__.py                         # NEW
│   │   │   ├── health.py                           # NEW (/healthz)
│   │   │   └── tasks.py                            # NEW (/tasks/ping)
│   │   ├── ledger/
│   │   │   ├── __init__.py                         # NEW (stub)
│   │   │   └── README.md                           # NEW (reserved for Feature 02)
│   │   ├── manufacturability/
│   │   │   ├── __init__.py                         # NEW (stub)
│   │   │   └── README.md                           # NEW (reserved for Feature 11)
│   │   ├── mcp/
│   │   │   ├── __init__.py                         # NEW (stub)
│   │   │   └── README.md                           # NEW (reserved for Feature 14)
│   │   ├── providers/
│   │   │   ├── __init__.py                         # NEW (stub)
│   │   │   └── README.md                           # NEW (reserved for Feature 05)
│   │   ├── pipeline/
│   │   │   ├── __init__.py                         # NEW (stub)
│   │   │   └── README.md                           # NEW (reserved for Features 06-10)
│   │   ├── models/
│   │   │   └── __init__.py                         # NEW (empty declarative base)
│   │   └── schemas/
│   │       └── __init__.py                         # NEW (empty)
│   └── tests/
│       ├── __init__.py                             # NEW
│       ├── conftest.py                             # NEW
│       └── test_health.py                          # NEW (smoke test)
│
├── worker/
│   ├── pyproject.toml                              # NEW
│   ├── uv.lock                                     # NEW (generated)
│   ├── ruff.toml                                   # NEW
│   ├── worker/
│   │   ├── __init__.py                             # NEW
│   │   ├── celery_app.py                           # NEW (Celery worker app)
│   │   ├── config.py                               # NEW
│   │   └── tasks/
│   │       ├── __init__.py                         # NEW
│   │       └── ping.py                             # NEW (ping task + blender --version smoke)
│   ├── blender_scripts/
│   │   └── smoke.py                                # NEW (hello-world run inside Blender)
│   └── tests/
│       ├── __init__.py                             # NEW
│       └── test_ping.py                            # NEW
│
├── web/
│   ├── package.json                                # NEW
│   ├── pnpm-lock.yaml                              # NEW (generated)
│   ├── tsconfig.json                               # NEW
│   ├── next.config.mjs                             # NEW
│   ├── tailwind.config.ts                          # NEW
│   ├── postcss.config.mjs                          # NEW
│   ├── .eslintrc.json                              # NEW
│   ├── .prettierrc                                 # NEW
│   ├── vitest.config.ts                            # NEW
│   ├── next-env.d.ts                               # NEW (generated)
│   ├── app/
│   │   ├── layout.tsx                              # NEW
│   │   ├── page.tsx                                # NEW (landing page, calls /healthz)
│   │   └── globals.css                             # NEW (Tailwind directives)
│   ├── components/
│   │   └── HealthBadge.tsx                         # NEW (renders API /healthz result)
│   ├── lib/
│   │   └── api.ts                                  # NEW (fetch wrapper)
│   ├── public/
│   │   └── favicon.ico                             # NEW (placeholder)
│   └── tests/
│       └── smoke.test.ts                           # NEW (Vitest)
│
├── addons/
│   ├── blender/
│   │   └── f2f_addon/
│   │       ├── __init__.py                         # NEW (bl_info + empty operator)
│   │       └── README.md                           # NEW
│   └── maya/
│       └── README.md                               # NEW (v1.1 placeholder)
│
└── README.md                                       # MODIFY — expand "Getting Started"
                                                    # with real, working commands
```

---

## Data Model

N/A — this feature does not introduce data models. The `api/app/models/` package
exists with an empty SQLAlchemy `DeclarativeBase` so Feature 02 has a plug-in point.
The baseline Alembic migration (`0001_baseline.py`) contains no operations; it only
establishes the migration head.

---

## Component Design

### `api/` — FastAPI service

**Responsibility**: HTTP surface + DB session + Celery dispatch. No business logic.
**Location**: `api/app/main.py`

```
FastAPI app
├── on_startup()                          # verify DB + Redis reachable (best-effort)
├── GET  /healthz  → {"status":"ok",      # route: routes/health.py
│                     "db": "up"|"down",
│                     "redis": "up"|"down",
│                     "version": "..."}
├── GET  /tasks/ping → dispatch celery    # route: routes/tasks.py
│                      ping task, return
│                      {"task_id": "..."}
└── GET  /tasks/ping/{task_id} → result   # poll task result
```

**Config** (`api/app/config.py` via `pydantic-settings`):

| Setting | Env var | Default |
|---|---|---|
| `database_url` | `DATABASE_URL` | `postgresql+psycopg://f2f:f2f@db:5432/f2f` |
| `redis_url` | `REDIS_URL` | `redis://redis:6379/0` |
| `s3_endpoint` | `S3_ENDPOINT` | `http://minio:9000` |
| `s3_bucket` | `S3_BUCKET` | `f2f-assets` |
| `s3_access_key` | `S3_ACCESS_KEY` | `f2fminio` |
| `s3_secret_key` | `S3_SECRET_KEY` | `f2fminio-secret` |
| `tripo_api_key` | `TRIPO_API_KEY` | `""` (unused in Feature 01) |
| `tripo_api_base` | `TRIPO_API_BASE` | `https://api.tripo3d.ai` |
| `environment` | `ENVIRONMENT` | `development` |
| `log_level` | `LOG_LEVEL` | `INFO` |

### `worker/` — Celery + Blender headless

**Responsibility**: Execute async jobs. For Feature 01, only the `ping` task.
**Location**: `worker/worker/celery_app.py`

```
Celery app (broker=REDIS_URL, backend=REDIS_URL)
└── tasks.ping() → str  # returns "pong" + `blender --version` stdout
```

### `web/` — Next.js 14

**Responsibility**: UI shell, API client, smoke display.
**Location**: `web/app/page.tsx` + `web/lib/api.ts`

```
/ (landing)
  └── <HealthBadge />  # fetches API_BASE/healthz, renders green/red dot
                       # uses NEXT_PUBLIC_API_BASE from env
```

### `addons/blender/f2f_addon/__init__.py`

```python
bl_info = {
    "name": "F2F",
    "author": "F2F",
    "version": (0, 1, 0),
    "blender": (4, 0, 0),
    "description": "F2F asset hand-off (placeholder - see Feature 13)",
    "category": "Import-Export",
}

def register(): pass
def unregister(): pass
```

---

## Data Flow

Single Feature-01 smoke flow:

```
Browser (localhost:3000)
  └─ fetch(NEXT_PUBLIC_API_BASE + "/healthz")
     └─ api container (localhost:8000)
        ├─ SELECT 1 on db     → "db":"up"
        └─ PING on redis      → "redis":"up"

Browser (localhost:3000)
  └─ fetch("/tasks/ping")
     └─ api container
        └─ celery.send_task("tasks.ping")
           └─ worker container (consumes from Redis)
              ├─ subprocess.run(["blender", "--version"])
              └─ return "pong | Blender 4.x ..."
     ← response: {"task_id":"..."}
  └─ fetch("/tasks/ping/{task_id}")
     ← response: {"status":"SUCCESS","result":"pong | Blender ..."}
```

---

## Configuration

### `.env.example` (committed)

```
# Core
ENVIRONMENT=development
LOG_LEVEL=INFO

# Database
DATABASE_URL=postgresql+psycopg://f2f:f2f@db:5432/f2f
POSTGRES_USER=f2f
POSTGRES_PASSWORD=f2f
POSTGRES_DB=f2f

# Redis
REDIS_URL=redis://redis:6379/0

# MinIO / S3
S3_ENDPOINT=http://minio:9000
S3_BUCKET=f2f-assets
S3_ACCESS_KEY=f2fminio
S3_SECRET_KEY=f2fminio-secret
MINIO_ROOT_USER=f2fminio
MINIO_ROOT_PASSWORD=f2fminio-secret

# Tripo 3D (unused in Feature 01; required from Feature 05)
TRIPO_API_KEY=
TRIPO_API_BASE=https://api.tripo3d.ai

# Web
NEXT_PUBLIC_API_BASE=http://localhost:8000
```

### `docker-compose.yml` services

| Service | Image / Build | Ports | Depends on | Notes |
|---|---|---|---|---|
| `db` | `postgres:16-alpine` | `5432:5432` | — | Named volume `db_data` |
| `redis` | `redis:7-alpine` | `6379:6379` | — | In-memory (no volume for v1.0) |
| `minio` | `minio/minio:latest` | `9000:9000`, `9001:9001` | — | Named volume `minio_data` |
| `createbuckets` | `minio/mc:latest` | — | `minio` | Runs `infra/minio/create-buckets.sh`, exits 0 |
| `api` | build `infra/docker/Dockerfile.api` | `8000:8000` | `db`, `redis`, `minio` | `uvicorn app.main:app --host 0.0.0.0` |
| `worker` | build `infra/docker/Dockerfile.worker` | — | `redis` | `celery -A worker.celery_app worker -l INFO` |
| `web` | build `infra/docker/Dockerfile.web` | `3000:3000` | `api` | `pnpm dev` |

Healthchecks on `db`, `redis`, `minio`, `api` (all trivial — `pg_isready`, `redis-cli
ping`, `/minio/health/live`, `/healthz`).

### Dockerfiles

| Dockerfile | Base | Installs | CMD |
|---|---|---|---|
| `Dockerfile.api` | `python:3.12-slim` | `uv`, copy `api/`, `uv sync` | `uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload` |
| `Dockerfile.worker` | `python:3.12-slim` | `uv`, **`apt-get install -y blender xvfb libgl1`**, copy `worker/`, `uv sync` | `celery -A worker.celery_app worker -l INFO` |
| `Dockerfile.web` | `node:20-slim` | `corepack enable` → pnpm, copy `web/`, `pnpm install` | `pnpm dev --hostname 0.0.0.0` |

### `ruff.toml` (api/ and worker/, identical)

```toml
line-length = 100
target-version = "py312"

[lint]
select = ["E", "F", "I", "B", "UP", "ASYNC", "S"]
ignore = ["S101"]  # allow assert in tests

[lint.per-file-ignores]
"tests/*" = ["S", "B"]
```

### `.eslintrc.json` (web/)

```json
{
  "extends": ["next/core-web-vitals", "prettier"],
  "rules": {
    "@typescript-eslint/no-unused-vars": ["error", { "argsIgnorePattern": "^_" }]
  }
}
```

### `.prettierrc` (web/)

```json
{ "semi": true, "singleQuote": true, "trailingComma": "all", "printWidth": 100 }
```

### `.github/workflows/ci.yml`

| Job | Runs on | Steps |
|---|---|---|
| `lint-web` | `ubuntu-latest` | setup-node 20 → pnpm install → `pnpm lint && pnpm format:check` |
| `test-web` | `ubuntu-latest` | setup-node 20 → pnpm install → `pnpm test` (vitest run) |
| `lint-api` | `ubuntu-latest` | setup-python 3.12 → install uv → `uv sync` → `ruff check . && ruff format --check .` |
| `test-api` | `ubuntu-latest` | setup-python 3.12 → install uv → `uv sync` → `pytest` |
| `lint-worker` | `ubuntu-latest` | same as `lint-api` but in `worker/` |
| `test-worker` | `ubuntu-latest` | same as `test-api` but in `worker/` |

**Triggers**: `push` on `feature/**` and `hotfix/**`; `pull_request` on `main`.
**Branch protection**: NOT enabled (per discussion decision).

---

## Security Considerations

| Surface | Concern | Mitigation |
|---|---|---|
| Default MinIO creds committed in `.env.example` | Local-only dev values; never production | Document in README: "v1.0 is local-only; for cloud deployment in v1.1+, rotate all `f2fminio*` secrets" |
| `TRIPO_API_KEY` | Real secret in developer `.env` | `.env` is gitignored (already in root `.gitignore`); committed file is `.env.example` with empty value |
| `/healthz` and `/tasks/ping` unauthenticated | Expected — v1.0 has no auth by design | Documented in `project-context.md`; Clerk in v1.1 |
| Docker images pulled by tag | Supply-chain risk | Accepted for v1.0 internal demo; digest pinning deferred |
| CI runs untrusted code on PRs | Standard GitHub Actions risk | Jobs do not have secrets; only lint + tests |

No PII handled in Feature 01.

---

## Trade-offs & Alternatives

| Decision | Alternative | Why chosen |
|---|---|---|
| Custom Blender image (`python:3.12-slim` + apt) | `linuxserver/blender`, `nytimes/blender` | Smaller (~1.2 GB vs ~2 GB), no external maintenance dependency, full control (decision Q5) |
| Single `docker-compose.yml` | Multiple compose files + override | Simpler for internal demo; split in v1.1 if cloud-vs-local diverges |
| Celery+Redis | RQ, BullMQ, Temporal, arq | Pre-approved in project-context; most mature Python option |
| `uv` for Python | `poetry`, `pip-tools` | Pre-approved in project-context; fastest resolver |
| `pnpm` for TS | `npm`, `yarn` | Pre-approved in project-context; fastest, disk-efficient |
| CI advisory (no branch protection) | Hard gate | Decision Q2; keeps emergency merges possible |
| `.env.example` committed | `.env.development` committed | Standard convention; `.env` stays gitignored |
| Stubs (`ledger/`, `manufacturability/`, `mcp/`) with README | No stubs; create in their own features | Prevents restructuring churn in later features; zero runtime cost |
| No OpenTelemetry | Add commented services | Decision Q6; keeps Stage 2 scope tight |

---

## Next

Create tasks doc → `tasks.md`
