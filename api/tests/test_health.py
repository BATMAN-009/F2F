"""Smoke tests for /healthz."""

from __future__ import annotations

from unittest.mock import patch

from fastapi.testclient import TestClient


def test_healthz_returns_expected_shape(client: TestClient) -> None:
    with (
        patch("app.routes.health._check_db", return_value="up"),
        patch("app.routes.health._check_redis", return_value="up"),
    ):
        response = client.get("/healthz")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["db"] == "up"
    assert body["redis"] == "up"
    assert "version" in body


def test_healthz_degraded_when_db_down(client: TestClient) -> None:
    with (
        patch("app.routes.health._check_db", return_value="down"),
        patch("app.routes.health._check_redis", return_value="up"),
    ):
        response = client.get("/healthz")

    assert response.status_code == 200
    assert response.json()["status"] == "degraded"
