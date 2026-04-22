# 🧪 Test Plan: Project Foundation

> **Feature**: `01` — Project Foundation
> **Tasks**: [`tasks.md`](tasks.md)
> **Date**: 2026-04-23

---

## Acceptance Criteria

Feature 01 is DONE when all are true:

- [ ] **AC-01** — Fresh clone → `cp .env.example .env` → `docker compose up -d` brings all services to healthy in <3 min on a typical laptop
- [ ] **AC-02** — `http://localhost:8000/healthz` returns `200` with `db:"up"` and `redis:"up"`
- [ ] **AC-03** — `http://localhost:8000/docs` shows FastAPI Swagger UI
- [ ] **AC-04** — `http://localhost:3000` loads, HealthBadge displays a green "healthy" indicator
- [ ] **AC-05** — `http://localhost:9001` MinIO console lists bucket `f2f-assets`
- [ ] **AC-06** — `/tasks/ping` dispatches → polling the task ID eventually returns `SUCCESS` with `pong | Blender ...`
- [ ] **AC-07** — `docker compose exec api alembic upgrade head` succeeds on a fresh DB
- [ ] **AC-08** — `pnpm lint && pnpm format:check && pnpm test` clean in `web/`
- [ ] **AC-09** — `ruff check . && ruff format --check . && pytest` clean in `api/` and `worker/`
- [ ] **AC-10** — GitHub Actions CI workflow green on the Feature 01 PR
- [ ] **AC-11** — `docker compose down` then `docker compose up -d` preserves DB and MinIO state (named volumes work)

---

## Test Cases

### TC-01: Fresh-clone happy path

| Property | Value |
|---|---|
| **Category** | Happy Path |
| **Precondition** | Clean host; Docker Desktop running |
| **Steps** | 1. `git clone https://github.com/BATMAN-009/F2F.git` → 2. `cd F2F` → 3. `cp .env.example .env` → 4. `docker compose up -d` → 5. wait until all healthchecks green → 6. open `:3000`, `:8000/healthz`, `:9001` |
| **Expected Result** | All 3 URLs respond; HealthBadge green; healthz JSON has `status:ok db:up redis:up`; MinIO console shows `f2f-assets` bucket |
| **Status** | ⬜ Not Run |

### TC-02: `/healthz` reports component status

| Property | Value |
|---|---|
| **Category** | Happy Path |
| **Precondition** | Stack running |
| **Steps** | `curl http://localhost:8000/healthz` |
| **Expected Result** | HTTP 200; JSON has keys `status`, `db`, `redis`, `version` |
| **Status** | ⬜ Not Run |

### TC-03: `/tasks/ping` end-to-end

| Property | Value |
|---|---|
| **Category** | Happy Path |
| **Precondition** | Stack running |
| **Steps** | 1. `curl :8000/tasks/ping` → get `task_id` → 2. poll `:8000/tasks/ping/{task_id}` until status `SUCCESS` |
| **Expected Result** | Final response has `status:SUCCESS`, `result` string starts with `"pong"` and contains `"Blender"` |
| **Status** | ⬜ Not Run |

### TC-04: MinIO bucket auto-provisioned

| Property | Value |
|---|---|
| **Category** | Happy Path |
| **Precondition** | Stack coming up from fresh volumes |
| **Steps** | 1. `docker volume rm f2f_minio_data` (or new clone) → 2. `docker compose up -d` → 3. log into MinIO console |
| **Expected Result** | `f2f-assets` bucket exists without manual creation |
| **Status** | ⬜ Not Run |

### TC-05: Alembic baseline migration

| Property | Value |
|---|---|
| **Category** | Happy Path |
| **Precondition** | Fresh DB |
| **Steps** | `docker compose exec api alembic upgrade head` |
| **Expected Result** | Exit 0; alembic_version table exists with revision `0001` |
| **Status** | ⬜ Not Run |

### TC-06: Local lint + tests

| Property | Value |
|---|---|
| **Category** | Happy Path |
| **Precondition** | `uv` and `pnpm` installed locally; `uv sync` run in both `api/` and `worker/`; `pnpm install` in `web/` |
| **Steps** | In each service folder: run lint and test commands per Phase B/C/D |
| **Expected Result** | All clean |
| **Status** | ⬜ Not Run |

### TC-07: CI workflow green on PR

| Property | Value |
|---|---|
| **Category** | Happy Path |
| **Precondition** | PR open for `feature/01-project-foundation` → `main` |
| **Steps** | Push; open PR; wait |
| **Expected Result** | All 6 jobs succeed |
| **Status** | ⬜ Not Run |

### TC-08: Volume persistence across restart

| Property | Value |
|---|---|
| **Category** | Happy Path |
| **Precondition** | Stack running |
| **Steps** | 1. Put test data in DB (insert a row manually) and upload object to MinIO via console → 2. `docker compose down` → 3. `docker compose up -d` |
| **Expected Result** | DB row and MinIO object still present |
| **Status** | ⬜ Not Run |

### TC-09: Missing `TRIPO_API_KEY` tolerated in Feature 01

| Property | Value |
|---|---|
| **Category** | Edge Case |
| **Precondition** | `.env` has `TRIPO_API_KEY=` (empty) |
| **Steps** | `docker compose up -d`; check all healthchecks |
| **Expected Result** | Stack comes up green; api logs do not error on missing Tripo key (not used yet) |
| **Status** | ⬜ Not Run |

### TC-10: DB outage surfaces in healthz

| Property | Value |
|---|---|
| **Category** | Error |
| **Precondition** | Stack running |
| **Steps** | 1. `docker compose stop db` → 2. `curl :8000/healthz` |
| **Expected Result** | Response body shows `db:"down"`; response status may be 200 with body indicating degraded, or 503 — either acceptable as long as it's deterministic |
| **Status** | ⬜ Not Run |

### TC-11: Blender absent in worker container (negative — should NOT happen)

| Property | Value |
|---|---|
| **Category** | Security / Integrity |
| **Precondition** | worker container built per Dockerfile.worker |
| **Steps** | `docker compose exec worker blender --version` |
| **Expected Result** | Exit 0, prints Blender version string |
| **Status** | ⬜ Not Run |

---

## Edge Cases

| # | Scenario | Expected Behavior |
|---|---|---|
| 1 | `.env` missing entirely | docker-compose fails fast with clear error naming the missing file |
| 2 | Ports 3000/8000/9000/9001/5432/6379 already in use | docker-compose fails fast with port-conflict error; README documents the ports |
| 3 | MinIO `createbuckets` runs before MinIO is ready | `depends_on: condition: service_healthy` on MinIO prevents this |
| 4 | CI runs on a force-pushed branch | CI runs on latest HEAD; no weirdness |
| 5 | `api` starts before `db` healthy | `depends_on: condition: service_healthy` on `db` prevents this |

---

## Security Tests

| # | Test | Expected |
|---|---|---|
| 1 | Default MinIO creds NOT valid for anything public | v1.0 is local-only; ports bound to loopback via docker default → OK |
| 2 | No real secrets committed (grep for `TRIPO_API_KEY=<non-empty>`) | `git log -p | grep -i 'TRIPO_API_KEY=.\+'` returns nothing |
| 3 | `.env` never appears in `git status` | Gitignored |

---

## Performance Considerations

No performance-critical paths in Feature 01. Informational targets only:

| Metric | Target | Actual |
|---|---|---|
| Cold `docker compose up -d` to all green | <3 min | — |
| `/healthz` latency | <100 ms | — |
| Worker container image size | <1.5 GB | — |

---

## Test Summary

| Category | Total | Pass | Fail | Skip |
|---|---|---|---|---|
| Happy Path | 8 | — | — | — |
| Error | 1 | — | — | — |
| Edge Case | 1 | — | — | — |
| Security | 3 | — | — | — |
| **Total** | 13 | — | — | — |

**Result**: ⬜ NOT RUN
