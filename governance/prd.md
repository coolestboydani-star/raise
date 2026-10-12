# PRD: RaiSE

---

## Problem

AI coding tools can lose context between sessions, skip prompt-only process instructions, and scatter decisions across tool logs. CI catches some defects after a commit, while teams still lack a portable record connecting work intent to implementation and validation.

## Goals

RaiSE provides a local-first workflow layer that records project and session state, guides work through explicit phases, and executes configured validation gates before advancing. External backlog and documentation systems remain adapters.

---

## Requirements

### RF-01: Governed workflow state

The CLI and supported agent integrations must create, resume, and close project-scoped session and work lifecycles with persistent identifiers and artifacts.

### RF-02: Executable validation gates

Configured tests, lint, format, and type checks must run as commands and report outcomes before the corresponding workflow phase advances.

### RF-03: Portable project context

Project instructions, knowledge graph, and session memory must remain in repository or developer-controlled storage and work across supported coding tools.

### RF-04: Traceable work artifacts

Scope, design, plan, implementation, review, and retrospective artifacts must be associated with work items and available to governance checks.

### RF-05: Adapter-based integrations

Backlog, documentation, and MCP integrations must use explicit adapters so the local CLI remains useful without hosted services.
