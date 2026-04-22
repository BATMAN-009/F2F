# 🗺️ Project Roadmap

> **Project**: F2F (working title)
> **Current Milestone**: v1.0 — Internal Demo (Pillar 1: The Engine)
> **Last Updated**: 2026-04-23

---

## Progress Overview

| Metric | Count |
|---|---|
| Total Features (v1.0) | 15 |
| 🟢 Complete | 0 |
| 🟡 In Progress | 1 |
| 🔴 Not Started | 14 |
| ⏸️ On Hold | 0 |

**Overall v1.0 Progress**: ░░░░░░░░░░ 0%

---

## v1.0 Feature List — Pillar 1: The Engine (Internal Demo, local docker-compose)

| # | Feature | Status | Depends On | Branch | Notes |
|---|---|---|---|---|---|
| 01 | Project foundation | � In Progress | — | `feature/01-project-foundation` | Monorepo, docker-compose (PG + Redis + MinIO + api + worker + web), lint/format, CI |
| 02 | Core data model + FastAPI skeleton + **Design Ledger** | 🔴 Not Started | #01 | — | `projects`, `assets`, `jobs` tables; **immutable provenance / event-log tables** capturing inputs, provider+model+seed, prompts, iterations, dimension history, material history, print history; SQLAlchemy + Alembic; health route |
| 03 | Next.js web app skeleton | 🔴 Not Started | #01 | — | App Router, layout, API client, R3F provider |
| 04 | Job queue infrastructure | 🔴 Not Started | #02 | — | Celery + Redis wiring, retry policy, dead-letter, example task |
| 05 | Tripo provider — single image → 3D | 🔴 Not Started | #02, #04 | — | `Provider` abstraction + Tripo adapter + single-image job; **writes ledger events** |
| 06 | Multi-view input pipeline | 🔴 Not Started | #05 | — | R/L/T/B + reference + prompt → Tripo |
| 07 | In-browser 3D preview | 🔴 Not Started | #03, #05 | — | R3F viewer for generated meshes |
| 08 | Custom texture upload & apply | 🔴 Not Started | #07 | — | Texture + resolution controls; Blender worker applies; **logs to ledger** |
| 09 | Real-world dimensions (H×W×D) | 🔴 Not Started | #07 | — | Scale + validate meshes; **logs to ledger** |
| 10 | Multi-format export (Blender worker) | 🔴 Not Started | #04, #09 | — | STL / USD / FBX / OBJ / 3MF / glTF; auto-remesh + watertight repair |
| 11 | **Manufacturability Analysis** ⭐ | 🔴 Not Started | #10 | — | Watertight/manifold check · wall-thickness heatmap · overhang + support-volume · center-of-gravity/stability · material-volume-based cost & print-time (FDM/SLA/CNC) · sustainability score (volume + recyclability + CO₂e). **The F2F moment.** |
| 12 | AR viewer | 🔴 Not Started | #11 | — | `<model-viewer>` with USDZ (iOS) + glTF (Android); shareable AR link |
| 13 | Blender add-on | 🔴 Not Started | #10 | — | Pull assets directly into Blender; ledger metadata stays attached |
| 14 | Public engine API routes + **MCP server** | 🔴 Not Started | #05–#11 | — | Documented REST surface for partners **and an MCP server wrapper** so Claude/ChatGPT/Cursor can drive F2F as a tool |
| 15 | Project / asset history UI + **ledger viewer** | 🔴 Not Started | #02, #03, #05 | — | List, filter, re-open past projects; provenance timeline per asset |

---

## Dependency Map

```
01 [Project foundation]
 ├── 02 [Data model + FastAPI + Design Ledger]
 │    ├── 04 [Job queue]
 │    │    └── 05 [Tripo single-image]
 │    │         ├── 06 [Multi-view]
 │    │         ├── 07 [Browser 3D preview] ── 08 [Texture]
 │    │         │                          └── 09 [Dimensions]
 │    │         │                                └── 10 [Export]
 │    │         │                                     ├── 11 [Manufacturability Analysis]
 │    │         │                                     │    └── 12 [AR viewer]
 │    │         │                                     └── 13 [Blender add-on]
 │    │         └── 14 [Public API + MCP server]
 │    │              (uses 05 + 06 + 08 + 09 + 10 + 11)
 │    └── 15 [History UI + ledger viewer]
 │         (uses 02 + 03 + 05)
 └── 03 [Next.js skeleton]
      └── (feeds 07, 12, 15)
```

---

## Milestones

### v1.0 — Internal Demo (Pillar 1: The Engine)

**Target**: When features 01–15 are merged
**Features Included**: #01–#15

| Criterion | Status |
|---|---|
| All v1.0 features merged | ⬜ |
| All test plans passing | ⬜ |
| Documentation complete | ⬜ |
| Local docker-compose `up` runs cleanly | ⬜ |
| End-to-end demo: photo → mesh → texture → dimension → export → **manufacturability report** → AR | ⬜ |
| Design Ledger records every step of a demo run; viewable end-to-end in #15 | ⬜ |
| MCP server reachable from Claude / Cursor and can drive the pipeline | ⬜ |

### v1.1 — Cloud + Auth + Pillar 2 (Match-to-Market) + Strategic Upgrades

Cloud deployment (Vercel + Fly.io + R2), Clerk auth, Maya add-on, visual similarity
search → "buy instead of make" suggestions. Also folds in strategic upgrades from the
**Backlog**: parametric variants, iterative refinement (delta-edit instead of
regenerate), evaluation harness + OpenTelemetry promoted to required, multi-provider
racing. Detailed roadmap defined after v1.0 ships.

### v1.2 — Pillar 3 (Manufacturer Discovery + Outreach + Payments) + **Decision Engine**

LLM-driven manufacturer finder, automated outreach, sample/quote/payment flow
(Stripe). **Pillars 2 + 3 are unified behind the Decision Engine** — the single
post-export screen showing "Buy existing / Print with F2F / Local manufacturer / DIY"
with real price · lead time · CO₂e · action. Detailed roadmap defined after v1.1 ships.

### v1.3+ — Pillar 4 (Vertical Apps)

First vertical: **Film / TV prop previsualization** (with on-set mobile axial 3D
printer / CNC integration). Then: architecture & interior miniatures. Likely to
include the live multiplayer R3F viewer for director + art director review.

---

## Backlog

> Captured ideas not yet scheduled into a milestone. Grouped by theme.

### Strategic (reshape the product — target v1.1 / v1.2)

| Feature Idea | Priority | Target | Notes |
|---|---|---|---|
| **Decision Engine** (unifies Pillar 2 + Pillar 3 into one post-export screen) | High | v1.2 | Ranked options: Buy existing / Print with F2F / Local manufacturer / DIY — with price, lead time, CO₂e |
| **Parametric variants** (3 scales × 3 materials × 3 topologies + auto-hollowed) | High | v1.1 | Reframes F2F from "generate" to "decide" |
| **Iterative refinement** (delta-edits in Blender; only re-call Tripo when necessary) | High | v1.1 | Respect the user's previous choice; saves provider API spend |
| **Multi-provider racing** (Tripo + Meshy + Hunyuan3D in parallel; user picks winner) | Medium | v1.1+ | Ties into `Provider` abstraction from Feature 05 |

### Input modalities (target v1.1+)

| Feature Idea | Priority | Notes |
|---|---|---|
| Sketch input mode | Medium | Deferred from v1.0 |
| Depth / LiDAR capture (iPhone Pro via WebXR) | High | One phone scan beats 4 photos |
| Video / walk-around input | Medium | "Record a 10s clip orbiting the object" |
| Mood-board input | Medium | 3–5 inspiration images blended |
| Conversational input | Medium | Natural language → structured brief → generation |

### Quality / operability (target v1.1 — add soon after MVP)

| Feature Idea | Priority | Notes |
|---|---|---|
| **Evaluation harness** (golden set of ~20 reference inputs, run on every PR) | High | Detects regressions when providers or Blender pipelines change |
| **OpenTelemetry + Jaeger** in docker-compose | High | Cheap to add; painful to retrofit once pipeline is live |
| Observability (Sentry errors + Grafana Cloud metrics/logs) | Medium | Needed when leaving local-only |
| GitHub Actions CI | Medium | Add as part of Feature 01 if scope allows; otherwise its own feature |

### UX / collaboration (target v1.1+)

| Feature Idea | Priority | Notes |
|---|---|---|
| Version tree UI (branching history, Figma-style) | Medium | Extends Feature 15; feeds off the Design Ledger |
| Live multiplayer R3F viewer (presence + comment pins) | High for v1.3 vertical | Essential for film/TV prop review (director + art director) |
| QR passport printed on physical product → scans to the ledger | Medium | Owner can reprint, remix, resell |
| Reprint / remix button on past objects | Medium | Closes the loop; drives repeat revenue |

### Pillar 2/3 specifics (detailed when those features are discussed)

| Feature Idea | Priority | Notes |
|---|---|---|
| Automatic negotiation bot (collects 3 quotes, normalizes, recommends) | Medium | v1.2 |
| Team / org accounts | Medium | Needs Clerk first (v1.1+) |
| Direct robotic-printer job submission | High (post-MVP) | Closes the loop to F2F's printing service |
| Self-hosted 3D generation model | Low | Only if Tripo cost / quality becomes a blocker |
| Mesh editing in-browser (sculpt, boolean) | Low | DCC hand-off may make this unnecessary |

---

## Change Log

> Track changes to the roadmap itself (not features).

| Date | Change | Reason |
|---|---|---|
| 2026-04-23 | Roadmap created with 14 v1.0 features | Project initialization |
| 2026-04-23 | Expanded v1.0 to 15 features: added **Design Ledger** (folded into #02), new **Manufacturability Analysis** (#11, between Export and AR), **MCP server** (folded into Public API as #14), ledger viewer in #15. Renumbered AR/Blender/API/History to 12–15. Added strategic backlog: Decision Engine (v1.2), Parametric Variants (v1.1), Iterative Refinement (v1.1), Multi-Provider Racing, Depth/LiDAR capture, Video input, Mood-board input, Evaluation harness, OpenTelemetry, Version tree UI, Live multiplayer viewer, QR passport, Reprint/remix. | User-approved strategic differentiator expansion |
