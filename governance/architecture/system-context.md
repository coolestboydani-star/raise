---
type: architecture_context
project: "raise"
status: active
tech_stack:
  language: Python 3.12+
  cli: Typer
  validation: pytest, Ruff, Pyright
  state: SQLite and repository-local files
  agent_protocol: MCP
external_dependencies:
  - GitHub Actions (CI)
  - Jira Cloud (optional backlog adapter)
  - Confluence (optional documentation adapter)
users:
  - software developers using AI coding assistants
  - AI coding assistants invoking RaiSE skills and MCP tools
  - CI pipelines validating governance evidence
governed_by: []
---

# System Context: raise

> C4 Level 1 — System Context diagram and description

## Overview

RaiSE runs locally beside a developer's repository. Developers and AI coding tools use the CLI, skills, and MCP server; optional adapters connect to backlog and documentation systems. CI can enforce test and governance gates on changes.

## Context Diagram

<!-- System context showing external actors and systems -->

```
┌──────────┐       ┌──────────────┐       ┌──────────┐
│  Users   │──────►│  raise  │◄──────│ External │
│          │       │              │       │ Systems  │
└──────────┘       └──────────────┘       └──────────┘
```

## External Interfaces

| System | Direction | Protocol | Description |
|--------|-----------|----------|-------------|
| AI coding assistant | Both | CLI, skills, MCP stdio/HTTP | Starts workflows, loads context, and records artifacts |
| GitHub Actions | Inbound | GitHub Actions workflow | Runs repository quality and governance checks |
| Jira Cloud | Outbound | Jira REST API via adapter | Optional work item search, update, and transition |
| Confluence | Outbound | Confluence API via adapter | Optional publication and retrieval of governance docs |
