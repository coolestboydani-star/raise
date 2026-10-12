"""Contract tests for the repository's Codex SessionStart hook."""

from pathlib import Path


def test_session_start_hook_routes_session_phrases_without_unsupported_cli() -> None:
    hook = (
        Path(__file__).resolve().parents[3]
        / ".codex-plugin"
        / "hooks"
        / "session_start.sh"
    )
    source = hook.read_text(encoding="utf-8")

    assert "rai session state" not in source
    assert "RAI INICIA SESION/SECCION" in source
    assert "rai-session-start" in source
    assert "RAI CIERRA SESION/SECCION" in source
    assert "rai-session-close" in source
    assert "without creating a duplicate" in source
