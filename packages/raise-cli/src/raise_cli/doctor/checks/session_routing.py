"""Check whether the active Rai session can be resolved safely by CLI and MCP."""

from __future__ import annotations

from pathlib import Path
from typing import ClassVar

from raise_cli._agent_session import discover_agent_session_id
from raise_cli.doctor.models import CheckResult, CheckStatus, DoctorContext
from raise_cli.doctor.protocol import DoctorCheck
from raise_cli.session.index import (
    read_all_active_sessions,
    resolve_active_session_pointer,
)
from raise_cli.session.scope import resolve_scope


class SessionRoutingCheck(DoctorCheck):
    """Detect active-session state the structured CLI/MCP close cannot share."""

    check_id: ClassVar[str] = "session-routing"
    category: ClassVar[str] = "session"
    description: ClassVar[str] = "CLI/MCP active-session resolution"
    requires_online: ClassVar[bool] = False

    def evaluate(self, context: DoctorContext) -> list[CheckResult]:
        """Report whether the current project/worktree has one close target."""
        project = context.working_dir.resolve()
        agent_session_id = discover_agent_session_id()
        pointer, reason = resolve_active_session_pointer(
            project,
            agent_session_id=agent_session_id,
        )
        if pointer is not None:
            return [
                CheckResult(
                    check_id=self.check_id,
                    category=self.category,
                    status=CheckStatus.PASS,
                    message=f"active session {pointer.id} is resolvable by CLI and MCP",
                )
            ]

        scope = resolve_scope(project, agent_session_id or "")
        scoped_pointers = [
            item
            for item in read_all_active_sessions(project_root=project)
            if item.worktree_id == scope.worktree_id
        ]
        if reason and "Multiple active sessions" in reason:
            return [
                CheckResult(
                    check_id=self.check_id,
                    category=self.category,
                    status=CheckStatus.WARN,
                    message=reason,
                    fix_hint=(
                        "Pass rai_session_id returned by rai-session-start to "
                        "rai-session-close."
                    ),
                )
            ]

        from raise_cli.onboarding.profile import load_developer_profile

        profile = load_developer_profile()
        profile_sessions = [
            item
            for item in (profile.active_sessions if profile is not None else [])
            if item.project and Path(item.project).resolve() == project
        ]
        if scoped_pointers or profile_sessions:
            detail = (
                reason or "Active session state is not resolvable by both adapters."
            )
            return [
                CheckResult(
                    check_id=self.check_id,
                    category=self.category,
                    status=CheckStatus.ERROR,
                    message=detail,
                    fix_hint=(
                        "Run rai session doctor and reconcile the active pointer "
                        "with ~/.rai/developer.yaml."
                    ),
                )
            ]

        return [
            CheckResult(
                check_id=self.check_id,
                category=self.category,
                status=CheckStatus.PASS,
                message="no active session to compare; CLI/MCP close routing is ready",
            )
        ]
