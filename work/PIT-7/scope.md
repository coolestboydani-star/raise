# PIT-7 — Unify CLI/MCP session lifecycle

## Parent epic

PIT-4 — Alinear estado de sesión RaiSE entre CLI y MCP.

## Problem

MCP and the CLI could disagree about the active session because the MCP opener resolved the server's working directory, and historical closed worktree registrations could shadow the active checkout path.

## Scope

- Resolve the caller's project checkout and canonical Rai session identity in both transports.
- Exclude closed worktree registrations from active path lookup.
- Fail explicitly when multiple open worktree registrations point at the same path.
- Preserve historic session rows and project/worktree isolation.
- Keep the Codex SessionStart hook on supported Rai commands.

## Acceptance criteria

- CLI-open/MCP-close and MCP-open/CLI-close resolve the same session exactly once.
- Missing or wrong-scope IDs return a non-success without mutating another session.
- Closed historical rows do not shadow the main checkout; duplicate open path registrations fail closed.
- Doctor identifies shared CLI/MCP state and passes for an active session.
- The Codex SessionStart hook has phrase guidance and does not call `rai session state`.

## Implementation references

- Source branch: `codex/rai-session-mcp-close-identity`.
- Source commits before review: `7e17f2b`, `96b641b`, `f75951a`.
- Local server binary installed at `/home/ubuntu/.local/share/rai-session-hotfix-ambiguity-96b641b`.
