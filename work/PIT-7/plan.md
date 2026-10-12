# PIT-7 — Implementation plan

1. Reproduce each transport direction and wrong-scope behavior against the real session index.
2. Resolve session identity from explicit Rai session ID, agent session ID, or a unique project/worktree pointer.
3. Resolve MCP open against the caller checkout and preserve the opener's worktree attribution on close.
4. Resolve only active worktree rows by path; reject multiple open rows instead of picking by creation time.
5. Extend regression tests for closed historical rows, ambiguity, no-session, and both cross-transport directions.
6. Update doctor and Codex session instructions; run full tests, Ruff, format, Pyright, then rebuild and smoke-test both executables.
7. Review the exact implementation and synchronize the target branch before opening the PR.

## Current status

Steps 1–6 are implemented and validated locally. Step 7 is in progress on the GitHub admission path.
