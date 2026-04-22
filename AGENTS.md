# AGENTS.md

F2F is an "idea → physical product" web platform. v1.0 (Internal Demo / MVP) ships
the core **Engine**: photo or multi-view input → AI-generated 3D mesh (via Tripo 3D)
→ custom texturing → real-world dimensions → multi-format export (STL/USD/FBX/OBJ/3MF)
→ AR preview on mobile → Blender add-on hand-off. Later releases add visual
match-to-market (v1.1), LLM-driven manufacturer discovery + payment outreach (v1.2),
and vertical apps starting with film/TV prop previsualization (v1.3+).

## Project Structure

```
F2F/
├── AGENTS.md                       # this file
├── README.md
├── docker-compose.yml              # v1.0 local-only deployment
│
├── web/                            # Next.js 14 + TS + R3F + <model-viewer>
├── api/                            # FastAPI — pipeline orchestration + DB
├── worker/                         # Celery + Blender headless
├── addons/
│   ├── blender/                    # Blender add-on (DCC hand-off)
│   └── maya/                       # (v1.1)
├── infra/                          # Dockerfiles, dev scripts
└── docs/                           # Mastery documentation
    ├── mastery.md                  # READ-ONLY framework reference
    ├── mastery-compact.md          # Compact framework (load this each session)
    ├── project-discussion.md
    ├── project-context.md
    ├── project-roadmap.md
    ├── project-changelog.md
    ├── features/
    └── references/
```

## Getting Started (for AI Agents)

Read docs in this exact order (matches the AI Agent Protocol in `docs/mastery.md`):

1. `docs/mastery-compact.md` — Framework rules (compact — all rules, no templates)
2. `docs/project-discussion.md` — Understand WHY F2F exists and key decisions
3. `docs/project-context.md` — Understand WHAT F2F is (formalized)
4. `docs/project-roadmap.md` — Understand WHERE the project stands
5. `docs/features/` (active) — Understand the current feature state

> Need a document template? Load it from the full `docs/mastery.md` — search for the
> specific template heading.

To find current work:
1. Check `docs/project-roadmap.md` for features marked 🟡 IN PROGRESS
2. Open that feature's folder: `discussion → architecture → tasks → changelog`
3. In `tasks.md`, find the last checked checkbox — that's where work stopped
4. In `changelog.md`, read the latest Session Note for context

## Key Rules

- **Docs before code** — discuss, design, and plan before building. Never skip stages.
- **Feature branches only** — all work happens on `feature/XX-name` branches, never on `main`.
- **Never delete branches** — kept forever as historical reference.
- **Human approval required** for: merging to main, modifying architecture after
  finalization, changing `project-context.md`, reordering the roadmap, adding
  dependencies.
- **AI agents CAN** autonomously: read docs, write code within active tasks, check off
  tasks, log changelog entries, create commits, push to feature branches.

See the full Autonomy Boundaries table in `docs/mastery.md` → AI Agent Protocol section.

## Conventions

**Branches**: `feature/XX-feature-name` from `main` (e.g., `feature/01-project-foundation`)

**Commits**: `type(scope): short description`
- Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `perf`, `hotfix`
- Scope: feature name or module (e.g., `engine`, `web`, `api`, `worker`, `addon`, `docs`)

**File naming**:
- `kebab-case.md` for docs
- `kebab-case.ts` modules / `PascalCase.tsx` React components in `web/`
- `snake_case.py` in `api/` and `worker/`

**Markdown style**: ATX headings (`#`), fenced code blocks (triple backtick).

## Stack at a Glance

- **Web**: Next.js 14 + TypeScript + React Three Fiber + `<model-viewer>`
- **API**: FastAPI (Python 3.12) + SQLAlchemy 2 + Alembic
- **Workers**: Celery + Redis, running Blender headless for format conversion
- **Database**: PostgreSQL 16
- **Storage**: MinIO (S3-compatible, local for v1.0)
- **AI Provider**: Tripo 3D (behind a `Provider` abstraction)
- **Auth**: None in v1.0 (single local user); Clerk in v1.1+
- **Lint/format**: Ruff (Python), ESLint + Prettier (TS)
- **Tests**: pytest (Python), Vitest + Playwright (TS)
- **Package mgrs**: uv (Python), pnpm (TS)
- **Deploy (v1.0)**: docker-compose, local only

## Full Protocol

The complete AI Agent Protocol — including context loading order, autonomy boundaries,
session handoff protocol, and communication style rules — is defined in:

**`docs/mastery.md` → Section: 🤖 AI Agent Protocol**
