# 💬 Project Discussion

> **Project**: F2F (working title)
> **Status**: 🟢 COMPLETE
> **Date Started**: 2026-04-23
> **Date Completed**: 2026-04-23

---

## What Are We Building?

**F2F is an "idea-to-physical-product" platform.** A user arrives with an idea — a
mental image or a handful of reference photos — and F2F carries it all the way to a
physical object in their hands, with AR preview along the way.

The platform has **four capability pillars**, staged over releases:

1. **The Engine (v1.0 — Internal Demo / MVP)**
   Image or multi-view (R/L/T/B + reference) + optional prompt → AI-generated 3D mesh
   (via Tripo 3D) → custom texturing at configurable resolution → real-world
   dimensions (H × W × D) → multi-format export (STL / USD / FBX / OBJ / 3MF) → AR
   preview on mobile → direct hand-off to Blender.

2. **Match-to-Market (v1.1)**
   After the 3D file is finalized, F2F runs a visual similarity search (Google
   Lens-style). If the product already exists in the market with **≥95% similarity**,
   F2F surfaces it as a **"buy instead of make"** suggestion with a deep-link to the
   e-commerce listing — saving the user time and manufacturing cost.

3. **Manufacturer Discovery & Outreach (v1.2)**
   If no close market match exists, F2F uses an LLM-driven discovery layer to
   identify the **right manufacturer** for that product class/material, automatically
   reaches out with the spec + 3D file, and collects **sample offers, quotes, and
   payment** — closing the loop from idea to order.

4. **Vertical Applications (v1.3+)**
   Specialized surfaces on top of the core engine. **First vertical = Film/TV prop
   previsualization** (art directors previsualize props, iterate with the director,
   approve, and print on-set via mobile axial 3D printers or CNC). Architecture and
   interior miniatures follow.

The platform is delivered as a **web-based engine with multiple routes** — meaning
**all of**: multiple UI surfaces, multiple API endpoints, and multiple input modes.

## Why Does This Project Exist?

- **3D content creation is slow and expert-only.** Designers, architects, end
  customers, and art departments cannot iterate on physical objects at the speed
  their imagination moves.
- **Existing AI 3D tools stop at the mesh.** Tripo, Meshy, Rodin and similar produce
  raw geometry and quit. They do not close the loop to texturing, real-world
  dimensions, AR preview, DCC integration, *or* manufacturing.
- **Manufacturing discovery is broken.** Finding the right factory/workshop for a
  bespoke object today means weeks of cold emails. An LLM + directory-driven outreach
  flow can compress that to hours.
- **Some ideas don't need manufacturing at all** — they already exist on the market.
  A visual-match layer turns "I want this made" into "here's where to buy it," which
  is faster and cheaper for the user and builds trust in the platform.
- **F2F already operates the physical layer** — a robotic 3D printing service for
  large-format, sustainable furniture and architectural products. The software engine
  turns that capability into a self-serve funnel: *idea → AR-verified model →
  print-ready file → F2F printing service*.
- **Wrapping existing AI (instead of training a proprietary model)** lets us ship
  quickly. Differentiation lives in the pipeline, texturing, AR, match-to-market,
  manufacturer discovery, and vertical UX — not in the base model.

## Target Users / Consumers

| User Type | Description | Primary Need |
|---|---|---|
| Designer / Architect | Professional creating custom furniture or architectural pieces | Fast iteration from concept image to dimensioned 3D model they can refine in Blender/Maya |
| End Customer | Buyer commissioning a custom piece | Preview the product in AR in their own space before ordering |
| Internal Manufacturing | F2F's own robotic printing team | Clean, print-ready files (STL/3MF) at correct real-world dimensions |
| Developer / Partner | Third-party integrating F2F into their own tooling | API access to the pipeline (route-based engine) |

## Core Use Cases

- **Image-to-3D**: Upload one image (+ optional prompt) → generate 3D wireframe → texture → export.
- **Multi-view-to-3D**: Upload right / left / top / bottom + reference images (+ prompt) → higher-fidelity 3D model.
- **Custom texturing**: Apply user-supplied textures at a chosen resolution to the generated mesh.
- **Dimension the model**: Specify real-world H × W × D so exports are print-ready.
- **Multi-format export**: Download as STL, USD, FBX, OBJ, or 3MF.
- **DCC hand-off**: Open the generated asset directly in Blender or Maya.
- **AR preview**: View the finalized, dimensioned model in AR on mobile (iOS/Android).

## Tech Stack Discussion

> ✅ **Approved** by the user on 2026-04-23, with v1.0 adjustments noted in the
> "Decisions Log" (no Clerk, no cloud, no Maya for v1.0).

| Layer | Options Considered | Chosen | Rationale |
|---|---|---|---|
| **Frontend framework** | Next.js (React+TS), SvelteKit, Nuxt | **Next.js 14 + TypeScript** | Mature React ecosystem for 3D (R3F), best-in-class deployment story, strong SSR for SEO/marketing surfaces |
| **3D rendering (web)** | Three.js, Babylon.js, PlayCanvas | **Three.js via React Three Fiber (R3F) + drei** | Declarative React API for 3D, huge community, proven for mesh + texture editors |
| **AR viewer** | `<model-viewer>`, WebXR, native SDKs | **Google `<model-viewer>`** (with WebXR fallback) | Ships AR on iOS (Quick Look / USDZ) and Android (Scene Viewer / glTF) with one tag — matches our need without writing native apps |
| **Backend (API / orchestration)** | Next.js API routes, FastAPI (Python), Go | **FastAPI (Python)** for the AI/3D pipeline; Next.js API routes for product/web concerns | Python is the lingua franca of AI/3D tooling (Tripo SDK, Blender bpy, trimesh, pygltflib); FastAPI is fast and typed |
| **AI 3D generation** | Tripo 3D, Meshy, Rodin, Stability 3D | **Tripo 3D (primary)**, pluggable provider interface | User explicitly requested Tripo; abstract behind a provider to swap later |
| **Format conversion** | Assimp, trimesh, pygltflib, **Blender headless (bpy)** | **Blender headless** as the universal converter (STL / USD / FBX / OBJ / 3MF / glTF) | Blender supports every target format reliably; runs as a worker |
| **DCC hand-off** | Custom Blender add-on, MCP server, file download + deep link | **Blender add-on + file download** for v1; Maya add-on later | Open-the-asset UX is best served by a native add-on pulling from our API |
| **Job queue / workers** | Celery+Redis, RQ, BullMQ, Temporal | **Celery + Redis** | 3D generation + Blender conversion are long-running; needs a real queue with retries |
| **Object storage** | S3, Cloudflare R2, Supabase Storage | **Cloudflare R2** | S3-compatible, no egress fees (critical for AR/3D downloads), cheap for large meshes |
| **Database** | PostgreSQL, MySQL, SQLite | **PostgreSQL** | Relational project/asset/job metadata; well-supported everywhere |
| **ORM / data** | Prisma, Drizzle, SQLAlchemy | **SQLAlchemy + Alembic** (Python side); **Drizzle** (TS side) — single DB, two typed clients | Matches the split stack |
| **Auth** | NextAuth, Clerk, Supabase Auth, custom | **Clerk** | Handles social login, MFA, org accounts out of the box — removes weeks of work |
| **Testing** | pytest, Jest, Vitest, Playwright | **pytest** (Python), **Vitest + Playwright** (TS) | Standard choices for each side |
| **Build / tooling** | pnpm, npm, yarn / uv, poetry, pip | **pnpm** (TS); **uv** (Python) | Fastest and most modern package managers on each side |
| **Deployment** | Vercel, Railway, Fly.io, AWS, GCP | **Vercel** (web) + **Fly.io or Railway** (FastAPI + workers) + **R2** (storage) | Web is edge-friendly; AI pipeline needs long-lived containers with GPU-adjacent networking |
| **Observability** | Sentry, Datadog, Grafana Cloud | **Sentry** (errors) + **Grafana Cloud** (metrics/logs) | Standard, free tiers sufficient for v1 |

## Architecture Discussion

### Proposed Pattern

**Modular monolith with a separate AI pipeline service**, connected by a job queue.

- `web/` — Next.js app. UI, auth, product routes, API facade, AR viewer.
- `api/` — FastAPI service. Pipeline orchestration, provider abstraction (Tripo),
  Blender worker dispatch, file/asset management.
- `worker/` — Celery workers. Run Blender headless for conversion/texturing.
- `addons/` — Blender (and later Maya) add-ons that talk to `api/`.
- `infra/` — IaC, deployment config.

Web submits a job → `api/` creates a job record → enqueues to workers → workers call
Tripo, run Blender, write results to R2 → web polls/subscribes for completion → UI
renders preview + AR + download buttons.

### Key Architectural Decisions (Proposed)

| Decision | Choice | Why |
|---|---|---|
| Split web and AI pipeline | Yes — two services | Lets web deploy on edge/Vercel while AI pipeline runs on GPU-adjacent long-lived hosts |
| AI provider abstraction | Yes — `Provider` interface | Tripo today, others tomorrow, without changing the pipeline |
| Blender as universal converter | Yes | Single dependency covers STL/USD/FBX/OBJ/3MF/glTF |
| AR via `<model-viewer>` | Yes | iOS USDZ + Android glTF from one viewer |
| Multi-route engine | Yes — RESTful + web routes built on same `api/` | User explicitly wants multiple routes into the engine |

## Project Structure Discussion

```
F2F/
├── web/                          # Next.js 14 + TS + R3F + model-viewer
│   ├── app/                      # App-router routes (the "multiple routes" surface)
│   ├── components/               # UI + 3D viewer + AR viewer
│   └── lib/                      # API client, auth, utilities
├── api/                          # FastAPI — pipeline orchestration
│   ├── app/
│   │   ├── routes/               # Public/engine routes (multiple entry routes)
│   │   ├── providers/            # Tripo + future AI providers
│   │   ├── pipeline/             # Mesh, texture, dimension, export steps
│   │   └── models/               # SQLAlchemy models
│   └── alembic/
├── worker/                       # Celery + Blender headless
│   └── tasks/                    # convert, texture, package
├── addons/
│   ├── blender/                  # Blender add-on to pull assets from api/
│   └── maya/                     # (later)
├── infra/                        # Deployment, IaC, docker-compose for dev
├── docs/                         # Mastery documentation
└── README.md
```

## Scope & Boundaries

### In Scope (v1.0 / MVP — Pillar 1: The Engine, Internal Demo, Local Only)

- Single-image → 3D via Tripo 3D
- Multi-view (R/L/T/B + reference) + prompt → 3D via Tripo 3D
- Mesh preview in browser (R3F)
- Custom texture upload + apply, with configurable resolution
- Custom real-world dimensions (H × W × D)
- Export: STL, USD, FBX, OBJ, 3MF (via Blender-headless worker)
- Blender add-on to open the asset directly
- AR preview on iOS + Android (`<model-viewer>`)
- Project / asset history UI (single local user — no auth)
- At least one "engine route" exposed as a documented REST API for programmatic use
- Local docker-compose deployment (PostgreSQL + Redis + MinIO + worker + api + web)

### Out of Scope (v1.0 / MVP) — Confirmed

- **Auth (Clerk)** — single local user for v1.0; Clerk in v1.1
- **Sketch input** — photos + multi-view + prompt only for v1.0
- **Cloud deployment** — local-only docker-compose for the demo
- **Maya add-on** — Blender only in v1.0; Maya in v1.1
- **Pillar 2 (Match-to-Market)** — v1.1
- **Pillar 3 (Manufacturer discovery + outreach + payments)** — v1.2
- **Pillar 4 (Film/TV prop vertical, architecture/interior miniatures)** — v1.3+
- Direct robotic-printer job submission (MVP ends at print-ready file export)
- Team/org accounts
- In-browser mesh editing (use DCC hand-off instead)
- Physics/structural simulation for architectural pieces
- Proprietary / self-hosted 3D generation model

### Known Constraints

- None stated by the user.
- Implicit: external dependency on Tripo 3D API (cost, rate limits, uptime) — must be
  designed around.

## Feature Brainstorm

> Ordering into sequence numbers happens in `project-roadmap.md` after this discussion
> is COMPLETE.

| Feature Idea | Priority | Notes / Dependencies |
|---|---|---|
| Project foundation (monorepo, lint, CI, docker-compose) | 🔴 Must Have | Feature 01 |
| Core data model + **Design Ledger** | 🔴 Must Have | Feature 02 — foundation for all later features and Pillars 2/3/4 |
| Auth + user accounts (Clerk) | 🟡 Should Have | Deferred to v1.1 per MVP scope |
| Tripo 3D provider integration (single image) | 🔴 Must Have | Wraps the external AI |
| Multi-view input → Tripo | 🔴 Must Have | Extension of single-image |
| In-browser 3D preview (R3F) | 🔴 Must Have | Needed before texture/dimension UX |
| Custom texturing + resolution controls | 🔴 Must Have | Differentiator |
| Real-world dimensions (H×W×D) | 🔴 Must Have | Print-ready requirement |
| Multi-format export pipeline (Blender worker) | 🔴 Must Have | STL/USD/FBX/OBJ/3MF + auto-remesh/watertight |
| **Manufacturability Analysis** | 🔴 Must Have | Feature 11 — the F2F moment |
| AR viewer (`<model-viewer>`) | 🔴 Must Have | Core value prop |
| Blender add-on | 🔴 Must Have | DCC hand-off |
| Public engine API routes + **MCP server** | 🔴 Must Have | "Multiple routes" + AI-agent addressable |
| Job queue + worker infra (Celery + Redis) | 🔴 Must Have | Supports all pipeline features |
| Project/asset history UI + **ledger viewer** | 🔴 Must Have | Quality-of-life + provenance visibility |
| Parametric variants (scale/material/topology + hollow) | 🟡 Should Have | Target v1.1 — reframes UX |
| Iterative refinement (delta-edits via Blender) | 🟡 Should Have | Target v1.1 — saves provider spend |
| Decision Engine (unifies Pillars 2 + 3) | 🟡 Should Have | Target v1.2 — single post-export screen |
| Multi-provider racing (Tripo + Meshy + Hunyuan3D) | 🟢 Nice to Have | v1.1+ |
| Depth / LiDAR capture (iPhone via WebXR) | 🟡 Should Have | v1.1+ — beats photo input |
| Evaluation harness (golden-set regression) | 🟡 Should Have | v1.1 |
| OpenTelemetry + Jaeger | 🟡 Should Have | v1.1 |
| Version tree UI (Figma-style) | 🟡 Should Have | v1.1+ — feeds off Design Ledger |
| Live multiplayer R3F viewer | 🟡 Should Have | Critical for v1.3 vertical (film/TV) |
| QR passport on physical product → ledger | 🟢 Nice to Have | Closes the loop |
| Reprint / remix button | 🟢 Nice to Have | Drives repeat revenue |
| Maya add-on | 🟢 Nice to Have | v1.1 |
| Direct manufacturing submission | 🟢 Nice to Have | v1.1+ |
| Payments / checkout | 🟢 Nice to Have | Business layer — v1.2 with Pillar 3 |
| In-browser mesh editing | 🟢 Nice to Have | Or never — DCC covers it |

## Conventions & Standards Discussion

| Convention | Standard | Notes |
|---|---|---|
| **TS formatting** | Prettier | Default config |
| **TS linting** | ESLint (next/core-web-vitals + @typescript-eslint) | Strict |
| **Python formatting** | Ruff format | Replaces Black |
| **Python linting** | Ruff | Fast, replaces flake8 + isort |
| **Naming (TS)** | camelCase vars/funcs, PascalCase components/types | — |
| **Naming (Python)** | snake_case | — |
| **File naming** | kebab-case (TS), snake_case (Python) | — |
| **Git workflow** | Mastery branching strategy | See `docs/mastery.md` |
| **Commit messages** | Mastery convention | See `docs/mastery.md` |

## Research & Prior Art

### Knowledge Gaps

- [ ] Tripo 3D API contract details (rate limits, cost, auth model) — needed before pipeline design
- [ ] Minimum mesh quality Tripo produces from a single image vs multi-view — affects UX copy and expectations
- [ ] USDZ export fidelity from Blender (iOS AR) — historically imperfect
- [ ] Best practice for applying custom textures to AI-generated meshes (UV unwrap quality from Tripo)
- [ ] Blender add-on distribution (self-hosted `.zip` vs. extension platform)

### Sources Consulted

*To be filled during Research stage if gaps above remain blocking. Lightweight findings
stay here; if research becomes extensive, promote to `research.md` per framework.*

| Source | Type | Key Takeaway |
|---|---|---|
| — | — | — |

### Key Findings

- *(none yet — research not conducted)*

### Impact on Decisions

- *(none yet)*

## Open Questions — RESOLVED

- [x] **Q1 — Project name**: "F2F" is a **working title** (may change pre-launch).
- [x] **Q2 — Domain/brand**: Deferred — no brand assets to align with yet.
- [x] **Q3 — Tech stack approval**: ✅ Approved.
- [x] **Q4 — Hosting constraints**: v1.0 is **local-only** (docker-compose). Cloud target chosen at v1.1.
- [x] **Q5 — Tripo access**: User has Tripo API key.
- [x] **Q6 — "Multiple routes"**: **All of the above** — UI surfaces + API endpoints + input modes.
- [x] **Q7 — Single-user vs multi-user**: **Single user, no auth** for v1.0; Clerk added in v1.1.
- [x] **Q8 — Out-of-scope confirmation**: ✅ Confirmed (see In/Out of Scope above).
- [x] **Q9 — Quality bar for v1.0**: **Internal demo.**
- [x] **Q10 — Timeline**: No fixed deadline.

## Decisions Log

| Date | Decision | Rationale |
|---|---|---|
| 2026-04-23 | Project type = Web app | User confirmed in kickoff |
| 2026-04-23 | Stage-by-stage human approval | User chose "Ask me at each major stage" |
| 2026-04-23 | 4-pillar staged platform (Engine → Match-to-Market → Manufacturer Discovery → Verticals) | User vision; reduces v1.0 risk |
| 2026-04-23 | Stack approved (Next.js+TS / R3F / model-viewer / FastAPI / Celery+Redis / Blender-headless / PostgreSQL / Tripo) | User approval |
| 2026-04-23 | v1.0 = Pillar 1 only (Engine), local docker-compose, no cloud | Internal-demo scope |
| 2026-04-23 | v1.0 skips Clerk auth (single local user) | Internal demo doesn't need multi-user |
| 2026-04-23 | v1.0 input modes: photo + multi-view + prompt (no sketch) | User deferred sketch input |
| 2026-04-23 | v1.0 ships Blender add-on only (no Maya) | Maya deferred to v1.1 |
| 2026-04-23 | Local storage = MinIO (S3-compatible) | Dev parity with future cloud R2/S3 |
| 2026-04-23 | First vertical (v1.3+) = Film/TV prop previsualization | User priority |
| 2026-04-23 | Visual-search vendor for v1.1 = decide during v1.1 discussion | Defer to its own feature discussion |
| 2026-04-23 | **Design Ledger** (immutable provenance event log) added as v1.0 cross-cutting concern; folded into Feature 02 | Foundational data for Pillars 2/3/4; trivial now, impossible to retrofit; strategic moat — user-approved |
| 2026-04-23 | **Manufacturability Analysis** added as new v1.0 Feature 11 (between Export and AR) | Delivers sustainable-furniture positioning in-product; prevents print failures; the "F2F moment" — user-approved |
| 2026-04-23 | **MCP server** added as v1.0 interface; folded into Feature 14 (Public API) | Makes F2F callable by any AI agent (Claude/ChatGPT/Cursor); 2026 distribution leverage — user-approved |
| 2026-04-23 | **Decision Engine** (unifies Pillars 2 + 3 into one post-export screen) scheduled for v1.2 | Reframes separate features as one coherent UX |
| 2026-04-23 | **Parametric variants** and **Iterative refinement** scheduled for v1.1 | Reframes F2F from "generate" to "decide"; reduces provider API spend |

## Discussion Complete ✅

**Summary**: F2F is a 4-pillar "idea → physical product" platform. v1.0 ships **Pillar 1
(the Engine)** as a local internal demo: image / multi-view input → Tripo 3D mesh →
custom texture → real-world dimensions → multi-format export (STL/USD/FBX/OBJ/3MF) →
AR preview → Blender hand-off. Stack: Next.js + R3F + model-viewer (web), FastAPI +
Celery + Redis + Blender-headless (pipeline), PostgreSQL + MinIO (local docker), Tripo
3D behind a `Provider` abstraction. Pillars 2–4 (match-to-market, manufacturer
discovery + payments, vertical apps) are roadmapped for v1.1, v1.2, v1.3+.

**Completed**: 2026-04-23

**Next Steps**:
1. ✅ Create `project-context.md`
2. ✅ Create `AGENTS.md` at project root
3. ✅ Create `project-roadmap.md`
4. ✅ Create `project-changelog.md`
5. ✅ Create `mastery-compact.md`
6. ✅ Initialize git, push to remote
7. → Begin Feature 01 (project-foundation) lifecycle
