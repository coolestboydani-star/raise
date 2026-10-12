---
type: architecture_design
project: "raise"
status: active
layers:
  - name: CLI and agent integrations
    description: User-facing commands, MCP tools, and skill workflows
    modules: [raise_cli.cli, raise_cli.pipeline, raise_cli.skills]
  - name: Workflow and governance domain
    description: Session state, backlog workflows, artifacts, and validation gates
    modules: [raise_cli.session, raise_cli.gates, raise_cli.governance]
  - name: Persistence and adapters
    description: Local storage and optional external system integrations
    modules: [raise_cli.storage, raise_cli.adapters, raise_core.graph]
---

# System Design: raise

> C4 Level 2 — Container/component decomposition

## Architecture Overview

The Python monorepo contains `raise-cli` for user-facing governance operations and `raise-core` for reusable graph, memory, and discovery capabilities. CLI commands and MCP tools share application services; storage and external adapters implement persistence boundaries.

## Components

| Component | Responsibility | Technology |
|-----------|---------------|------------|
| raise-cli | Commands, sessions, gates, pipelines, adapters, and MCP server | Python, Typer, Pydantic |
| raise-core | Knowledge graph, memory, and code discovery primitives | Python |
| Local project state | Persist project metadata, session indexes, and graph data | YAML, SQLite, JSON |
| External adapters | Optional backlog and documentation integrations | Adapter protocols, HTTP APIs |

## Key Decisions

Branch targeting is resolved from the project manifest. External systems are accessed through adapters. Workflow state and validation evidence are persisted so phase transitions can be audited.
