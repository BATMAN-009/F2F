# F2F

> **An "idea → physical product" platform.**
> Photo or multi-view → AI 3D → custom texture → real-world dimensions →
> multi-format export → AR preview → Blender hand-off → (later) match-to-market,
> manufacturer discovery, and vertical apps.

> ⚠️ **Status: pre-release.** v1.0 (Internal Demo) is being built feature-by-feature
> using the [Mastery framework](docs/mastery.md). No code has shipped yet.

---

## What Is F2F?

F2F is a web-based engine that takes a user's idea — expressed as one image, multiple
images (right/left/top/bottom + reference), or a prompt — and turns it into a
physical product. The pipeline:

1. **Generate** a 3D mesh via Tripo 3D (provider-agnostic abstraction).
2. **Texture** with a user-supplied image at configurable resolution.
3. **Dimension** the model to real-world H × W × D.
4. **Preview** in AR on iOS / Android via `<model-viewer>`.
5. **Export** to STL / USD / FBX / OBJ / 3MF (via headless Blender).
6. **Hand off** to Blender directly via the F2F add-on.

Later releases add visual match-to-market (don't manufacture if it already exists),
LLM-driven manufacturer discovery + automated outreach + payments, and vertical
applications starting with film/TV prop previsualization.

## Roadmap (v1.0 — Internal Demo)

See [`docs/project-roadmap.md`](docs/project-roadmap.md) for the full feature list and
dependencies. v1.0 is **local-only** (docker-compose), single-user, no auth.

## Architecture

- **Web** — Next.js 14 + TypeScript + React Three Fiber + `<model-viewer>`
- **API** — FastAPI + SQLAlchemy 2 + Alembic
- **Workers** — Celery + Redis + Blender headless
- **Database** — PostgreSQL 16
- **Storage** — MinIO (S3-compatible, local; Cloudflare R2 in v1.1+)
- **AI Provider** — Tripo 3D (behind a `Provider` abstraction)

Full details: [`docs/project-context.md`](docs/project-context.md).

## Repository Layout

```
F2F/
├── AGENTS.md                 # AI agent orientation
├── README.md                 # this file
├── docker-compose.yml        # (created in Feature 01)
├── web/                      # Next.js app
├── api/                      # FastAPI service
├── worker/                   # Celery + Blender workers
├── addons/blender/           # Blender add-on
├── infra/                    # Dockerfiles + dev scripts
└── docs/                     # Mastery documentation
```

## Development Process — Mastery Framework

This project uses [Mastery](docs/mastery.md), a discipline-first framework where every
feature flows through six stages: **Discuss → Design → Plan → Build → Ship → Reflect**.

- All work happens on `feature/XX-name` branches; `main` is always deployable.
- Branches are **never deleted** — they are historical record.
- Every merge to `main` requires human approval.
- Read [`AGENTS.md`](AGENTS.md) before contributing (human or AI).

## Getting Started

**Prerequisites**: Docker Desktop (with `docker compose`), Git. For local dev
outside containers (optional): Python 3.12 + [`uv`](https://docs.astral.sh/uv/),
Node 20 + [`pnpm`](https://pnpm.io/) 9.

```bash
git clone https://github.com/BATMAN-009/F2F.git
cd F2F
cp .env.example .env              # safe local defaults; edit TRIPO_API_KEY later
docker compose up -d --build      # start db · redis · minio · api · worker · web
docker compose exec api alembic upgrade head   # no-op baseline today; lands real migrations in Feature 02
```

Service URLs (once healthy):

| Service | URL | Notes |
|---|---|---|
| Web | http://localhost:3000 | Landing page + `HealthBadge` calling `/healthz` |
| API | http://localhost:8000 | FastAPI; Swagger at `/docs` |
| API health | http://localhost:8000/healthz | Reports `db`/`redis` status |
| MinIO console | http://localhost:9001 | Login `f2fminio` / `f2fminio-secret`; bucket `f2f-assets` is auto-created |

Smoke-test the async worker path:

```bash
curl http://localhost:8000/tasks/ping         # returns {"task_id": "..."}
curl http://localhost:8000/tasks/ping/<id>    # poll until "status":"SUCCESS"
# result looks like "pong | Blender 4.x ..."
```

Convenience wrappers (`infra/scripts/dev.ps1` on Windows, `infra/scripts/dev.sh`
on macOS/Linux):

```bash
./infra/scripts/dev.sh up        # docker compose up -d --build
./infra/scripts/dev.sh logs api  # tail one service
./infra/scripts/dev.sh migrate   # alembic upgrade head
./infra/scripts/dev.sh shell     # bash inside the api container
./infra/scripts/dev.sh down
```

## Development Workflow

All three services can also run and be tested outside Docker.

### Web (`web/`)

```bash
cd web
pnpm install
pnpm dev            # http://localhost:3000
pnpm lint           # next lint
pnpm format:check   # prettier --check .
pnpm test           # vitest run
pnpm build          # production build (smoke)
```

### API (`api/`)

```bash
cd api
uv sync
uv run uvicorn app.main:app --reload       # http://localhost:8000
uv run ruff check . && uv run ruff format --check .
uv run pytest
```

### Worker (`worker/`)

```bash
cd worker
uv sync
uv run celery -A worker.celery_app worker -l INFO
uv run ruff check . && uv run ruff format --check .
uv run pytest       # runs the ping task in eager mode; Blender not required on host
```

### CI

GitHub Actions runs 6 jobs (`lint-web`, `test-web`, `lint-api`, `test-api`,
`lint-worker`, `test-worker`) on every push to `feature/**` / `hotfix/**` and on
PRs targeting `main`. Workflow: [`.github/workflows/ci.yml`](.github/workflows/ci.yml).
CI is **advisory** — branch protection is intentionally off for v1.0 so emergency
merges are never blocked.

## Troubleshooting

- **Bucket not found right after `docker compose up`** — the `createbuckets` sidecar
  waits for MinIO's healthcheck, then creates `f2f-assets`. Give it ~5 s on first
  boot. `docker compose logs createbuckets` shows its one-shot output.
- **Worker image is large (~1.5 GB)** — expected. The image ships the full apt
  Blender + xvfb + libgl1 runtime so Features 08–11 can texture, remesh, and export
  without a second build. Subsequent builds are fast thanks to Docker layer caching.
- **First `pnpm install` inside the web container is slow** — Next.js pulls a
  platform-specific `@next/swc` binary the first time. Cached thereafter.
- **Port already in use** — F2F binds `3000`, `5432`, `6379`, `8000`, `9000`, `9001`.
  Free the port or stop any other `docker compose` stack using it.
- **`/healthz` shows `db: down` or `redis: down`** — the dependency isn't healthy
  yet. `docker compose ps` shows container health; `docker compose logs db` /
  `logs redis` for details.

## License

TBD.

## Maintainer

[BATMAN-009](https://github.com/BATMAN-009)
