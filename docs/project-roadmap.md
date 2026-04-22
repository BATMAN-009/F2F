# 🗺️ Project Roadmap

> **Project**: F2F (working title)
> **Current Milestone**: v1.0 — Internal Demo (Pillar 1: The Engine)
> **Last Updated**: 2026-04-23

---

## Progress Overview

| Metric | Count |
|---|---|
| Total Features (v1.0) | 14 |
| 🟢 Complete | 0 |
| 🟡 In Progress | 0 |
| 🔴 Not Started | 14 |
| ⏸️ On Hold | 0 |

**Overall v1.0 Progress**: ░░░░░░░░░░ 0%

---

## v1.0 Feature List — Pillar 1: The Engine (Internal Demo, local docker-compose)

| # | Feature | Status | Depends On | Branch | Notes |
|---|---|---|---|---|---|
| 01 | Project foundation | 🔴 Not Started | — | — | Monorepo, docker-compose (PG + Redis + MinIO + api + worker + web), lint/format, CI |
| 02 | Core data model + FastAPI skeleton | 🔴 Not Started | #01 | — | `projects`, `assets`, `jobs` tables; SQLAlchemy + Alembic; health route |
| 03 | Next.js web app skeleton | 🔴 Not Started | #01 | — | App Router, layout, API client, R3F provider |
| 04 | Job queue infrastructure | 🔴 Not Started | #02 | — | Celery + Redis wiring, retry policy, dead-letter, example task |
| 05 | Tripo provider — single image → 3D | 🔴 Not Started | #02, #04 | — | `Provider` abstraction + Tripo adapter + single-image job |
| 06 | Multi-view input pipeline | 🔴 Not Started | #05 | — | R/L/T/B + reference + prompt → Tripo |
| 07 | In-browser 3D preview | 🔴 Not Started | #03, #05 | — | R3F viewer for generated meshes |
| 08 | Custom texture upload & apply | 🔴 Not Started | #07 | — | Texture + resolution controls; Blender worker applies |
| 09 | Real-world dimensions (H×W×D) | 🔴 Not Started | #07 | — | Scale + validate meshes |
| 10 | Multi-format export (Blender worker) | 🔴 Not Started | #04, #09 | — | STL / USD / FBX / OBJ / 3MF / glTF |
| 11 | AR viewer | 🔴 Not Started | #10 | — | `<model-viewer>` with USDZ (iOS) + glTF (Android) |
| 12 | Blender add-on | 🔴 Not Started | #10 | — | Pull assets directly into Blender |
| 13 | Public engine API routes | 🔴 Not Started | #05–#10 | — | Documented REST surface for partners |
| 14 | Project / asset history UI | 🔴 Not Started | #03, #05 | — | List, filter, re-open past projects |

---

## Dependency Map

```
01 [Project foundation]
 ├── 02 [Data model + FastAPI]
 │    ├── 04 [Job queue]
 │    │    └── 05 [Tripo single-image]
 │    │         ├── 06 [Multi-view]
 │    │         ├── 07 [Browser 3D preview] ── 08 [Texture]
 │    │         │                          └── 09 [Dimensions]
 │    │         │                                └── 10 [Export]
 │    │         │                                     ├── 11 [AR viewer]
 │    │         │                                     └── 12 [Blender add-on]
 │    │         └── 13 [Public engine API]
 │    │              (uses 05 + 06 + 08 + 09 + 10)
 │    └── 14 [History UI]
 │         (uses 03 + 05)
 └── 03 [Next.js skeleton]
      └── (feeds 07, 11, 14)
```

---

## Milestones

### v1.0 — Internal Demo (Pillar 1: The Engine)

**Target**: When features 01–14 are merged
**Features Included**: #01–#14

| Criterion | Status |
|---|---|
| All v1.0 features merged | ⬜ |
| All test plans passing | ⬜ |
| Documentation complete | ⬜ |
| Local docker-compose `up` runs cleanly | ⬜ |
| End-to-end demo: photo → mesh → texture → dimension → export → AR | ⬜ |

### v1.1 — Cloud + Auth + Pillar 2 (Match-to-Market)

Cloud deployment (Vercel + Fly.io + R2), Clerk auth, Maya add-on, visual similarity
search → "buy instead of make" suggestions. Detailed roadmap defined after v1.0 ships.

### v1.2 — Pillar 3 (Manufacturer Discovery + Outreach + Payments)

LLM-driven manufacturer finder, automated outreach, sample/quote/payment flow
(Stripe). Detailed roadmap defined after v1.1 ships.

### v1.3+ — Pillar 4 (Vertical Apps)

First vertical: **Film / TV prop previsualization** (with on-set mobile axial 3D
printer / CNC integration). Then: architecture & interior miniatures.

---

## Backlog

> Captured ideas not yet scheduled into a milestone.

| Feature Idea | Priority | Notes |
|---|---|---|
| Sketch input mode | Medium | Deferred from v1.0; useful UX for designers |
| Mesh editing in-browser (sculpt, boolean) | Low | DCC hand-off may make this unnecessary |
| Team / org accounts | Medium | Needs Clerk first (v1.1+) |
| Direct robotic-printer job submission | High (post-MVP) | Closes the loop to F2F's printing service |
| Self-hosted 3D generation model | Low | Only if Tripo cost / quality becomes a blocker |
| Observability (Sentry + Grafana Cloud) | Medium | Needed when leaving local-only |
| GitHub Actions CI | Medium | Add as part of Feature 01 if scope allows; otherwise its own feature |

---

## Change Log

> Track changes to the roadmap itself (not features).

| Date | Change | Reason |
|---|---|---|
| 2026-04-23 | Roadmap created with 14 v1.0 features | Project initialization |
