---
type: architecture_domain_model
project: "raise"
status: active
bounded_contexts:
  - name: Workflow lifecycle
    description: Sessions, stories, epics, pipelines, and phase transitions
    modules: [raise_cli.pipeline, raise_cli.session, raise_cli.work_item]
  - name: Governance and validation
    description: Scope artifacts, policies, quality gates, and traceability
    modules: [raise_cli.governance, raise_cli.gates, raise_cli.artifacts]
  - name: Project context
    description: Knowledge graph, code discovery, and persistent memory
    modules: [raise_core.graph, raise_core.discovery, raise_cli.memory]
  - name: Integrations
    description: Backlog, documentation, MCP, and SCM adapters
    modules: [raise_cli.adapters, raise_cli.scm, raise_cli.pipeline.mcp]
shared_kernel:
  # modules: list of module names shared across bounded contexts.
  # Examples:
  #   modules:
  #     - constants
  #     - logging
  modules: []
---

# Domain Model: raise

> Bounded contexts and shared kernel

## Bounded Contexts

Work items and sessions belong to the workflow lifecycle context. Governance artifacts describe and constrain those changes. Project context supplies repository knowledge to workflows. Integrations translate local domain operations to external services without owning workflow policy.

## Shared Kernel

Shared kernel: project identity, work item keys, session identifiers, and typed result models are exchanged across contexts. Session identity and agent runtime identity remain distinct values.
