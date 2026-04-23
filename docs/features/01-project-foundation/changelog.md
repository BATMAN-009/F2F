# 📝 Changelog: Project Foundation

> **Feature**: `01` — Project Foundation
> **Branch**: `feature/01-project-foundation`
> **Started**: 2026-04-23

---

## Session Notes

### Session 4 — 2026-04-23 — Stage 4 (Build) — Phase D: Web scaffold

- Committed Next.js 14 scaffold under `web/` (package.json, tsconfig, Tailwind, ESLint, Prettier, Vitest configs).
- App shell: `app/layout.tsx`, `app/page.tsx` (landing), `components/HealthBadge.tsx` (calls `/healthz`), `lib/api.ts` (fetch wrapper), `app/globals.css` (Tailwind directives).
- Smoke test `tests/smoke.test.ts` wired with Vitest + jsdom.
- Added placeholder `public/favicon.ico` (minimal 78-byte ICO).
- Ran `pnpm install` (pnpm 9.15.0, Node 24) — committed `pnpm-lock.yaml`.
- `pnpm format:check` clean; `pnpm lint` clean; `pnpm test` green; `pnpm build` succeeds (static).
- **Deviation (minor)**: Removed `@typescript-eslint/no-unused-vars` override from `web/.eslintrc.json` (plugin not bundled with `eslint-config-next@14`); logged in Deviations table below.
- Stopped at: end of Phase D. Next: Phase E (Blender add-on scaffold).

### Session 3.5 — 2026-04-23 — Stage 4 (Build) — Phases A, B, C

- Phase A (`c4953e9`): `.editorconfig`, `.gitattributes`, `.env.example` per architecture.
- Phase B (`c5b66a1`): FastAPI scaffold — `/healthz`, `/tasks/ping`, `alembic` baseline, stub packages (ledger / manufacturability / mcp / providers / pipeline / models / schemas), conftest + `test_health`. `uv sync` / `ruff` / `pytest` all green.
- Phase C (`e8c483f`): Celery worker — `celery_app.py`, `tasks.ping` (graceful Blender absence), `blender_scripts/smoke.py`, eager-mode `test_ping`. `uv sync` / `ruff` / `pytest` all green.

### Session 3 — 2026-04-23 — Stage 3 (Plan)

- Wrote `tasks.md` with 8 phases (A–H) + testing (Y) + cleanup (Z), 56 tasks total.
- Wrote `testplan.md` with 11 AC, 11 test cases, edge/security/perf sections.
- Initialized this changelog.

### Session 2 — 2026-04-23 — Stage 2 (Design)

- Wrote `architecture.md`: full file tree (~60 new files), docker-compose service table with healthchecks, three Dockerfile specs, CI workflow (6 jobs), complete `.env.example`, security + trade-offs sections.
- Architecture FINALIZED.

### Session 1 — 2026-04-23 — Stage 1 (Discuss)

- Drafted `discussion.md`: problem framing, scope (scaffolding only), 4 user stories, 12 functional + 4 non-functional requirements.
- Raised 8 open questions; user answered all:
  1. Versions: Node 20 LTS / pnpm 9 / Python 3.12 / latest Blender apt.
  2. CI is advisory — no branch protection.
  3. Tailwind CSS enabled in `web/` from the start.
  4. MinIO bucket `f2f-assets` auto-provisioned by a `createbuckets` sidecar.
  5. Custom Blender image built on `python:3.12-slim` + apt Blender + xvfb + libgl1.
  6. Skip OpenTelemetry in Feature 01; revisit v1.1.
  7. Commit `.env.example` with safe local defaults; keep `.env` gitignored.
  8. License TBD — leave out of this feature.
- Marked discussion 🟢 COMPLETE. Committed `d648772`.

---

## Deviations from Plan

| Date | Deviation | Rationale |
|---|---|---|
| 2026-04-23 | Removed `@typescript-eslint/no-unused-vars` rule override from `web/.eslintrc.json` | `eslint-config-next@14` does not bundle `@typescript-eslint/eslint-plugin`; the rule is undefined at lint time. `next/core-web-vitals` already enforces unused-var checks via its own pipeline. Minor amendment — architecture intent preserved. |

---

## Final Summary

_Filled at Stage 5 / 6._
