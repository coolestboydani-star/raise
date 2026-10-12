from __future__ import annotations

import asyncio
import json
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace

from raise_cli.cli.commands.session import resolve_close_guard, session_app
from raise_cli.developer_profile.persistence import save_developer_profile
from raise_cli.developer_profile.profile import ActiveSession, DeveloperProfile
from raise_cli.doctor.checks.session_routing import SessionRoutingCheck
from raise_cli.doctor.models import CheckStatus, DoctorContext
from raise_cli.pipeline import mcp_tools_session
from raise_cli.session.index import (
    ActiveSessionPointer,
    read_all_active_sessions,
    resolve_active_session_pointer,
    write_active_session,
)
from raise_cli.session.scope import SessionScope


def _pointer(
    session_id: str, *, agent_session_id: str = "", worktree_id: str = ""
) -> ActiveSessionPointer:
    return ActiveSessionPointer(
        id=session_id,
        name=session_id,
        started=datetime(2026, 10, 12),
        cc_session_id=agent_session_id,
        worktree_id=worktree_id,
    )


def _stub_pointer_store(
    monkeypatch, pointers: list[ActiveSessionPointer], worktree_id: str = ""
) -> None:
    monkeypatch.setattr(
        "raise_cli.session.index.read_all_active_sessions",
        lambda **_kwargs: pointers,
    )
    monkeypatch.setattr(
        "raise_cli.session.scope.resolve_scope",
        lambda _project, _agent_session_id=None: SessionScope(worktree_id=worktree_id),
    )


def _open_cli_session_without_runtime_id(project: Path) -> str:
    from typer.testing import CliRunner

    save_developer_profile(DeveloperProfile(name="Tester"))
    result = CliRunner().invoke(
        session_app,
        ["start", "--project", str(project), "--format", "json"],
    )
    assert result.exit_code == 0, result.output
    payload = json.loads(result.stdout)
    assert not payload["rai_meta"]["agent_session_id"]
    return payload["rai_meta"]["rai_session_id"]


def _open_mcp_session_without_runtime_id(project: Path) -> str:
    save_developer_profile(DeveloperProfile(name="Tester"))
    payload = json.loads(
        asyncio.run(
            mcp_tools_session._session_open_impl(cwd=str(project), include_bundle=True)
        )
    )
    assert not payload["rai_meta"]["agent_session_id"]
    return payload["rai_meta"]["rai_session_id"]


def test_explicit_rai_session_id_selects_pointer(monkeypatch) -> None:
    pointer = _pointer("R-123", agent_session_id="agent-1")
    _stub_pointer_store(monkeypatch, [pointer])

    resolved, reason = resolve_active_session_pointer(
        Path("/repo"), rai_session_id="R-123"
    )

    assert resolved == pointer
    assert reason is None


def test_explicit_rai_session_id_cannot_cross_worktrees(monkeypatch) -> None:
    pointer = _pointer("R-other", worktree_id="wt-other")
    _stub_pointer_store(monkeypatch, [pointer], "wt-current")

    resolved, reason = resolve_active_session_pointer(
        Path("/repo"), rai_session_id="R-other"
    )

    assert resolved is None
    assert reason is not None
    assert "No active session" in reason


def test_missing_agent_id_uses_only_pointer_in_current_worktree(monkeypatch) -> None:
    main_pointer = _pointer("R-main")
    worktree_pointer = _pointer("R-wt", agent_session_id="agent-1", worktree_id="wt-1")
    _stub_pointer_store(monkeypatch, [main_pointer, worktree_pointer], "wt-1")

    resolved, reason = resolve_active_session_pointer(
        Path("/repo"), rai_session_id=None
    )

    assert resolved == worktree_pointer
    assert reason is None


def test_cli_opened_sqlite_pointer_can_be_closed_by_mcp_without_runtime_id(
    monkeypatch, tmp_path: Path
) -> None:
    monkeypatch.delenv("RAISE_AGENT_SESSION_ID", raising=False)
    monkeypatch.delenv("RAISE_CC_SESSION_ID", raising=False)
    pointer = _pointer("R-cli", agent_session_id="cli-agent")
    write_active_session(pointer, project_root=tmp_path, cc_session_id="cli-agent")

    resolved, reason = resolve_active_session_pointer(tmp_path, rai_session_id=None)

    assert resolved == pointer
    assert reason is None


def test_mcp_opened_profile_session_can_be_resolved_by_cli_close(
    tmp_path: Path,
) -> None:
    profile = DeveloperProfile(
        name="Tester",
        active_sessions=[
            ActiveSession(
                session_id="R-mcp",
                started_at=datetime(2026, 10, 12),
                project=str(tmp_path),
            )
        ],
    )

    session_id, resolved_via_agent = resolve_close_guard(profile, tmp_path, None)

    assert session_id == "R-mcp"
    assert resolved_via_agent is False


def test_mcp_close_completes_cli_session_when_runtime_id_is_unavailable(
    monkeypatch, tmp_path: Path
) -> None:
    pointer = _pointer("R-cli", agent_session_id="cli-agent")
    write_active_session(pointer, project_root=tmp_path, cc_session_id="cli-agent")
    profile = DeveloperProfile(name="Tester")

    monkeypatch.setattr(
        mcp_tools_session,
        "discover_agent_session_id",
        lambda override=None: None,
    )
    monkeypatch.setattr(
        "raise_cli.onboarding.profile.load_developer_profile", lambda: profile
    )
    monkeypatch.setattr(
        "raise_cli.session.close.process_session_close",
        lambda *_args, **_kwargs: SimpleNamespace(
            success=True,
            session_id="R-cli",
            patterns_added=0,
            corrections_added=0,
            messages=[],
        ),
    )
    monkeypatch.setattr(mcp_tools_session, "_emit_session_topic", lambda **_kwargs: "")
    monkeypatch.setattr(
        "raise_cli.session.close._maybe_emit_session_cost_kpi", lambda *_args: None
    )

    response = json.loads(
        asyncio.run(
            mcp_tools_session._session_close_full_impl(
                json.dumps(
                    {"summary": "close from MCP", "session_type": "maintenance"}
                ),
                cwd=str(tmp_path),
            )
        )
    )

    assert response["status"] == "ok"
    assert response["session_id"] == "R-cli"
    assert read_all_active_sessions(project_root=tmp_path) == []


def test_real_mcp_open_can_be_closed_by_cli(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.delenv("RAISE_AGENT_SESSION_ID", raising=False)
    monkeypatch.delenv("RAISE_CC_SESSION_ID", raising=False)
    session_id = _open_mcp_session_without_runtime_id(tmp_path)

    from typer.testing import CliRunner

    result = CliRunner().invoke(
        session_app,
        [
            "close",
            "--summary",
            "Close MCP-opened session through CLI",
            "--project",
            str(tmp_path),
            "--no-tokens",
        ],
    )

    assert result.exit_code == 0, result.output
    assert session_id in result.output
    assert read_all_active_sessions(project_root=tmp_path) == []


def test_real_open_can_be_closed_by_mcp_without_runtime_id(
    monkeypatch, tmp_path: Path
) -> None:
    monkeypatch.delenv("RAISE_AGENT_SESSION_ID", raising=False)
    monkeypatch.delenv("RAISE_CC_SESSION_ID", raising=False)
    session_id = _open_cli_session_without_runtime_id(tmp_path)

    response = json.loads(
        asyncio.run(
            mcp_tools_session._session_close_full_impl(
                json.dumps(
                    {
                        "summary": "Close CLI-opened session through MCP",
                        "session_type": "maintenance",
                    }
                ),
                cwd=str(tmp_path),
                rai_session_id=session_id,
            )
        )
    )

    assert response["status"] == "ok"
    assert response["session_id"] == session_id
    assert read_all_active_sessions(project_root=tmp_path) == []


def test_agent_id_may_resolve_unique_unbound_cross_transport_pointer(
    monkeypatch,
) -> None:
    pointer = _pointer("R-unbound")
    _stub_pointer_store(monkeypatch, [pointer])

    resolved, reason = resolve_active_session_pointer(
        Path("/repo"), rai_session_id=None, agent_session_id="agent-1"
    )

    assert resolved == pointer
    assert reason is None


def test_ambiguous_runtime_free_close_fails_without_selecting_pointer(
    monkeypatch,
) -> None:
    pointers = [_pointer("R-1"), _pointer("R-2", agent_session_id="agent-2")]
    _stub_pointer_store(monkeypatch, pointers)

    resolved, reason = resolve_active_session_pointer(
        Path("/repo"), rai_session_id=None
    )

    assert resolved is None
    assert reason is not None
    assert "Multiple active sessions" in reason
    assert "R-1" in reason
    assert "R-2" in reason


def test_absent_pointer_returns_no_active_session(monkeypatch) -> None:
    _stub_pointer_store(monkeypatch, [])

    resolved, reason = resolve_active_session_pointer(
        Path("/repo"), rai_session_id=None
    )

    assert resolved is None
    assert reason is not None
    assert "No active session" in reason


def test_doctor_warns_when_close_target_is_ambiguous(
    monkeypatch, tmp_path: Path
) -> None:
    pointers = [_pointer("R-1"), _pointer("R-2", agent_session_id="agent-2")]
    _stub_pointer_store(monkeypatch, pointers)
    monkeypatch.setattr(
        "raise_cli.doctor.checks.session_routing.read_all_active_sessions",
        lambda **_kwargs: pointers,
    )
    monkeypatch.setattr(
        "raise_cli.doctor.checks.session_routing.resolve_scope",
        lambda _project, _agent_session_id=None: SessionScope(),
    )
    monkeypatch.setattr(
        "raise_cli.doctor.checks.session_routing.discover_agent_session_id",
        lambda: None,
    )
    monkeypatch.setattr(
        "raise_cli.onboarding.profile.load_developer_profile",
        lambda: DeveloperProfile(name="Tester"),
    )

    result = SessionRoutingCheck().evaluate(DoctorContext(working_dir=tmp_path))[0]

    assert result.status is CheckStatus.WARN
    assert "Multiple active sessions" in result.message


def test_doctor_errors_when_profile_and_pointer_state_disagree(
    monkeypatch, tmp_path: Path
) -> None:
    _stub_pointer_store(monkeypatch, [])
    monkeypatch.setattr(
        "raise_cli.doctor.checks.session_routing.read_all_active_sessions",
        lambda **_kwargs: [],
    )
    monkeypatch.setattr(
        "raise_cli.doctor.checks.session_routing.resolve_scope",
        lambda _project, _agent_session_id=None: SessionScope(),
    )
    profile = DeveloperProfile(
        name="Tester",
        active_sessions=[
            ActiveSession(
                session_id="R-orphan",
                started_at=datetime(2026, 10, 12),
                project=str(tmp_path),
            )
        ],
    )
    monkeypatch.setattr(
        "raise_cli.onboarding.profile.load_developer_profile", lambda: profile
    )

    result = SessionRoutingCheck().evaluate(DoctorContext(working_dir=tmp_path))[0]

    assert result.status is CheckStatus.ERROR
    assert "No active session" in result.message
