"""Health endpoint — best-effort component checks."""

from __future__ import annotations

from typing import Any

import redis as redis_lib
from fastapi import APIRouter
from sqlalchemy import text

from app import __version__
from app.config import get_settings
from app.db import engine

router = APIRouter(tags=["health"])


def _check_db() -> str:
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return "up"
    except Exception:
        return "down"


def _check_redis() -> str:
    try:
        client = redis_lib.from_url(get_settings().redis_url, socket_connect_timeout=1)
        client.ping()
        return "up"
    except Exception:
        return "down"


@router.get("/healthz")
def healthz() -> dict[str, Any]:
    db_status = _check_db()
    redis_status = _check_redis()
    overall = "ok" if (db_status == "up" and redis_status == "up") else "degraded"
    return {
        "status": overall,
        "db": db_status,
        "redis": redis_status,
        "version": __version__,
    }
