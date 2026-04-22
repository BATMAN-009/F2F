# 🏛️ MASTERY — Compact Reference

> Compact, rules-only variant of `mastery.md`. Load this at the start of every AI
> agent session for fast context. For document **templates**, search the full
> `docs/mastery.md`. For full prose explanations, also see the full file.
>
> ⚠️ **READ-ONLY** in consuming projects. Edit only in the framework's origin repo.

---

## Core Principles

1. Think before you type — no code until discussion is complete.
2. Design before you build — architecture is documented, not improvised.
3. Plan before you execute — every task is written down and checkable.
4. Test before you ship — every feature has a test plan.
5. Document as you go — changes are logged, not remembered.
6. Review when done — reflect, learn, improve.
7. Never edit `docs/mastery.md` in consuming projects.

---

## AI Agent Protocol

### Context Loading Order (every new session)

1. `docs/mastery-compact.md` (this file)
2. `docs/project-discussion.md`
3. `docs/project-context.md`
4. `docs/project-roadmap.md`
5. `docs/features/<active>/` (discussion → architecture → tasks → changelog)

If `mastery-compact.md` is missing, fall back to `docs/mastery.md`.

### Determining Current State

1. Check roadmap for 🟡 IN PROGRESS feature.
2. Open that folder; read docs in order.
3. In `tasks.md`, last checked checkbox = where work stopped.
4. In `changelog.md`, latest Session Note = recent context.
5. `git log --oneline -10` on the feature branch shows recent commits.

### Autonomy Boundaries

| Action | AI autonomous? |
|---|---|
| Read any project document | ✅ |
| Write code within an active task | ✅ |
| Check off completed tasks | ✅ |
| Log changelog entries | ✅ |
| Create commits on feature branch | ✅ |
| Push to feature branch | ✅ |
| Update project changelog | ✅ |
| Create a new feature's discussion doc | ✅ |
| Amend architecture (minor, logged) | ✅ |
| Modify architecture (structural change) | ❌ Discuss first |
| Skip any lifecycle stage | ❌ Never |
| Merge to main | ❌ Always human-approved |
| Delete any branch | ❌ Always human-approved |
| Delete or overwrite existing docs | ❌ Always human-approved |
| Change `project-context.md` | ❌ Always human-approved |
| Reorder roadmap | ❌ Always human-approved |
| Add new dependencies/packages | ❌ Always human-approved |
| Edit `docs/mastery.md` | ❌ Never (read-only in projects) |
| Perform verification cross-check | ✅ |
| Skip a required cross-check | ❌ Never |

### Verification Cross-Checks

When to cross-check:

| Trigger | Verify |
|---|---|
| After planning docs created | Discussion ↔ architecture ↔ tasks ↔ testplan alignment |
| Every ~5 build tasks (or after high-complexity/high-risk task) | Code ↔ architecture, tasks checked off, changelog current |
| Before requesting merge | Full cross-check — all items below |

What to verify:

1. Architecture ↔ Code — implementation matches arch doc; deviations logged.
2. Tasks ↔ Code — completed tasks reflected in code; checkboxes updated.
3. Testplan ↔ Tests — testplan cases have corresponding tests; statuses filled.
4. Changelog ↔ Session — changelog reflects this session.
5. Dependencies ↔ Architecture — only approved dependencies used.

Fix gaps autonomously; log the cross-check; escalate architectural deviations to human.

### Session Handoff

End of every session, the outgoing party MUST:

1. Update changelog with what was done.
2. Update task checkboxes (completed + partial).
3. Add a Session Note at top of feature changelog:

```
### Session Note — YYYY-MM-DD
- Who: [Human / AI Agent Name]
- Duration: [time or "async"]
- Worked On: [brief]
- Stopped At: [exact task ID]
- Blockers: [issues or "None"]
- Next Steps: [what next session picks up]
```

### Communication Style

- Ask before assuming when ambiguous.
- Reference docs when making decisions.
- Log deviations from architecture/tasks before proceeding.
- Never silently skip a step; confirm with human first.
- Ask about testing approach if a `testplan.md` exists.

---

## Document Ecosystem

```
AGENTS.md                         (project root)
SKILL.md                          (project root, optional)
llms.txt                          (project root, optional)
docs/
├── mastery.md                    READ-ONLY full framework + templates
├── mastery-compact.md            this file — load each session
├── project-discussion.md         WHY (foundation conversation)
├── project-context.md            WHAT (formalized identity)
├── project-roadmap.md            WHEN (feature plan)
├── project-changelog.md          shipped history
├── _archive/                     (mid-project adoption only)
├── features/XX-feature-name/
│   ├── discussion.md             always
│   ├── architecture.md           always
│   ├── tasks.md                  always
│   ├── testplan.md               always
│   ├── api.md                    when feature exposes external interfaces
│   ├── research.md               when knowledge gaps are significant
│   ├── changelog.md              always
│   ├── review.md                 always
│   ├── summary.md                only for retroactive features
│   └── lightweight.md            only when meets ALL lightweight criteria
└── references/                   ADRs, specs, guides
```

---

## Feature Lifecycle (6 Stages)

```
1. DISCUSS → 2. DESIGN → 3. PLAN → 4. BUILD → 5. SHIP → 6. REFLECT
discussion.md  architecture.md  tasks.md     changelog.md    review.md
                                testplan.md
                                api.md (if needed)
                                research.md (if needed)
```

### Stage Entry / Exit

| Stage | Entry | Exit |
|---|---|---|
| 1 Discuss | Feature in roadmap | discussion.md COMPLETE |
| 2 Design | Discussion COMPLETE | architecture.md FINALIZED |
| 3 Plan | Architecture FINALIZED | tasks + testplan + api (if needed) created; feature branch created |
| 4 Build | Branch + planning docs done | All task checkboxes ✅; tests pass |
| 5 Ship | All tasks ✅; tests pass | Merged to main (human-approved) |
| 6 Reflect | Merged | review.md complete |

### Architecture Amendments

Minor amendments after finalization (renamed fields, signature tweaks, small additions)
= log in feature changelog with rationale, mark amended sections in arch doc with
`(amended YYYY-MM-DD)`. Structural changes = discuss + human approval.

### Stage 5 — Ship Checklist

- Self-review all changes
- Security review (auth gaps, input validation, secrets, PII, injection)
- Final test plan pass
- Human approval
- Merge to main; push main
- Update `project-changelog.md`
- Update README / public docs (if user-facing change)
- Create release with tag (if project uses versioned releases)
- **Keep the feature branch** — never delete

---

## Hotfix Workflow (Abbreviated Lifecycle)

When: production broken / security vuln / data risk / fix is small + understood.

Flow: IDENTIFY → branch `hotfix/desc` from main → FIX (minimal change, no refactors)
→ VERIFY (test it; test nothing else broke) → MERGE (human-approved) → DOCUMENT
(append to relevant feature changelog or `references/hotfix-log.md`; update
`project-changelog.md`).

Rules:
- Skip Discussion / Architecture / Tasks docs.
- Never skip testing.
- Always document after the fact.
- Complex / multi-system fix is NOT a hotfix — use full lifecycle.

### Rollback / Recovery

When fix > revert effort, or root cause unclear, or time pressure high:
`git revert -m 1 <merge-commit>` → test → human-approved push → document in
`project-changelog.md` → fix on the original feature branch → re-Ship.

---

## Lightweight Feature Variant

Eligibility (ALL must be true):

1. No new code logic (docs-only, config-only, trivial change).
2. No architectural decisions.
3. Well-understood scope (few sentences).
4. Low risk.
5. Self-contained (no impact on other in-progress features).

If ANY criterion is not met → use full lifecycle.

Lifecycle: CREATE `lightweight.md` → WORK (log progress in changelog section) →
VERIFY → SHIP (human-approved merge; fill Reflection after).

Rules: still uses feature branch; still requires human approval; branch never
deleted; if scope grows → upgrade to full lifecycle (lightweight.md becomes
discussion.md).

---

## Naming Conventions

| Element | Format | Example |
|---|---|---|
| Feature folder | `XX-feature-name` (2-digit zero-padded, kebab-case) | `01-project-foundation` |
| Doc filenames | type names | `discussion.md`, `architecture.md`, etc. |
| Branch | `feature/XX-feature-name` (matches folder) | `feature/02-data-model` |
| Hotfix branch | `hotfix/short-description` | `hotfix/payment-rounding` |

Sequence assignment = dependency order (see full mastery.md for the 10-step ordering
guide).

---

## Phase Organization (Tasks Doc)

Phases adapt to project type. Always end with a Testing phase and a Documentation /
Cleanup phase. Suggested phase sets per project type are in the full mastery.md.

---

## Git

### Branching Rules

- `main` — always deployable; only receives feature/hotfix merges.
- `feature/XX-name` — from latest `main`; one per feature.
- `hotfix/desc` — from latest `main`; critical fixes only.
- **Never delete branches.**
- One feature at a time by default; see Parallel Features for exceptions.

### Commit Convention

`type(scope): short description`

Types: `feat | fix | docs | style | refactor | test | chore | perf | hotfix`
Scope: feature name or module.

---

## Parallel Features

Safe when: features touch different files, no shared dependencies, both branched
from same main commit.

Risky when: same files, dependency between them, shared schemas being changed.

Rules:
1. Branch from latest main.
2. Coordinate when overlap is discovered.
3. Merge smaller/simpler first.
4. Rebase the other after.
5. Re-run full tests after rebase.
6. Document in changelog.

---

## References Directory

`docs/references/` holds project-wide artifacts not tied to a feature:

- `ADR-NNN-title.md` — architecture decision records
- `style-guide.md`
- `glossary.md`
- `hotfix-log.md`
- `spec-name.md` — third-party specs being followed
- `onboarding.md`
- `runbook-topic.md`
- `process-overrides.md` — any project-specific deviations from this framework

---

## Quick Reference — When To Do What

| Situation | Action |
|---|---|
| New feature idea | Add to roadmap backlog → start full lifecycle when scheduled |
| Tiny docs-only change | Lightweight variant |
| Production broken | Hotfix workflow |
| Architecture changed mid-build | Log in changelog; if structural → human approval |
| Test plan exists, building tests | Ask developer about TC traceability before generating |
| Ending a session | Session Note + checkbox + changelog updates |
| Starting a session | Read context loading order from top |
| Before merge | Full verification cross-check |
