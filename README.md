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

> The commands below are the **target** environment. They become real once Feature 01
> (project-foundation) ships.

```bash
git clone https://github.com/BATMAN-009/F2F.git
cd F2F
docker compose up -d           # start PostgreSQL, Redis, MinIO, api, worker, web
# Web:    http://localhost:3000
# API:    http://localhost:8000  (Swagger at /docs)
# MinIO:  http://localhost:9001
```

## License

TBD.

## Maintainer

[BATMAN-009](https://github.com/BATMAN-009)
