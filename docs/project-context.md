# 🎯 Project Context

> **Project**: F2F (working title)
> **Version**: Pre-release (v1.0 in planning)
> **Last Updated**: 2026-04-23

---

## What Is This Project?

F2F is an "idea → physical product" platform delivered as a web-based engine. It
takes a user's input (one or more reference photos, optionally with a prompt),
generates a 3D mesh via an AI provider (Tripo 3D), lets the user texture it, scale
it to real-world dimensions, preview it in AR, export it to standard 3D formats
(STL / USD / FBX / OBJ / 3MF), and hand it off to Blender for further refinement.

The platform is structured as **four capability pillars** released in stages:

1. **The Engine** (v1.0 — Internal Demo / MVP) — the core image/multi-view → 3D →
   texture → dimension → AR + export pipeline.
2. **Match-to-Market** (v1.1) — visual similarity search; if the generated product
   already exists in the market with ≥95% similarity, redirect the user to the
   e-commerce listing.
3. **Manufacturer Discovery & Outreach** (v1.2) — LLM-driven manufacturer finder
   plus automated sample/quote/payment outreach.
4. **Vertical Applications** (v1.3+) — film/TV prop previsualization first; then
   architecture and interior miniatures.

This document describes the project as it is being built **right now** (v1.0). The
post-MVP pillars are tracked in `project-roadmap.md`.

## Project Type

| Property | Value |
|---|---|
| **Type** | Web application + AI/3D pipeline service + Blender add-on |
| **Platform** | Web (desktop browsers); AR on iOS + Android via `<model-viewer>` |
| **Distribution (v1.0)** | Self-hosted via local docker-compose (internal demo) |
| **Distribution (v1.1+)** | SaaS (web on Vercel; api/worker on Fly.io or Railway) |

## Tech Stack

| Layer | Technology | Why |
|---|---|---|
| **Web language** | TypeScript | Type safety + ecosystem for React/3D |
| **Web framework** | Next.js 14 (App Router) | Mature React, SSR, easy deploy story |
| **3D in browser** | Three.js via React Three Fiber + drei | Declarative R3F; best-in-class for mesh + texture editors |
| **AR viewer** | Google `<model-viewer>` (USDZ on iOS, glTF on Android) | One tag ships AR on both mobile platforms |
| **API language** | Python 3.12 | Lingua franca of AI/3D tooling (Tripo SDK, trimesh, pygltflib, bpy) |
| **API framework** | FastAPI | Fast, typed, async; auto OpenAPI docs |
| **AI 3D provider** | Tripo 3D (behind a `Provider` abstraction) | User-supplied; abstracted to swap later |
| **Format conversion** | Blender headless (`bpy` / CLI) | Single tool handles STL / USD / FBX / OBJ / 3MF / glTF reliably |
| **Job queue** | Celery + Redis | Long-running 3D + Blender jobs need a real queue with retries |
| **Database** | PostgreSQL 16 | Relational metadata (projects, assets, jobs) |
| **ORM (Python)** | SQLAlchemy 2 + Alembic | Standard Python ORM with migrations |
| **DB client (TS)** | Drizzle (read-only views — optional) | If web ever needs direct DB access |
| **Object storage** | MinIO (local v1.0) → Cloudflare R2 (v1.1+) | S3-compatible; dev parity with future cloud |
| **Auth (v1.0)** | None — single local user | Internal demo simplification |
| **Auth (v1.1+)** | Clerk | Social login, MFA, orgs without writing them |
| **Testing (Python)** | pytest + pytest-asyncio | Standard |
| **Testing (TS)** | Vitest (unit) + Playwright (e2e) | Standard |
| **Lint / format (TS)** | ESLint (next/core-web-vitals + @typescript-eslint) + Prettier | Standard |
| **Lint / format (Python)** | Ruff (lint + format) | Replaces flake8 + isort + Black; fast |
| **Package mgr (TS)** | pnpm | Fast, disk-efficient |
| **Package mgr (Python)** | uv | Fastest modern resolver/installer |
| **Container runtime** | Docker + docker-compose | v1.0 deployment target |
| **CI** | GitHub Actions | Lint + test on PR; aligned with Mastery feature-branch flow |
| **Observability (v1.1+)** | Sentry (errors) + Grafana Cloud (metrics/logs) | Deferred from v1.0 |

## Architecture Overview

### Pattern

**Modular monolith with a separated AI pipeline service**, connected by a job queue.

- The web app (Next.js) handles UI, the in-browser 3D viewer, the AR viewer, file
  uploads/downloads, and a thin API facade that proxies to the pipeline service.
- The pipeline service (FastAPI) owns all business logic: provider abstraction,
  job orchestration, asset management, and the database.
- Celery workers run the long-running pieces: Tripo API calls, Blender format
  conversion, texture application.
- The Blender add-on talks directly to the pipeline service to pull assets into a
  user's local Blender.

### Project Structure

```
F2F/
├── AGENTS.md                       # AI agent orientation (project root)
├── README.md                       # Human-facing project overview
├── docker-compose.yml              # v1.0 local-only deployment
├── .gitignore
├── .editorconfig
│
├── web/                            # Next.js 14 + TS + R3F + model-viewer
│   ├── app/                        # App-router routes (the "multiple UI surfaces")
│   ├── components/                 # UI + 3D viewer + AR viewer
│   ├── lib/                        # API client, utilities
│   ├── public/
│   ├── package.json
│   └── tsconfig.json
│
├── api/                            # FastAPI — pipeline orchestration
│   ├── app/
│   │   ├── routes/                 # Public/engine REST routes
│   │   ├── providers/              # Tripo + future AI providers
│   │   ├── pipeline/               # Mesh, texture, dimension, export steps
│   │   ├── models/                 # SQLAlchemy models
│   │   ├── schemas/                # Pydantic schemas
│   │   └── main.py
│   ├── alembic/                    # Migrations
│   ├── tests/
│   └── pyproject.toml
│
├── worker/                         # Celery + Blender headless
│   ├── tasks/                      # convert, texture, package
│   ├── blender_scripts/            # Standalone .py scripts run by `blender -b -P`
│   └── pyproject.toml
│
├── addons/
│   ├── blender/                    # Blender add-on to pull assets from api/
│   │   └── f2f_addon/
│   └── maya/                       # (v1.1)
│
├── infra/
│   ├── docker/                     # Dockerfiles for api / worker / web
│   └── scripts/                    # Dev helpers
│
└── docs/                           # Mastery documentation
    ├── mastery.md                  # READ-ONLY framework reference
    ├── mastery-compact.md          # Compact framework (loaded by AI agents)
    ├── project-discussion.md
    ├── project-context.md          # this file
    ├── project-roadmap.md
    ├── project-changelog.md
    ├── features/                   # Per-feature folders
    └── references/                 # ADRs, specs, guides
```

### Key Architectural Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Split web from AI pipeline | Two services connected by a job queue | Web stays light + edge-friendly; pipeline runs long jobs on heavier hosts |
| AI provider abstraction | `Provider` interface; Tripo as first impl | Enables swapping/adding providers without changing pipeline |
| Blender as universal converter | Yes (headless, called from worker) | Single dependency covers every export format |
| AR via `<model-viewer>` | Yes | One tag ships USDZ on iOS + glTF on Android |
| Multiple "engine routes" | UI surfaces + REST API + multiple input modes | Matches the "multiple routes" requirement |
| v1.0 deployment | Local docker-compose only | Internal-demo scope |
| v1.0 storage | MinIO (S3-compatible) | Dev parity with future R2/S3 |
| v1.0 auth | None (single local user) | Internal-demo simplification |

## Conventions & Standards

### Code Style

| Convention | Standard |
|---|---|
| **TS formatting** | Prettier (default + project `.prettierrc`) |
| **TS linting** | ESLint (`next/core-web-vitals` + `@typescript-eslint`) |
| **Python formatting** | Ruff format |
| **Python linting** | Ruff (selects E, F, I, B, UP, ASYNC, S; line length 100) |
| **TS naming** | `camelCase` vars/funcs, `PascalCase` components/types |
| **Python naming** | `snake_case` funcs/vars, `PascalCase` classes |
| **TS file naming** | `kebab-case.ts` for modules, `PascalCase.tsx` for React components |
| **Python file naming** | `snake_case.py` |
| **Docs file naming** | `kebab-case.md` |
| **Markdown style** | ATX headings (`#`), fenced code blocks (triple backtick) |

### Git Conventions

- Branching: `feature/XX-feature-name` from `main` — see `docs/mastery.md`.
- Hotfixes: `hotfix/short-description` from `main`.
- Commits: `type(scope): short description` — see `docs/mastery.md`.
- Branches are **never deleted** (Mastery rule).
- Every merge to `main` requires human approval.

### Environment Setup (v1.0)

```bash
# Prerequisites: Docker Desktop, Node 20+, pnpm, Python 3.12, uv

# 1. Clone
git clone https://github.com/BATMAN-009/F2F.git
cd F2F

# 2. Install web deps
cd web && pnpm install && cd ..

# 3. Install api + worker deps
cd api && uv sync && cd ..
cd worker && uv sync && cd ..

# 4. Bring up local stack
docker compose up -d

# 5. Run migrations
docker compose exec api alembic upgrade head

# 6. Open the app
# Web:    http://localhost:3000
# API:    http://localhost:8000  (Swagger at /docs)
# MinIO:  http://localhost:9001  (console)
```

> Concrete commands above are the **target** for after Feature 01 ships. They are
> documented here so the architecture is clear; Feature 01 will make them real.

### Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `DATABASE_URL` | Yes | `postgresql+psycopg://f2f:f2f@db:5432/f2f` | PostgreSQL DSN for api + worker |
| `REDIS_URL` | Yes | `redis://redis:6379/0` | Celery broker + result backend |
| `S3_ENDPOINT` | Yes | `http://minio:9000` | MinIO endpoint (S3 API) |
| `S3_BUCKET` | Yes | `f2f-assets` | Bucket for meshes + textures + exports |
| `S3_ACCESS_KEY` | Yes | `f2fminio` | MinIO access key |
| `S3_SECRET_KEY` | Yes | `f2fminio-secret` | MinIO secret key |
| `TRIPO_API_KEY` | Yes | — | Tripo 3D API key (user-supplied) |
| `TRIPO_API_BASE` | No | `https://api.tripo3d.ai` | Override for testing |
| `NEXT_PUBLIC_API_BASE` | Yes | `http://localhost:8000` | API base URL for the web app |

## Scope & Constraints

### In Scope (v1.0 — Internal Demo)

- Pillar 1 (The Engine) — see `project-discussion.md` for the full feature list
- Local docker-compose deployment only
- Single local user (no auth)
- Blender add-on (no Maya)
- Photo + multi-view + prompt inputs (no sketch)

### Out of Scope (v1.0)

- Pillars 2, 3, 4 (match-to-market, manufacturer discovery, vertical apps)
- Cloud deployment (Vercel / Fly.io / R2)
- Auth (Clerk)
- Maya add-on
- Sketch input
- Direct robotic-printer job submission
- Payments / checkout
- Team/org accounts
- In-browser mesh editing
- Physics / structural simulation
- Proprietary 3D generation model

### Known Constraints

- External dependency on Tripo 3D API (cost, rate limits, uptime) — must be designed
  around with retries, caching of generation results, and clear error UX.
- Blender headless adds significant container size (~500 MB+) — accepted trade-off
  for universal format support.
- USDZ export fidelity from Blender is historically imperfect — to be verified
  during the AR feature.

## Team & Roles

| Role | Who | Responsibilities |
|---|---|---|
| **Lead / Owner** | BATMAN-009 (udaykiran) | Final decisions, merge approval |
| **AI Agent** | GitHub Copilot (and any tool reading `AGENTS.md`) | Implementation within Mastery framework |
| **Contributors** | None yet | — |
