# Rai Memory — raise

> Permanent knowledge for this project. Loaded into system prompt.

---

## RaiSE Framework Process

### Work Lifecycle (Always Follow)

```
EPIC LEVEL:
  /rai-epic-start → /rai-epic-design → /rai-epic-plan → [stories] → /rai-epic-close

STORY LEVEL (per story):
  /rai-story-start → /rai-story-design* → /rai-story-plan → /rai-story-implement → /rai-story-review → /rai-story-close

* *design optional for S/XS stories

SESSION LEVEL:
  /rai-session-start → [work] → /rai-session-close
```

## Available Skills (19 total)

### Session Skills
- `/rai-session-start` — Load memory, analyze progress, propose focused work
- `/rai-session-close` — Capture learnings, update memory, log session

### Epic Skills
- `/rai-epic-start` — Initialize epic scope and directory structure
- `/rai-epic-design` — Design epic scope, stories, architecture
- `/rai-epic-plan` — Sequence stories with milestones and dependencies
- `/rai-epic-close` — Epic retrospective, metrics capture, tracking update

### Story Skills
- `/rai-story-start` — Create story branch and scope commit
- `/rai-story-design` — Create lean specification for complex stories
- `/rai-story-plan` — Decompose into atomic executable tasks
- `/rai-story-implement` — Execute tasks with TDD and validation gates
- `/rai-story-review` — Extract learnings, identify improvements
- `/rai-story-close` — Verify, merge, cleanup

### Discovery Skills
- `/rai-discover-start` — Initialize codebase discovery
- `/rai-discover-scan` — Extract symbols and synthesize descriptions
- `/rai-discover-validate` — Human review of synthesized descriptions, then export to graph format

### Meta Skills
- `/rai-skill-create` — Create new skills with framework integration

### Other Skills
- `/rai-research` — Epistemologically rigorous research
- `/rai-debug` — Root cause analysis using lean methods
- `/rai-framework-sync` — Sync framework files across locations

---

### Gate Requirements

| Gate | Required Before |
|------|-----------------|
| **Epic directory and scope initialized** | **Epic design** (/rai-epic-start) |
| **Story branch and scope commit** | **Story work** (/rai-story-start) |
| **Plan exists** | **Implementation** (/rai-story-plan) |
| **Retrospective complete** | **Story close** (/rai-story-review) |
| **Epic retrospective complete** | **Epic close** (/rai-epic-close) |
| Tests pass | Before any commit |
| Type checks pass | Before any commit |
| Linting passes | Before any commit |
| Full gate after merge | After merging target branch into MR branch |
| Scoped tests per task | After each task during implementation |

---

## Critical Process Rules

1. **TDD Always** — RED-GREEN-REFACTOR, no exceptions
2. **Commit After Task** — Commit after each completed task, not just story end
3. **Full Skill Cycle** — Use skills even for small stories
4. **Ask Before Subagents** — Get permission before spawning subagents
5. **Delete Branches After Merge** — Clean up merged branches immediately
6. **Pipeline Is The Only Entry Point** — Start work via pipeline_start, never invoke skills directly
7. **MR Always Via Skill** — Create merge requests via /rai-mr-create, never manual glab/gh
8. **Worktree Before Branch** — Enter worktree before creating story branch, not after
9. **Verify Branch Before Commit** — Assert expected branch in same command as commit in secondary worktrees
10. **Merge Is Not Deploy** — Verify deployment occurred after merge for components with deployables
11. **Estimation Anchors** — Fibonacci scale 1-8 with calibrated backlog anchors for consistent sizing
12. **HITL Default** — Pause after significant work for human review
13. **HITL Scoping** — At Ha/Ri level, only pause for high-impact decisions or errors unresolvable after 2 attempts
14. **Direct Communication** — No praise-padding, say what needs saying
15. **Redirect When Dispersing** — Gently redirect tangents to parking lot
16. **Type Everything** — Type annotations on all code
17. **Pydantic Models** — Use Pydantic for all data structures
18. **Simple First** — Simple heuristics over complex solutions
19. **Adapters Over MCP** — Use rai adapters (backlog, docs) as canonical path; MCP only when user explicitly requests it
20. **Test Scoping** — Per-task: rai gate check --scope <dir>. Story close: package-scoped. Full suite: only at /rai-mr-create
21. **Re-Run Gate After Merge** — Always re-run full gate after merging target branch into MR branch

---

## Branch Model

```
main (stable)
  └── main (development)
        └── story/s{N}.{M}/{name}
```

- Stories branch from and merge to main
- main merges to main at release
- Epics are logical containers (directory + tracker), not branches
- Several release lines may coexist, declared in .raise/manifest.yaml branches.release_lines[] (status: active | bugfix-only | sunset); branches.development always names the active line (ADR-033 amendment, RAISE-17066)
- The target branch is resolved from the manifest (rai worktree resolve-base / resolve_target), never inferred from origin/release/* and never hardcoded; ambiguity fails loud
- Admission: feature/story work targets the active line only; bugfixes may target a bugfix-only line; sunset lines accept nothing. Fixes propagate oldest → newer line by MR, never to main

---

## Key Patterns (from memory)

- **raise:BASE-051:** Hook extension pattern: typed event + subscriber + entry point + error isolation. Adding new cross-cutting behavior requires zero changes to existing code.
- **raise:BASE-052:** Parallel research agents with distinct orthogonal questions produce higher-quality synthesis than sequential research — each goes deep on its axis, triangulation happens in synthesis.
- **raise:BASE-053:** Separating parallel agent work by layer (e.g., code vs content, backend vs frontend) eliminates file collisions — the agent with freshest context on a file owns it.
- **raise:BASE-054:** Explain-then-ask: present context and implications BEFORE requesting a decision. Questions without framing cause rejections and rework.
- **raise:BASE-055:** U-shaped attention in LLMs: beginning and end get highest attention, middle is a dead zone (>30% accuracy drop). Position critical instructions at top and bottom of prompts.
- **raise:BASE-056:** Design is not optional — even for XS stories. Design grounds integration decisions: where to thread parameters, what to expose in CLI, what tests validate. Skip design = skip grounding.
- **raise:BASE-057:** Code as Gemba — before designing, go to the code. Read the actual implementation, not your memory of it. Observation before analysis, science after wisdom. The code is the source of truth; docs and memory are maps, not territory.
- **raise:BASE-058:** Grounding over speed for foundational infrastructure — design phase for each story even when parallelizable. Corrections compound just like learnings do. Shared understanding is the bottleneck, not velocity.
- **raise:BASE-059:** Autonomous memory with notification: Rai writes patterns during sessions without asking permission, but always notifies the human with a brief summary of what was learned. Maintains observability while reducing ceremony friction.
- **raise:BASE-060:** Bare except Exception in error-isolation patterns can hide import errors, type errors, and other bugs. Log the actual exception (at least at debug level) in catch-all handlers to avoid silent failures.

---

*Last updated: 2026-10-12*
*Generated by `rai init`*
