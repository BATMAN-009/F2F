"""Test the smoke ping task."""

from __future__ import annotations

from worker.tasks.ping import ping


def test_ping_returns_pong() -> None:
    result = ping.apply().get()
    assert isinstance(result, str)
    assert result.startswith("pong")
